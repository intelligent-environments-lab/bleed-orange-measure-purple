# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 17:12:34 2020

@author: CalvinL2
"""
import pandas as pd
import numpy as np

from sensors.common.common_parent_datafile import CommonFile


class APSPMfile(CommonFile):
    """Stores and manipulates one PM csv file from an APS sensor"""

    def __init__(self, pmfile):
        raw_data = pd.read_csv(pmfile, index_col=False)

        def _isolate_pm(data):
            start_row_index = data.index[data.iloc[:, 1] == 'Date'][0]
            data = data.iloc[start_row_index:, :].copy()
            data.rename(columns=data.iloc[0], inplace=True)
            data = data.iloc[1:, :]
            data.reset_index(drop=True, inplace=True)
            return data

        def _parse_pm25(data):
            array_1 = []
            timestamps = []
            for row in data.iterrows():
                # Access series in tuple (technical detail), convert to np array
                row = np.array(row[1])

                col_names = data.columns

                # Access pm values part of series
                row_pm = row[col_names.get_loc('<0.523') : col_names.get_loc(2.642)]

                # Sum mass to get pm 2.5 mass
                array_1.append(np.sum(row_pm.astype(float)) * 1000)

                timestamps.append(row[1] + ' ' + row[2])

            timestamps = CommonFile.to_datetime(
                pd.Series(timestamps), '%m/%d/%y %H:%M:%S', isCentral=True
            )

            array_1 = pd.Series(array_1)
            array_1 = pd.concat([timestamps, array_1], axis=1)
            array_1.columns = ['time', 'pmdata']
            array_1 = array_1.set_index('time', drop=True)  # .astype(float)
            return array_1

        data = _isolate_pm(raw_data)
        pm25_data = _parse_pm25(data)
        super().__init__(pm25_data)

    @property
    def pm25(self):
        """Returns PM 2.5 values in a panda series."""
        return self[:].astype(float)['pmdata']


if __name__ == "__main__":
    debug = APSPMfile('input\\test3\\Test_C_0304.csv')
