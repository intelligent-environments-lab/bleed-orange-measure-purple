# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 01:33:45 2020

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
        
for filename in os.listdir(cwd+r'\input\archive'):
    if filename.endswith(".csv") and filename.startswith("PA"):
        PAfiles.append(PAfile('input\\archive\\'+filename))
        
fig = plt.figure(figsize=(20,10))
time =[]
for file in PAfiles:
    # file.set_frequency('H')
    plt.plot_date(date2num(file.time),file.pm,'.',xdate=True,label=file.sensorname)
    plt.legend()
    time = file.time
fig.savefig('rawdata.svg')

fig = plt.figure(figsize=(20,10))
time =[]  
for file in PAfiles:
    # file.set_frequency('H')
    plt.plot_date(date2num(file.time),file.pm.rolling(window = 15).mean(),'-',xdate=True,label=file.sensorname)
    plt.legend()
fig.savefig('rolling.svg')

fig = plt.figure(figsize=(20,10))

for file in PAfiles:
    file.set_frequency('H')
    time = file.time

for file in PAfiles:
    # file.set_frequency('H')
    plt.plot_date(date2num(file.time),file.pm,'-',xdate=True,label=file.sensorname)
    plt.legend()
fig.savefig('rolling.svg')
    
sum_pm = np.zeros(len(PAfiles[0].pm))
for idx,file in enumerate(PAfiles):
    sum_pm += file.pm
avg = np.array(sum_pm)/len(PAfiles)

plt.plot_date(date2num(time),avg,'--',xdate=True,label='Average')
plt.legend()


fig.autofmt_xdate()
fig.savefig('hourly w avg.svg')

f = plt.figure(figsize=(20,10))
for file in PAfiles:
    plt.plot_date(date2num(file.time),file.pm,'.',xdate=True,label=file.sensorname)
    plt.legend()
f.savefig('hourly2.svg')

time =[]  

for file in PAfiles:
    file.set_frequency('H')
    time = file.time
    
f = plt.figure(figsize=(20,10))
for file in PAfiles:
    plt.plot_date(date2num(file.time),file.pm-avg,'-',xdate=True,label=file.sensorname)
    plt.legend()
f.savefig('error.svg')