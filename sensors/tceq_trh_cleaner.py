# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 05:27:17 2020

@author: CalvinL2
"""
import pandas as pd
import numpy as np
        

def findPM2_5(rawdata):
    """Isolates data associated with a particular air quality parameter.(DataFrame)"""
    first_column = rawdata.iloc[:,0]
    search_value = 'Date'
    location = first_column.index[first_column == search_value][0] #Finds the desired parameter data
    target_data = rawdata.iloc[location:,:]
    target_data.reset_index(drop=True, inplace=True) #optional, zeros the index column
    return target_data
    


def flatten(data):
    """Converts a 2D TCEQ array into a linear array.(DataFrame)"""
    dates = np.array(data.iloc[1:,0])
    hours = np.array(data.iloc[0,1:])
    timestamp = np.array([date+' '+hour for date in dates for hour in hours])
    
    values = np.array(data.iloc[1:,1:]).flatten()

    return pd.DataFrame([timestamp,values]).transpose()

def str2num(data):
    '''Converts column of strings to float values'''
    data = (data.replace('AQI',np.nan)
                .replace('QAS',np.nan)
                .replace('PMA',np.nan)
                .replace('LIM',np.nan)
                .replace('LST',np.nan)
                .replace('FEW',np.nan)
                .astype(float))
    return data

temp = pd.read_csv('data/ytd/raw/temp.csv',index_col = False)
rh = pd.read_csv('data/ytd/raw/rh.csv',index_col = False)
temp = findPM2_5(temp)
temp = flatten(temp)
temp[0]=pd.to_datetime(temp[0], format='%m/%d/%Y %H:%M')
temp.columns=['Time','Temperature(F)']
temp.set_index('Time', inplace=True)
temp = str2num(temp)

rh = findPM2_5(rh)
rh = flatten(rh)
rh[0]=pd.to_datetime(rh[0], format='%m/%d/%Y %H:%M')
rh.columns=['Time','Relative Humidity(%)']

rh.set_index('Time', inplace=True)
rh = str2num(rh)
temp.insert(0,rh.columns[0], rh)
data = temp
data.reset_index(inplace=True)
data.to_csv('tceq_trh.csv', index=False)
