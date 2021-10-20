import pandas as pd
from matplotlib.path import Path
import joblib
from mpl_toolkits.basemap import Basemap as bp
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


intensity_I_model = joblib.load('model/intensityOne.joblib')
# intensity_II_model = joblib.load('model/intensityTwo.joblib')
# intensity_III_model = joblib.load('model/intensityThree.joblib')
intensity_IV_model = joblib.load('model/intensityFour.joblib')


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
        self.dfI = pd.DataFrame(data=None, columns=['a'])
        self.dfII = pd.DataFrame(data=None, columns=['a'])
        self.dfIII = pd.DataFrame(data=None, columns=['a'])
        self.dfIV = pd.DataFrame(data=None, columns=['a'])

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
        map = bp(projection='mill',
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

        self.df = self.df.loc[self.df['is_in_land'] == True]

    @staticmethod
    def func_model_intensity_i(x):
        x['intensity_prediction'] = intensity_I_model.predict([[x['ev_latitude'],
                                                                x['ev_longitude'],
                                                                x['ev_mag_value'],
                                                                x['ev_depth'],
                                                                x['e_num_testimonies'],
                                                                x['pt_longitude'],
                                                                x['pt_latitude'],
                                                                x['t_epicenter_distance_km']]])
        return x['intensity_prediction'][0]

    # @staticmethod
    # def func_model_intensity_ii(x):
    #     x['intensity_prediction'] = intensity_II_model.predict([[x['ev_latitude'],
    #                                                              x['ev_longitude'],
    #                                                              x['ev_mag_value'],
    #                                                              x['ev_depth'],
    #                                                              x['e_num_testimonies'],
    #                                                              x['pt_longitude'],
    #                                                              x['pt_latitude'],
    #                                                              x['t_epicenter_distance_km']]])
    #     return x['intensity_prediction'][0]
    #
    # @staticmethod
    # def func_model_intensity_iii(x):
    #     x['intensity_prediction'] = intensity_III_model.predict([[x['ev_latitude'],
    #                                                               x['ev_longitude'],
    #                                                               x['ev_mag_value'],
    #                                                               x['ev_depth'],
    #                                                               x['e_num_testimonies'],
    #                                                               x['pt_longitude'],
    #                                                               x['pt_latitude'],
    #                                                               x['t_epicenter_distance_km']]])
    #     return x['intensity_prediction'][0]
    #

    @staticmethod
    def func_model_intensity_iv(x):
        x['intensity_prediction'] = intensity_IV_model.predict([[x['ev_latitude'],
                                                                 x['ev_longitude'],
                                                                 x['ev_mag_value'],
                                                                 x['ev_depth'],
                                                                 x['e_num_testimonies'],
                                                                 x['pt_longitude'],
                                                                 x['pt_latitude'],
                                                                 x['t_epicenter_distance_km']]])
        return x['intensity_prediction'][0]

    def predict_intensity_i(self):
        self.df['intensityI_prediction'] = self.df.apply(self.func_model_intensity_i, axis=1)
        self.dfI = self.df.loc[self.df['intensityI_prediction'] == 1]

    def predict_intensity_ii(self):
        self.df['intensityII_prediction'] = self.df.apply(self.func_model_intensity_ii, axis=1)
        self.dfII = self.df.loc[self.df['intensityII_prediction'] == 1]

    def predict_intensity_iii(self):
        self.df['intensityIII_prediction'] = self.df.apply(self.func_model_intensity_iii, axis=1)
        self.dfIII = self.df.loc[self.df['intensityIII_prediction'] == 1]

    def predict_intensity_iv(self):
        self.df['intensityIV_prediction'] = self.df.apply(self.func_model_intensity_iv, axis=1)
        self.dfIV = self.df.loc[self.df['intensityIV_prediction'] == 1]

    # @staticmethod
    # def test_map_earthquake_event():
    #     fig = plt.figure(figsize=(20, 17))
    #
    #     lowercornerlat = 16.22
    #     lowercornerlong = 120.20
    #     uppercornerlat = 17.20
    #     uppercornerlong = 122.60
    #     # 17.12
    #     # m = Basemap(projection='mill', llcrnrlat = 16.18, llcrnrlon = 120.20, urcrnrlat = 17.20, urcrnrlon = 122.51,
    #     #             resolution = 'h')
    #     m = bp(projection='mill',
    #            llcrnrlat=lowercornerlat,
    #            llcrnrlon=lowercornerlong,
    #            urcrnrlat=uppercornerlat,
    #            urcrnrlon=uppercornerlong,
    #            resolution='h')
    #
    #     m.drawcountries(color='red')
    #     m.drawstates(color='blue')
    #     m.drawcounties(color='orange')
    #
    #     # m.fillcontinents(lake_color ='aqua')
    #     # m.fillcontintents(color='lightgreen')
    #     # m.etopo()
    #     # m.shadedrelief()
    #
    #     m.drawmapboundary(fill_color='#B3FFFF')
    #     m.fillcontinents(color='white', lake_color='aliceblue')
    #     m.drawrivers(color='skyblue')
    #
    #     PHILlat, PHILlon = 16.73, 121.55
    #     xpt, ypt = m(PHILlon, PHILlat)
    #     m.plot(xpt, ypt, 'r*', markersize=24, label='epicenter')
    #
    #     m.drawcoastlines()
    #
    #     # m.scatter(121.55,16.84, latlon=True, c ='red')
    #
    #     # m.drawparallels(np.arange(16.18,17.20,30),labels=[1,1,0,1], fontsize=8)
    #     # m.drawmeridians(np.arange(120.120,122.51,30),labels=[1,1,0,1], rotation=45, fontsize=8)
    #     plt.xlabel('Longitude', labelpad=80, fontsize=18)
    #     plt.ylabel('Latitude', labelpad=80, fontsize=18)
    #
    #     m.drawparallels(np.arange(lowercornerlat, uppercornerlat, .10), labels=[1, 1, 0, 0], color='lightgray')
    #     m.drawmeridians(np.arange(lowercornerlong, uppercornerlong, .10), labels=[0, 0, 1, 1], color='lightgray')
    #
    #     plt.legend()
    #     plt.title('Earthquake Intensity', fontsize=22)
    #     # plt.savefig('test.png')
    #     # plt.show()
    #     return plt.show()
