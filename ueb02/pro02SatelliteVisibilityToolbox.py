# Paul Arzberger
# 00311430
# Informatics 2 - SS19
# Gruppe A - Programm 2: Satellitensichtbarkeiten

import ftplib
import os
import datetime
import glob
import numpy
import cartopy.crs as ccrs
from matplotlib import pyplot as plt

class InvalidDirectoryError(BaseException):
    """
    Class that handles Error Messages if a directroy is not found on the ftp server
    """
    def __init__(self, arg):
        self.errorstring = arg

class Satellite():
    """
    Satellite object that stores the entire satorbit coordinates in ECEF for one day for a GPS Satellite or the Grace A
    Satellite
    """

    # Constructor
    def __init__(self,name,  xyz_array, ax_dot, ax_tail, ax_text, ax_vis=None):
        if isinstance(name, str):
            self.__name = name

        if isinstance(xyz_array, numpy.ndarray):

            self.__xyz = xyz_array

        self.dot = ax_dot
        self.tail = ax_tail
        self.vis = ax_vis
        self.sat_annotation = ax_text

    # getter methods
    def get_koords(self, index_start, index_end=None):
        """
        returns the xyz koords for a specific time epoch of the satellite instance
        :param index_start: int - index for the self.__xyz array
        :param index_end: int - index for the self.__xyz array
        :return: 1n array/narray - returns the koordinates for the specified epoch time
        """

        if index_end:
            return self.__xyz[index_start:index_end, :]
        else:
            return self.__xyz[index_start, :]


    def trafo_xyz_polar(self, input_x, input_y, input_z):
        """
        transforms carth coords to polar coords
        :param input_x: 1n array or skalar
        :param input_y: 1n array or skalar
        :param input_z: 1n array or skalar
        :return: float - lam and phi
        """

        r = numpy.sqrt(input_x ** 2 + input_y ** 2 + input_z ** 2)
        phi = numpy.arcsin(input_z / r) * (180 / numpy.pi)
        lam = numpy.arctan2(input_y, input_x) * (180 / numpy.pi)

        return lam, phi

    def calc_lam_phi_ndim(self, input_epoch_xyz):
        """
        calculates the polar coordinates lam, phi from xyz for a nx3 array
        :param input_epoch_xyZ:
        :return:
        """
        x = input_epoch_xyz[:, 0]
        y = input_epoch_xyz[:, 1]
        z = input_epoch_xyz[:, 2]

        return self.trafo_xyz_polar(x, y, z)

    def calc_lam_phi_arr(self, input_epoch_xyz):
        """
        calculates lam and phi from xyz if the array is only shape (3,)
        :param input_epoch_xyZ:
        :return:
        """

        x = input_epoch_xyz[0]
        y = input_epoch_xyz[1]
        z = input_epoch_xyz[2]

        lam, phi = self.trafo_xyz_polar(x, y, z)

        return numpy.array([lam]), numpy.array([phi])

    def get_lam_phi(self, index_start, index_end=None):
        """
        calculates phi and lam out of the selected epochs
        :param index_start: int index where the epochs should start
        :param index_end:   int index where the epochs should start
        :return: float - lam and phi as floats
        """

        if index_end:

            epoch_xyz = self.__xyz[index_start:index_end, :]
            return self.calc_lam_phi_ndim(epoch_xyz)

        else:

            epoch_xyz = self.__xyz[index_start, :]

            return self.calc_lam_phi_arr(epoch_xyz)

    def calc_vis_angle(self,index_epoch, input_grace_koords):
        """
        calculate the visibility angle between a gps satellite and the grace a satellite
        :param index_epoch:         int - used to select the epoch data from the gps instances xyz data block
        :param input_grace_koords: numpy array
        :return: angle in degrees
        """

        gps_pos = self.__xyz[index_epoch]

        # vector graceA - Koord Center
        vec_grace_earth = numpy.array((0, 0, 0)) - input_grace_koords

        # vector graceA - GPS
        vec_grace_gps = gps_pos - input_grace_koords

        dot = numpy.dot(vec_grace_gps, vec_grace_earth)

        grace_mod = numpy.sqrt((vec_grace_earth * vec_grace_earth).sum())

        gps_mod = numpy.sqrt((vec_grace_gps * vec_grace_gps).sum())

        cos_angle = dot / (grace_mod * gps_mod)

        angle = numpy.arccos(cos_angle) * (360/2 / numpy.pi)

        return angle

    def __str__(self):
        return "Satellite instance %s  " % (self.__name)



