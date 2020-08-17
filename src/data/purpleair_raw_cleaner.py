# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 17:22:14 2020

@author: CalvinL2
"""
import os
import pandas as pd
import numpy as np

# TODO: improve outlier removal to replace value instead of deleting a row


def list_files(path):
    '''
    Creates a list of files in the provided directory

    Parameters
    ----------
    path : str
        the relative path (from repo root) to the directory containing the target files.

    Returns
    -------
    filepaths : list
        a list of the relative path strings for the target files.

    '''
    filepaths = [
        path + '/' + filename
        for filename in os.listdir(path)
        if os.path.isfile(path + '/' + filename)
    ]
    return filepaths


def remove_outlier(df, param):
    '''
    Removes outlier using IQR twice.

    The first time it uses 5 * IQR to remove
    outliers that are way out of range of the dataset. Then it uses 1.5 IQR to
    remove outliers that are more local to a timeframe.

    Parameters
    ----------
    df : dataframe
        Original dataset.
    param : str
        Column name to perform outlier removal on.

    Returns
    -------
    dataframe
        Returns a dataframe with the outliers remove.

    '''
    # https://stackoverflow.com/questions/34782063/how-to-use-pandas-filter-with-iqr
    # Broad outlier removal
    Q1 = df[param].quantile(0.25)
    Q3 = df[param].quantile(0.75)
    IQR = Q3 - Q1
    mask = df[param].between(Q1 - 5 * IQR, Q3 + 5 * IQR, inclusive=True)
    df = df.loc[mask, :].copy()

    # Local outlier removal
    Q1 = df[param].rolling(180, center=True).quantile(0.25)
    Q3 = df[param].rolling(180, center=True).quantile(0.75)
    IQR = Q3 - Q1
    mask = (
        (df[param] >= Q1 - 1.5 * IQR)
        & (df[param] <= Q3 + 1.5 * IQR)
        & (df[param] <= 500)
    )

    return df.loc[mask, :]

# @profile
def to_datetime(dataset):
    '''
    Converts the time column from strings to datetime objects.

    Parameters
    ----------
    dataset : dataframe
        Pandas dataframe with time (strings)  as the first column.

    Returns
    -------
    dataset : dataframe
        Pandas dataframe with time (Pandas datetimes) as the first column.

    '''
    # Converts string time to datetime
    dataset['Time'] = pd.to_datetime(
        dataset.iloc[:, 0], format='%Y-%m-%d %H:%M:%S %Z'
    ).dt.tz_convert('US/Central')

    # Replaces NaT value resulting from datetime savings change with the preceding time
    # value shifted forward by one hour
    NaT_loc = dataset[pd.isnull(dataset['Time'])].index
    if len(NaT_loc) != 0:
        NaT_loc = NaT_loc[0]
        dataset.loc[NaT_loc, 'Time'] = dataset['Time'].copy()[
            NaT_loc - 1
        ] + pd.Timedelta('1h')
    return dataset

# TODO check if outlier removes a whole row or just a values
def main(path='data/raw/purpleair', save_location='data/interim/purpleair'):
    '''
    Entry point for script.

    Parameters
    ----------
    path : str
        Folder path (relative) containing the input files.
    save_location : str, optional
        Folder path (relative) for the output files. The default is ''.

    Returns
    -------
    None.

    '''
    # Create a list of filepaths in the provided directory
    if os.path.isdir(path) and isinstance(path, str):
        filepaths = list_files(path)
    else:
        print('Error: files not found')
        return

    datasets = {}
    # Import and perform operations for each provided file
    for filepath in filepaths:
        # Import csv while excluding some columns
        dataset = pd.read_csv(filepath)
        dataset = dataset.drop(columns=['entry_id', 'UptimeMinutes', 'RSSI_dbm'])

        # Function calls to modify dataframe
        dataset = to_datetime(dataset)
        dataset = remove_outlier(dataset, 'PM2.5_ATM_ug/m3')
        dataset = dataset.set_index('Time').resample('H').mean()

        # Create filename and export file
        filename = filepath[filepath.rfind('/') + 1 : -4].replace(
            'Real Time', 'Hourly Average'
        )
        if save_location != '':
            save_location += '/'
        dataset.to_parquet(f'{save_location}{filename}.parquet')
        sensor_name = filename[0:filename.find('(')].strip()
        dataset['sensor_name']=np.array(len(dataset)*[sensor_name])
        datasets[filepath] = dataset
    
    return
    


if __name__ == '__main__':
    main()
