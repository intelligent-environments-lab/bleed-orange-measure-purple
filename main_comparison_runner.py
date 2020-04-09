# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 02:51:22 2020

@author: CalvinL2
"""
import os
import matplotlib.pyplot as plt

from aps_pm_datafile import APSPMfile
from aps_trh_datafile import APSTRHfile
from pa_datafile import PAfile


#Get current working directory
cwd = os.getcwd()

# %% Import Purple Air Files
PAfiles = []
relative_path = 'input\\test3'

for filename in os.listdir(cwd+'\\'+relative_path):
    if filename.endswith(".csv") and filename.startswith("PA"):
        PAfiles.append(PAfile(relative_path+'\\'+filename))

# %% Import APS Files
TrhFile = APSTRHfile(f'{relative_path}\\Test_0304_CO_TRH.csv')
PmFile = APSPMfile(f'{relative_path}\\Test_C_0304.csv')

# %% Plot data

f = plt.figure(figsize=(20, 10))
start_date = PmFile.hourly_time[0]
end_date = PmFile.hourly_time[PmFile.hourly_time.size - 1]

for file in PAfiles:
    # Match PA time range to APS time range
    time = file.hourly_time[(file.hourly_time >= start_date) & (file.hourly_time <= end_date)]
    pm = file.hourly_pm25[(file.hourly_time >= start_date) & (file.hourly_time <= end_date)]

    plt.plot_date(time, pm, '-', label=file.sensorname)

plt.plot_date(PmFile.hourly_time, PmFile.hourly_pm25, '-', label='APS')

plt.legend()
plt.savefig('output//test.svg')

# %% reference code

# file.data[file.data.index >= '2020-03-03 17:40:13-06:00' ]
