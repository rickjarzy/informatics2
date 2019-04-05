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
    def __init__(self, time, epoch_type=""):
        """
        creates an instance of class Epoch and assignes the instance attribute time a datetime-value
        :param time: of type datetime
        :param epoch_type: string - that is handed to the screenprint and defines which of the inheriting classes is created.
                                    if the epoch_type is Empty a default empty string is handed to the print function
        """
        if isinstance(time, datetime.datetime):
            print("+ Creating new {}Epoch instance with time: {}".format(epoch_type, time) )
            #print("  type: ", type(time))
            self.__time = time          # has to be of type datetime
        else:
            raise ValueError("!! The input time is not of type datetime.datetime !!")

    # string representation if you print the instance on the screen
    def __str__(self):
        return "Timeepoch {}".format(self.time)

    # make the private attribute accessible for the public as a property
    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, time):
        self.__time = time

class PositionEpoch(Epoch):

    #Constructor
    def __init__(self, time, x=0., y=0., z=0.):
        super().__init__(time, "Position")

        try:
            if isinstance(float(x), float) and isinstance(float(y), float) and isinstance(float(z), float):
                self.__x = x
                self.__y = y
                self.__z = z
                print("  x={}\n  y={}\n  z={}".format(self.__x, self.__y, self.__z))

        except ValueError:
            print("!!ERROR Constructor: \n  one of he inputparameters x: {} - {} - y: {} - {} - z: {} - {} is not useable\n"
                             "  input must be a number or at least typecastable to a number"
                             .format(x, type(x), y, type(y), z, type(z)))
            # delete instance if input parameters are wrong
            del self

    def __str__(self):
        return "PositionEpoch Instance {}\nx={}\ny={}\nz={}".format(self.time, self.__x, self.__y, self.__z)

    def __del__(self):
        print("- Delete PositionEpoch Instance {}\n  x={}\n  y={}\n  z={}".format(self.time, self.__x, self.__y, self.__z))

class PolarEpoch(Epoch):

    # constructor
    def __init__(self, time, distance=0., zenith=0., azimuth=0.):
        super().__init__(time, "Polar")
        try:
            if float(distance) and float(zenith) and float(azimuth):
                self.__distance = distance
                self.__zenith = zenith
                self.__azimuth = azimuth
                print("  distance={}\n  zenith={}\n  azimuth={}".format(self.__x, self.__y, self.__z))

        except ValueError:
            print("!!ERROR Constructor: \n  one of he inputparameters distance: {} - {} - zenith: {} - {} - azimuth: {} - {} is not useable\n"
                             "  input must be a number or at least typecastable to a number"
                             .format(distance, type(distance), zenith, type(zenith), azimuth, type(azimuth)))
            # delete instance if input parameters are wrong
            del self
    # string representation if you print the class to the screen
    def __str__(self):
        return "PolarEpoch Instance {}\n  distance={}\n  zenith={}\n  azimuth={}".format(self.time, self.__distance, self.__zenith, self.__azimuth)

    def __del__(self):
        print("- Delete PolarEpoch Instance {}\n  distance={}\n  zenith={}\n  azimuth={}".format(self.time, self.__distance, self.__zenith, self.__azimuth))

# =====================================================================================
# Function listing
# =====================================================================================

def read_obs_data(input_file_path, input_start_epoch_seconds, input_class_type):

    # open file with context manager
    with open(input_file_path,"r") as file:

        start_epoch_seconds = input_start_epoch_seconds

        observation_list = []   # will be returned
        cou = 0
        for line in file.readlines():

            # read out each line of the file, strip the \n at the end and split it at the white space
            [t_sec_str, dist_m_str, zenit_rad_str, azimuth_rad_str] = line.rstrip("\n").split()

            # calculate new epoch with timeinformation of type datetime
            print("- t_sec_str: ", t_sec_str)
            print("- t_sec_str float:   ", float(t_sec_str))


            new_epoch = datetime.datetime.fromtimestamp(start_epoch_seconds + float(t_sec_str))

            print("- start epoch: ", datetime.datetime.fromtimestamp(input_start_epoch_seconds))
            print("- new   epoch: ", new_epoch, " - type: ", type(new_epoch))

            if input_class_type == "PolarEpoch":
                observation_list.append(PolarEpoch(new_epoch))
            else:
                observation_list.append(PositionEpoch(new_epoch))

            cou += 1
            if cou == 10:
                break
        print("- len of observation_list: ", len(observation_list))
        print(observation_list[0])
    pass

# =====================================================================================
# Main Proramm
# =====================================================================================


if __name__ == "__main__":

    # start time epoch as string taken from the lab report
    start_epoch_string = "2018-03-13 15:10:00"

    #convert start epoch string into datetime object
    start_epoch_datetime_object = datetime.datetime.strptime(start_epoch_string, '%Y-%m-%d %H:%M:%S')

    #convert start_epoch of type datetime into total seconds type float
    start_epoch_seconds = start_epoch_datetime_object.timestamp()


    print("Start Import")

    read_obs_data("obsDrone.txt", start_epoch_seconds, "PositionEpoch")

    check = PositionEpoch(start_epoch_datetime_object, 10, "100", "100")
    check2 = PolarEpoch(start_epoch_datetime_object, 10, "100", "59.456")
    print(type(check))
    print(check)

    print("Programm ENDE")