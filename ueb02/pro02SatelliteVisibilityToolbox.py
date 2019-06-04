import ftplib
import os
import gzip
import shutil

def download_file(ftp_connection, sat_orbit_filename):
    """
    download a file from a specific ftp location
    :param ftp_connection:      ftp_connection instance
    :param sat_orbit_filename:  filename that will be downloaded
    :return: None
    """
    with open(sat_orbit_filename, "wb") as download_file:
        print("- start download of %s " % sat_orbit_filename)
        ftp_connection.retrbinary("RETR %s" % sat_orbit_filename, download_file.write)


def decompress_file(filename, filename_txt):
    """
    decompresses gz file
    :param filename:     string - gz filename
    :param filename_txt: string - filename of the extracted txt filen
    :return: None
    """
    # decompress the gz file and extract the txt file
    with gzip.open(filename, "rb") as decompress_gzfile:
        with open(filename_txt, "wb") as receiving_file:
            shutil.copyfileobj(decompress_gzfile, receiving_file)

def extract_txt_from_gz_file(filename, input_overwrite):
    """
    decompresses a *.gz file and extracts its txt file content
    :param filename: string - filename of the gz file
    :return: None
    """

    #check if file is a gz file
    if ".gz" in filename:
        # check if file has been downloaded
        if os.path.exists(filename):
            filename_txt = filename.split(".gz")[0]

            # if the overwrite flag was set decompress the downloaded files again
            if input_overwrite:
                decompress_file(filename, filename_txt)
                print("- decompress %s " % filename)

            else:

                if os.path.exists(filename_txt):
                    print("- %s allready exists - does not need to be decompressed")

                # decompress the gz file and extract the txt file
                print("- decompress %s " % filename)
                decompress_file(filename, filename_txt)

        # if something wents south print an error message
        else:
            print("# ERROR %s could not be decompressed" % filename)



def collect_sat_orbit_data(input_date, input_ftp_dir, time_start, time_end, input_overwrite):


    """
    downloads the sat orbit files from a specific ftp connection to a local directory

    :param input_date:      string - YYYY-MM-DD
    :param input_ftp_dir:   string
    :param time_start:      number -
    :param time_end:        number
    :param input_overwrite: bool - if set the files in the ftp dir will be downloaded again
    :return: None
    """

    print("\n- start FTP connection\n-------------------\"\n- date: %s \n- starttime: %s\n- endtime: %s"%(input_date, time_start, time_end))

    # access ftp server
    with ftplib.FTP("ftp.tugraz.at") as ftp_connection:

        ftp_connection.login()
        ftp_connection.cwd(input_ftp_dir + input_date)
        print("- content of folder")
        print("- ", ftp_connection.nlst())


        # todo: split date and download blue marble picture for the month of date
        # todo: download blue marble!!

        ftp_files_list = ftp_connection.nlst()
        print("- found %d sat orbit files in dir %s" % (len(ftp_files_list), input_date))

        # check if date_dir exists
        if os.path.exists(input_date):
            print("- directory for %s exists" % input_date)
        else:
            print("- create new sat data epoch dir %s " % input_date)
            os.mkdir(input_date)

        # change working dir to selected date directory
        os.chdir(input_date)

        for sat_orbit_filename in ftp_files_list:

            # if overwrite flag is set overwrite all files in dir with new downloads
            if input_overwrite:
                download_file(ftp_connection, sat_orbit_filename)
                extract_txt_from_gz_file(sat_orbit_filename, input_overwrite)

            else:
                #check if file in ftp dir exists in local datespecific directory
                if os.path.exists(sat_orbit_filename):
                    print("- found %s in %s dir - skip download" % (sat_orbit_filename, input_date))

                    # check if content of gz file exists
                    if os.path.exists(sat_orbit_filename.split(".gz")[0]):
                        print("- found TXT content of %s " % sat_orbit_filename)

                    # if something went wrong and only the gz file was downloaded but not decompressed, decompress the file
                    else:
                        extract_txt_from_gz_file(sat_orbit_filename, input_overwrite)

                # if the file was not found in the datespecific directory download it from the ftp dir
                else:
                    download_file(ftp_connection, sat_orbit_filename)
                    extract_txt_from_gz_file(sat_orbit_filename, input_overwrite)