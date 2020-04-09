# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 23:22:59 2020

@author: CalvinL2
"""
import pandas as pd

from common_parent_datafile import CommonFile

class APSTRHfile(CommonFile):
    """Stores and manipulates one temperature/relative_humidity csv file from an APS sensor"""
    def __init__(self, RHfile):
        super().__init__()
        self.data = pd.read_csv(RHfile, index_col=False)

        self.data['time'] = super()._str2date(self.data['Date Time'], '%d %b %Y %H:%M')
        self.data = self.data.set_index('time')

        self.frequency = None

    @property
    def rh(self):
        """Returns relative humidity values of type:float in a series"""
        return self.data[' RH(%)']

    @property
    def t(self):
        """Returns temperature values of type:float in a series"""
        return self.data[' TEMP(C)']

    @property
    def time(self):
        """Returns datetime objects in a numpy array."""
        return self.data.index.values

    @property
    def hourly_time(self):
        """Returns hourly averaged datetime objects in numpy array"""
        return super().resample(self.data, 'time', 'H')

    @property
    def hourly_rh(self):
        """Returns hourly averaged relative humidity values"""
        return super().resample(self.data, ' RH(%)', 'H')

    @property
    def hourly_t(self):
        """Returns hourly averaged temperature values."""
        return super().resample(self.data, ' TEMP(C)', 'H')

if __name__ == "__main__":
    DEBUGTEST = APSTRHfile('input\\test3\\Test_0304_CO_TRH.csv')
