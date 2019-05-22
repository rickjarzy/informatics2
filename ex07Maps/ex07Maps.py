import numpy
from matplotlib import pyplot as plt
import cartopy.crs as ccrs


if __name__ == "__main__":

    # read out satdata and skip header information
    sat_data = numpy.loadtxt(r"orbit.txt", skiprows=2)
    blue_mrbl_jpg = plt.imread(r"bluemarble01.jpg")

    # calc the norm of the vector for each epoch
    r = numpy.linalg.norm(sat_data[:, 1:], axis=1)

    phi = numpy.arcsin(sat_data[:, 3] / r) * 180/numpy.pi
    print(numpy.nanmax(phi))
    lam = numpy.arctan2(sat_data[:, 2], sat_data[:, 1]) * (180 / numpy.pi)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
    ax.imshow(blue_mrbl_jpg, origin='upper', transform=ccrs.PlateCarree())
    ax.plot(lam, phi, color='red', transform=ccrs.PlateCarree())
    ax.set_title("Grace orbit on 2008-01-01")


    #ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    #ax.imshow(blue_mrbl_jpg, origin='upper', transform=ccrs.Robinson())
    #ax.plot(lam, phi, color='red', )    #linestyle='None'



    #

    plt.show()

    print("Programm ENDE")