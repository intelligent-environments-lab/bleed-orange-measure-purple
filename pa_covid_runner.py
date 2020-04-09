# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 17:12:21 2020

@author: CalvinL2
"""

from pa_datafile import PAfile
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import matplotlib.dates as mdates
import numpy as np

import os

#Get current working directory
cwd = os.getcwd()

PAfiles = []
        
for filename in os.listdir(cwd+r'\input\pa_covid'):
    if filename.endswith(".csv") and filename.startswith("PA"):
        PAfiles.append(PAfile('input\\pa_covid\\'+filename))
        
fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(1,1,1)  
time =[]
for file in PAfiles:
    # file.set_frequency('H')
    plt.plot_date(file.hourly_time,file.hourly_pm,'.',xdate=True,label=file.sensorname)
    plt.legend()
    time = file.time

ax.xaxis.set_major_locator(mdates.DayLocator(interval=1)) 
ax.grid()
plt.ylim(0,70)
fig.autofmt_xdate()
plt.title('Hourly PM 2.5 Values from UT PurpleAirs for Mar 1 to Apr 8')
plt.ylabel('PM 2.5 (ug/m3)')
plt.xlabel('Time')
fig.savefig('output//march_ut_pa_hourly_pm.svg')


fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(1,1,1)  
time =[]
for file in PAfiles:
    # file.set_frequency('H')
    plt.plot_date(file.hourly_time,file.hourly_temp,'.',xdate=True,label=file.sensorname)
    plt.legend()
    time = file.time

ax.xaxis.set_major_locator(mdates.DayLocator(interval=1)) 
ax.grid()
# plt.ylim(0,70)
fig.autofmt_xdate()
plt.title('Hourly Temperature Values from UT PurpleAirs for Mar 1 to Apr 8')
plt.ylabel('Temperature(F)')
plt.xlabel('Time')
fig.savefig('output//march_ut_pa_hourly_temp.svg')


fig = plt.figure(figsize=(20,10))
time =[]  
