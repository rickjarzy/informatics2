import datetime


class Epoch():
    """
    class Epoch contains the time attribute and is the base class for the classes
    PositionEpoch and PolarEpoch
    """

    def __init__(self, time):

        if isinstance(time, datetime.datetime):
            print("Create Epoch with time: ", time)
            self.__time = time          # has to be of type datetime
        else:
            raise ValueError("!! The input time is not of type datetime.datetime !!")

    def __str__(self):
        return "Timeepoch {}".format(self.time)
    # make the private attribute accessible for the public
    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, time):
        self.__time = time

# =====================================================================================
# Function listing
# =====================================================================================

def read_obs_data(input_file_path, input_start_epoch_seconds):


    # open file with context manager
    with open(input_file_path,"r") as file:

        start_epoch_seconds = input_start_epoch_seconds

        observation_dict = []   # will be returned
        cou = 0
        for line in file.readlines():

            # read out each line of the file, strip the \n at the end and split it at the white space
            [t_sec_str, dist_m_str, zenit_rad_str, azimuth_rad_str] = line.rstrip("\n").split()

            # calculate new epoch with timeinformation of type datetime
            start_epoch_seconds += float(t_sec_str)
            new_epoch = datetime.datetime.fromtimestamp(start_epoch_seconds)
            print("t_sec_str:   ", t_sec_str)
            print("start epoch: ", datetime.datetime.fromtimestamp(input_start_epoch_seconds))
            print("new   epoch: ", new_epoch, " - type: ", type(new_epoch))

            observation_dict.append(Epoch(new_epoch))

            cou += 1
            if cou == 10:
                break


    pass

if __name__ == "__main__":

    # start time epoch as string taken from the lab report
    start_epoch_string = "2018-03-13 15:10:00"

    #convert start epoch string into datetime object
    start_epoch_datetime_object = datetime.datetime.strptime(start_epoch_string, '%Y-%m-%d %H:%M:%S')

    #convert start_epoch of type datetime into total seconds type float
    start_epoch_seconds = start_epoch_datetime_object.timestamp()


    print("Start Import")

    read_obs_data("obsDrone.txt", start_epoch_seconds)



    print("Programm ENDE")