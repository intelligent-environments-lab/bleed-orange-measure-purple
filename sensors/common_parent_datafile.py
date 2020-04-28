# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 00:15:47 2020

@author: CalvinL2
"""
import copy
from datetime import datetime, timezone, timedelta

import pandas as pd

class CommonFile():
    """Superclass for sensor classes"""
    def __init__(self, data):
        self.data = data
        self.resampled_data = data
        self._frequency = None

    @property
    def time(self):
        """Returns datetime index objects in a pandas series."""
        return self[:].index

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

    @staticmethod
    def str2date(timearray, timeformat, tzone=None, isCentral=False):
        """Converts column of strings to datetime objects"""
        time = []
        central = timezone(timedelta(hours=-6))
        for _, val in enumerate(timearray):
            value = datetime.strptime(val, timeformat)
            if isCentral:
                tzone = central
            time.append(value.replace(tzinfo=tzone).astimezone(tz=central))
        return time

    @staticmethod
    def to_datetime(timearray, timeformat, isCentral=False):
        """ Wrapper function for pandas.to_datetime"""
        if isCentral:
            return pd.to_datetime(timearray, format=timeformat).dt.tz_localize('US/Central')
        return pd.to_datetime(timearray, format=timeformat).dt.tz_convert('US/Central')


    def resample(self, freq):
        """Resamples the data using the provided frequency"""
        if freq is None:
            self.resampled_data = self.data
            return self
        self.resampled_data = self[:].resample(freq).mean()
        return self

    def rolling(self, num=1):
        """Returns an copy of the datafile w ith rolling average data"""
        copyfile = copy.deepcopy(self)
        copyfile.resampled_data = copyfile[:].rolling(window=num, min_periods=1, center=True).mean()
        return copyfile

    def __getitem__(self, key):
        if isinstance(key, str):
            if key in self.resampled_data.columns:
                return self.resampled_data[key]
            if hasattr(self, key):
                return getattr(self, key)
            return None
        return self.resampled_data[key]
    
    def plot(self, *args, **kwargs):
        return self.resampled_data.plot(*args, **kwargs)

