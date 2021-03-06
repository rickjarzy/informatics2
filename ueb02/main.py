# Paul Arzberger
# 00311430
# Informatics 2 - SS19
# Gruppe A - Programm 2: Satellitensichtbarkeiten

# todo: finish logic to catch and round time input that contains seconds
# todo: finish logic for wrong time intervall input
# todo: plot stuff
# todo: catch value errors for time interval
# todo: finish dynamic satellite tail logic
# todo: cmd - visibility lines


import argparse
import datetime
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs


from pro02SatelliteVisibilityToolbox import collect_sat_orbit_data, \
                                            Satellite, \
                                            read_out_sat_orbit_files, \
                                            calc_utc_date,\
                                            animate_orbit_movement, create_start_end_epoch_index, start_screen


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Generates an animated visualization of GRACE satellite visibility to the GPS constellation for a single day.")

    parser.add_argument("date", type=str, nargs='*', help="date to visualize (format: YYYY-MM-DD)")
    parser.add_argument("-n", "--novisibilty", help="don't show visibility lines", action="store_true")
    parser.add_argument("-o", "--outfile", help="save animation to this file")
    parser.add_argument("-t", "--time", help="start and end time in hours to limit animation "
                                             "\n default start:9 - end:10", nargs=2)

    parser.add_argument("-d", "--dir", help="specifiy the ftp directory where to search for the date specific orbit files\n"
                                            "default: /outgoing/ITSG/teaching/2019SS_Informatik2/orbit/",
                                       default="/outgoing/ITSG/teaching/2019SS_Informatik2/orbit/")

    parser.add_argument("-ow", "--overwrite", help="Overwrites existing sat data and downloads them again from ftp server\n default: False",
                                              action="store_true", default=False)
    parser.add_argument("-v", "--verbosity", help="If flag is set additional process information is printed", action="store_true")

    args = parser.parse_args()
    outfile_str = start_screen(args)
    try:
        if args.date:

            # month - specifies blue marble picture
            blue_marble_month_filename = "bluemarble%s.jpg" % args.date[0].split("-")[1]

            # download sat orbit data from ftp server - if sucessful True is handed back
            success_token = collect_sat_orbit_data(args.date[0], blue_marble_month_filename, args.dir, args.overwrite, args.verbosity)

            # if download was successful continue with animation
            if success_token:
                # read out the sat orbit data from the dir that was created or selected
                sat_orbits_dict, sat_orbits_indizes, fig, ax = read_out_sat_orbit_files(args.verbosity)

                # list with all satellite names that are visibible at that day
                sat_names = [sat_name for sat_name in sat_orbits_dict]

                # used to determin the index at the specific epoch
                sat_epochs_date_list = [sat_epoch for sat_epoch in sat_orbits_indizes]
                sat_epochs_start_date = sat_epochs_date_list[0]

                # check if time intervall has been handed
                if args.time:
                    index_start, index_end =  create_start_end_epoch_index(args.time[0], args.time[1], sat_epochs_start_date, sat_orbits_indizes)

                # if not use predefined time range
                else:
                    index_start, index_end = create_start_end_epoch_index(12, 13, sat_epochs_start_date, sat_orbits_indizes)

                if args.novisibilty:
                    print("# Visibility lines have been turned on")

                print("# Start index: ", index_start, " - end index: ", index_end)
                print("# processing %s satellites ... " % str(len(sat_names)))

                print("\n\n# start plotting and writing out animation\n"
                      "  ----------------------------------------")

                blue_marble_img = plt.imread(blue_marble_month_filename)

                number_of_iteration = abs(index_start - index_end)
                print("# number of frames: ", number_of_iteration)

                # FUNC ANIMATION
                # ==============

                ax.imshow(blue_marble_img, origin='upper', extent=[-180, 181, -90, 91], transform=ccrs.PlateCarree())  # extend hinzufügen

                # are only used for the legend
                ax_grace, = ax.plot([], [], "o", color="red", label="GRACE A",)
                ax_gps, = ax.plot([], [], "o", color="yellow", label="GPS",)
                ax_vis, = ax.plot([], [], color="cyan", label="VISIBILITY")
                text = ax.text(-178, -85, "", transform=ccrs.PlateCarree(), bbox=dict(facecolor='white', pad=4))

                plt.legend(loc='lower center', bbox_to_anchor=(0.95, 0))

                anim = animation.FuncAnimation(fig,
                                               animate_orbit_movement,
                                               number_of_iteration,
                                               fargs=(sat_orbits_dict, sat_epochs_date_list, index_start, args.novisibilty, ax_grace, ax_gps, ax_vis, text),
                                               interval=50,
                                               blit=True)

                plt.show()

                print("start rendering and saving animation to file:  %s ..." % outfile_str)


                anim.save(outfile_str)
            else:
                print("\n# Programm END - download was not possible \n  input date: {}\n  input time: {}".format(args.date, args.time))

        else:
            print("# ERROR - no date has been handed")
    except KeyboardInterrupt:
        print("# Programm stopped by user via STRG+C")

    # mainly for wrong time interval input - e.g "-t xx xx"
    except TypeError:
        print("""\n# Type ERROR!!! - please insert float or int for the time interval "-t" - no strings are allowed\n"""
              """  userinput %s - %s\n""" % (args.time[0], args.time[1]))

    print("# Programm ENDE")