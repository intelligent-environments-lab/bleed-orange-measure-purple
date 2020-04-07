# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 00:15:47 2020

@author: CalvinL2
"""

from datetime import datetime, timezone, timedelta

class commonfile():
    def __init__(self):
        self.frequency = None

    def set_frequency(self,freq):
        # Use 'H' for hourly mean 
        self.frequency = freq
        
    def _str2date(self,timearray,timeformat, tzone = None):
            ''' Converts column of strings to datetime objects'''
            time = []
            central = timezone(timedelta(hours=-6))
            for idx,val in enumerate(timearray):
                value = datetime.strptime(val,timeformat)
                time.append(value.replace(tzinfo=tzone).astimezone(tz=central)) 
            return time
    
    # def resample(self,data,col_name):
    #     frequency = self.frequency
        
    #     # Determines if the column specified is the index column, need better name
    #     def find_column_data(data_):
    #         if col_name in data_:
    #             return data_[col_name]
    #         elif col_name == data_.index.name:
    #             return data_.index.values
    #         else:
    #             print('An error has occured')
        
    #     # Determines if resampling was requested
    #     if frequency is not None:
    #         resampled_data = data.resample(frequency).mean()
    #         return find_column_data(resampled_data)
    #     else:
    #         return find_column_data(data)
        
    def resample(self,data,col_name,frequency=None):        
        # Determines if the column specified is the index column, need better name
        def find_column_data(data_):
            if col_name in data_:
                return data_[col_name]
            elif col_name == data_.index.name:
                return data_.index.values
            else:
                print('An error has occured')
        
        # Determines if resampling was requested
        if frequency is not None:
            resampled_data = data.resample(frequency).mean()
            return find_column_data(resampled_data)
        else:
            return find_column_data(data)
        
        # freq = self.frequency
        # if freq is not None:
        #     sample = self.pm25data.resample(freq).mean()
        #     return sample.index.values
        # else:
        #     return data.index.values
    