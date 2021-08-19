# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 12:26:32 2020

@author: CalvinL2
"""

import pandas as pd


def parquet_to_feather(input_file):
    filename = input_file
    datafile = pd.read_parquet(filename)
    filename = filename.replace('interim', 'processed').replace('parquet', 'feather')
    datafile.reset_index().to_feather(filename)


def main():
    root = 'data/interim/tceq'
    PMfile = []
    PMfile.append(pd.read_parquet(f'{root}/CAMS 171 PM-2.5.parquet'))
    PMfile.append(pd.read_parquet(f'{root}/CAMS 1068 PM-2.5.parquet'))

    PMfile2 = pd.concat(PMfile)
    PMfile2 = PMfile2.groupby(PMfile2.index).mean()
    PMfile2.to_parquet('data/processed/CAMS_171_1068_PM_2_5.parquet')


if __name__ == '__main__':
    main()
