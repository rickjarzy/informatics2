import numpy
from matplotlib import pyplot as plt
import cartopy.crs as ccrs

if __name__ == "__main__":

    gravity_data = numpy.load(r"data/gravityField.npy")

    print(gravity_data)

    print(gravity_data.shape)



    print("Programm ENDE")