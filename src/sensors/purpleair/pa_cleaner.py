# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 04:05:22 2020

@author: CalvinL2
"""
import os
import pandas as pd

def clean_multiple(cwd, file_dir):
    return [clean_data(file_dir, filename)
                for filename in os.listdir(cwd+'\\'+file_dir)
                if filename.endswith(".csv") and filename.startswith("PA")]

def clean_data(file_dir, filename):
    data = pd.read_csv(file_dir+'\\'+filename).drop(['entry_id', 'RSSI_dbm', 'UptimeMinutes', 'ADC'], axis=1, errors='ignore').dropna(axis=1, how='all')
    if not os.path.exists(file_dir+'/clean/'):
        os.makedirs(file_dir+'/clean/')
    data.to_csv(file_dir+'/clean/'+filename, index=False)
    
clean_multiple(os.getcwd(),'data/ytd')