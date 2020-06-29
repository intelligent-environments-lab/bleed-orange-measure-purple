# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 17:22:14 2020

@author: CalvinL2
"""
import os
import pandas as pd
# TODO: improve outlier removal to replace value instead of deleting a row
def remove_outlier(df, param):
    # https://stackoverflow.com/questions/34782063/how-to-use-pandas-filter-with-iqr
    Q1 = df[param].quantile(0.25)
    Q3 = df[param].quantile(0.75)
    IQR = Q3-Q1
    mask = df[param].between(Q1-5*IQR, Q3+5*IQR, inclusive=True)
    df = df.loc[mask, :].copy()

    Q1 = df[param].rolling(180, center=True).quantile(0.25)
    Q3 = df[param].rolling(180, center=True).quantile(0.75)
    IQR = Q3-Q1
    mask = (df[param] >= Q1-1.5*IQR)&(df[param] <= Q3+1.5*IQR)&(df[param] <= 500)

    return df.loc[mask, :]

def list_files(path):
    filepaths = [
        path + '/' + filename
        for filename in os.listdir(path)
        if os.path.isfile(path + '/' + filename)
    ]
    return filepaths

def format_time(dataset):
    dataset['Time'] = (
        pd.to_datetime(dataset.iloc[:, 0], format='%Y-%m-%d %H:%M:%S %Z')
        .dt.tz_convert('US/Central')
    )
    NaT_loc = dataset[pd.isnull(dataset['Time'])].index
    if len(NaT_loc) != 0:
        NaT_loc = NaT_loc[0]
        dataset.loc[NaT_loc, 'Time'] = dataset['Time'].copy()[
            NaT_loc - 1
        ] + pd.Timedelta('1h')
    return dataset

def main(path, save_location=''):
    if os.path.isdir(path) and isinstance(path, str):
        filepaths = list_files(path)
    else:
        return

    for filepath in filepaths:
        cols = list(pd.read_csv(filepath, nrows=1))
        dataset = pd.read_csv(
            filepath,
            usecols=[
                col
                for col in cols
                if col not in ['entry_id', 'UptimeMinutes', 'RSSI_dbm']
            ],
        )
        dataset = dataset.rename(
            columns={
                'created_at': 'Time',
                'PM1.0_CF1_ug/m3': 'PM1.0 CF1 (ug/m3)',
                'PM2.5_CF1_ug/m3': 'PM2.5 CF1 (ug/m3)',
                'PM10.0_CF1_ug/m3': 'PM10.0 CF1 (ug/m3)',
                'Temperature_F': 'Temperature (F)',
                'Humidity_%': 'Humidity(%)',
                'PM2.5_ATM_ug/m3': 'PM2.5 (ug/m3)',
            }
        )
        dataset = format_time(dataset)
        dataset = remove_outlier(dataset, 'PM2.5 (ug/m3)')
        dataset = dataset.set_index('Time').resample('H').mean()
        filename = filepath[filepath.rfind('/') + 1 : -4].replace('Real Time', 'Hourly Average')
        if save_location != '':
            save_location += '/'
        dataset.to_parquet(f'{save_location}{filename}.parquet')

    return


if __name__ == '__main__':
    main('data/raw/purpleair', save_location='data/interim/purpleair')
