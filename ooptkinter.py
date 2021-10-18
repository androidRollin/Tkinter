import tkinter as tk
from formfunctions import *
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title("DOST-PHIVOLCS")
        self.iconbitmap("PHIVOLCS.ico")
        self.eval('tk::PlaceWindow . center')
        self.geometry("350x280")
        center(self)
        self.resizable(0, 0)

        # Form frame
        self.form_frame = ttk.Frame(self)
        # Labels
        self.l_earthquake = ttk.Label(self.form_frame, text="Earthquake Intensity Mapping")
        self.l_ev_latitude = ttk.Label(self.form_frame, text="Latitude Degrees (-90 to 90): ")
        self.l_ev_longitude = ttk.Label(self.form_frame, text="Longitude Degrees (-180 to 180): ")
        self.l_ev_mag_value = ttk.Label(self.form_frame, text="Magnitude (Mw (2.5 to 9.5)): ")
        self.l_ev_depth = ttk.Label(self.form_frame, text="Depth (km (0 to 700)): ")
        self.l_ev_num_testimonies = ttk.Label(self.form_frame, text="Total Number of Testimonies: ")

        # Label Positioning
        self.l_earthquake.grid(row=0, column=0, columnspan=2, pady=15)
        self.l_ev_latitude.grid(row=1, column=0, sticky=W, pady=10, padx=15)
        self.l_ev_longitude.grid(row=2, column=0, sticky=W, pady=10, padx=15)
        self.l_ev_mag_value.grid(row=3, column=0, sticky=W, pady=10, padx=15)
        self.l_ev_depth.grid(row=4, column=0, sticky=W, pady=10, padx=15)
        self.l_ev_num_testimonies.grid(row=5, column=0, sticky=W, pady=10, padx=15)

        # Entry Widgets
        self.e_ev_latitude = Entry(self.form_frame)
        self.e_ev_longitude = Entry(self.form_frame)
        self.e_ev_mag_value = Entry(self.form_frame)
        self.e_ev_depth = Entry(self.form_frame)
        self.e_ev_num_testimonies = Entry(self.form_frame)

        # Entry Positioning
        self.e_ev_latitude.grid(row=1, column=1, pady=2)
        self.e_ev_longitude.grid(row=2, column=1, pady=2)
        self.e_ev_mag_value.grid(row=3, column=1, pady=2)
        self.e_ev_depth.grid(row=4, column=1, pady=2)
        self.e_ev_num_testimonies.grid(row=5, column=1, pady=2)

        self.button_submit = Button(self.form_frame, text="Submit", command=self.checkInputs, width=15)
        self.button_submit.grid(row=6, columnspan=2, pady=2)


        self.set_inputs()
        self.form_frame.grid()
        self.form_frame.tkraise()

        # Progress Frame
        self.progress_frame = ttk.Frame(self)

        # configure the grid to place the progress bar is at the center
        # self.progress_frame.columnconfigure(0, weight=1)
        # self.progress_frame.rowconfigure(0, weight=1)

        # progressbar
        self.pb = ttk.Progressbar(self.progress_frame, orient=tk.HORIZONTAL, mode='indeterminate')
        self.pb.grid(row=0, column = 0)

        self.l_loading_status = ttk.Label(self.progress_frame, text="Feeding the data into the model...")
        self.l_loading_status.grid(row=1, rowspan = 2 )

        self.progress_frame.rowconfigure(0, weight=1)
        self.l_loading_status.rowconfigure(1, weight=1)
        self.progress_frame.grid_columnconfigure(0, weight=1)


    def checkInputs(self):
        latitude = self.e_ev_latitude.get()
        longitude = self.e_ev_longitude.get()
        magnitude = self.e_ev_mag_value.get()
        depth = self.e_ev_depth.get()
        num_testimonies = self.e_ev_num_testimonies.get()

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
                                    print("Pass")
                                    self.start_processing()

    def start_processing(self):
        # place the progress frame
        self.progress_frame.tkraise()
        self.pb.start(10)
        self.progress_frame.grid(row=0, column=0, sticky=tk.NSEW)


    def set_inputs(self):
        self.e_ev_latitude.insert(0, -90)
        self.e_ev_longitude.insert(0, 180)
        self.e_ev_mag_value.insert(0, 9.5)
        self.e_ev_depth.insert(0, 500)
        self.e_ev_num_testimonies.insert(0, 50)


if __name__ == "__main__":
    app = App()
    app.mainloop()
