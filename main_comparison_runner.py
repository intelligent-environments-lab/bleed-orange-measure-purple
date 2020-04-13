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
relative_path = 'input\\test3'

PAfiles = PAfile.import_pa_files(os.getcwd(), relative_path)

# %% Import APS Files
TrhFile = APSTRHfile(f'{relative_path}\\Test_0304_CO_TRH.csv')
PmFile = APSPMfile(f'{relative_path}\\Test_C_0304.csv')

# %% Plot data

f = plt.figure(figsize=(20, 10))
start_date = PmFile.hourly.time[0]
end_date = PmFile.hourly.time[PmFile.hourly.time.size - 1]

for file in PAfiles:
    # Match PA time range to APS time range
    time = file.hourly.time[(file.hourly.time >= start_date) & (file.hourly.time <= end_date)]
    pm = file.hourly.pm25[(file.hourly.time >= start_date) & (file.hourly.time <= end_date)]

    plt.plot_date(time, pm, '-', label=file.sensorname)

plt.plot_date(PmFile.hourly.time, PmFile.hourly.pm25, '-', label='APS')

plt.legend()
plt.savefig('output//test.svg')

# %% reference code

# file.data[file.data.index >= '2020-03-03 17:40:13-06:00' ]
