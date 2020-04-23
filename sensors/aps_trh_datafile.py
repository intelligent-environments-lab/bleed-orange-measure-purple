# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 23:22:59 2020

@author: CalvinL2
"""
import pandas as pd

from sensors.common_parent_datafile import CommonFile

class APSTRHfile(CommonFile):
    """Stores and manipulates one temperature/relative_humidity csv file from an APS sensor"""
    def __init__(self, RHfile):
        data = pd.read_csv(RHfile, index_col=False)

        data['time'] = CommonFile.str2date(data['Date Time'], '%d %b %Y %H:%M')
        data = data.set_index('time')

        super().__init__(data)


    @property
    def humidity(self):
        """Returns relative humidity values of type:float in a series"""
        return self[' RH(%)']

    @property
    def temperature(self):
        """Returns temperature values of type:float in a series"""
        return self[' TEMP(C)']

if __name__ == "__main__":
    debug = APSTRHfile('input\\test3\\Test_0304_CO_TRH.csv')