def animate_orbit_movement(i, input_sat_orbits_dict, input_sat_epochs_date_list,input_index_start, input_visibility, input_ax_grace, input_ax_gps, input_ax_vis, input_text):
    """
    function to render a frame for the animation
    :param i:                           int - is incremented automatically
    :param input_sat_orbits_dict:       dict - contains the sat instances as values, keys are sat names
    :param input_sat_epochs_date_list:  list - list that contains all date and time information for each epoch
    :param input_index_start:           int - at which index of the epochs starts the animation
    :param input_visibility:            bool - should visibility lines be plotted
    :param input_ax_grace:              mpl line2d instance - only used for legend purposes
    :param input_ax_gps:                mpl line2d instance - only used for legend purposes
    :param input_ax_vis:                mpl line2d instance - only used for legend purposes
    :param input_text:                  mpl Axe instance - used to show the actual satellite epoch
    :return:                            list - retruns all plot objects that are of interest for the frame
    """

    # list with all plot instances that will be seen in the frame
    plot_objects_list = [input_ax_grace, input_ax_gps, input_ax_vis]

    # text with date and time
    input_text.set_text("{}".format(input_sat_epochs_date_list[input_index_start+i]))

    plot_objects_list.append(input_text)

    print("- rendering frame ", i)

    # walk through all satellites in the sat_orbits_dict and plot their epoch position
    for sat_name in input_sat_orbits_dict:

        # if the current sat is graceA do specific stuff for grace
        if "graceA" == sat_name:

            # satellite tail logic: check that index doesnt get negative
            if input_index_start+i in range(0, 6 + 1, 1):

                index_from = input_index_start + i
                index_to = None
            else:
                satellite_tail = 3
                index_from = input_index_start + i - satellite_tail
                index_to = input_index_start + i

            # grace satellite instance
            grace_instance = input_sat_orbits_dict["graceA"]

            # get actual position of satellite epoch in polar coordinates
            sat_data_lam, sat_data_phi = grace_instance.get_lam_phi(index_from, index_to)

            # update satellite and text position - hand it back via the returned list plot_objects_list
            grace_instance.dot.set_data(sat_data_lam[-1], sat_data_phi[-1])
            grace_instance.tail.set_data(sat_data_lam, sat_data_phi)
            grace_instance.sat_annotation.set_position((sat_data_lam[-1], sat_data_phi[-1]))

            plot_objects_list.append(grace_instance.dot)
            plot_objects_list.append(grace_instance.tail)
            plot_objects_list.append(grace_instance.sat_annotation)

        else:
            # satellite tail logic: check that index doesnt get negative
            if input_index_start+i in range(0, 6+1, 1):

                index_from = input_index_start + i
                index_to = None
            else:
                satellite_tail = 6
                index_from = input_index_start + i - satellite_tail
                index_to = input_index_start + i

            # grab a GPS instance
            gps_instance = input_sat_orbits_dict[sat_name]

            # if visibility is on -print visibiliity lines
            if input_visibility:

                # grab graceA instance to calc the angel
                grace_instance = input_sat_orbits_dict["graceA"]

                # calcualte the vis angle between graceA and a GPS satellite
                angle = gps_instance.calc_vis_angle(input_index_start+i, grace_instance.get_koords(input_index_start + i))



                # the gps satellites are only visible if their skalarproduct is bigger than 90°
                if angle >= 90:

                    grace_lam, grace_phi = grace_instance.get_lam_phi(input_index_start+i)
                    gps_lam, gps_phi = gps_instance.get_lam_phi(input_index_start + i)

                    # line of sight from grave to gps satellite
                    lam_line_of_sight = [grace_lam, gps_lam]
                    phi_line_of_sight = [grace_phi, gps_phi]

                    gps_instance.vis.set_data(lam_line_of_sight, phi_line_of_sight)
                    plot_objects_list.append(gps_instance.vis)

                else:

                    gps_instance.vis.set_data([], [])
                    plot_objects_list.append(gps_instance.vis)

            # get actual position of satellite epoch in polar coordinates
            gps_data_lam, gps_data_phi = gps_instance.get_lam_phi(index_from, index_to)

            # update satellite and text position - hand it back via the returned list plot_objects_list
            gps_instance.tail.set_data(gps_data_lam, gps_data_phi)
            gps_instance.dot.set_data(gps_data_lam[-1], gps_data_phi[-1])
            gps_instance.sat_annotation.set_position((gps_data_lam[-1], gps_data_phi[-1]))

            plot_objects_list.append(gps_instance.dot)
            plot_objects_list.append(gps_instance.tail)
            plot_objects_list.append(gps_instance.sat_annotation)


    #return list with all instances that got changed and should be plotted in the frame
    return plot_objects_list

