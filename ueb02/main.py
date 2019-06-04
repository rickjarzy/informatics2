import argparse
from pro02SatelliteVisibilityToolbox import collect_sat_orbit_data



if __name__ == "__main__":

    parser = argparse.ArgumentParser("Generates an animated visualization of GRACE satellite visibility to the GPS constellation for a single day.")

    parser.add_argument("date", type=str, nargs='*', help="date to visualize (format: YYYY-MM-DD)")
    parser.add_argument("-n", "--novisibilty", help="don't show visibility lines", action="store_true")
    parser.add_argument("-o", "--outfile", help="save animation to this file")
    parser.add_argument("-t", "--time", help="start and end time in hours to limit animation "
                                             "\n default start:9 - end:10", nargs=2, default=[9, 10])
    parser.add_argument("-d", "--dir", help="specifiy the ftp directory where to search for the date specific orbit files\n"
                                            "default: /outgoing/ITSG/teaching/2019SS_Informatik2/orbit/",
                                       default="/outgoing/ITSG/teaching/2019SS_Informatik2/orbit/")
    parser.add_argument("-ow", "--overwrite", help="Overwrites existing sat data and downloads them again from ftp server\n default: False",
                                              action="store_true", default=False)

    args = parser.parse_args()

    print("Args: ", args)
    print("args time: ", args.time)

    if args.date:

        #todo: check if input date is of type datetime YYYY-MM-DD
        collect_sat_orbit_data(args.date[0], args.dir, args.time[0], args.time[1], args.overwrite)



    else:
        print("# ERROR - no date has been handed")

    print("Programm ENDE")