import argparse
import glob
import datetime
import numpy
from pro02SatelliteVisibilityToolbox import collect_sat_orbit_data, Satellite, read_out_sat_orbit_files, calc_utc_date


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

    if args.date:

        # month - specifies blue marble picture
        blue_marble_month_filename = "bluemarble%s.jpg" % args.date[0].split("-")[1]

        # download sat orbit data from ftp server
        collect_sat_orbit_data(args.date[0], blue_marble_month_filename, args.dir, args.overwrite, args.verbosity)

        # read out the sat orbit data from the dir that was created or selected
        sat_orbits_dict, sat_orbits_indizes = read_out_sat_orbit_files(args.verbosity)

        # list with all satellite names that are visibible at that day
        sat_names = [sat_name for sat_name in sat_orbits_dict]

        # check if some time intervall has been handed

        # todo: finish logic to catch and round time input that contains seconds
        # todo: finish logic for wrong time intervall input
        # todo: select intervall sat data
        # todo: plot stuff


        if (float(args.time[0])>=0 and float(args.time[0])<24) and (args.time[1]>=float(args.time[0]) and float(args.time[1])<24):
            print("\nhanded new time ranges")
            args_time_start = float(args.time[0])
            args_time_end = float(args.time[1])

            start_datetime_object = sat_orbits_dict[sat_names[0]][0].time +datetime.timedelta(hours=args_time_start)
            end_datetime_object = sat_orbits_dict[sat_names[0]][0].time + datetime.timedelta(hours=args_time_end)

            if start_datetime_object.second > 0:

                print("Seconds start: ", start_datetime_object.second)
            if end_datetime_object.second > 0:

                print("Seconds end: ", end_datetime_object.second)
                sec = end_datetime_object.second

                delta = 60 - sec

                print("Delta: ", delta)

                new_end_time = end_datetime_object + datetime.timedelta(seconds=delta)

                print("new end time: ", new_end_time)




            datetime_start = sat_orbits_dict[sat_names[0]][0].time + datetime.timedelta(hours=args_time_start)
            datetime_end = sat_orbits_dict[sat_names[0]][0].time + datetime.timedelta(hours=args_time_end)

            print("start intervall: ", datetime_start)
            print("end intervall: ", datetime_end)

            index_start = sat_orbits_indizes[datetime_start]
            index_end = sat_orbits_indizes[datetime_end]

        else:
            index_start = sat_orbits_indizes[sat_orbits_dict[sat_names[0]][0].time + datetime.timedelta(hours=0)]
            index_end = sat_orbits_indizes[sat_orbits_dict[sat_names[0]][0].time + datetime.timedelta(hours=24)]

        print("Start index: ", index_start, " - end index: ", index_end)
        print("sat names: ", sat_names)


    else:
        print("# ERROR - no date has been handed")

    print("Programm ENDE")