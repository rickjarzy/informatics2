# Paul Arzberger
# 00311430
# Informatics 2 - SS19
# Gruppe A - Programm 1: Drohnengetragenes Laserscanning

import datetime
import numpy
import time
import scipy.ndimage
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
# =====================================================================================
# Class Definitions
# =====================================================================================
class Epoch:
    """
    class Epoch contains the time attribute of type datetime and is the base class for the classes
    PositionEpoch and PolarEpoch
    """
    # Constructor
    def __init__(self, time, epoch_type="", verbose_input=False):
        """
        creates an instance of class Epoch and assignes the instance attribute time a datetime-value
        :param time: of type datetime
        :param epoch_type: string - that is handed to the screenprint and defines which of the inheriting classes is created.
                                    if the epoch_type is Empty a default empty string is handed to the print function
        :param verbose_input: True/False - will be set at the attribute self.__verbose and takes influence the information that
                                    gets screened during the instantiation and deleting process of the class Epoch and its heritating
                                    subclasses
        """
        if isinstance(time, datetime.datetime):

            #print("  type: ", type(time))
            self.__time = time              # has to be of type datetime
            self.__verbose = verbose_input  # bool True or False - takes influence if info is screened during instantiation or deleting process


            # if verbose is set True the instantiation information will be printed to screen
            if self.__verbose:
                print("+ Creating new {}Epoch instance with time: {}".format(epoch_type, time))
        else:
            raise ValueError("!! The input time is not of type datetime.datetime !!")

    # string representation if you print the instance on the screen
    def __str__(self):
        return "Timeepoch {}".format(self.time)

    def __del__(self):
        if self.__verbose:
            print("- DELETE ALLLLL ")

    # make the private attribute accessible for the public as a property
    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, time):
        self.__time = time

    # property getter method to access verbose in the classes that inherrit from Epoch
    @property
    def verbose(self):
        return self.__verbose

    @verbose.setter
    def verbose(self, bool_val):
        self.__verbose = bool_val


class PositionEpoch(Epoch):

    #Constructor
    def __init__(self, time, x=0., y=0., z=0., verbose_input=False):
        """

        :param time: datetime - the epochs time when it was recorded
        :param x:    float - x coordinate
        :param y:    float - y coordinate
        :param z:    float - z coordinate
        :param verbose_input: bool - if set true, instantiantion and deletion will print messeges to the screen
        """
        super().__init__(time, "Position", verbose_input)

        try:
            if isinstance(float(x), float) and isinstance(float(y), float) and isinstance(float(z), float):
                self.__x = x
                self.__y = y
                self.__z = z

                if self.verbose:
                    print("  x={} y={} z={}\n".format(self.__x, self.__y, self.__z))

        except ValueError:
            print("!!ERROR Constructor: \n  one of he inputparameters x: {} - {} - y: {} - {} - z: {} - {} is not useable\n"
                             "  input must be a number or at least typecastable to a number"
                             .format(x, type(x), y, type(y), z, type(z)))
            # delete instance if input parameters are wrong
            del self

    # string representation of the instance
    def __str__(self):
        return "PositionEpoch Instance {}\n   x={} y={} z={}\n".format(self.time, self.__x, self.__y, self.__z)

    # if verbose in the base class is true - a message will be printed out when the instance DIES
    def __del__(self):
        if self.verbose:
            print("- Delete PositionEpoch Instance {}\n  x={} y={} z={}".format(self.time, self.__x, self.__y,
                                                                                self.__z))

    # PROPERTIES
    # ---------------------------
    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self, value):
        self.__y = value

    @property
    def z(self):
        return self.__z

    @z.setter
    def z(self, value):
        self.__z = value


