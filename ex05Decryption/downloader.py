import os
import shutil
import ftplib
import gzip

# global variables - critical stuff and not that beautiful - only use them if you know what you are doing
HOST = "ftp.tugraz.at"
DIRECTORY = "/outgoing/ITSG/teaching/2019SS_Informatik2"

def download(host, directory, filename, overwrite=False):
    """
    Downloads a specific file from the TU GRAZ FTP Server. If the file is not found it will be created and the content
    will be streamed from the server. if the file is found - depending on the overwrite flag, it will be kept or a new
    file is written and the content will be downloaded

    :param host:        string - with ftp connection url
    :param directory:   string - holds a directory info
    :param filename:    string - holds the filename to be downloaded or created
    :param overwrite:   bool   - if set TRUE file will be overwritten, if False file will be kept and not downloaded
    :return:
    """
    print("\n- start FTP connection\n-----------------------")
    # connect to the FTP
    with ftplib.FTP(host) as ftp_connection:

        ftp_connection.login()  # log into ftp server
        ftp_connection.cwd(directory)  # change dir on ftp server
        print("- content of ftp folder: ")  # look inside the directory
        print("- ", ftp_connection.nlst())

        # if overwrite is set to true - overwrite the existing file or create it
        if overwrite:
            print("- File %s wird erstellt/überschrieben\n  starte download ..." % filename)
            # create the file
            with open(filename, "wb") as downloadFile:
                # download the content of the server file
                ftp_connection.retrbinary("RETR %s/%s" % (directory, filename), downloadFile.write)

        # if overwrite is set to False or default
        else:
            # if the file allready exists in our root dir we dont want to download it
            if os.path.exists(filename):
                print("- File %s existiert - skip download" % filename)
            # if it is not found in the root dir of our local system we want to download it
            else:
                print("- File %s existiert NICHT\n  starte download ..." % filename)
                # create the file
                with open(filename, "wb") as downloadFile:

                    # download the content of the server file
                    ftp_connection.retrbinary("RETR %s/%s" % (directory, filename), downloadFile.write)


def decompress(filename):
    """

    Decompress '.gz' files. if a non '.gz' file is handed an exception is thrown. If the file to decompress is not found
    it will be downloaded from the TU GRAZ FTP Server. Returns the handed filename as string without the '.gz' extension or None

    :param filename: string - should have '.gz' ending
    :return: string - filename with out extension of '.gz' OR None
    """
    print("\n# start decompression of file: %s \n#############################################" % filename)

    # check if handed filename has the extension .gz
    if ".gz" in filename:                               # if file has the extension gz

        if os.path.exists(filename):                    # check if the file exists

            print("# filename enthält die endung gz : %s" % filename)

            # if the file was found on the system split its string at the '.gz' position and use evereything before
            filename_txt = filename.split(".gz")[0]

            print("# txt filename: ", filename_txt)

            # create an txt file with string before the '.gz' extension and decompress the content of the .gz file
            with gzip.open(filename, 'rb') as decompressFile:
                with open(filename_txt, 'wb') as receivingFile:
                    shutil.copyfileobj(decompressFile, receivingFile)

        # if the file was not found download it and decompress the content
        else:
            print("# ERROR - %s konnte nicht gefunden werden!!" % filename)

            download(HOST, DIRECTORY, filename)
            filename_txt = decompress(filename)
        print("# return ", filename_txt)
        return filename_txt
    # if the handed filename has no '.gz' extension throw an Exception
    else:
        raise Exception("# not a gzip file")
        return None
