# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 00:14:12 2020

@author: Calvin J Lin
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def mark_outliers(data):
    diff =  abs(data['Channel A PM2.5 (ug/m3)']-data['Channel B PM2.5 (ug/m3)'])
    pct_error = diff*100/data['Channel A PM2.5 (ug/m3)']
    data['outlier'] = (diff > 5) & (pct_error > 16)
    return data

def remove_marked_outliers(data):
    data_cleaned = data.loc[~data.loc[:,'outlier']]
    return data_cleaned

# https://stackoverflow.com/questions/15799162/resampling-within-a-pandas-multiindex
def resample_by_sensor(df):
    grouper = df.groupby([pd.Grouper(level='sensor_name'),pd.Grouper(level='created_at',freq='D')])
    data_averaged = grouper.mean()
    
    #This part doesn't work, creates nans but they're ignored by pd during error calc
    #insufficient_timepoints = grouper.count() < grouper.count().max()*0.9
    #data = data_averaged[~insufficient_timepoints]
    return data_averaged

def scatter_facet_grid(data,x_col='Channel B PM2.5 (ug/m3)',y_col='Channel A PM2.5 (ug/m3)', hue='outlier', bound=150):
    data = data.loc[(data[y_col]<bound) &(data[x_col]<bound)]
    g = sns.FacetGrid(data.reset_index().set_index('created_at'), col="sensor_name", hue=hue, palette=['blue','red'], col_wrap=5)
    g.map(sns.scatterplot,x_col,y_col)
    
def main():
    # Import the data
    data_A = pd.read_parquet('data/interim/PurpleAir MASTER realtime individual.parquet').drop(columns=['entry_id'])
    print('Primary_A imported')
    data_B = pd.read_parquet('data/interim/PurpleAir B MASTER realtime individual.parquet')[['PM2.5_ATM_ug/m3']]
    print('Primary_B imported')
    
    data_A = resample_by_sensor(data_A).rename(columns={'PM2.5_ATM_ug/m3':'Channel A PM2.5 (ug/m3)'})
    data_B = resample_by_sensor(data_B).rename(columns={'PM2.5_ATM_ug/m3':'Channel B PM2.5 (ug/m3)'})
    data = pd.concat([data_A, data_B], axis=1,join='inner')

    marked_data = mark_outliers(data)
    
    data_cleaned = remove_marked_outliers(data)
    scatter_facet_grid(data_cleaned)
    plt.show()
    data_cleaned.drop(columns='outlier').to_parquet('data/processed/PurpleAir daily individual.parquet')                                                         

main()