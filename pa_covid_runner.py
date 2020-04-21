# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 17:12:21 2020

@author: CalvinL2
"""
import os
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from plotly.offline import plot
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from datafiles.pa_datafile import PAfiles
from datafiles.TCEQ_pm_datafile import TCEQfile

from timer_1 import Timer

#https://plotly.com/python/getting-started/

def remove_outlier(df,param):
    # https://stackoverflow.com/questions/34782063/how-to-use-pandas-filter-with-iqr
    Q1 = df[param].quantile(0.25)
    Q3 = df[param].quantile(0.75)
    IQR = Q3-Q1
    mask = df[param].between(Q1-3*IQR,Q3+3*IQR,inclusive=True)
    return df.loc[mask,:]

def remove_outlier_2(df,param):
    # https://stackoverflow.com/questions/34782063/how-to-use-pandas-filter-with-iqr
    Q1 = df[param].rolling(360,center=True).quantile(0.25)
    Q3 = df[param].rolling(360,center=True).quantile(0.75)
    IQR = Q3-Q1
    mask = (df[param]>=Q1-1.5*IQR)&(df[param]<=Q3+1.5*IQR)
    return df.loc[mask,:]

def remove_outlier_3(df,param):
    # https://stackoverflow.com/questions/34782063/how-to-use-pandas-filter-with-iqr
    Q1 = df[param].quantile(0.25)
    Q3 = df[param].quantile(0.75)
    IQR = Q3-Q1
    mask = df[param].between(Q1-5*IQR,Q3+5*IQR,inclusive=True)
    df = df.loc[mask,:].copy()
    
    Q1 = df[param].rolling(180,center=True).quantile(0.25)
    Q3 = df[param].rolling(180,center=True).quantile(0.75)
    IQR = Q3-Q1
    mask = (df[param]>=Q1-1.5*IQR)&(df[param]<=Q3+1.5*IQR)
    return df.loc[mask,:]

def plot_purpleair_pm(fig,files,param='PM2.5_ATM_ug/m3'):        
    for file in files:
        if file.hourly[param] is not None:
            file.raw
            filtered = remove_outlier_3(file[:],param)
            # values = file.raw[param]
            values = filtered[param]
            time = values.index.to_pydatetime()
            fig.add_trace(go.Scattergl(x=time, y=values,
                    mode='markers',
                    name=file.sensorname), row=1, col=1)

def plot_avg_param(fig,param='Temperature_F',second_y=False, r=2,c=1):
    combined_data = [file.hourly[param] for file in pa_files if file[param] is not None]
    avg = sum(combined_data)/len(combined_data)
    values = avg
    time = values.index.to_pydatetime()
    fig.add_trace(go.Scattergl(x=time, y=values,
                    mode='lines',
                    name=param), row=r, col=c, secondary_y=second_y)
    
def plot_avg_pm(fig,param='PM2.5_ATM_ug/m3',second_y=False, r=1,c=1):
    combined_data = [remove_outlier_3(file[:],param).resample('H').mean()[param] for file in pa_files if file[param] is not None]
    avg = sum(combined_data)/len(combined_data)
    values = avg
    time = values.index.to_pydatetime()
    fig.add_trace(go.Scattergl(x=time, y=values,
                    mode='lines',
                    name=param), row=r, col=c, secondary_y=second_y)

def label_plot2(fig):
    fig.update_layout(
        yaxis2=dict(title="Temperature(F)",side='left',anchor='x2'),
        yaxis3=dict(title="Relative humidity(%)",side='right',anchor='x2')
        )
    
def label_plot(fig):
    fig.update_layout(
        title = 'UT PurpleAir',
        yaxis_title = 'PM 2.5(ug/m3)'#,
        #xaxis = dict(rangeslider=dict(visible=True))
        )
    plot(fig, filename='Mar1-Apr8r.html')

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                    x_title='Time(CST)',
                    specs = [[{"secondary_y":False}], [{"secondary_y":True}]])
# fig = go.Figure()
pa_files = PAfiles('input\\pa_covid')
plot_purpleair_pm(fig,pa_files)
plot_avg_param(fig, param='Temperature_F')
plot_avg_param(fig, param='Humidity_%', second_y=True)
plot_avg_pm(fig, param='PM2.5_ATM_ug/m3')

sample = TCEQfile('C:/Users/CalvinLin/My Files/GitHub/bleed-orange-measure-purple/input/tceq_pm_mar.csv')
fig.add_trace(go.Scattergl(x=sample.data['Time'], y=sample.data['PM2.5'],
                    mode='lines',name='TCEQpm'),row=1,col=1)

label_plot2(fig)
label_plot(fig)

#eval
#getattr

def timegraph(files,param='pm25'):
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(1, 1, 1)
    
    for file in files:
        if file.hourly[param] is not None:
            plt.plot_date(file.hourly.time, file.hourly[param], 'o-', xdate=True,
                          label=file.sensorname)

    rolling_data = [file[param] for file in files if file[param] is not None]
    avg = sum(rolling_data)/len(rolling_data)
    avg = avg.rolling(window=48).mean()
    plt.plot_date(avg.index.values, avg,
                  '-k', xdate=True, linewidth=4,
                  label='Rolling Average')
    
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    # ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))

    ax.grid()
    plt.legend(loc='upper left')
    fig.autofmt_xdate()
    plt.ylim(0, 70)
    plt.xlim([datetime.date(2020, 3, 17), datetime.date(2020, 4, 8)])    
    plt.title(f'Hourly {param} Values from UT PurpleAirs for Mar 1 to Apr 8')
    plt.ylabel('PM 2.5 (ug/m3)')
    plt.xlabel('Time')
    
    fig.savefig(f'output//march_ut_pa_hourly_{param}.svg')
