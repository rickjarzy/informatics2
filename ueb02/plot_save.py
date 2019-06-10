                #satellite_tail = 1

                #ax.imshow(blue_marble_img, origin='upper', transform=ccrs.Robinson())

                # frames_for_anim_list = []
                # for sat_name in sat_names:
                #
                #     if "graceA" == sat_name:
                #         print("GRACE A MATCH")
                #         sat_label = "GRACE A"
                #         sat_color = "red"
                #
                #     else:
                #         sat_label = "GPS"
                #         sat_color = "green"
                #
                #     print("- proccessing satorbit for %s" % sat_name)
                #
                #     for sat_data_index in range(index_start, index_end+1):
                #         #print(sat_data_index, " - ", sat_orbits_dict[sat_name][sat_data_index].time)
                #
                #         sat_data_phi = [satellite.phi() for satellite in sat_orbits_dict[sat_name][sat_data_index-satellite_tail:sat_data_index]]
                #         sat_data_lam = [satellite.lam() for satellite in sat_orbits_dict[sat_name][sat_data_index-satellite_tail:sat_data_index]]
                #
                #         ax.annotate(sat_name, (sat_data_lam[-1], sat_data_phi[-1]))
                #         plot_orbit = ax.plot(sat_data_lam, sat_data_phi, label=sat_label, color=sat_color, transform=ccrs.Geodetic())
                #
                #         # dynamic tail of satellite tail
                #         if satellite_tail <= 5:
                #             satellite_tail += 1