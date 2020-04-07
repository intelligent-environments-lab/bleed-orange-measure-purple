# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 09:30:11 2020

@author: CalvinL2
"""

# %% Imports
import pandas as pd
from datetime import datetime, timezone

from visualize_data import plot_timeseries, violin_plot
from common_parent_datafile import commonfile

# %%
class PAfile(commonfile):
    
    def __init__(self,filename):
        # BUG Need to discriminate between primary and secondary files
        super()
        data = pd.read_csv(filename,index_col = False)
        
        # Remove leading backslash (if any)
        filename = filename[filename.rfind('/')+1:]
        
        # Extract data from filename
        self._parse_filename(filename)
        
        # Converts string to datetime object
        timestamps = super()._str2date(data.loc[:,'created_at'],'%Y-%m-%d %H:%M:%S %Z',tzone = timezone.utc)
        
        # Creates datetime column and makes it the index for the df, use df.index.values or df.index.name to access
        data.insert(0,'time',timestamps)
        data = data.set_index('time')
        
        # Defining instance variables for the object
        # TODO use dictionary
        self.data = data
        self.filename = filename
        self.frequency = None
            
    def _parse_filename(self,filename):
        #BUG account for edited filename
        
        # Some adjustments to format to make parsing easier
        filename = filename[filename.rfind('\\')+1:]
        filename = filename.replace('(','').replace(')','')
        
        # Iterates across parts of a file name with space as the seperator
        def iterate():
            nonlocal filename
            index = filename.find(' ')
            value = filename[0:index]
            filename = filename[index+1:]
            return value
        
        # Uses iterate function to extract data from the filename
        self.sensorname = iterate()
        self.sensor_environment = iterate()
        self.latitude = iterate()
        self.longitude = iterate()
        
        return None
    
    
    @property    
    def time(self): return self.data.index.values
    
    @property
    def pm(self): return self.data['PM2.5_ATM_ug/m3']
    
    @property
    def hourly_time(self): return super().resample(self.data,'time','H')

    @property
    def hourly_pm(self): return super().resample(self.data,'PM2.5_ATM_ug/m3','H')

