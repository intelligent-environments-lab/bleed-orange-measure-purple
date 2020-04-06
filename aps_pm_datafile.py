# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 17:12:34 2020

@author: CalvinL2
"""
import pandas as pd
import numpy as np

from common_parent_datafile import commonfile

class APSPMfile(commonfile):
    def __init__(self,pmfile):
        super()
        self.raw_data = pd.read_csv(pmfile,index_col =False)
        
        def _isolate_pm(data):
            start = data.index[data['Sample File'] == 'Date'][0]
            end = data.index[data['Sample File'] == 'Event 1'][0]
            data = data.iloc[start:end,:]
            return data
        
        pm25data = _isolate_pm(self.raw_data)
        
        self.pm25data = self._parse_pm25(pm25data)
        self.frequency = None


    def _parse_pm25(self,data):
        temparray = []
        timearray = []
        for col in data.iloc[:,1:].iteritems():
            col = np.array(col[1])    #Access series in tuple (technical detail), convert to np array
            col_pm = col[3:] #Access pm values part of series
            timestamp =  col[0]+' '+col[1]
            timearray.append(timestamp)
            temparray.append(np.sum(col_pm.astype(float))*1000)
    
            # print(col)
        timearray = np.array(timearray)
        # timearray = self._str2date(np.array(timearray))
        timearray = super()._str2date(np.array(timearray),'%m/%d/%y %H:%M:%S')

        temparray= pd.DataFrame([timearray,temparray]).transpose()
        temparray.columns = ['time','pmdata']
        temparray = temparray.set_index('time').astype(float)
        return temparray
    

    @property
    def time(self): return self.pm25data.index.values
        
    @property
    def pm(self): return self.pm25data.astype(float)['pmdata']
    
    @property
    def hourly_time(self): return super().resample(self.pm25data.astype(float),'time','H')
    
    @property 
    def hourly_pm(self): return super().resample(self.pm25data.astype(float),'pmdata','H')
