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

    # make protected attributes callable
    @property
    def time(self):
        return self.__time

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def z(self):
        return self.__z

    @property
    def name(self):
        return self.__name

    # member functions

    def r(self):
        return numpy.sqrt( self.__x**2 + self.__y**2 + self.__z**2)

    def phi(self):
        return numpy.arcsin(self.__z/self.r()) * (180 / numpy.pi)

    def lam(self):
        return numpy.arctan2(self.__y, self.__x) * (180 / numpy.pi)

    def get_koords(self):
        return numpy.array([self.__x, self.__y, self.__z])


def plot_orbit_time_series(input_sat_orbits_dict, input_sat_names, input_index_start, input_index_end, input_blue_marble_month_filename):
    satellite_tail = 1

    blue_marble_img = plt.imread(input_blue_marble_month_filename)

    # plot trajectory:
    fig = plt.figure()

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    frames_for_anim_list = []
    for sat_data_index in range(input_index_start, input_index_end + 1, 1):

        for sat_name in input_sat_names:

            if "graceA" == sat_name:
                #print("GRACE A MATCH")
                sat_label = "GRACE A"
                sat_color = "red"

            else:
                sat_label = "GPS"
                sat_color = "green"

            #print("- proccessing satorbit for %s" % sat_name, " - at epoch: ", sat_data_index)

            #print(sat_data_index, " - ", input_sat_orbits_dict[sat_name][sat_data_index].time)

            sat_data_phi = [satellite.phi() for satellite in input_sat_orbits_dict[sat_name][sat_data_index - satellite_tail:sat_data_index]]
            sat_data_lam = [satellite.lam() for satellite in input_sat_orbits_dict[sat_name][sat_data_index - satellite_tail:sat_data_index]]

            #print("sat phi: ", sat_data_phi)

            ax.annotate(sat_name, (sat_data_lam[-1], sat_data_phi[-1]))
            ax.set_xlabel("PHI")
            ax.set_ylabel("LAM")
            orbit_frame = ax.plot(sat_data_lam, sat_data_phi, label=sat_label, color=sat_color, transform=ccrs.Geodetic())


            frames_for_anim_list.append((orbit_frame,))
        # dynamic tail of satellite tail
        if satellite_tail <= 10:
            satellite_tail += 2
    plt.show()

    #plot_annotation = ax.annotate("", (0, 0))
    # print(plot_anotation.__dir__())
    # print(plot_orbit_object[0].__dir__())
    # handles, labels = ax.get_legend_handles_labels()

    # plt.legend(list(set(handles)), list(set(labels)))
    # plt.legend()

    return frames_for_anim_list, fig

def calc_skalar_product(input_grace_position, input_gps_position):

    dot = numpy.dot(input_grace_position, input_gps_position)
    grace_mod = numpy.sqrt((input_grace_position * input_grace_position).sum())
    gps_mod = numpy.sqrt((input_gps_position * input_gps_position).sum())
    cos_angle = dot / grace_mod / gps_mod
    angle = numpy.arccos(cos_angle) * (180 / numpy.pi)

    return angle


# fargs=(sat_orbits_dict, sat_names, index_start, ax)
def animate_orbit_movement(i, input_sat_orbits_dict, input_sat_names, input_index_start, input_ax):


    print("- rendering frame ", i)
    for sat_name in input_sat_names:

        if "graceA" == sat_name:
            #print("- GRACE A MATCH")
            sat_label = "GRACE A"
            sat_color = "red"
            satellite_tail = 8

        else:
            satellite_tail = 5
            sat_label = "GPS"
            sat_color = "yellow"

            grace_position = input_sat_orbits_dict["graceA"][input_index_start + i]
            gps_sat_position = input_sat_orbits_dict[sat_name][input_index_start + i]

            angle = calc_skalar_product(grace_position.get_koords(), gps_sat_position.get_koords())

            if angle >= 90:
                lam_line_of_sight = [grace_position.lam(), gps_sat_position.lam()]
                phi_line_of_sight = [grace_position.phi(), gps_sat_position.phi()]

                input_ax.plot(lam_line_of_sight, phi_line_of_sight, color="cyan", label="visibility")

                #print("Winkel Zwischen Sat: ", angle)
        sat_data_phi = [satellite.phi() for satellite in input_sat_orbits_dict[sat_name][input_index_start + i - satellite_tail: input_index_start + i]]
        sat_data_lam = [satellite.lam() for satellite in input_sat_orbits_dict[sat_name][input_index_start + i - satellite_tail: input_index_start + i]]


        #print("- proccessing satorbit for %s" % sat_name, " lam: ", sat_data_lam)

        input_ax.plot(sat_data_lam, sat_data_phi, color=sat_color, label=sat_label, transform=ccrs.Geodetic())
        input_ax.plot(sat_data_lam[-1], sat_data_phi[-1], 'o', color=sat_color, markersize=2, label=sat_label, transform=ccrs.Geodetic())
        input_ax.annotate(sat_name, (sat_data_lam[-1], sat_data_phi[-1]), color=sat_color )

    return input_ax

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
    for sat in sat_orbit_txt_list:
        index_sat_epoch = 0

        sat_name = sat.split(".")[1]
        if input_verbosity: ("- reading out and storing data of satellite: ", sat_name)
        # list of satellite epochs of type Satellite
        sat_epoch_list = []

        # read out satdata from gz
        sat_data = numpy.loadtxt(sat, skiprows=2)

        # refzdatum 1858-11-17

        for epoch in sat_data:
            # calc the UTC date for the mdj entry
            epoch_date = calc_utc_date(epoch[0])

            # write index of every epoch onto dict - gets refilled every time - not beautiful i hope i find a better solution
            satellite_orbits_time_epoch_index_dict[epoch_date] = index_sat_epoch

            # append every sat epoch to a list and store it on the satellit_orbits_dict with sat_name as key and the list as value
            sat_epoch_list.append(Satellite(epoch_date, sat_name, epoch[1], epoch[2], epoch[3]))

            # print(start_date)
            # print(epoch_date)
            # print(jul_date)
            index_sat_epoch += 1

        # store all orbit epochs of each satellite onto a dict with the satname as the key and a list with Satellite objects as value
        satellite_orbits_dict[sat_name] = sat_epoch_list
    print("- finished reading out and storing of sat orbit data")

    return satellite_orbits_dict, satellite_orbits_time_epoch_index_dict


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