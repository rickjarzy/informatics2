import ftplib
import os
import gzip
import shutil
import datetime

class Satellite:

    def __init__(self, time, name, x=0., y=0., z=0., verbose=False):

        if float(x) and float(y) and float(z):
            self.__x = x
            self.__z = z
            self.__y = y

        if isinstance(time, datetime.datetime):
            self.__time = time

        if isinstance(name, str):
            self.__name = name

        if isinstance(verbose, bool):
            self.__verbose = verbose
        if self.__verbose:
            print("+ Create new {} Epoch - {}".format(self.__name, self.__time))

    def __str__(self):
        return "GPS %s - Epoch %s " % (self.__name, self.__time)

    def __del__(self):
        print("- Delete Instance GPS %s - Epoch %s " % (self.__name, self.__time)) if self.__verbose else False


def download_file(ftp_connection, sat_orbit_filename, input_verbosity):
    """
    download a file from a specific ftp location
    :param ftp_connection:      ftp_connection instance
    :param sat_orbit_filename:  filename that will be downloaded
    :return: None
    """
    with open(sat_orbit_filename, "wb") as download_file:
        if input_verbosity: print("- start download of %s " % sat_orbit_filename)

        ftp_connection.retrbinary("RETR %s" % sat_orbit_filename, download_file.write)


def collect_sat_orbit_data(input_date, input_ftp_dir, time_start, time_end, input_overwrite, input_verbosity):


    """
    downloads the sat orbit files from a specific ftp connection to a local directory

    :param input_date:      string - YYYY-MM-DD
    :param input_ftp_dir:   string
    :param time_start:      number -
    :param time_end:        number
    :param input_overwrite: bool - if set the files in the ftp dir will be downloaded again
    :return: None
    """

    print("\n- start FTP connection\n-----------------------\n- date: %s \n- starttime: %s\n- endtime: %s"%(input_date, time_start, time_end))

    # access ftp server
    with ftplib.FTP("ftp.tugraz.at") as ftp_connection:

        ftp_connection.login()
        ftp_connection.cwd(input_ftp_dir + input_date)



        # todo: split date and download blue marble picture for the month of date
        # todo: download blue marble!!

        ftp_files_list = ftp_connection.nlst()
        if input_verbosity:
            print("- content of folder")
            print("- ", ftp_files_list)
            print("- found %d sat orbit files in dir %s" % (len(ftp_files_list), input_date))

        # check if date_dir exists
        if os.path.exists(input_date):
            print("- directory for %s exists" % input_date)
        else:
            print("- create new sat data epoch dir %s " % input_date)
            os.mkdir(input_date)

        # change working dir to selected date directory
        os.chdir(input_date)
        print("- start downloading %d files from ftp" % len(ftp_files_list))
        for sat_orbit_filename in ftp_files_list:

            # if overwrite flag is set overwrite all files in dir with new downloads
            if input_overwrite:
                download_file(ftp_connection, sat_orbit_filename, input_verbosity)

            else:
                #check if file in ftp dir exists in local datespecific directory
                if os.path.exists(sat_orbit_filename):
                    if input_verbosity: print("- found %s in %s dir - skip download" % (sat_orbit_filename, input_date))

                # if the file was not found in the datespecific directory download it from the ftp dir
                else:
                    download_file(ftp_connection, sat_orbit_filename, input_verbosity)

        print("- finished download")