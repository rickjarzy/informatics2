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
    stages = len(sig_ele["amplitudes"])
    fig, ax = plt.subplots(figsize=(10, 5))
    t = sig_noi[:,0]
    for i in range(0,stages,1):
        print("Calc Signal N {}\n-------------".format(i))
        A = float(sig_ele["amplitudes"][i])
        f = float(sig_ele["frequencies"][i])
        phi = float(sig_ele["phases"][i])
        linecolor = sig_ele["colors"][i]
        calc_signal = A * numpy.sin(2 * numpy.pi * f * t + phi * (numpy.pi/180))

        ax.plot(t, calc_signal, label="A = {}, f = {} Hz, phi = {} deg".format(A,f,phi))
    plt.legend()
    plt.show()

if __name__ == "__main__":

    signal_elements = readSignals("signals.txt")

    signal_noise = numpy.loadtxt("noise.txt")

    plotSignal(signal_elements, signal_noise)







    print("Programm ENDE")