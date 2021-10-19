import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from mpl_toolkits.basemap import Basemap
import numpy as np
import joblib

intensity_one_model = joblib.load('model/intensityTwo.joblib')

class RandomForest:
    def __init__(self, e_latitude, e_longitude, e_mag_value, e_depth, e_num_testimonies):
        self.e_latitude = float(e_latitude)
        self.e_longitude = float(e_longitude)
        self.e_mag_value = float(e_mag_value)
        self.e_depth = float(e_depth)
        self.e_num_testimonies = int(e_num_testimonies)
        self.lower_corner_lat = float((float(e_latitude) - 0.55) - .5)
        self.lower_corner_long = float((float(e_longitude) - 1.35) - .5)
        self.upper_corner_lat = float((float(e_latitude) + 0.47) + .5)
        self.upper_corner_long = float((float(e_longitude) + 0.96) + .5)
        self.pt_latitude = []
        self.pt_longitude = []
        self.df = pd.DataFrame(data=None, columns=['a'])

    def get_all_points_in_box_map(self):
        i = self.lower_corner_lat
        while i <= self.upper_corner_lat:
            # print(round(i, 2))
            j = self.lower_corner_long
            while j <= self.upper_corner_long:
                # print("Latitude {}, Longitude {}".format(round(i,2),round(j,2)))
                self.pt_latitude.append(format(round(i, 2)))
                self.pt_longitude.append(format(round(j, 2)))
                j += .01
            i += .01

    def create_dataframe(self):
        list_tuples = list(zip(self.pt_latitude, self.pt_longitude))
        self.df = pd.DataFrame(list_tuples, columns=["pt_latitude", "pt_longitude"])
        self.df['ev_latitude'] = self.e_latitude
        self.df['ev_longitude'] = self.e_longitude
        self.df['ev_mag_value'] = self.e_mag_value
        self.df['ev_depth'] = self.e_depth
        self.df['e_num_testimonies'] = self.e_num_testimonies
        self.df["pt_longitude"] = self.df["pt_longitude"].astype(float)
        self.df["pt_latitude"] = self.df["pt_latitude"].astype(float)

    @staticmethod
    def haversine_np(lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)

        All args must be of equal length.

        """
        lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2

        c = 2 * np.arcsin(np.sqrt(a))
        km = 6367 * c
        return km

    def get_distance_from_ev_to_insert_in_df(self):
        self.df['t_epicenter_distance_km'] = RandomForest.haversine_np(self.df['ev_longitude'],
                                                                       self.df['ev_latitude'],
                                                                       self.df['pt_longitude'],
                                                                       self.df['pt_latitude'])
        print(self.df)

    def filter_land_coordinates(self):
        map = Basemap(projection='mill',
                      llcrnrlat=self.lower_corner_lat,
                      llcrnrlon=self.lower_corner_long,
                      urcrnrlat=self.upper_corner_lat,
                      urcrnrlon=self.upper_corner_long,
                      resolution='h')

        lons = self.df['pt_longitude']
        lats = self.df['pt_latitude']

        x, y = map(lons, lats)

        locations = np.c_[x, y]

        polygons = [Path(p.boundary) for p in map.landpolygons]

        result = np.zeros(len(locations), dtype=bool)

        for polygon in polygons:
            result += np.array(polygon.contains_points(locations))

        self.df['is_in_land'] = result

        df = self.df.loc[self.df['is_in_land'] == True]

    def func_model_intensity_I(self, x):
        x['intensity_prediction'] = intensity_one_model.predict([[x['ev_latitude'],
                                                                  x['ev_longitude'],
                                                                  x['ev_mag_value'],
                                                                  x['ev_depth'],
                                                                  x['e_num_testimonies'],
                                                                  x['pt_longitude'],
                                                                  x['pt_latitude'],
                                                                  x['t_epicenter_distance_km']]])
        return x['intensity_prediction'][0]

    def predict_intensity_I(self):
        self.df['intensityI_prediction'] = self.df.apply(self.func_model_intensity_I, axis=1)