class PolarEpoch(Epoch):

    # constructor
    def __init__(self, time, distance=0., zenith=0., azimuth=0., verbose_input=False):
        """

        :param time:
        :param distance:
        :param zenith:
        :param azimuth:
        :param verbose_input:
        """
        super().__init__(time, "Polar", verbose_input)
        try:
            if float(distance) and float(zenith) and float(azimuth):
                self.__distance = distance
                self.__zenith = zenith
                self.__azimuth = azimuth

                if self.verbose:
                    print("  distance={} zenith={} azimuth={}".format(self.__distance, self.__zenith, self.__azimuth))

        except ValueError:
            print("!!ERROR Constructor: \n  one of he inputparameters distance: {} - {} - zenith: {} - {} - azimuth: {} - {} is not useable\n"
                             "  input must be a number or at least typecastable to a number"
                             .format(distance, type(distance), zenith, type(zenith), azimuth, type(azimuth)))
            # delete instance if input parameters are wrong
            del self

    # string representation of the instance if you print the class to the screen
    def __str__(self):
        return "PolarEpoch Instance {}\n   distance={} zenith={} azimuth={}\n" \
                .format(self.time, self.__distance, self.__zenith, self.__azimuth)

    def __del__(self):

        # if verbose in the base class is true - a message will be printed out when the instance DIES
        if self.verbose:
            print("- Delete PolarEpoch Instance {}\n  distance={} zenith={} azimuth={}".format(self.time, self.__distance, self.__zenith, self.__azimuth))

    def __eq__(self, other):

        pass

    # PROPERTIES
    # ---------------------------

    @property
    def distance(self):
        return self.__distance

    @distance.setter
    def distance(self, value):
        self.__distance = value

    @property
    def zenith(self):
        return self.__zenith

    @zenith.setter
    def zenith(self, value):
        self.__zenith = value

    @property
    def azimuth(self):
        return self.__azimuth

    @azimuth.setter
    def azimuth(self, value):
        self.__azimuth = value

    @property
    def tachymeter_epoch(self):
        return self.__tachymeter_epoch

    @tachymeter_epoch.setter
    def tachymeter_epoch(self, tachy_epoch):
        """
        sets the corresponding tachymeter epoch to the laser scanner epoch
        :param value: PolarEpoch instance
        :return: none
        """
        print("   Assign Tachymeter Epoch to Scanner Epoch")
        if isinstance(tachy_epoch, PolarEpoch):
            self.__tachymeter_epoch = tachy_epoch
        else:
            raise TypeError("!! ERROR - handed instance is not of type PolarEpoch\n   input: {} is of type {}".format(tachy_epoch, type(tachy_epoch)))

    # getter methods to calculate the x, y, z coordinates of the polar epoch - as property
    def x_1ha(self, origin):
        """
        Calculates the X Part of the "Erste Hauptaufgabe" from the origin to the  other position and returns it

        :return: float
        """
        if isinstance(origin, PositionEpoch):
            return origin.x + self.__distance * numpy.sin(self.__zenith) * numpy.cos(self.__azimuth)
        else:
            raise TypeError("!! ERROR - handed instance is not of type PositionEpoch\n   input: {} is of type {}".format(origin, type(origin)))

    def y_1ha(self, origin):
        """
        Calculates the Y Part of the "Erste Hauptaufgabe" from the origin to the  other position and returns it
        :return: float
        """
        if isinstance(origin, PositionEpoch):
            return origin.y + self.__distance * numpy.sin(self.__zenith) * numpy.sin(self.__azimuth)
        else:
            raise TypeError("!! ERROR - handed instance is not of type PositionEpoch\n   input: {} is of type {}".format(origin, type(origin)))

    def z_1ha(self, origin):
        """
        Calculates the Z Part of the "Erste Hauptaufgabe" from the origin to the  other position and returns it
        :return: float
        """
        if isinstance(origin, PositionEpoch):
            return origin.z + self.__distance * numpy.cos(self.__zenith)
        else:
            raise TypeError("!! ERROR - handed instance is not of type PositionEpoch\n   input: {} is of type {}".format(origin, type(origin)))


class Timer():
    """
    Timer class to check how long the algorithm runs
    """
    def __init__(self):
        self.__starttime = None
        self.__endtime = None

    # overwrite the enter method
    def __enter__(self):
        print("Start taking Time ...")
        self.__starttime = time.process_time()
        return self

    # overwrite the exit method
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Process took {} [sec] to finish\n".format(time.process_time()-self.__starttime))
# =====================================================================================
# Function listing
# =====================================================================================

def read_obs_data(input_file_path, input_start_epoch, verbose=False):
    """
    Function to read out the observed tachimeter data and the laser scanner data. it takes the filepath as input and the start_epoch
    :param input_file_path:         string - filepath to the file to read out
    :param input_start_epoch:   datetime - startepoch of the tachymeter measurements
    :param verbose:                 True/False - per default False. is handed to the class Instance and allows to print some instatiation screening info
    :return:                  list - list with instances of PolarEpochs
    """

    #convert start_epoch of type datetime into total seconds type float
    start_epoch_seconds = input_start_epoch.timestamp()

    # open file with context manager
    with open(input_file_path,"r") as file:

        observation_list = []   # will be returned with Objects of type PolarEpoch
        #cou = 0

        for line in file.readlines():

            # read out each line of the file, strip the \n at the end and split it at the white spaces to tokens and store them in a list
            [t_sec_str, dist_m_str, zenit_rad_str, azimuth_rad_str] = line.rstrip("\n").split()

            # add the observed time from the file to the start time epoch to get the new epoch in datetime format
            new_epoch = datetime.datetime.fromtimestamp(start_epoch_seconds + float(t_sec_str))

            # append each observation to the returnlist as type PolarEpoch
            observation_list.append(PolarEpoch(new_epoch, float(dist_m_str), float(zenit_rad_str), float(azimuth_rad_str), verbose))

            #if cou == 15:
            #    break
            #cou += 1

        print("- len of observation_list - %s : " % input_file_path, len(observation_list))

    return observation_list


