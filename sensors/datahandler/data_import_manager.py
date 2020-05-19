# -*- coding: utf-8 -*-
"""
Created on Tue May 12 01:17:07 2020

@author: CalvinL2
"""

import os

import pandas as pd

class DataHandler:
     def __init__(self, paths):
         self.paths = paths
         self.cwd = os.getcwd()
         
         # Check if a subfolder called processed_data exists
         for path in self.paths:
             processed_data_path = path + '/processed_data'
             if self._processed_data_available(processed_data_path):
                 dfs = import_csvs(processed_data_path)
             else:
                 dfs = import_csvs(path)
                 
     
     def _processed_data_available(self, path):
         return os.path.isdir(self.cwd+'/'+path)
     
     def import_csvs(self, path):
         return [pd.read_csv(path+'/'+filename) 
                 for filename in os.listdir(self.cwd+'/'+path)]
     
     def isPurple(self, df):
         
         
             
             
if __name__ == '__main__':
    dh = DataHandler(['data/2020/1 Jan'])
    