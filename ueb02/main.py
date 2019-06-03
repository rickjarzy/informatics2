import argparse
import ftplib

def collect_sat_orbit_data(input_date, time_start=None, time_end=None):
    print("\n- start FTP connection\n-------------------\"\n- date: %s \n- starttime: %s\n- endtime: %s"%(input_date, time_start, time_end))

    # access ftp server
    with ftplib.FTP("ftp.tugraz.at") as ftp_connection:

        ftp_connection.login()
        ftp_connection.cwd("/outgoing/ITSG/teaching/2019SS_Informatik2/orbit/%s" % input_date)
        print("- content of folder")
        print("- ", ftp_connection.nlst())

        # todo: download the satdata into specific dir on disk
        # todo: split date and download blue marble picture for the month of date
        # todo: write gz function



if __name__ == "__main__":

    parser = argparse.ArgumentParser("Generates an animated visualization of GRACE satellite visibility to the GPS constellation for a single day.")

    parser.add_argument("date", type=str, nargs='*', help="date to visualize (format: YYYY-MM-DD)")
    parser.add_argument("-n", "--novisibilty", help="don't show visibility lines", action="store_true")
    parser.add_argument("-o", "--outfile", help="save animation to this file")
    parser.add_argument("-t", "--time", help="start and end time in hours to limit animation", nargs=2, default=[9, 10])

    args = parser.parse_args()

    print("Args: ", args)
    print("args time: ", args.time)

    #todo: check if input date is of type datetime YYYY-MM-DD
    collect_sat_orbit_data(args.date[0], args.time[0], args.time[1])

    print("Programm ENDE")