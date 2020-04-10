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
if not path.exists(CACHE) or not USE_CACHE:
    print('Importing data from csv...', flush=True, end="")
    PAfiles = PAfile.import_pa_files(os.getcwd(), 'input\\pa_covid')
    print('Done', flush=True)
    pkl.dump(PAfiles, open(CACHE, 'wb'))
else:
    print('Loading data from cache...', flush=True, end="")
    PAfiles = pkl.load(open(CACHE, 'rb'))
    print('Done', flush=True)

fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot(1, 1, 1)
for file in PAfiles:
    # file.set_frequency('H')
    plt.plot_date(file.hourly_pm25.index.values,
                  file.hourly_pm25,
                  '.', xdate=True, label=file.sensorname)
ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
ax.grid()
plt.ylim(0, 70)
fig.autofmt_xdate()
plt.title('Hourly PM 2.5 Values from UT PurpleAirs for Mar 1 to Apr 8')
plt.ylabel('PM 2.5 (ug/m3)')
plt.xlabel('Time')
plt.legend()
fig.savefig('output//march_ut_pa_hourly_pm.svg')


fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot(1, 1, 1)
for file in PAfiles:
    # file.set_frequency('H')
    plt.plot_date(file.hourly_time, file.hourly_temp, '.', xdate=True, label=file.sensorname)

ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
ax.grid()
# plt.ylim(0,70)
fig.autofmt_xdate()
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
