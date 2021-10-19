import threading
import tkinter as tk
from formfunctions import *
from tkinter import ttk
from threading import Thread


class RandomForestMachineLearningThread(Thread):
    def __init__(self, latitude, longitude, magnitude, depth, num_testimonies, loading_status):
        super().__init__()
        self.latitude = latitude
        self.longitude = longitude
        self.magnitude = magnitude
        self.depth = depth
        self.num_testimonies = num_testimonies
        self.loading_status = loading_status
        print("Hello Machine Learning")

    def run(self):
        self.loading_status.configure(text="Loading Models and Preprocessing Data")
        import randomforestml as rf
        ev1 = rf.RandomForest(self.latitude, self.longitude, self.magnitude, self.depth, self.num_testimonies)
        ev1.get_all_points_in_box_map()
        ev1.create_dataframe()
        ev1.get_distance_from_ev_to_insert_in_df()
        print("In here")
        self.loading_status.configure(text="Determining and Filtering land area points in the map")
        ev1.filter_land_coordinates()
        self.loading_status.configure(text="  Intensity One model is predicting intensity one coordinates")
        ev1.predict_intensity_I()
        self.loading_status.configure(text="  Intensity One coordinates, predicted")



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

        self.button_submit = Button(self.form_frame, text="Submit", command=self.handle_machine_learning_rf, width=15)
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

        # Dummy data

        self.dummy = ttk.Label(self.progress_frame, text="")
        self.dummy.grid(row=0)

        self.dummy = ttk.Label(self.progress_frame, text="")
        self.dummy.grid(row=1)

        self.dummy = ttk.Label(self.progress_frame, text="")
        self.dummy.grid(row=2)

        self.dummy = ttk.Label(self.progress_frame, text="")
        self.dummy.grid(row=3)

        self.dummy = ttk.Label(self.progress_frame, text="")
        self.dummy.grid(row=4)

        self.dummy = ttk.Label(self.progress_frame, text="")
        self.dummy.grid(row=5)

        # Center the Loading Bar
        self.pb = ttk.Progressbar(self.progress_frame, orient=tk.HORIZONTAL, mode='indeterminate')
        self.pb.grid(row=6, columnspan=2)

        # Dummy data
        self.dummy = ttk.Label(self.progress_frame, text="10%")
        self.dummy.grid(row=7)

        self.loading_status = ttk.Label(self.progress_frame, text="  Feeding the data into the model...")
        self.loading_status.grid(row=8)

        self.progress_frame.columnconfigure(0, weight=1)

        # self.progress_frame.rowconfigure(0, weight=1)
        # self.progress_frame.grid_columnconfigure(0, weight=1)

    def handle_machine_learning_rf(self):
        if self.check_inputs() == 1:
            return
        else:
            progress_bar_thread = self.display_progress_bar
            t1 = threading.Thread(target=progress_bar_thread)
            t1.start()
            machine_learning_thread = RandomForestMachineLearningThread(self.e_ev_latitude.get(),
                                                                        self.e_ev_longitude.get(),
                                                                        self.e_ev_mag_value.get(),
                                                                        self.e_ev_depth.get(),
                                                                        self.e_ev_num_testimonies.get(),
                                                                        self.loading_status)
            machine_learning_thread.start()

    def check_inputs(self):
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
                                    return 0
                                    # machine_learning_thread = self.random_forest_learn()
                                    # t1 = threading.Thread(target=machine_learning_thread)
                                    # t1.start()
                                    # self.monitor(t1)

    def monitor(self, download_thread):
        """ Monitor the download thread """
        if download_thread.is_alive():
            self.after(100, lambda: self.monitor(download_thread))
        else:
            pass
            print("end")
            # self.stop_downloading()
            # self.set_picture(download_thread.picture_file)

    def display_progress_bar(self):
        # place the progress frame
        self.progress_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.progress_frame.tkraise()
        self.pb.start(10)

    def set_inputs(self):
        self.e_ev_latitude.insert(0, 13.82)
        self.e_ev_longitude.insert(0, 120.35)
        self.e_ev_mag_value.insert(0, 5.7)
        self.e_ev_depth.insert(0, 66)
        self.e_ev_num_testimonies.insert(0, 515)


if __name__ == "__main__":
    app = App()
    app.mainloop()
