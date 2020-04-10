# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 17:12:21 2020

@author: CalvinL2
"""
import os
from os import path
import pickle as pkl

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from pa_datafile import PAfile

USE_CACHE = True
CACHE = 'PAfiles_cache.pkl'

# Using caching for improved performance
def import_pa():
    """Imports all PurpleAir files in current directory, uses caching to speed up future runs"""
    if not path.exists(CACHE) or not USE_CACHE:
        print('Importing data from csv...', flush=True, end="")
        PAfiles = PAfile.import_pa_files(os.getcwd(), 'input\\pa_covid')
        print('Done', flush=True)
        pkl.dump(PAfiles, open(CACHE, 'wb'))
    else:
        print('Loading data from cache...', flush=True, end="")
        PAfiles = pkl.load(open(CACHE, 'rb'))
        print('Done', flush=True)
    return PAfiles

PAfiles = import_pa()

fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot(1, 1, 1)

for file in PAfiles:
    plt.plot_date(file.hourly.time, file.hourly.pm25, '.', xdate=True,
                  label=file.sensorname)

rolling_data = [file.pm25 for file in PAfiles]
pa_avg = sum(rolling_data)/len(rolling_data)
pa_avg = pa_avg.rolling(window=48).mean()
plt.plot_date(pa_avg.index.values, pa_avg,
              '-k', xdate=True, linewidth=4,
              label='Rolling Average')

ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
ax.grid()

plt.ylim(0, 70)
plt.title('Hourly PM 2.5 Values from UT PurpleAirs for Mar 1 to Apr 8')
plt.ylabel('PM 2.5 (ug/m3)')
plt.xlabel('Time')
plt.legend()

fig.autofmt_xdate()
fig.savefig('output//march_ut_pa_hourly_pm.svg')


fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot(1, 1, 1)

for file in PAfiles:
    # file.set_frequency('H')
    plt.plot_date(file.hourly.time, file.hourly.temperature, '.', xdate=True, label=file.sensorname)

ax.grid()
# plt.ylim(0,70)
fig.autofmt_xdate()
ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))

plt.title('Hourly Temperature Values from UT PurpleAirs for Mar 1 to Apr 8')
plt.ylabel('Temperature(F)')
plt.xlabel('Time')
plt.legend()

fig.savefig('output//march_ut_pa_hourly_temp.svg')

# def label_timeseries(fig,title,xlabel='Time',ylabel=None):
#     fig.autofmt_xdate()
#     plt.title(title)
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.legend()
# fig = plt.figure(figsize=(20, 10))
# time = []

#eval
#getattr
