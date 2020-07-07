# -*- coding: utf-8 -*-
"""
Created on Sun May 24 15:44:24 2020

@author: CalvinL2
"""


import pandas as pd


def replace_strings(pd_series):
    """ Numbers only please """
    return pd.to_numeric(pd_series, errors='coerce')


def to_datetimeindex(df, column='Time', tz='US/Central'):
    """ Time column to datetimeindex """
    df[column] = pd.to_datetime(df[column])
    df = df.set_index(column).tz_convert(tz)

    return df


def process_data(years, column):
    for k, v in years.items():
        years[k][column] = replace_strings(v[column])
        years[k] = to_datetimeindex(v)

    years = {k: v[column] for k, v in years.items()}
    return years


def add_col_name(years, column):
    for _, value in years.items():
        value.rename(column, inplace=True)
    return years


def export(data):
    for key, value in data.items():
        value.index = value.index.tz_convert('UTC').strftime("%Y-%m-%d %H:%M:%S %Z")
        value.to_csv(f'{key} Webberville-Interstate PM 2.5.csv')


root = 'data/zolton'
column = 'PM 2.5 (ug/m3)'


Interstate = {
    '2018': pd.read_csv(f'{root}/2018 Interstate.csv'),
    '2019': pd.read_csv(f'{root}/2019 Interstate.csv'),
    '2020': pd.read_csv(f'{root}/2020 Interstate.csv'),
}
Interstate = process_data(Interstate, column)

Webber = {
    '2018': pd.read_csv(f'{root}/2018 Webber pm2.5.csv'),
    '2019': pd.read_csv(f'{root}/2019 Webber pm2.5.csv'),
    '2020': pd.read_csv(f'{root}/2020 Webber pm2.5.csv'),
}
Webber = process_data(Webber, column)

combined = {
    '2018': pd.concat([Interstate['2018'], Webber['2018']], axis=1).mean(axis=1),
    '2019': pd.concat([Interstate['2019'], Webber['2019']], axis=1).mean(axis=1),
    '2020': pd.concat([Interstate['2020'], Webber['2020']], axis=1).mean(axis=1),
}

combined = add_col_name(combined, column)
export(combined)
