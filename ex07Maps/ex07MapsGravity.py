import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cartopy.crs as ccrs


def animate(i, data, text, coast, grid):
    print("i, ", i)
    print("max: ",numpy.nanmax(gravity_data[i]), " min: ", numpy.nanmin(gravity_data[i]))
    grid.set_array(data[i].flatten())
    text.set_text("Month: 2008-{}".format(i+1))
    return text, coast, grid

def animate_via_function(input_data, input_lon, input_lat):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
    ax.set_global()
    ax.set_title("Seasonal gravity ignal from GRACE")

    grid = ax.pcolormesh(input_lon, input_lat, input_data[0], cmap='RdBu', vmin=numpy.nanmin(input_data),
                         vmax=numpy.nanmax(input_data), transform=ccrs.PlateCarree())
    coast = ax.coastlines()
    text = ax.text(-175,-25, "", transform=ccrs.PlateCarree(), bbox=dict(facecolor='white', pad=4))
    cbar = fig.colorbar(grid, orientation='horizontal', extend='both', extendfrac=0.025, aspect=50, pad=0.025,
                        shrink=0.75)
    cbar.set_label("Equivalent water height [cm]")

    anim = animation.FuncAnimation(fig,  # figure object
                                   animate,  # callable animation function
                                   gravity_data.shape[0],  # number of frames
                                   fargs=(gravity_data, text, coast, grid),  # parameters passed to function
                                   interval=500,  # delay between frames [ms]
                                   blit=True)  # blitting (only redraw changes)

    anim.save("animation_func.mp4")


def artist_animation(input_data, input_lon, input_lat):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
    ax.set_global()
    frames = []

    for index in numpy.arange(0,input_data.shape[0],1):
        single_frame = ax.pcolormesh(input_lon, input_lat, input_data[index], cmap='RdBu', vmin=numpy.nanmin(input_data),
                         vmax=numpy.nanmax(input_data), transform=ccrs.PlateCarree())
        frames.append((single_frame,))

    anim = animation.ArtistAnimation(fig, frames, interval=500, blit=True )
    anim.save("animation_artist.mp4")



gravity_data = numpy.load(r"gravityField.npy")

lon = numpy.arange(-180, 181, 1)
lat = numpy.arange(90, -91, -1)


animate_via_function(gravity_data, lon, lat)
artist_animation(gravity_data, lon, lat)



frames = []



