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

class Satellite():

    def __init__(self,name,  xyz_array, ax_dot, ax_tail, ax_vis=None):
        if isinstance(name, str):
            self.name = name

        if isinstance(xyz_array, numpy.ndarray):

            self.__xyz = xyz_array

        self.dot = ax_dot
        self.tail = ax_tail
        self.vis = ax_vis

    # getter methods
    def get_koords(self, index_start, index_end=None):
        if index_end:
            return self.__xyz[index_start:index_end]
        else:
            return self.__xyz[index_start]

    def calc_lam_phi(self, input_epoch_xyZ):
        x = input_epoch_xyZ[0]
        y = input_epoch_xyZ[1]
        z = input_epoch_xyZ[2]

        r = numpy.sqrt(x ** 2 + y ** 2 + z ** 2)
        phi = numpy.arcsin(z / r) * (180 / numpy.pi)
        lam = numpy.arctan2(y, x) * (180 / numpy.pi)

        return lam, phi

    def get_lam_phi(self, index_start, index_end=None):
        if index_end:
            epoch_xyz = self.__xyz[index_start:index_end]
            return self.calc_lam_phi(epoch_xyz)

        else:
            epoch_xyz = self.__xyz[index_start]

            return self.calc_lam_phi(epoch_xyz)

    def calc_vis_angle(self,index_epoch, input_grace_koords):
        """
        calculate the visibility angle between a gps satellite and the grace a satellite
        :param index_epoch:         int - used to select the epoch data from the instances xyz data block
        :param input_grace_koords: numpy array
        :return:
        """

        gps_pos = self.__xyz[index_epoch]

        dot = numpy.dot(input_grace_koords, gps_pos)
        grace_mod = numpy.sqrt((input_grace_koords * input_grace_koords).sum())
        gps_mod = numpy.sqrt((gps_pos * gps_pos).sum())
        cos_angle = dot / grace_mod / gps_mod
        angle = numpy.arccos(cos_angle) * (180 / numpy.pi)

        return angle


    def __str__(self):
        return "Satellite instance %s  " % (self.__name)



# fargs=(sat_orbits_dict, sat_names, index_start, ax)
def animate_orbit_movement(i, input_sat_orbits_dict, input_sat_names, input_index_start, input_visibility, input_ax_grace, input_ax_gps, input_ax_vis):
    plot_objects_list = [input_ax_grace, input_ax_gps, input_ax_vis]
    print("- rendering frame ", i)
    print("- render input_index_start ", input_index_start)
    for sat_name in input_sat_names:

        if "graceA" == sat_name:
            #print("- GRACE A MATCH")
            satellite_tail = 8

            grace_instance = input_sat_orbits_dict[sat_name]

            sat_data_lam, sat_data_phi = grace_instance.get_lam_phi(input_index_start + i - satellite_tail, input_index_start + i)

            grace_instance.dot.set_data(sat_data_lam[-1], sat_data_phi[-1])
            grace_instance.tail.set_data(sat_data_lam, sat_data_phi)

            plot_objects_list.append(grace_instance.dot)
            plot_objects_list.append(grace_instance.tail)

        else:
            satellite_tail = 5
            gps_instance = input_sat_orbits_dict[sat_name]

            if input_visibility:

                grace_instance = input_sat_orbits_dict["graceA"]

                angle = gps_instance.calc_vis_angle(input_index_start+1, grace_instance.get_koords(input_index_start + i))


                if angle >= 90:
                    grace_lam, grace_phi = grace_instance.get_lam_phi(input_index_start+i)
                    gps_lam, gps_phi = gps_instance.get_lam_phi(input_index_start + i)
                    lam_line_of_sight = [grace_lam, gps_lam]
                    phi_line_of_sight = [grace_phi, gps_phi]

                    gps_instance.vis.set_data(lam_line_of_sight, phi_line_of_sight)
                    plot_objects_list.append(gps_instance.vis)

                else:
                    gps_instance.vis.set_data([], [])
                    plot_objects_list.append(gps_instance.vis)

                    #print("Winkel Zwischen Sat: ", angle)

            gps_data_lam, gps_data_phi = gps_instance.get_lam_phi(input_index_start + i - satellite_tail, input_index_start + i)
            gps_instance.tail.set_data(gps_data_lam, gps_data_phi)
            gps_instance.dot.set_data(gps_data_lam[-1], gps_data_phi[-1])

            plot_objects_list.append(gps_instance.dot)
            plot_objects_list.append(gps_instance.tail)

        #print("- proccessing satorbit for %s" % sat_name, " lam: ", sat_data_lam)

        #input_ax.plot(sat_data_lam, sat_data_phi, color=sat_color, label=sat_label, transform=ccrs.Geodetic())
        #input_ax.plot(sat_data_lam[-1], sat_data_phi[-1], 'o', color=sat_color, markersize=2, label=sat_label, transform=ccrs.Geodetic())
        #input_ax.annotate(sat_name, (sat_data_lam[-1], sat_data_phi[-1]), color=sat_color )

    #return input_ax_grace, input_ax_gps, input_ax_vis
    return plot_objects_list