def calc_utc_date(input_julian):
    """
    calcs the UTC time from MDJ Date
    :param input_julian: float - modiefied julian date
    :return:             datetime - UTC time for modified julian date
    """

    start_date = datetime.datetime(1858, 11, 17)
    epoch_date = start_date + datetime.timedelta(days=input_julian)

    return epoch_date


def read_out_sat_orbit_files(input_verbosity):
    """
    function that reads out all downloaded orbit files for the gps and graceA satellite
    :param input_verbosity: bool - prints additional information to the process on the screen
    :return:    dict, dict, mpl fig, mpl Axe instance - satellite_orbits_dict, satellite_orbits_time_epoch_index_dict, fig, ax
    """
    # browse working dir ( that is changed in the collect_sat_orbit_data function to the selected date dir)
    sat_orbit_gz_list = glob.glob('*.gz')

    # dict that has the "GPS Sat name" as key and  Satellite Instance as value
    satellite_orbits_dict = {}

    # stores the index to all sat epochs
    satellite_orbits_time_epoch_index_dict = {}
    print("\n- start reading out and storing of sat orbit data\n"
          "  -----------------------------------------------")

    # figure that is needed for the animation
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    for sat in sat_orbit_gz_list:
        # index that is stored as value on the satellite_orbits_time_epoch_index_dict
        index_sat_epoch = 0

        #generate satname from orbit file
        sat_name = sat.split(".")[1]

        if input_verbosity: print("- reading out and storing data of satellite: ", sat_name)

        # read out satdata from gz
        sat_data = numpy.loadtxt(sat, skiprows=2)

        # refzdatum 1858-11-17
        for epoch in sat_data:
            # calc the UTC date for the mdj entry
            epoch_date = calc_utc_date(epoch[0])

            # write index of every epoch onto dict - gets refilled every time - not beautiful i hope i find a better solution
            satellite_orbits_time_epoch_index_dict[epoch_date] = index_sat_epoch

            index_sat_epoch += 1

        # store all satellite instances onto a dict with the satname as the key and the satellite instance as value

        if sat_name == "graceA":
            print("- storing graceA ",sat_name, " file name ", sat )
            # def __init__(self,name,  xyz_array, ax_dot, ax_tail, ax_vis):
            # append every sat epoch to a list and store it on the satellit_orbits_dict with sat_name as key and the list as value

            grace_ax_dot_line2d_instance, = ax.plot([], [], "o", color="red", transform=ccrs.Geodetic())
            grace_ax_tail_line2d_instance, = ax.plot([], [], color="red", transform=ccrs.Geodetic())
            grace_ax_text = ax.text(0, 0, sat_name, transform=ccrs.PlateCarree(), color="red")

            satellite_orbits_dict[sat_name] = Satellite(sat_name, sat_data[:, 1:],
                                            grace_ax_dot_line2d_instance,
                                            grace_ax_tail_line2d_instance,
                                            grace_ax_text
                                            )
        # GPS Satellite Epochs
        else:

            gps_ax_dot_line2d_instance, = ax.plot([], [], "o", color="yellow", transform=ccrs.Geodetic())
            gps_ax_tail_line2d_instance, = ax.plot([], [], color="yellow", transform=ccrs.Geodetic())
            gps_ax_vis_line2d_instance, = ax.plot([], [], color="cyan")
            gps_ax_text = ax.text(0, 0, sat_name, transform=ccrs.PlateCarree(), color="yellow")

            satellite_orbits_dict[sat_name] = Satellite(sat_name, sat_data[:, 1:],
                                            gps_ax_dot_line2d_instance,
                                            gps_ax_tail_line2d_instance,
                                            gps_ax_text,
                                            gps_ax_vis_line2d_instance
                                            )


    print("- finished reading out and storing of sat orbit data")

    return satellite_orbits_dict, satellite_orbits_time_epoch_index_dict, fig, ax


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


