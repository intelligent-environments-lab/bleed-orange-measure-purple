# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 01:22:28 2020

@author: CalvinL2
"""

# %% Imports
import pandas as pd
import numpy as np

from sensors.common_parent_datafile import CommonFile

# %% Read File
class TCEQfile(CommonFile):
    def __init__(self,filename):
        data = pd.read_csv(filename,index_col = False)
        
        PMdata = self.findPM2_5(data)
        if not PMdata.empty:
            #TODO change numerical indicies to column names
            PMdata = self.flatten(PMdata)
            PMdata[0] = CommonFile.str2date(PMdata[0],'%m/%d/%Y %H:%M',isCentral=True)
            PMdata[1] = self.str2num(PMdata[1])
            PMdata.columns = ['Time','PM2.5']
            PMdata.set_index('Time', inplace=True)
        
        super().__init__(PMdata)

    @property
    def pm25(self):
        return self['PM2.5']

    def findPM2_5(self,rawdata):
        """Isolates data associated with a particular air quality parameter.(DataFrame)"""
        first_column = rawdata.iloc[:,0]
        search_value = 'PM-2.5 (Local Conditions) (POC 3) measured in micrograms per cubic meter (local conditions)'
        location = first_column.index[first_column == search_value] #Finds the desired parameter data
        if location.size > 0: #Verifies that it actually found the data 
            location = location[0]  #array to single value
            if first_column[location+3] == 'Date': #Verifies that data structure is as anticipated
                target_data = rawdata.iloc[location+3:,:]
                target_data.reset_index(drop=True, inplace=True) #optional, zeros the index column
                return target_data
            else:
                return None
        else: 
            return None

    def flatten(self,data):
        """Converts a 2D TCEQ array into a linear array.(DataFrame)"""
        dates = np.array(data.iloc[1:,0])
        hours = np.array(data.iloc[0,1:])
        timestamp = np.array([date+' '+hour for date in dates for hour in hours])
        
        values = np.array(data.iloc[1:,1:]).flatten()

        return pd.DataFrame([timestamp,values]).transpose()

    def str2num(self,data):
        '''Converts column of strings to float values'''
        data = np.array(data.replace('AQI',np.nan)
                        .replace('QAS',np.nan)
                        .replace('PMA',np.nan)
                        .replace('LIM',np.nan)
                        .astype(float))
        return data