def calc_utc_date(input_julian):
    start_date = datetime.datetime(1858, 11, 17)
    epoch_date = start_date + datetime.timedelta(days=input_julian)

    return epoch_date


def read_out_sat_orbit_files(input_verbosity):
    # browse working dir ( that is changed in the collect_sat_orbit_data function to the selected date dir)
    sat_orbit_txt_list = glob.glob('*.gz')

    # dict that has the "GPS Sat name" as key and a list of epochs of type Satellite as value
    satellite_orbits_dict = {}

    # stores the index to all sat epochs
    satellite_orbits_time_epoch_index_dict = {}
    print("- start reading out and storing of sat orbit data\n"
          "  -----------------------------------------------")

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    for sat in sat_orbit_txt_list:
        index_sat_epoch = 0

        sat_name = sat.split(".")[1]
        if input_verbosity: ("- reading out and storing data of satellite: ", sat_name)

        # read out satdata from gz
        sat_data = numpy.loadtxt(sat, skiprows=2)

        # refzdatum 1858-11-17

        # allocate an array where the calculated lat and long values will be stored
        sat_lonlat_array = numpy.zeros((sat_data.shape[0], 2))

        for epoch in sat_data:
            # calc the UTC date for the mdj entry
            epoch_date = calc_utc_date(epoch[0])

            # write index of every epoch onto dict - gets refilled every time - not beautiful i hope i find a better solution
            satellite_orbits_time_epoch_index_dict[epoch_date] = index_sat_epoch

            index_sat_epoch += 1

        # store all satellite instances onto a dict with the satname as the key and the satellite instance as value

        if sat_name == "graceA":
            # def __init__(self,name,  xyz_array, ax_dot, ax_tail, ax_vis):
            # append every sat epoch to a list and store it on the satellit_orbits_dict with sat_name as key and the list as value

            grace_ax_dot_line2d_instance, = ax.plot([], [], "o", color="red", transform=ccrs.Geodetic())
            grace_ax_tail_line2d_instance, = ax.plot([], [], color="red", transform=ccrs.Geodetic())

            satellite_orbits_dict[sat_name] = Satellite(sat_name, sat_data[:, 1:],
                                            grace_ax_dot_line2d_instance,
                                            grace_ax_tail_line2d_instance,
                                            )
        # GPS Satellite Epochs
        else:

            gps_ax_dot_line2d_instance, = ax.plot([], [], "o", color="yellow", transform=ccrs.Geodetic())
            gps_ax_tail_line2d_instance, = ax.plot([], [], color="yellow", transform=ccrs.Geodetic())
            gps_ax_vis_line2d_instance, = ax.plot([], [], color="cyan")

            satellite_orbits_dict[sat_name] = Satellite(sat_name, sat_data[:, 1:],
                                            gps_ax_dot_line2d_instance,
                                            gps_ax_tail_line2d_instance,
                                            gps_ax_vis_line2d_instance,
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
    downloads the sat orbit files from a specific ftp connection to a local directory

    :param input_date:      string - YYYY-MM-DD
    :param input_ftp_dir:   string
    :param time_start:      number -
    :param time_end:        number
    :param input_overwrite: bool - if set the files in the ftp dir will be downloaded again
    :return: None
    """

    print("\n- start FTP connection\n  -----------------------\n- date: %s " % (input_date))

    # access ftp server
    with ftplib.FTP("ftp.tugraz.at") as ftp_connection:

        # login and change dir on ftp to the date specific dir for the sat orbits
        ftp_connection.login()
        ftp_connection.cwd(input_ftp_dir + input_date)

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

    args_time_start = float(input_args_time_start)
    args_time_end = float(input_args_time_end)

    print("\n- searching for start and end index of epochs\n"
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