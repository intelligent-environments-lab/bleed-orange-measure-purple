# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 17:06:54 2020

@author: CalvinL2
"""
import pandas as pd
import plotly.express as px
from plotly.offline import plot

from sensors.TCEQ_pm_datafile import TCEQfile
from sensors.pa_datafile import PAfile, PAfiles
from analysis.outliers_remover import remove_outlier

import numpy as np

def geo_df2(files, param):
    """Creates a new dataframe that works with animation in mapbox"""
    def append_coords(file):
        column = remove_outlier(file[:], 'PM2.5_ATM_ug/m3').resample('D').mean()['PM2.5_ATM_ug/m3']
        lat = pd.Series(file.latitude, index=[i for i in range(column.size)])
        lat.index = column.index
        long = pd.Series(file.longitude, index=[i for i in range(column.size)])
        long.index =  column.index
        modified = pd.concat([column,lat,long], axis=1).rename(columns={0:'lat',1:'lon'})
        modified.reset_index(inplace=True)
        modified['time'] = modified['time'].dt.strftime('%b %d')
        return modified
    files = [append_coords(file) for file in files]
    return pd.concat(files)

# pa_files = PAfiles('data\\pa_covid')
# # fn = pa_files['PA_II_E6D8']
# sample = TCEQfile('data/tceq_pm_mar.csv')

pa_files = PAfiles('data/ytd')
sample = TCEQfile('data/ytd/tceq.csv')

px.set_mapbox_access_token(open("token.txt").read())
df = geo_df2(pa_files, 'pm25')
df.dropna(axis=0, how='any', inplace=True)
df['textlabel']=df['PM2.5_ATM_ug/m3'].astype(int, errors='ignore').astype(str)

# row = df[df.index == '2020-02-29 20:00:00-06:00']
fig = px.scatter_mapbox(df, lat = 'lat', lon = 'lon', size='PM2.5_ATM_ug/m3', text='textlabel', color='PM2.5_ATM_ug/m3', size_max=60, zoom=14,
                        color_continuous_scale=px.colors.diverging.RdYlBu[::-1],
                        animation_frame='time')#,
                        # range_color=[int(df['PM2.5_ATM_ug/m3'].min(skipna=True)),int(df['PM2.5_ATM_ug/m3'].max(skipna=True))])
                
fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 2000
# fig = px.density_mapbox(df, lat = 'lat', lon = 'lon', z='PM2.5_ATM_ug/m3', radius=200, zoom=14,
                        # color_continuous_scale=px.colors.diverging.RdYlGn[::-1])
plot(fig, filename='interactive_map_c.html')