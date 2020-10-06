# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 00:14:12 2020

@author: Calvin J Lin
"""
import pandas as pd
from plotly import graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

def mark_outliers(data_A, data_B, bound=100):
    data = pd.concat([data_A, data_B[['Channel B PM2.5 (ug/m3)']]], axis=1,join='inner')
    data['diff'] =  abs(data['Channel A PM2.5 (ug/m3)']-data['Channel B PM2.5 (ug/m3)'])
    data['percent_error'] = data['diff']*100/data['Channel A PM2.5 (ug/m3)']
    data['outlier'] = (data['diff'] > 5) & (data['percent_error'] > 16)
    data = data.loc[(data['Channel A PM2.5 (ug/m3)']<bound) &(data['Channel B PM2.5 (ug/m3)']<bound)]
    return data

def remove_marked_outliers(data):
    data_cleaned = data.loc[data.loc[:,'outlier']==False]
    return data_cleaned

def main():
    # Import the data
    data_A = pd.read_parquet('data/interim/PurpleAir MASTER realtime individual.parquet')
    print('Primary_A imported')
    data_B = pd.read_parquet('data/interim/PurpleAir B MASTER realtime individual.parquet')
    print('Primary_B imported')
    
    # https://stackoverflow.com/questions/15799162/resampling-within-a-pandas-multiindex
    data_A = data_A.groupby([pd.Grouper(level='sensor_name'),pd.Grouper(level='created_at', freq='D')]).mean()\
        .rename(columns={'PM2.5_ATM_ug/m3':'Channel A PM2.5 (ug/m3)'})
    data_B = data_B.groupby([pd.Grouper(level='sensor_name'),pd.Grouper(level='created_at', freq='D')]).mean()\
        .rename(columns={'PM2.5_ATM_ug/m3':'Channel B PM2.5 (ug/m3)'})

    data = mark_outliers(data_A, data_B)
    
    data_cleaned = remove_marked_outliers(data).drop(columns=['outlier','entry_id'])
    data_cleaned.to_parquet('data/processed/PurpleAir hourly individual.parquet')                                                         

main()