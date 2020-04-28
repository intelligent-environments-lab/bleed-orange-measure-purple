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

from sensors.pa_datafile import PAfiles
from sensors.TCEQ_pm_datafile import TCEQfile

#https://plotly.com/python/getting-started/

def remove_outlier(df, param):
    # https://stackoverflow.com/questions/34782063/how-to-use-pandas-filter-with-iqr
    Q1 = df[param].quantile(0.25)
    Q3 = df[param].quantile(0.75)
    IQR = Q3-Q1
    mask = df[param].between(Q1-5*IQR, Q3+5*IQR, inclusive=True)
    df = df.loc[mask, :].copy()

    Q1 = df[param].rolling(180, center=True).quantile(0.25)
    Q3 = df[param].rolling(180, center=True).quantile(0.75)
    IQR = Q3-Q1
    mask = (df[param] >= Q1-1.5*IQR)&(df[param] <= Q3+1.5*IQR)
    return df.loc[mask, :]

def plot_purpleair_pm(fig, files, param='PM2.5_ATM_ug/m3'):
    for file in files:
        if file.hourly[param] is not None:
            file.frequency = None
            filtered = remove_outlier(file[:], param).resample('D').mean()
            # values = file.raw[param]
            values = filtered[param]
            time = values.index.to_pydatetime()
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
    
    #A list of series with PM data
    combined_data = [remove_outlier(file[:], param).resample('H').mean()[param].rename(file.sensorname) 
                     for file in pa_files if file[param] is not None]
    combined_data =  pd.concat(combined_data, axis=1) #columns = sensors, rows = pm values
    avg = combined_data.mean(axis=1)  #average all sensors
    values = avg
    time = values.index.to_pydatetime()
    fig.add_trace(go.Scattergl(x=time, y=values,
                               mode='lines',
                               name=param), row=r, col=c, secondary_y=second_y)

def label_plot2(fig):
    fig.update_layout(
        yaxis2=dict(title="Temperature(F)", side='left', anchor='x2'),
        yaxis3=dict(title="Relative humidity(%)", side='right', anchor='x2')
        )

def label_plot(fig):
    fig.update_layout(
        title='UT PurpleAir',
        yaxis_title='PM 2.5(ug/m3)'#,
        #xaxis = dict(rangeslider=dict(visible=True))
        )
    plot(fig, filename='plots/Mar1-Apr8.html')

def make_raw_plot():
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        x_title='Time(CST)',
                        specs=[[{"secondary_y":False}], [{"secondary_y":True}]])
    # fig = go.Figure()
    pa_files = PAfiles('data\\pa_covid')
    plot_purpleair_pm(fig, pa_files)
    plot_avg_param(fig, param='Temperature_F')
    plot_avg_param(fig, param='Humidity_%', second_y=True)
    plot_avg_pm(fig, param='PM2.5_ATM_ug/m3')

    sample = TCEQfile('data/tceq_pm_mar.csv')
    fig.add_trace(go.Scattergl(x=sample.time, y=sample.data['PM2.5'],
                               mode='lines', name='TCEQpm'), row=1, col=1)

    label_plot2(fig)
    label_plot(fig)

pa_files = PAfiles('data\\pa_covid')
sample = TCEQfile('data/tceq_pm_mar.csv')
make_raw_plot()
