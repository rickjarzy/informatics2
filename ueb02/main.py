import argparse
import glob
import datetime
import numpy
from pro02SatelliteVisibilityToolbox import collect_sat_orbit_data, Satellite



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
    parser.add_argument("-v", "--verbosity", help="If flag is set additional process information is printed", action="store_true")

    args = parser.parse_args()

    print("Args: ", args)
    print("args time: ", args.time)

    if args.date:

        #todo: check if input date is of type datetime YYYY-MM-DD
        collect_sat_orbit_data(args.date[0], args.dir, args.time[0], args.time[1], args.overwrite, args.verbosity)

        sat_orbit_txt_list = glob.glob('*.gz')

        # dict that has the "GPS Sat name" as key and a list of epochs of type Satellite as value
        satellite_orbits_dict = {}

        # stores the index to all
        satellite_orbits_time_epoch_index_dict = {}

        for sat in sat_orbit_txt_list:
            index_sat_epoch = 0

            # list of satellite epochs of type Satellite
            sat_epoch_list = []

            sat_data = numpy.loadtxt(sat, skiprows=2)


            # todo: convert mod jul date to UTC
            jul_date = sat_data[0,0]
            print(jul_date)

            break



    else:
        print("# ERROR - no date has been handed")

    print("Programm ENDE")