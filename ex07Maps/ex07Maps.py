import numpy
from matplotlib import pyplot as plt
import cartopy.crs as ccrs


if __name__ == "__main__":

    # read out satdata and skip header information
    sat_data = numpy.loadtxt(r"data/orbit.txt", skiprows=2)
    blue_mrbl_jpg = plt.imread(r"data/bluemarble01.jpg")

    print(sat_data[:, 1:])

    # calc the norm of the vector for each epoch
    r = numpy.linalg.norm(sat_data[:, 1:], axis=1)

    phi = numpy.arcsin(sat_data[:, 3]/r)

    lam = numpy.arctan2(sat_data[:, 2],sat_data[:, 1])

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
    ax.imshow(blue_mrbl_jpg, origin='upper', transform=ccrs.PlateCarree())
    ax.tissot(facecolor='red', alpha=0.4)
    plt.show()

    print("Programm ENDE")