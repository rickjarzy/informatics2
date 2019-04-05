# Paul Arzberger
# 00311430
# Informatics 2 - SS19
# Gruppe A - Programm 1: Drohnengetragenes Laserscanning

import datetime
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
            self.__verbose = verbose_input  # bool True or False - takes influence if info is screened during instantiation or deleting prcoess

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

    # string representation of the instance
    def __str__(self):
        return "PositionEpoch Instance {}\nx={} y={} z={}\n".format(self.time, self.__x, self.__y, self.__z)

    # if verbose in the base class is true - a message will be printed out when the instance DIES
    def __del__(self):
        if self.verbose:
            print("- Delete PositionEpoch Instance {}\n  x={} y={} z={}".format(self.time, self.__x, self.__y, self.__z))


class PolarEpoch(Epoch):

    # constructor
    def __init__(self, time, distance=0., zenith=0., azimuth=0., verbose_input=False):
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

    # string representation of the instance if you print the class to the screen
    def __str__(self):
        return "PolarEpoch Instance {}\n  distance={} zenith={} azimuth={}\n".format(self.time, self.__distance, self.__zenith, self.__azimuth)

    def __del__(self):

        # if verbose in the base class is true - a message will be printed out when the instance DIES
        if self.verbose:
            print("- Delete PolarEpoch Instance {}\n  distance={} zenith={} azimuth={}".format(self.time, self.__distance, self.__zenith, self.__azimuth))



# =====================================================================================
# Function listing
# =====================================================================================

def read_obs_data(input_file_path, input_start_epoch_str, verbose=False):
    """
    Function to read out the observed tachimeter data and the laser scanner data. it takes the filepath as input and the start_epoch
    :param input_file_path:         string - filepath to the file to read out
    :param input_start_epoch_str:   string - string of observation starttime in datetime format
    :param verbose:                 True/False - per default False. is handed to the class Instance and allows to print some instatiation screening info
    :return:                  list - list with instances of PolarEpochs
    """

    #convert start epoch string into datetime object
    start_epoch_datetime_object = datetime.datetime.strptime(input_start_epoch_str, '%Y-%m-%d %H:%M:%S')

    #convert start_epoch of type datetime into total seconds type float
    start_epoch_seconds = start_epoch_datetime_object.timestamp()

    # open file with context manager
    with open(input_file_path,"r") as file:

        observation_list = []   # will be returned with Objects of type PolarEpoch
        cou = 0

        for line in file.readlines():

            # read out each line of the file, strip the \n at the end and split it at the white spaces to tokens and store them in a list
            [t_sec_str, dist_m_str, zenit_rad_str, azimuth_rad_str] = line.rstrip("\n").split()

            # add the observed time from the file to the start time epoch to get the new epoch in datetime format
            new_epoch = datetime.datetime.fromtimestamp(start_epoch_seconds + float(t_sec_str))

            # append each observation to the returnlist as type PolarEpoch
            observation_list.append(PolarEpoch(new_epoch, float(dist_m_str), float(zenit_rad_str), float(azimuth_rad_str), verbose))

            cou += 1
            if cou == 10:
                break
        print("- len of observation_list: ", len(observation_list))

    return observation_list

# =====================================================================================
# Main Programm
# =====================================================================================


if __name__ == "__main__":

    # start time epoch as string taken from the lab report
    start_epoch_string = "2018-03-13 15:10:00"

    print("Start Import")

    # read out laser scanner data - add third function parameter verbose=True to see if class objects get deleted
    scanner_polar_epochs_list = read_obs_data("obsDrone.txt", start_epoch_string)

    # read out tachymeter data - add third function parameter verbose=True to see if class objects get deleted
    tachy_polar_epochs_list = read_obs_data("obsTachy.txt", start_epoch_string, verbose=True)

    print("tachy 1 - zenith: ", tachy_polar_epochs_list[0].zenith)
    print(tachy_polar_epochs_list[0])

    print("Programm ENDE")