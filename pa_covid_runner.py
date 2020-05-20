# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 17:12:21 2020

@author: CalvinL2
"""

from plotly.offline import plot
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

from sensors.purpleair.pa_datafile import PAfiles, PAfiles
from sensors.tceq.TCEQ_pm_datafile import TCEQfile
from sensors.common.util.importer import Util

#https://plotly.com/python/getting-started/

# %%
def plot_purpleair_pm(fig, files, param='PM2.5_ATM_ug/m3'):
    for file in files:
        if file.hourly[param] is not None:
            file.frequency = 'H'
            
            # values = file.raw[param]
            values = file[param]
            
            time = values.index
            fig.add_trace(go.Scattergl(x=time, y=values,
                                       mode='lines',
                                       name=file.sensorname), row=1, col=1)

def plot_avg_param(fig, param='Temperature_F', second_y=False, r=2, c=1):
    """Plots relative humidity and temperature in the second subplot"""
    combined_data = [file.hourly[param].rename(file.sensorname) for file in pa_files 
                     if file[param] is not None]
    combined_data = pd.concat(combined_data, axis=1)
    avg = combined_data.mean(axis=1)
    values = avg
    time = values.index.to_pydatetime()
    fig.add_trace(go.Scattergl(x=time, y=values,
                               mode='lines',
                               name=param), row=r, col=c, secondary_y=second_y)


def plot_avg_pm(fig, param='PM2.5_ATM_ug/m3', second_y=False, r=1, c=1):
    
    #A list of series with PM data (non rolling)
    # combined_data = [file[:].resample(freq).mean()[param].rename(file.sensorname) 
    #                   for file in pa_files if file[param] is not None]
    
    #Rolling
    combined_data = [file.data.resample('H').mean().rolling(window=100, min_periods=1, center=True).mean()[param].rename(file.sensorname) 
                    for file in pa_files]
    
    combined_data =  pd.concat(combined_data, axis=1) #columns = sensors, rows = pm values
    avg = combined_data.mean(axis=1)  #average all sensors
    values = avg
    time = values.index.to_pydatetime()
    fig.add_trace(go.Scattergl(x=time, y=values,
                               mode='lines',
                               name='PurpleAir PM2.5'), row=r, col=c, secondary_y=second_y)

def plot_tceq_trh(fig, freq=None):
    tceq_trh = pd.read_csv('data/monthly/tceq_trh.csv')
    tceq_trh['Time']=pd.to_datetime(tceq_trh['Time'], format='%Y-%m-%d %H:%M:%S')
    tceq_trh = tceq_trh.set_index('Time')
    # tceq_trh = tceq_trh.resample(freq).mean()
    tceq_trh = tceq_trh.rolling(window=100, min_periods=1, center=True).mean()

    fig.add_trace(go.Scattergl(x=tceq_trh.index, y=tceq_trh['Temperature(F)'],
                               mode='lines', name='TCEQ Temperature'), row=2, col=1, secondary_y=False)
    fig.add_trace(go.Scattergl(x=tceq_trh.index, y=tceq_trh['Relative Humidity(%)'],
                               mode='lines', name='TCEQ Relative Humidity'), row=2, col=1, secondary_y=True)
    
def label_plot(fig):
    fig.update_layout(
        yaxis2=dict(title="Temperature(F)", side='left', anchor='x2'),
        yaxis3=dict(title="Relative humidity(%)", side='right', anchor='x2'),
        title='UT PurpleAir Rolling Hourly (window=100)',
        yaxis_title='PM 2.5(ug/m3)'
        )
   

def make_raw_plot(pa_files, tceq):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        x_title='Time(CST)', vertical_spacing=0.05,
                        specs=[[{"secondary_y":False}], [{"secondary_y":True}]])
    # fig = go.Figure()
    print('Subplots created')
    # plot_purpleair_pm(fig, pa_files)
    print('PurpleAir Individual data plotted')
    # plot_avg_param(fig, param='Temperature_F')
    # plot_avg_param(fig, param='Humidity_%', second_y=True)
    
    # PurpleAir PM2.5 Average
    plot_avg_pm(fig, param='PM2.5_ATM_ug/m3')

    # TCEQ PM2.5 
    tceq_a = tceq.rolling(100)
    # tceq_a = tceq.resample(frequency)
    fig.add_trace(go.Scattergl(x=tceq_a.time, y=tceq_a['PM2.5'],
                                mode='lines', name='TCEQ PM2.5'), row=1, col=1)
    
    # TCEQ Temp & Humidity
    plot_tceq_trh(fig, freq='D')
    
    label_plot(fig)
    plot(fig, filename='temp-timeplot.html')

# %%
@Util.caching(cachefile='purpleair.cache')
def import_PAfiles():
    return PAfiles('data/monthly', keepOutliers=False)

pa_files = import_PAfiles()

tceq = TCEQfile('data/monthly/tceq.csv')
# %%
make_raw_plot(pa_files, tceq)
