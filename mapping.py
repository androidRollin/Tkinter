import pandas as pd
from mpl_toolkits.basemap import Basemap as bp
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np


class Map:
    def __init__(self, upper_corner_lat,
                 lower_corner_lat,
                 upper_corner_long,
                 lower_corner_long,
                 e_latitude,
                 e_longitude,
                 e_mag_value,
                 e_depth,
                 dfI
                 # dfII,
                 # dfIII,
                 ,dfIV
                 ):
        # Map Points
        self.lower_corner_lat = lower_corner_lat
        self.lower_corner_long = lower_corner_long
        self.upper_corner_lat = upper_corner_lat
        self.upper_corner_long = upper_corner_long
        self.e_latitude = float(e_latitude)
        self.e_longitude = float(e_longitude)
        self.e_mag_value = float(e_mag_value)
        self.e_depth = float(e_depth)
        self.dfI = dfI
        # self.dfII = dfII
        # self.dfIII = dfIII
        self.dfIV = dfIV
        self.df_ph_city_filter = pd.DataFrame(data=None, columns=['a'])
        print(self.dfI)

    def determine_cities_included_in_map(self):
        df_ph_city = pd.read_csv("dataset/worldcities.csv")
        columns = ['city_ascii', 'country', 'iso2', 'iso3', 'admin_name', 'capital', 'population', 'id']
        df_ph_city.drop(columns, inplace=True, axis=1)
        self.df_ph_city_filter = df_ph_city[(df_ph_city['lat'] < self.upper_corner_lat) &
                                       (df_ph_city['lat'] > self.lower_corner_lat) &
                                       (df_ph_city['lng'] < self.upper_corner_long) &
                                       (df_ph_city['lng'] > self.lower_corner_long)]


    def map_earthquake_event(self):
        fig = plt.figure(figsize=(95, 50), dpi=20)
        m = bp(projection='mill',
               llcrnrlat=self.lower_corner_lat,
               llcrnrlon=self.lower_corner_long,
               urcrnrlat=self.upper_corner_lat,
               urcrnrlon=self.upper_corner_long,
               resolution='h')

        m.drawcountries(color='red')
        m.drawstates(color='blue')
        # m.drawcounties(color='orange')

        # m.fillcontinents(lake_color ='aqua')
        # m.fillcontintents(color='lightgreen')
        # m.etopo()
        # m.shadedrelief()

        m.drawmapboundary(fill_color='#B3FFFF')
        m.fillcontinents(color='white', lake_color='aliceblue')
        m.drawrivers(color='skyblue')

        # CitScilat, CitScilon = 16.74, 121.55
        # xpt, ypt = m(CitScilon, CitScilat)
        # m.plot(xpt, ypt,'g^', markersize=15)

        # Earthquake Intensity III, 63.6% Accurracy
        # xpt, ypt = m(self.dfIII['pt_longitude'], self.dfIII['pt_latitude'])
        # m.plot(xpt, ypt, '.', markersize=24, color="#82F9FB", alpha=0.636, label='III')
        #
        # # Earthquake Intensity II, 70.6% Accurracy
        # xpt, ypt = m(self.dfII['pt_longitude'], self.dfII['pt_latitude'])
        # m.plot(xpt, ypt, '.', markersize=24, color="#DFE6FE", alpha=0.706, label='II')
        #

        # Earthquake Intensity IV, 74.2% Accurracy
        xpt, ypt = m(self.dfIV['pt_longitude'], self.dfIV['pt_latitude'])
        m.plot(xpt, ypt, '.', markersize=24, color="#7EFBDF", alpha=0.742, label='IV')

        # Earthquake Intensity I, 76.5 Accurracy
        xpt, ypt = m(self.dfI['pt_longitude'], self.dfI['pt_latitude'])
        # m.plot(xpt, ypt, '.', markersize=24, color="whitesmoke", alpha=0.765, label='I')
        m.plot(xpt, ypt, '.', markersize=24, color="whitesmoke", alpha=1, label='I')

        xpt, ypt = m(self.df_ph_city_filter['lng'], self.df_ph_city_filter['lat'])
        city_name = self.df_ph_city_filter['city']
        m.plot(xpt, ypt, 'ok', markersize=15, alpha=0.70)
        for label, xpt, ypt in zip(city_name, xpt + 0.5, ypt + 0.5):  # add annotation (city names)
            plt.text(xpt + 1500, ypt + 0.01, label, color='black', fontsize=24, alpha=0.90)

        PHILlat, PHILlon = self.e_latitude, self.e_longitude
        xpt, ypt = m(PHILlon, PHILlat)
        m.plot(xpt, ypt, 'r*', markersize=48, label='epicenter', alpha=1.0)

        # plt.text(xpt,ypt,'City',fontsize=12)
        # I = mpatches.Patch([],[], color="whitesmoke", marker = '.', markersize = 15, alpha = 0.765, label = 'I')

        m.drawcoastlines()

        # m.scatter(121.55,16.84, latlon=True, c ='red')

        # m.drawparallels(np.arange(16.18,17.20,30),labels=[1,1,0,1], fontsize=8)
        # m.drawmeridians(np.arange(120.120,122.51,30),labels=[1,1,0,1], rotation=45, fontsize=8)
        plt.xlabel('Longitude', labelpad=125, fontsize=30)
        plt.ylabel('Latitude', labelpad=140, fontsize=30)

        m.drawparallels(np.arange(self.lower_corner_lat,
                                  self.upper_corner_lat, .10),
                        labels=[1, 1, 0, 0],
                        color='lightgray',
                        fontsize=22)
        m.drawmeridians(np.arange(self.lower_corner_long,
                                  self.upper_corner_long, .10),
                        labels=[0, 0, 1, 1],
                        color='lightgray',
                        fontsize=22,
                        rotation=45)
        # np.arange(start, stop, step)

        plt.legend(prop={'size': 35}, loc='upper center', bbox_to_anchor=(0.5, -0.90),
                   fancybox=True, shadow=True, ncol=5, facecolor='white', framealpha=1.0)

        plt.title('Earthquake Intensity', y=1.08, fontsize=50)
        # plt.savefig('test.png')
        plt.show()
