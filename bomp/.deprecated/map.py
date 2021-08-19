# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 17:06:54 2020

@author: CalvinL2
"""
import pandas as pd
import plotly.express as px
from plotly.offline import plot


from dotenv import load_dotenv, find_dotenv
import os
import numpy as np


def list_files(path):
    filepaths = [
        path + '/' + filename
        for filename in os.listdir(path)
        if os.path.isfile(path + '/' + filename)
    ]
    return filepaths


def geo_df2(datasets):
    """Creates a new dataframe that works with animation in mapbox"""

    def append_coords(dataset, filename):
        dataset = dataset.set_index('Time')
        column = dataset.resample('D').mean()['PM2.5 (ug/m3)']
        filename = filename.replace('(', '').replace(')', '').split()
        lat = filename[2]
        long = filename[3]
        lat = pd.Series(lat, index=[i for i in range(column.size)]).astype(float)
        lat.index = column.index
        long = pd.Series(long, index=[i for i in range(column.size)]).astype(float)
        long.index = column.index
        modified = pd.concat([column, lat, long], axis=1).rename(
            columns={0: 'lat', 1: 'lon'}
        )
        modified.reset_index(inplace=True)
        modified['Time'] = modified['Time'].dt.strftime('%b %d')
        return modified

    datasets = [
        append_coords(dataset, filename) for filename, dataset in datasets.items()
    ]
    return pd.concat(datasets)


if __name__ == '__main__':
    root = 'data/processed/purpleair'

    # Loads mapbox api key from secret .env file
    load_dotenv(find_dotenv())
    px.set_mapbox_access_token(os.getenv('MAPBOX_TOKEN'))

    # Import the data
    filepaths = list_files(root)
    filepaths = [filepath for filepath in filepaths if 'combined' not in filepath]
    pa_files = {
        filepath[filepath.rfind('/') + 1 :]: pd.read_feather(filepath)
        for filepath in filepaths
    }

    # Transform the data
    df = geo_df2(pa_files)

    df.dropna(axis=0, how='any', inplace=True)
    df['textlabel'] = df['PM2.5 (ug/m3)'].astype(int, errors='ignore').astype(str)
    df['fixedsize'] = pd.Series([2]).repeat(df.count()[0] + 1).reset_index(drop=True)
    fig = px.scatter_mapbox(
        df,
        lat='lat',
        lon='lon',
        size='fixedsize',  # size='PM2.5_ATM_ug/m3',
        text='textlabel',
        color='PM2.5 (ug/m3)',
        size_max=30,
        zoom=14,
        color_continuous_scale=px.colors.diverging.RdYlBu[::-1],
        animation_frame='Time',
    )  # ,
    # range_color=[int(df['PM2.5_ATM_ug/m3'].min(skipna=True)),int(df['PM2.5_ATM_ug/m3'].max(skipna=True))])

    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 2000
    # fig = px.density_mapbox(df, lat = 'lat', lon = 'lon', z='PM2.5_ATM_ug/m3', radius=200, zoom=14,
    # color_continuous_scale=px.colors.diverging.RdYlGn[::-1])
    plot(fig, filename='reports/working/temp-map.html')
