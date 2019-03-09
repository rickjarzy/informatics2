# Paul Arzberger
# 00311430
# Informatics 2 - SS19

import numpy
from matplotlib import pyplot as plt

def readSignals(file_path):

    # open file with context manager
    with open(file_path) as file:

        return_dict = {}

        for line in file.readlines():

            parts = line.rstrip("\n").split("=")            # remove newline and split at the equals sign
            #print(parts)                                    # element of signal on index 0 - stages as index 0 as csv
            #pint(parts[1].split(","))                      #split right side - so list with elements exists
            return_dict[parts[0]] = parts[1].split(",")     # write info onto return dict with elements of signal as key
        #print(return_dict)
        return return_dict


def plotSignal(sig_ele, sig_noi):

    fig, ax = plt.figure(figsize=(10,5))

    ax.plot()



if __name__ == "__main__":

    signal_elements = readSignals("signals.txt")

    signal_noise = numpy.loadtxt("noise.txt")


    signal_calc = numpy.ones((signal_noise.shape[0], len(signal_elements["amplitudes"])))
    signal_calc = numpy.multiply(signal_calc, signal_noise[:,0])



    print(signal_calc)
    print(signal_calc.shape)





    print("Programm ENDE")