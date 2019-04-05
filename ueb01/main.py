import datetime
from .Epochs import Epochs

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
            observation_list.append(Epochs.PolarEpoch(new_epoch, float(dist_m_str), float(zenit_rad_str), float(azimuth_rad_str), verbose))

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