def collect_sat_orbit_data(input_date, input_blue_marble_month_filename, input_ftp_dir, input_overwrite, input_verbosity):

    """
    connects and downloads the sat orbit files from a specific ftp connection to a local directory

    :param input_date:                          string - YYYY-MM-DD used to select the epoch download folder
    :param input_blue_marble_month_filename:    string - filename for the böuemarble img used as background in the frames of the animation
    :param input_ftp_dir:                       string - path to the download folder with the epochs dirs
    :param input_overwrite:                     bool - if flag is set and the epoch download folder exists on disk, its content will be overwritten
    :param input_verbosity:                     bool - if set additional process informations will be printed
    :return: No return values
    """

    print("\n\n- start FTP connection\n  -----------------------\n- date: %s " % (input_date))

    # access ftp server
    with ftplib.FTP("ftp.tugraz.at") as ftp_connection:

        # login and change dir on ftp to the date specific dir for the sat orbits
        ftp_connection.login()
        try:
            ftp_connection.cwd(input_ftp_dir + input_date)
        except:
            raise InvalidDirectoryError("ERROR - Directory : {} - was not found on ftp.tugraz.at".format(input_ftp_dir + input_date))

        ftp_files_list = ftp_connection.nlst()
        if input_verbosity:
            print("- content of folder %s\n" % input_ftp_dir)
            print("- ", ftp_files_list)
            print("\n- found %d sat orbit files in dir %s" % (len(ftp_files_list), input_date))

        # check if date_dir exists
        if os.path.exists(input_date):
            print("- directory for %s exists" % input_date)
        else:
            print("- create new sat data epoch dir %s " % input_date)
            os.mkdir(input_date)

        # change working dir to selected date directory
        os.chdir(input_date)

        print("\n- start downloading %d files from ftp ..." % len(ftp_files_list))
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

        # change to blue marble dir
        ftp_connection.cwd("/outgoing/ITSG/teaching/2019SS_Informatik2/bluemarble/")

        # download blue marble picture
        if os.path.exists(input_blue_marble_month_filename):
            print("\n- blue marble file %s allready exists - skip download" % input_blue_marble_month_filename)
            pass

        else:
            print("\n- start downloading %s from ftp" % input_blue_marble_month_filename)
            download_file(ftp_connection, input_blue_marble_month_filename, input_verbosity)

        print("- finished download - close connection\n")


def create_start_end_epoch_index(input_args_time_start, input_args_time_end, input_sat_epoch_start_date, input_sat_orbit_indizes):
    """
    creates the start and end index out of the user's time input. these timedepending indizes are used to select the specidic sat orbit epochs
    :param input_args_time_start:       str - user input
    :param input_args_time_end:         str - user input
    :param input_sat_epoch_start_date:  datetime - start date and time form the day
    :param input_sat_orbit_indizes:     dict with key datetime of satepoch and value the index
    :return:   int int - the start and end index of the epochs specified by the user input
    """
    try:
        args_time_start = float(input_args_time_start)
        args_time_end = float(input_args_time_end)

        print("\n\n- searching for start and end index of epochs\n"
              "  ----------------------------------------------")
        if (args_time_start >= 0 and args_time_end < 24) and (args_time_end >= args_time_start and args_time_end <= 24):
            print("- handed new time ranges")

            # create time stamp of type datetime
            start_datetime_object = input_sat_epoch_start_date + datetime.timedelta(hours=args_time_start)
            end_datetime_object = input_sat_epoch_start_date + datetime.timedelta(hours=args_time_end)

            # "translate" fractal to seconds
            if start_datetime_object.second > 0:
                print("- Seconds start: ", start_datetime_object.second)
            if end_datetime_object.second > 0:
                print("- Seconds end: ", end_datetime_object.second)
                sec = end_datetime_object.second

                delta = 60 - sec

                print("- Delta: ", delta)

                new_end_time = end_datetime_object + datetime.timedelta(seconds=delta)

                print("- new end time: ", new_end_time)

            # start time and end time of selectetd intervall - they are used to select the indizes of the epoch list
            datetime_start = input_sat_epoch_start_date + datetime.timedelta(hours=args_time_start)
            datetime_end = input_sat_epoch_start_date + datetime.timedelta(hours=args_time_end)

            print("- start intervall: ", datetime_start)
            print("- end intervall: ", datetime_end)

            index_start = input_sat_orbit_indizes[datetime_start]
            index_end = input_sat_orbit_indizes[datetime_end]

        else:
            # if no time values are handed the default values are used - 12 - 13 h
            print("- No or wrong time intervall has been handed {} : {} - switching to 0 : 24 ".format(args_time_start,
                                                                                                     args_time_end))
            # switch do prefefined time range
            datetime_start = input_sat_epoch_start_date + datetime.timedelta(hours=12)
            datetime_end = input_sat_epoch_start_date + datetime.timedelta(hours=13)

            index_start = input_sat_orbit_indizes[datetime_start]
            index_end = input_sat_orbit_indizes[datetime_end]

        return index_start, index_end
    except ValueError:
        print("""\n- ERROR!!! - please insert float or int after "-t" - no strings are allowed\n"""
              """  userinput %s - %s\n""" %(input_args_time_start, input_args_time_end))