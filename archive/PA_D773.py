# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 09:30:11 2020

@author: CalvinL2
"""
# %% Imports
import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta

from PA import plot_timeseries,str2date
    
class Session:
    def __init__(self,start,end):
        self.start=start
        self.end=end
        self.seconds=(end-start).total_seconds()
      
def findsessions(timearray):
    starttime = timearray[0]
    lengths = []
    for idx,time in enumerate(timearray):
        if idx == 0:
            continue
        if timearray[idx] - timearray[idx-1] >= timedelta(minutes=3):
            lengths.append(Session(starttime,timearray[idx-1]))
            starttime = timearray[idx]
    return lengths
# pd.group(['hour']).mean()
    #resample('60 min')
#df.setindex
    #seaborn sns sns.heatmap
#look at hourly time scale
if __name__ == '__main__':
    data = pd.read_csv('PA_II_D773 (outside) (30.289035 -97.735372) Primary Real Time 02_14_2020 02_28_2020.csv')
    data['time'] = str2date(data.loc[:,'created_at'])
    
    # d = data[{'time','Humidity_%'}]    
    # d2 = d[0:20]
    # plot_timeseries(data['time'],data['Humidity_%'])
    # plot_timeseries(data['time'],data['Temperature_F'])
    plot_timeseries(data['time'],data['PM2.5_ATM_ug/m3'])
    plt.figure()

    plt.boxplot(data['PM2.5_ATM_ug/m3'])
    
    batterylife=findsessions(data['time'])

