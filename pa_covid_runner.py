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

from pa_datafile import PAfile, PAfiles
from timer_1 import Timer

#https://plotly.com/python/getting-started/
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

def plotnew(files,param='pm25'):
    fig = go.Figure()
        
    for file in files:
        if file.hourly[param] is not None:
            fig.add_trace(go.Scattergl(x=file.raw[:].index.to_pydatetime(), y=file.raw[param],
                    mode='markers',
                    name=file.sensorname))
    plot(fig)
    
pa_files = PAfiles('input\\pa_covid')
plotnew(pa_files)
# pmplot = timegraph(pa_files,'pm25')
# tempplot = timegraph(pa_files,'temperature')

# fig = plt.figure(figsize=(20, 10))
# ax = fig.add_subplot(1, 1, 1)

# for file in pa_files:
#     plt.plot_date(file.hourly.time, file.hourly.pm25, '.', xdate=True,
#                   label=file.sensorname)

# rolling_data = [file.pm25 for file in pa_files]
# pa_avg = sum(rolling_data)/len(rolling_data)
# pa_avg = pa_avg.rolling(window=48).mean()
# plt.plot_date(pa_avg.index.values, pa_avg,
#               '-k', xdate=True, linewidth=4,
#               label='Rolling Average')

# ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
# ax.grid()

# plt.ylim(0, 70)
# plt.title('Hourly PM 2.5 Values from UT PurpleAirs for Mar 1 to Apr 8')
# plt.ylabel('PM 2.5 (ug/m3)')
# plt.xlabel('Time')
# plt.legend()

# fig.autofmt_xdate()
# fig.savefig('output//march_ut_pa_hourly_pm.svg')


# fig = plt.figure(figsize=(20, 10))
# ax = fig.add_subplot(1, 1, 1)

# for file in pa_files:
#     # file.set_frequency('H')
#     if file.hourly.temperature is not None:
#         plt.plot_date(file.hourly.time, file.hourly.temperature, '.', xdate=True, label=file.sensorname)

# ax.grid()
# # plt.ylim(0,70)
# fig.autofmt_xdate()
# ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))

# plt.title('Hourly Temperature Values from UT PurpleAirs for Mar 1 to Apr 8')
# plt.ylabel('Temperature(F)')
# plt.xlabel('Time')
# plt.legend()

# fig.savefig('output//march_ut_pa_hourly_temp.svg')


        

#eval
#getattr
