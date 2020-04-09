# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 17:12:34 2020

@author: CalvinL2
"""
import pandas as pd
import numpy as np

from common_parent_datafile import CommonFile

class APSPMfile(CommonFile):
    """Stores and manipulates one PM csv file from an APS sensor"""
    def __init__(self, pmfile):
        super().__init__()
        raw_data = pd.read_csv(pmfile, index_col=False)

        def _isolate_pm(data):
            start_row_index = data.index[data.iloc[:, 1] == 'Date'][0]
            data = data.iloc[start_row_index:, :].copy()
            data.rename(columns=data.iloc[0], inplace=True)
            data = data.iloc[1:, :]
            data.reset_index(drop=True, inplace=True)
            return data

        self.data = _isolate_pm(raw_data)

        self.pm25_data = self._parse_pm25(self.data)
        self.frequency = None


    def _parse_pm25(self, data):
        array_1 = []
        timearray = []
        for row in data.iterrows():
            #Access series in tuple (technical detail), convert to np array
            row = np.array(row[1])

            col_names = data.columns

            #Access pm values part of series
            row_pm = row[col_names.get_loc('<0.523'):col_names.get_loc(2.642)]

            timestamp = row[1]+' '+row[2]
            timearray.append(timestamp)

            #Sum mass to get pm 2.5 mass
            array_1.append(np.sum(row_pm.astype(float))*1000)

        timearray = np.array(timearray)
        # timearray = self._str2date(np.array(timearray))
        timearray = super()._str2date(np.array(timearray), '%m/%d/%y %H:%M:%S')

        array_1 = pd.DataFrame([timearray, array_1]).transpose()
        array_1.columns = ['time', 'pmdata']
        array_1 = array_1.set_index('time').astype(float)
        return array_1


    @property
    def time(self):
        """Returns datetime objects in a numpy array."""
        return self.pm25_data.index.values

    @property
    def pm25(self):
        """Returns PM 2.5 values in a panda series."""
        return self.pm25_data.astype(float)['pmdata']

    @property
    def hourly_time(self):
        """Returns hourly averaged datetime objects in numpy array"""
        return super().resample(self.pm25_data.astype(float), 'time', 'H')

    @property
    def hourly_pm25(self):
        """Returns hourly averaged PM 2.5 values in a panda series."""
        return super().resample(self.pm25_data.astype(float), 'pmdata', 'H')

if __name__ == "__main__":
    DEBUGTEST = APSPMfile('input\\test3\\Test_C_0304.csv')
