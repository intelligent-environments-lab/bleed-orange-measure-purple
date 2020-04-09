# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 17:12:21 2020

@author: CalvinL2
"""

from pa_datafile import PAfile
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import numpy as np

import os

#Get current working directory
cwd = os.getcwd()

PAfiles = []
        
for filename in os.listdir(cwd+r'\input\pa_covid'):
    if filename.endswith(".csv") and filename.startswith("PA"):
        PAfiles.append(PAfile('input\\pa_covid\\'+filename))
        
fig = plt.figure(figsize=(20,10))
time =[]
for file in PAfiles:
    # file.set_frequency('H')
    plt.plot_date(file.hourly_time,file.hourly_pm,'-',xdate=True,label=file.sensorname)
    plt.legend()
    time = file.time
plt.ylim(0,100)
fig.savefig('output//covid_rawdata.svg')

fig = plt.figure(figsize=(20,10))
time =[]  
