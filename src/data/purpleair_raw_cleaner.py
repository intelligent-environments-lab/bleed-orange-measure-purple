# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 17:22:14 2020

@author: CalvinL2
"""
import os
import pandas as pd
import numpy as np

import re

# TODO: improve outlier removal to replace value instead of deleting a row


def list_files(path):
    """
    Creates a list of files in the provided directory

    Parameters
    ----------
    path : str
        the relative path (from repo root) to the directory containing the target files.

    Returns
    -------
    filepaths : list
        a list of the relative path strings for the target files.

    """
    filepaths = [
        path + '/' + filename
        for filename in os.listdir(path)
        if os.path.isfile(path + '/' + filename)
    ]
    return filepaths


def parse_filename(filename):
    pattern = r'(?P<sensor>[\w\s]+)\s\((?P<environment>[a-z]{6,9})\)\s\((?P<lat>\-?\d+\.\d+)\s(?P<lon>\-?\d+\.\d+)\)\s(?P<frequency>[a-zA-Z\s]+)\s(?P<start_date>[0-9\_]{8,10})\s(?P<end_date>[0-9\_]{8,10})'
    return re.search(pattern, filename)


def remove_outlier(df, param):
    """
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

    """
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


def to_datetime(dataset):
    """
    Converts the time column from strings to datetime objects.

    Parameters
    ----------
    dataset : dataframe
        Pandas dataframe with time (strings)  as the first column.

    Returns
    -------
    dataset : dataframe
        Pandas dataframe with time (Pandas datetimes) as the first column.

    """
    # Converts string time to datetime
    dataset.loc[:, 'created_at'] = pd.to_datetime(
        dataset.loc[:, 'created_at'], format='%Y-%m-%d %H:%M:%S %Z'
    ).dt.tz_convert('US/Central')

    # Replaces NaT value resulting from datetime savings change with the preceding time
    # value shifted forward by one hour
    NaT_loc = dataset[pd.isnull(dataset['created_at'])].index
    if len(NaT_loc) != 0:
        NaT_loc = NaT_loc[0]
        dataset.loc[NaT_loc, 'created_at'] = dataset['created_at'].copy()[
            NaT_loc - 1
        ] + pd.Timedelta('1h')
    return dataset


# TODO check if outlier removes a whole row or just a values
# @profile
def main(path='data/raw/purpleair', save_location='data/interim/purpleair'):
    """
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

    """
    # Create a list of filepaths in the provided directory
    if os.path.isdir(path) and isinstance(path, str):
        filepaths = list_files(path)
    else:
        print('Error: files not found')
        return

    print('Importing csvs')
    datasets = {}
    for filepath in filepaths:
        dataset = pd.read_csv(
            filepath,
            usecols=[
                'created_at',
                'PM1.0_CF1_ug/m3',
                'PM2.5_CF1_ug/m3',
                'PM10.0_CF1_ug/m3',
                'Temperature_F',
                'Humidity_%',
                'PM2.5_ATM_ug/m3',
            ],
            # dtype={
            #     'created_at':'str',
            #     'PM1.0_CF1_ug/m3':'float32',
            #     'PM2.5_CF1_ug/m3':'float32',
            #     'PM10.0_CF1_ug/m3': 'float32',
            #     'Temperature_F':'uint32',
            #     'Humidity_%':'uint32',
            #     'PM2.5_ATM_ug/m3':'float32',
            # },
        )
        regex_match = parse_filename(filepath)
        sensor_name = regex_match['sensor']
        lat = regex_match['lat']
        lon = regex_match['lon']
        num_rows = len(dataset)
        dataset['sensor_name'] = np.repeat(sensor_name, num_rows)
        dataset['lat'] = np.repeat(lat, num_rows).astype('float64')
        dataset['lon'] = np.repeat(lat, num_rows).astype('float64')
        datasets[sensor_name] = dataset
        datasets[sensor_name] = dataset

    print('Processing data')
    for sensor_name, dataset in datasets.items():
        dataset = to_datetime(dataset)
        dataset = remove_outlier(dataset, 'PM2.5_ATM_ug/m3')
        dataset = dataset.set_index(
            ['sensor_name', 'created_at']
        )  # .resample('H').mean()
        datasets[sensor_name] = dataset

    unified_dataset = pd.concat(list(datasets.values()))
    unified_dataset.to_parquet(
        'data/interim/PurpleAir MASTER realtime individual.parquet',
        compression='brotli',
    )
    unified_dataset.resample('H', level='created_at').mean().drop(
        columns=['lat', 'lon']
    ).to_parquet(
        f'data/processed/PurpleAir combined hourly average.parquet',
        compression='brotli',
    )


if __name__ == '__main__':
    main()
