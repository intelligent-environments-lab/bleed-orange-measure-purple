# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 00:15:47 2020

@author: CalvinL2
"""

from datetime import datetime, timezone, timedelta

class CommonFile():
    """Superclass for sensor specific subclasses"""
    def __init__(self, data):
        self.data = data
        self.resampled_data = data
        self._frequency = None
        
    @staticmethod
    def str2date(timearray, timeformat, tzone=None):
        """Converts column of strings to datetime objects"""
        time = []
        central = timezone(timedelta(hours=-6))
        for _, val in enumerate(timearray):
            value = datetime.strptime(val, timeformat)
            time.append(value.replace(tzinfo=tzone).astimezone(tz=central))
        return time

    @property
    def frequency(self):
        """The frequency used for panda's resampling function"""
        return self._frequency

    @frequency.setter
    def frequency(self, var):
        # TIP Unknown effect with invalid frequency
        if var != self._frequency:
            self._frequency = var
            if var is None:
                self.resampled_data = self.data
                return
            self.resampled_data = self[:].resample(self.frequency).mean()

    @property
    def time(self):
        """Returns datetime objects in a numpy array."""
        return self[:].index.values
    
    @property
    def hourly_time(self):
        """Returns hourly averaged datetime objects in numpy array"""
        return self[:].resample('H').mean().index.values
    
    def __getitem__(self, key):
        return self.resampled_data[key]
