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
                                            animate_orbit_movement, plot_orbit_time_series


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

    print("Args: ", args)
    print("args time: ", args.time)
    try:
        if args.date:

            # month - specifies blue marble picture
            blue_marble_month_filename = "bluemarble%s.jpg" % args.date[0].split("-")[1]

            # download sat orbit data from ftp server
            collect_sat_orbit_data(args.date[0], blue_marble_month_filename, args.dir, args.overwrite, args.verbosity)

            # read out the sat orbit data from the dir that was created or selected
            sat_orbits_dict, sat_orbits_indizes, fig, ax = read_out_sat_orbit_files(args.verbosity)

            # list with all satellite names that are visibible at that day
            sat_names = [sat_name for sat_name in sat_orbits_dict]

            # used to determin the index at the specific epoch
            sat_epochs_start_date = [sat_epoch for sat_epoch in sat_orbits_indizes][0]


            # check if time intervall has been handed
            if args.time:

                args_time_start = float(args.time[0])
                args_time_end = float(args.time[1])
                print("\n- start plotting and writing out animation\n"
                      "  ----------------------------------------")
                if (args_time_start>=0 and args_time_end<24) and (args_time_end>=args_time_start and args_time_end<=24):
                    print("handed new time ranges")

                    # create time stamp of type datetime
                    start_datetime_object = sat_epochs_start_date + datetime.timedelta(hours=args_time_start)
                    end_datetime_object = sat_epochs_start_date + datetime.timedelta(hours=args_time_end)

                    # "translate" fractal to seconds
                    if start_datetime_object.second > 0:

                        print("Seconds start: ", start_datetime_object.second)
                    if end_datetime_object.second > 0:

                        print("Seconds end: ", end_datetime_object.second)
                        sec = end_datetime_object.second

                        delta = 60 - sec

                        print("Delta: ", delta)

                        new_end_time = end_datetime_object + datetime.timedelta(seconds=delta)

                        print("new end time: ", new_end_time)

                    # start time and end time of selectetd intervall - they are used to select the indizes of the epoch list
                    datetime_start = sat_epochs_start_date + datetime.timedelta(hours=args_time_start)
                    datetime_end = sat_epochs_start_date + datetime.timedelta(hours=args_time_end)

                    print("start intervall: ", datetime_start)
                    print("end intervall: ", datetime_end)

                    index_start = sat_orbits_indizes[datetime_start]
                    index_end = sat_orbits_indizes[datetime_end]

                else:
                    # if no time values are handed the default values are used - 12 - 13 h
                    print("No or wrong time intervall has been handed {} : {} - switching to 0 : 24 ".format(args.time[0], args.time[1]))
                    index_start = sat_epochs_start_date + datetime.timedelta(hours=12)
                    index_end = sat_epochs_start_date + datetime.timedelta(hours=13)

                print("Start index: ", index_start, " - end index: ", index_end)
                print("processing %s satellites ... " % str(len(sat_names)))

                blue_marble_img = plt.imread(blue_marble_month_filename)

                # plot trajectory:

                # ARTITS ANIMATION
                # ===============
                #frames, artist_fig = plot_orbit_time_series(sat_orbits_dict, sat_names, index_start, index_end, blue_marble_month_filename)
                #anim = animation.ArtistAnimation(artist_fig, frames, interval=50, repeat_delay=1000)

                number_of_iteration = abs(index_start - index_end)
                print("number of iterations: ", number_of_iteration)

                # FUNC ANIMATION
                # ==============

                #fig = plt.figure()
                #ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
                ax.imshow(blue_marble_img, transform=ccrs.Robinson())
                # are only used for the legend
                ax_grace, = ax.plot([0, 0], [0, 0], color="red", label="GRACE A", transform=ccrs.Geodetic())
                ax_gps, = ax.plot([0, 0], [0, 0], color="yellow", label="GPS", transform=ccrs.Geodetic())
                ax_vis, = ax.plot([0, 0], [0, 0], color="cyan", label="VISIBILITY")

                #plt.legend()
                anim = animation.FuncAnimation(fig, animate_orbit_movement, number_of_iteration, fargs=(sat_orbits_dict, sat_names, index_start, ax_grace, ax_gps, ax_vis), interval=250)

                # check if outfile was handed or use default name constructed by date and time
                if args.outfile:
                    outfile_str = args.outfile
                    if ".mp4" in outfile_str:
                        pass
                    else:
                        outfile_str += ".mp4"
                else:
                    if args.time:
                        outfile_str = "animation_%s_%s-%s.mp4" % (args.date[0], args.time[0].replace(".", "-"), args.time[1].replace(".", "-"))
                    else:
                        outfile_str = "animation_%s.mp4" % (args.date[0])

                print("start rendering animation %s ..." % outfile_str)
                anim.save(outfile_str)

        else:
            print("# ERROR - no date has been handed")
    except KeyboardInterrupt:
        print("Programm stopped by user via STRG+C")

    print("Programm ENDE")