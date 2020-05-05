# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 13:41:40 2020

@author: CalvinL2
"""


from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

from sensors.pa_datafile import PAfiles
from sensors.TCEQ_pm_datafile import TCEQfile
from sensors.analysis.outliers_remover import remove_outlier

def plot_avg_pm(param='PM2.5_ATM_ug/m3', second_y=False, r=1, c=1, freq=None):
    
    #A list of series with PM data
    # combined_data = [remove_outlier(file[:], param).resample(freq).mean()[param].rename(file.sensorname) 
    #                   for file in pa_files if file[param] is not None]
    
    combined_data = [remove_outlier(file[:], param).resample('H').mean().rolling(window=100, min_periods=1, center=True).mean()[param].rename(file.sensorname) 
                    for file in pa_files if file[param] is not None]
    combined_data =  pd.concat(combined_data, axis=1) #columns = sensors, rows = pm values
    avg = combined_data.mean(axis=1)  #average all sensors
    values = avg
    time = values.index.to_pydatetime()
    values.name='PA PM2.5'
    return values



pa_files = PAfiles('data/ytd')
tceq = TCEQfile('data/ytd/tceq.csv')
tceq_trh = pd.read_csv('data/ytd/tceq_trh.csv')

tceq_trh['Time']=pd.to_datetime(tceq_trh['Time'], format='%Y-%m-%d %H:%M:%S').dt.tz_localize('US/Central', nonexistent='NaT')
tceq_trh.set_index('Time', inplace=True)
data = plot_avg_pm()
data = pd.concat([data,tceq.hourly.pm25,tceq_trh['Relative Humidity(%)']], axis=1).dropna(how='any')
# data = pd.concat([data,tceq.hourly.pm25,tceq_trh['Temperature(F)']], axis=1).dropna(how='any')

fig = go.Figure(data=go.Scattergl(
    y=data['PA PM2.5'],
    x=data['PM2.5'],
    mode='markers',
    marker=dict(
        color=data['Relative Humidity(%)'],
        # color=data['Temperature(F)'],
        colorscale=px.colors.sequential.thermal,
        showscale=True
        )
    ))

fig.update_layout(
    width=800,
    height=800
    )

fig['layout']['xaxis'].update(title='TCEQ PM2.5', range=[0,35])
fig['layout']['yaxis'].update(title='PurpleAir PM2.5', range=[0,35])


plot(fig)