def bubble_sort(input_list):
    """

    :param input_list:
    :return:
    """

    number_of_elements = len(input_list)

    for max_iterations in range(number_of_elements-1, 0, -1):       # walk from biggest/last to lowest/first element
        for index in range(max_iterations):
            if input_list[index].time > input_list[index+1].time:             # if the neighbour right to the actual position is bigger
                input_list[index], input_list[index +1] = input_list[index +1], input_list[index]   # switch positions

    return input_list

def create_datetime_object(input_time):
    pass

# =====================================================================================
# Main Programm
# =====================================================================================

if __name__ == "__main__":

    with Timer():
        # start time epoch as string taken from the lab report
        start_epoch_string = "2018-03-13 15:10:00"

        #convert start epoch string into datetime object
        start_epoch_datetime_object = datetime.datetime.strptime(start_epoch_string, '%Y-%m-%d %H:%M:%S')

        tachymeter_position = PositionEpoch(start_epoch_datetime_object, -51.280, -4.373, 1.340, True)

        print("Start Import")

        # read out laser scanner data - add third function parameter verbose=True to see if class objects get deleted
        scanner_polar_epochs_list = read_obs_data("obsDrone.txt", start_epoch_datetime_object)

        # read out tachymeter data - add third function parameter verbose=True to see if class objects get deleted
        tachy_polar_epochs_list = read_obs_data("obsTachy.txt", start_epoch_datetime_object)

        # sorts the chaotic tachymeter observations and writes it back on the variable
        # you also could do bubble_sort(tachy_polar_epochs_list) but its not that easy to read if the return value is missing
        tachy_polar_epochs_list = bubble_sort(tachy_polar_epochs_list)

        # calculating drone position relative to the tachymeter position by using
        drone_traj_position_list = [PositionEpoch(polarep.time, polarep.x_1ha(tachymeter_position), polarep.y_1ha(tachymeter_position), polarep.z_1ha(tachymeter_position)) for polarep in tachy_polar_epochs_list]

        print("len of position_list: ", len(drone_traj_position_list))

        scanner_point_measurement_x_list = []
        scanner_point_measurement_y_list = []
        scanner_point_measurement_z_list = []

        scanner_ground_point_full_x_list = []
        scanner_ground_point_full_y_list = []
        scanner_ground_point_full_z_list = []
        print("Matching Epochs ...")

        raster_50_50_dict = {}                # initializing the 5,45x0,50 raster where to store the laserscanner values from each drone-trajectory-line
        start_recording = False         # initial values for laserscanner, at the beginning it does not record groundpoints
        stop_recording = True           # intial values for laserscanner , at the beginning it does not record groundpoints
        cou_line = 0

        for tachy_pos_epoch in drone_traj_position_list:

            # filter all epochs of the scanner that are recorded at the same time like the tachy_epoch
            sub_list_scanner_epochs = list(filter(lambda scanner_epoch: scanner_epoch.time == tachy_pos_epoch.time, scanner_polar_epochs_list))

            # build mean of measurements
            if len(sub_list_scanner_epochs) > 0:
                start_recording = True      # turn on the recording flag

                z_value = numpy.nanmean(numpy.array([item.z_1ha(tachy_pos_epoch) for item in sub_list_scanner_epochs]))
                scanner_point_measurement_z_list.append(z_value)
                scanner_point_measurement_x_list.append(tachy_pos_epoch.x)
                scanner_point_measurement_y_list.append(tachy_pos_epoch.y)

                for groundpoint in sub_list_scanner_epochs:
                    scanner_ground_point_full_x_list.append(tachy_pos_epoch.x)
                    scanner_ground_point_full_y_list.append(tachy_pos_epoch.y)
                    scanner_ground_point_full_z_list.append(groundpoint.z_1ha(tachy_pos_epoch))


                # if the laser scanner switches to start recording create a new list where the groundpoints will get stored
                if start_recording and stop_recording:

                    cou_line += 1
                    print("Start Recording - line %d" % cou_line)
                    raster_line = []

                stop_recording = False          # turn of the not recording flag
                raster_line.append(z_value)


            else:   # if laserscanner is not measureing set the flags to not recording mode

                start_recording = False

                # when recording stops - write out collected data to raster_50_50_dict
                if start_recording == False and stop_recording == False:
                    print("Stop Recording - line %d" % cou_line)

                    # every second line hast to be reversed because of the drones heading changing for 180 degree
                    if (cou_line % 2 == 0):

                        for z_val in reversed(raster_line):
                            raster_50_50_dict[str(cou_line)] = raster_line
                    else:
                        for z_val in raster_line:
                            raster_50_50_dict[str(cou_line)] = raster_line

                stop_recording = True
                pass


        # get the numbers of obersvations for each laser scanner line
        max_col_list = [len(raster_50_50_dict[laser_scanner_data]) for laser_scanner_data in raster_50_50_dict]

        # create a raster for the laserscanner data
        raster_50_50_arr = numpy.zeros((cou_line, max(max_col_list)))

        for row in raster_50_50_dict:

            for col in range(0,len(raster_50_50_dict[row]),1):
                raster_50_50_arr[int(row)-1, col] = raster_50_50_dict[row][col]

        print("Max cols: ", max(max_col_list))
        print("Raster_50_50 shape: ", raster_50_50_arr.shape)


        # resample raster to 50x50



        # Trajectory
        plt.figure()
        plt.plot([drone_pos.x for drone_pos in drone_traj_position_list], [drone_pos.y for drone_pos in drone_traj_position_list], label="raw trajectory")
        plt.plot(drone_traj_position_list[0].x, drone_traj_position_list[0].y, label="start point", marker='^', markerfacecolor='red', markersize=6, linewidth=3)
        plt.plot(drone_traj_position_list[-1].x, drone_traj_position_list[-1].y, label="end point", marker='^', markerfacecolor='red', markersize=6, linewidth=3)
        plt.plot(scanner_point_measurement_x_list, scanner_point_measurement_y_list, label="trajectory where points get collected")
        plt.legend()
        plt.xlabel("X Coordinates [m]")
        plt.ylabel("Y Coordinates [m]")
        plt.title("2D Drone Trajectory")


        # 3d Surface plot
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        X, Y = numpy.meshgrid(scanner_point_measurement_x_list, scanner_point_measurement_y_list)
        print("X type: {}\n\X len: {} \nshape {}".format(type(X), len(X), X.shape))

        Z = numpy.array(scanner_point_measurement_z_list).reshape(1, len(scanner_point_measurement_z_list))
        print("Z type: {}\n\Z len: {} \nshape {}".format(type(Z), len(Z), Z.shape))
        # Plot the surface.
        surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                               linewidth=0, antialiased=False)
        # Customize the z axis.
        ax.set_zlim(numpy.nanmin(Z), numpy.nanmax(Z))
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        # Add a color bar which maps values to colors.
        fig.colorbar(surf, shrink=0.5, aspect=5)
        ax.set_title("3D Surface Plot")


        # 3d Scattrer plot
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot3D(scanner_point_measurement_x_list, scanner_point_measurement_y_list, scanner_point_measurement_z_list, 'gray')
        ax.scatter3D(scanner_point_measurement_x_list, scanner_point_measurement_y_list, scanner_point_measurement_z_list,
                     c=scanner_point_measurement_z_list, cmap='jet', linewidths=0.5,)
        ax.set_title("Scatter plot")
        ax.set_xlabel("X Coorinates of Groundpoint [m]")
        ax.set_ylabel("Y Coorinates of Groundpoint [m]")
        ax.set_zlabel("MEAN Z Coorinates of Groundpoint [m]")


        # 3d Scattrer plot - FULL resolution
        fig = plt.figure()
        ax = fig.gca(projection='3d')

        ax.scatter3D(scanner_ground_point_full_x_list, scanner_ground_point_full_y_list, scanner_ground_point_full_z_list,
                     c=scanner_ground_point_full_z_list, cmap='jet', linewidths=0.5,)
        ax.set_title("Scatter plot - Full Resolution")
        ax.set_xlabel("X Coorinates of Groundpoint [m]")
        ax.set_ylabel("Y Coorinates of Groundpoint [m]")
        ax.set_zlabel("MEAN Z Coorinates of Groundpoint [m]")

        # tri surface
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_trisurf(scanner_point_measurement_x_list, scanner_point_measurement_y_list, scanner_point_measurement_z_list,
                        cmap='viridis', edgecolor='none')
        ax.set_title("Trisurface ")

        # tri surface
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_trisurf(scanner_ground_point_full_x_list, scanner_ground_point_full_y_list, scanner_ground_point_full_z_list,
                        cmap='viridis', edgecolor='none')
        ax.set_title("Trisurface - Full Resolution")

        # imshow
        plt.figure()
        plt.imshow(raster_50_50_arr)
        plt.title("Raster 5,5 X 0,5 [m]")



        #plt.show()

        print("Programm ENDE")
