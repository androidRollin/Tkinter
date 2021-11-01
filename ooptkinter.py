import sys
import threading
import tkinter as tk
from formfunctions import *
from tkinter import ttk
from threading import Thread
from PIL import ImageTk, Image
from tkinter import messagebox

class RandomForestMachineLearningThread(Thread):
    def __init__(self, latitude, longitude, magnitude, depth, num_testimonies, loading_status, percentage_progress):
        super().__init__()
        self.latitude = latitude
        self.longitude = longitude
        self.magnitude = magnitude
        self.depth = depth
        self.num_testimonies = num_testimonies
        self.loading_status = loading_status
        self.percentage_progress = percentage_progress
        print("Hello Machine Learning")

    def run(self):
        # self.percentage_progress.configure(text="10%")
        # self.loading_status.configure(text="  Loading Random Forest Models...")
        # import randomforestml as rf
        # self.percentage_progress.configure(text="20%")
        # self.loading_status.configure(text="  Processing coordinates in the map...")
        # ev1 = rf.RandomForest(self.latitude, self.longitude, self.magnitude, self.depth, self.num_testimonies)
        # ev1.get_all_points_in_box_map()
        # ev1.create_dataframe()
        # ev1.get_distance_from_ev_to_insert_in_df()
        # self.percentage_progress.configure(text="30%")
        # self.loading_status.configure(text="  Determining land area points in the map...")
        # ev1.filter_land_coordinates()
        # self.percentage_progress.configure(text="40%")
        # self.loading_status.configure(text="""  Classifying/Predicting "Not Felt" Intensity I coordinates...""")
        # ev1.predict_intensity_i()
        # self.percentage_progress.configure(text="50%")
        # self.loading_status.configure(text="""  Classifying/Predicting "Weak" Intensity II coordinates...""")
        # ev1.predict_intensity_ii()
        # self.percentage_progress.configure(text="60%")
        # self.loading_status.configure(text="""  Classifying/Predicting "Weak" Intensity III coordinates...""")
        # ev1.predict_intensity_iii()
        # self.percentage_progress.configure(text="70%")
        # self.loading_status.configure(text="""  Classifying/Predicting "Light" Intensity IV coordinates...""")
        # ev1.predict_intensity_iv()
        # import mapping as mp
        # upper_corner_lat = getattr(ev1, 'upper_corner_lat')
        # lower_corner_lat = getattr(ev1, 'lower_corner_lat')
        # upper_corner_long = getattr(ev1, 'upper_corner_long')
        # lower_corner_long = getattr(ev1, 'lower_corner_long')
        # e_latitude = getattr(ev1, 'e_latitude')
        # e_longitude = getattr(ev1, 'e_longitude')
        # e_mag_value = getattr(ev1, 'e_mag_value')
        # e_depth = getattr(ev1, 'e_depth')
        # df_i = getattr(ev1, 'dfI')
        # df_ii = getattr(ev1, 'dfII')
        # df_iii = getattr(ev1, 'dfIII')
        # df_iv = getattr(ev1, 'dfIV')
        # self.percentage_progress.configure(text="80%")
        # self.loading_status.configure(text="""  Determining cities included in the map...""")
        # ev_map = mp.Map(upper_corner_lat, lower_corner_lat, upper_corner_long, lower_corner_long,
        #                 e_latitude, e_longitude, e_mag_value, e_depth, df_i, df_ii, df_iii, df_iv)
        # ev_map.determine_cities_included_in_map()
        # self.percentage_progress.configure(text="90%")
        # self.loading_status.configure(text="""  Mapping the earthquake event...""")
        # ev_map.map_earthquake_event()
        # print("Hello World")
        import testbasemap as tbm
        tbm.show_map()
        sys.exit()



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
        self.percentage_progress = ttk.Label(self.progress_frame, text="10%")
        self.percentage_progress.grid(row=7)

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
            t1.setDaemon(True)
            t1.start()
            machine_learning_thread = RandomForestMachineLearningThread(self.e_ev_latitude.get(),
                                                                        self.e_ev_longitude.get(),
                                                                        self.e_ev_mag_value.get(),
                                                                        self.e_ev_depth.get(),
                                                                        self.e_ev_num_testimonies.get(),
                                                                        self.loading_status,
                                                                        self.percentage_progress)
            machine_learning_thread.setDaemon(True)
            machine_learning_thread.start()

            self.monitor(machine_learning_thread)

    def check_inputs(self):
        latitude = self.e_ev_latitude.get()
        longitude = self.e_ev_longitude.get()
        magnitude = self.e_ev_mag_value.get()
        depth = self.e_ev_depth.get()
        num_testimonies = self.e_ev_num_testimonies.get()

        res = checkIfEmpty(latitude, longitude, magnitude, depth, num_testimonies)
        if res == 1:
            return 1
        else:
            res = checkIfQuantity(latitude, longitude, magnitude, depth, num_testimonies)
            if res == 1:
                return 1
            else:
                res = checkLatitudeRange(latitude)
                if res == 1:
                    return 1
                else:
                    res = checkLongitudeRange(longitude)
                    if res == 1:
                        return 1
                    else:
                        res = checkMagnitude(magnitude)
                        if res == 1:
                            return 1
                        else:
                            res = checkDepth(depth)
                            if res == 1:
                                return 1
                            else:
                                res = checkTestimonies(num_testimonies)
                                if res == 1:
                                    return 1
                                else:
                                    return 0
                                    # machine_learning_thread = self.random_forest_learn()
                                    # t1 = threading.Thread(target=machine_learning_thread)
                                    # t1.start()
                                    # self.monitor(t1)
    def stop_show_map(self):
        self.form_frame.tkraise()
        self.pb.stop()

    def monitor(self, download_thread):
        """ Monitor the download thread """
        if download_thread.is_alive():
            self.after(100, lambda: self.monitor(download_thread))
        else:
            print("end")
            self.stop_show_map()
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
    splash_root = Tk()
    splash_root.title("Splash Screen")
    splash_root.geometry("650x350")
    splash_root.eval('tk::PlaceWindow . center')
    center_splash(splash_root)

    # Hide Title Bar
    splash_root.overrideredirect(True)


    path = "dost_logo.jpg"

    img = ImageTk.PhotoImage(Image.open(path))

    panel = tk.Label(splash_root, image=img)

    panel.pack(side= "bottom", fill="both", expand = "yes")


    def main_window():
        splash_root.destroy()
        app = App()

        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                app.destroy()

        app.protocol("WM_DELETE_WINDOW", on_closing)
        app.mainloop()



    # Splash Screen Timer
    splash_root.after(3000, main_window)

    mainloop()
