# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 09:38:04 2020

@author: CalvinL2
"""

import os
import pandas as pd


def list_files(path):
    filepaths = [
        path + '/' + filename
        for filename in os.listdir(path)
        if os.path.isfile(path + '/' + filename)
    ]
    return filepaths


def parquet_to_feather(input_file):
    filename = input_file
    datafile = pd.read_parquet(filename)
    filename = filename.replace('interim', 'processed').replace('parquet', 'feather')
    datafile.reset_index().to_feather(filename)


def main():
    root = 'data/interim/purpleair'

    filepaths = list_files(root)

    for filepath in filepaths:
        parquet_to_feather(filepath)

    datasets = [pd.read_parquet(filepath) for filepath in filepaths]
    combined = pd.concat(datasets)
    combined_average = combined.groupby(combined.index).mean()
    combined_average.reset_index().to_feather(
        'data/processed/purpleair/PA_combined_hourly_average.feather'
    )


if __name__ == '__main__':
    main()
