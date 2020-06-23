# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 17:22:28 2020

@author: CalvinL2
"""
import os
import numpy as np
import pandas as pd

def flatten(matrix_df):
    dates = np.array(matrix_df.iloc[1:,0])
    hours = np.array(matrix_df.iloc[0,1:])
    timestamp = np.array([date+' '+hour for date in dates for hour in hours])

    values = np.array(matrix_df.iloc[1:,1:]).flatten()

    flattened_df = pd.DataFrame([timestamp,values]).transpose()
    return flattened_df

def clean_invalid_measurements(series):
    new_series = pd.to_numeric(series, errors='coerce')
    return new_series

def negative_to_zero(series):
    series[series<=0]=0
    return series

def has_substring(dataset, substring):
    first_column = dataset[0]
    for value in first_column:
        if substring in value:
            return True
    return False

def match_param_name(dataset):
    first_column = dataset[0].str
    if has_substring(dataset,'Nitric Oxide'):
        return 'NO (ppb)'
    if has_substring(dataset,'Nitric Dioxide'):
        return 'NO2 (ppb)'
    if has_substring(dataset,'Oxides of Nitrogen'):
        return 'NOx (ppb)'
    if has_substring(dataset,'Ozone'):
        return 'O3 (ppb)'
    if has_substring(dataset,'PM-2.5'):
        return 'PM2.5 (ug/m3)'
    return

def get_col_names(dataset):
    param_col_name = match_param_name(dataset)
    col_names = ['Time', param_col_name]
    return col_names

def per_dataset_clean(dataset):
    start_row = dataset[0].index[dataset[0]=='Date'][0]
    matrix = dataset.iloc[start_row:,:]
    table = flatten(matrix)
    table.iloc[:,1] = clean_invalid_measurements(table.iloc[:,1].copy())
    table.iloc[:,1] = negative_to_zero(table.iloc[:,1].copy())
    table.columns = get_col_names(dataset)
    table = format_time(table)
    table.set_index('Time')
    return

def format_time(dataset):
    dataset['Time'] = pd.to_datetime(dataset.iloc[:,0], format='%m/%d/%Y %H:%M').dt.tz_localize('US/Central', ambiguous='NaT', nonexistent='shift_forward').dt.tz_convert('UTC')
    NaT_loc = dataset[pd.isnull(dataset['Time'])].index[0]
    dataset['Time'][NaT_loc] = dataset['Time'].copy()[NaT_loc-1] + pd.Timedelta('1h')
    return dataset

def list_files(path):
    filepaths = [path+'/'+filename for filename in os.listdir(path)
                 if os.path.isfile(path+'/'+filename)]
    return filepaths

def main(path):
    if os.path.isdir(path) and isinstance(path, str):
        filepaths = list_files(path)
    else:
        return
    datasets = {filepath[filepath.rfind('/')+1:-4].replace('Summary Report for ','').replace('(Local Conditions) ',''):pd.read_csv(filepath, names=list(range(25)))
     for filepath in filepaths}

    for filename, data in datasets.items():
        datasets[filename] = per_dataset_clean(data)


    return
if __name__ == '__main__':
    main('data/raw/tceq')