from formfunctions import *

root = Tk()
root.title("DOST-PHIVOLCS")
root.iconbitmap("PHIVOLCS.ico")
root.eval('tk::PlaceWindow . center')
root.geometry("350x280")
center(root)
root.resizable(0, 0)

# Creating a Label Widget
l_earthquake = Label(root, text="Earthquake Intensity Mapping")
l_ev_latitude = Label(root, text="Latitude Degrees (-90 to 90): ")
l_ev_longitude = Label(root, text="Longitude Degrees (-180 to 180): ")
l_ev_mag_value = Label(root, text="Magnitude (Mw (2.5 to 9.5)): ")
l_ev_depth = Label(root, text="Depth (km (0 to 700)): ")
l_ev_num_testimonies = Label(root, text="Total Number of Testimonies: ")

# grid method to arrange labels in respective
# rows and columns as specified
l_earthquake.grid(row=0, column=0, columnspan=2, pady=15)
l_ev_latitude.grid(row=1, column=0, sticky=W, pady=10, padx=15)
l_ev_longitude.grid(row=2, column=0, sticky=W, pady=10, padx=15)
l_ev_mag_value.grid(row=3, column=0, sticky=W, pady=10, padx=15)
l_ev_depth.grid(row=4, column=0, sticky=W, pady=10, padx=15)
l_ev_num_testimonies.grid(row=5, column=0, sticky=W, pady=10, padx=15)

# entry widgets, used to take entry from user
e_ev_latitude = Entry(root)
e_ev_longitude = Entry(root)
e_ev_mag_value = Entry(root)
e_ev_depth = Entry(root)
e_ev_num_testimonies = Entry(root)

# positioning
e_ev_latitude.grid(row=1, column=1, pady=2)
e_ev_longitude.grid(row=2, column=1, pady=2)
e_ev_mag_value.grid(row=3, column=1, pady=2)
e_ev_depth.grid(row=4, column=1, pady=2)
e_ev_num_testimonies.grid(row=5, column=1, pady=2)


def checkInputs():
    latitude = e_ev_latitude.get()
    longitude = e_ev_longitude.get()
    magnitude = e_ev_mag_value.get()
    depth = e_ev_depth.get()
    num_testimonies = e_ev_num_testimonies.get()

    res = checkIfEmpty(latitude, longitude, magnitude, depth, num_testimonies)
    if res == 1:
        return
    else:
        res = checkIfQuantity(latitude, longitude, magnitude, depth, num_testimonies)
        if res == 1:
            return
        else:
            res = checkLatitudeRange(latitude)
            if res == 1:
                return
            else:
                res = checkLongitudeRange(longitude)
                if res == 1:
                    return
                else:
                    res = checkMagnitude(magnitude)
                    if res == 1:
                        return
                    else:
                        res = checkDepth(depth)
                        if res == 1:
                            return
                        else:
                            res = checkTestimonies(num_testimonies)
                            if res == 1:
                                return
                            else:
                                print("Success, proceeding")


button_submit = Button(text="Submit", command=checkInputs, width = 15)
button_submit.grid(row=6, columnspan=2, pady=2)

root.mainloop()
