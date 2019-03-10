# Paul Arzberger
# 00311430
# Informatics 2 - SS19
# Gruppe A
import numpy
from matplotlib import pyplot as plt

def readSignals(file_path):
    """Reads out the signals.txt and writes the content on a dict"""
    # open file with context manager
    with open(file_path,"r") as file:

        return_dict = {}                                # allocate dict

        for line in file.readlines():

            parts = line.rstrip("\n").split("=")            # remove newline and split at the equals sign
            #print(parts)                                    # element of signal on index 0 - stages as index 0 as csv
            #pint(parts[1].split(","))                      #split right side - so list with elements exists
            return_dict[parts[0]] = parts[1].split(",")     # write info onto return dict with elements of signal as key
        #print(return_dict)
        print("# data import %s successful" % file_path)
        return return_dict


def plotSignal(ax, sig_ele, sig_noi, i):
    """Calculates two sgnals one with noise and one pure The calculated signals will be plot in a single figure and saved as png
    """
    A = float(sig_ele["amplitudes"][i])
    f = float(sig_ele["frequencies"][i])
    phi = float(sig_ele["phases"][i])
    t = sig_noi[:, 0]  # the time in ms from the sig_noise txt
    linecolor = sig_ele["colors"][i]

    calc_signal = A * numpy.sin(2 * numpy.pi * f * t + phi * (numpy.pi/180))                    # signal without noise
    calc_noise = A * numpy.sin(2 * numpy.pi * f * t + phi * (numpy.pi / 180))+sig_noi[:,i+1]    # signal with noise

    ax.set_xlabel("Time [s]")
    ax.set_xlim((0,1))
    ax.grid(True)
    ax.plot(t, calc_signal, label="A = {}, f = {} Hz, phi = {} deg".format(A, f, phi), color=linecolor)
    ax.plot(t, calc_noise, marker='o', color=linecolor, linewidth=0)


if __name__ == "__main__":

    print("ex01Signals\nPaul Arzberger\n=======================================\n")

    #readout the signal noise and time info
    signal_noise = numpy.loadtxt("noise.txt")
    print("data import %s successful" % "noise.txt")

    # read out the signal infos
    signal_elements = readSignals("signals.txt")

    stages = len(signal_elements["amplitudes"])     # how many different signals will be calculated
    fig, ax = plt.subplots(figsize=(10, 5)) # create the plot objects

    # create so many plots and signals according to stages
    for i in range(0,stages,1):
        print("- Calc signal and noisy signal Nr {} ...".format(i))
        # calculate and plot the signals
        plotSignal(ax, signal_elements, signal_noise, i)

    plt.legend()
    plt.show()
    print("- save fig signals.png")
    fig.savefig("signals.png", dpi=300, format="png")
    print("Programm ENDE")