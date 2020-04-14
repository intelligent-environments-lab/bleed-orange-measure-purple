# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 00:15:47 2020

@author: CalvinL2
"""
import copy
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
        """Used to set frequency via equality operator"""
        # TIP Unknown effect with invalid frequency
        if var != self._frequency:
            self._frequency = var
            self.resample(var)

    def resample(self, freq):
        """Resamples the data using the provided frequency"""
        if freq is None:
            self.resampled_data = self.data
            return self
        self.resampled_data = self[:].resample(freq).mean()
        return self

    def rolling(self, num=1):
        """Returns an copy of the datafile with rolling average data"""
        copyfile = copy.deepcopy(self)
        copyfile.resampled_data = copyfile[:].rolling(window=num).mean()
        return copyfile

    @property
    def time(self):
        """Returns datetime objects in a numpy array."""
        return self[:].index.values

    @property
    def hourly(self):
        """Set resampling frequency to hourly"""
        self.frequency = 'H'
        return self

    @property
    def raw(self):
        """Set resampling frequency to None"""
        self.frequency = None
        return self

    def __getitem__(self, key):
        if type(key) == str:
            if key in self.resampled_data.columns: 
                return self.resampled_data[key]
            if hasattr(self,key):
                return getattr(self,key)
            else:
                return 
        return self.resampled_data[key]
