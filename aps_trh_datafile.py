# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 23:22:59 2020

@author: CalvinL2
"""
import pandas as pd

from common_parent_datafile import commonfile

class APSTRHfile(commonfile):

    def __init__(self, RHfile):
        super().__init__()
        self.data = pd.read_csv(RHfile, index_col=False)

        self.data['time'] = super()._str2date(self.data['Date Time'], '%d %b %Y %H:%M')
        self.data = self.data.set_index('time')

        self.frequency = None

    @property
    def rh(self):
        return self.data[' RH(%)']

    @property
    def t(self):
        return self.data[' TEMP(C)']

    @property
    def time(self):
        return self.data.index.values

    @property
    def hourly_time(self):
        return super().resample(self.data, 'time', 'H')

    @property
    def hourly_rh(self):
        return super().resample(self.data, ' RH(%)', 'H')

    @property
    def hourly_t(self):
        return super().resample(self.data, ' TEMP(C)', 'H')
