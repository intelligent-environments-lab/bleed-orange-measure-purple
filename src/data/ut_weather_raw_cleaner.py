# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 10:01:59 2020

@author: CalvinL2
"""

import pandas as pd
import numpy as np


def format_time(dataset):
    time_data = dataset['Date'] + ' ' + dataset['        Time']
    time_data = pd.to_datetime(time_data, format='%m/%d/%y %I:%M %p').dt.tz_localize(
        'US/Central', ambiguous='NaT', nonexistent='shift_forward'
    )

    dataset.insert(0, 'Time', time_data)
    NaT_loc = dataset[pd.isnull(dataset['Time'])].index
    if len(NaT_loc) != 0:
        NaT_loc = NaT_loc[0]
        dataset.loc[NaT_loc, 'Time'] = dataset['Time'].copy()[
            NaT_loc - 1
        ] + pd.Timedelta('1h')

    dataset = dataset.drop(labels=['Date', '        Time'], axis=1)
    return dataset


def main():
    filename = 'data/external/ut_weather/UTPD Wx Station 5 min data/utweather_5min_12192018-06032020.csv'
    data = pd.read_csv(
        filename,
        usecols=['Date', '        Time', 'Out Temp', 'Out Hum', 'Dew Pt'],
        na_values=['---'],
    )
    data = format_time(data)
    data = data.astype({'Out Temp': 'float64', 'Dew Pt': 'float64'})
    data = data.set_index('Time')
    data = data.resample('H').mean()
    data.reset_index().to_feather(
        filename.replace('external', 'processed')
        .replace('5 min', 'hourly')
        .replace('5min', 'hourly')
        .replace('.csv', '.feather')
    )


if __name__ == '__main__':
    main()
