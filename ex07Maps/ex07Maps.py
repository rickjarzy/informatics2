# Paul Arzberger
# 00311430
# Informatics 2 - SS19
# Gruppe A



import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs


def animate(i, data, text, coast, grid):

    """
    function that creates all the singe frames of the animation
    :param i:
    :param data: ndim numpy array - with gravity data for 12 months
    :param text: text that should be printed in a little box on a certain position and holds time stamp information
    :param coast: matplotlib object that visualizes the coastline of the earth
    :param grid: matpolotlib meshgrid object - for each time stamp an own pcolormesh is created and returned
    :return: text, coast, grid - have to be returned in the exact same way they have handed to the function
    """
    print("create frame for month ", i)
    print("max: ",numpy.nanmax(gravity_data[i]), " min: ", numpy.nanmin(gravity_data[i]))
    grid.set_array(data[i].flatten())
    text.set_text("Month: 2008-{}".format(i+1))
    return text, coast, grid

def animate_via_function(input_data, input_lon, input_lat):
    """
    creates the animation for the gravity field
    :param input_data: ndim numpy array with gravity data for 12 months
    :param input_lon: list - with longitude information as float ( same size as input_lat)
    :param input_lat: list - with latitude information as fload ( same size as input_lon)
    :return:
    """
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
    ax.set_global()
    ax.set_title("Seasonal gravity ignal from GRACE")

    grid = ax.pcolormesh(input_lon, input_lat, input_data[0], cmap='RdBu', vmin=numpy.nanmin(input_data),
                         vmax=numpy.nanmax(input_data), transform=ccrs.PlateCarree())
    coast = ax.coastlines()

    # print a field with the date information
    text = ax.text(-175,-25, "", transform=ccrs.PlateCarree(), bbox=dict(facecolor='white', pad=4))
    cbar = fig.colorbar(grid, orientation='horizontal', extend='both', extendfrac=0.025, aspect=50, pad=0.025,
                        shrink=0.75)

    cbar.set_label("Equivalent water height [cm]")

    # create an FuncAnimation object
    anim = animation.FuncAnimation(fig,  # figure object
                                   animate,  # callable animation function
                                   gravity_data.shape[0],  # number of frames
                                   fargs=(gravity_data, text, coast, grid),  # parameters passed to function
                                   interval=500,  # delay between frames [ms]
                                   blit=True)  # blitting (only redraw changes)

    # save created animation to disc
    anim.save("animation_gravity.mp4")





if __name__ == "__main__":

    # 1.) Sat Orbit
    # =======================

    # read out satdata and skip header information
    sat_data = numpy.loadtxt(r"orbit.txt", skiprows=2)
    blue_mrbl_jpg = plt.imread(r"bluemarble01.jpg")

    # calc the norm of the vector for each epoch
    r = numpy.linalg.norm(sat_data[:, 1:], axis=1)
    phi = numpy.arcsin(sat_data[:, 3] / r) * 180/numpy.pi
    lam = numpy.arctan2(sat_data[:, 2], sat_data[:, 1]) * (180 / numpy.pi)


    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
    ax.imshow(blue_mrbl_jpg, origin='upper', transform=ccrs.PlateCarree())
    ax.plot(lam, phi, color='red', transform=ccrs.Geodetic())       # transform plot
    ax.set_title("Grace orbit on 2008-01-01")

    plt.show()

    # 2.) Animation
    # =======================

    gravity_data = numpy.load(r"gravityField.npy")
    lon_gravity_field_plot = numpy.arange(-180, 181, 1)
    lat_gravity_field_plot = numpy.arange(90, -91, -1)

    animate_via_function(gravity_data, lon_gravity_field_plot, lat_gravity_field_plot)

    print("Programm ENDE")