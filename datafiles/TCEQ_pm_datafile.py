# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 01:22:28 2020

@author: CalvinL2
"""

# %% Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from datetime import datetime, timezone, timedelta

from datafiles.common_parent_datafile import CommonFile

# %% Read File
class TCEQfile(CommonFile):
    def __init__(self,filename):
        data = pd.read_csv(filename,index_col = False)
        
        PMdata = self.findPM2_5(data)
        if not PMdata.empty:
            #TODO change numerical indicies to column names
            PMdata = self.flatten(PMdata)
            PMdata[0] = CommonFile.str2date(PMdata[0],'%m/%d/%Y %H:%M',isCentral=True)
            PMdata[1] = self.str2num(PMdata[1])
            PMdata.columns = ['Time','PM2.5']
        self.data = PMdata

    def findPM2_5(self,rawdata):
        """Isolates data associated with a particular air quality parameter.(DataFrame)"""
        first_column = rawdata.iloc[:,0]
        search_value = 'PM-2.5 (Local Conditions) (POC 3) measured in micrograms per cubic meter (local conditions)'
        location = first_column.index[first_column == search_value] #Finds the desired parameter data
        if location.size > 0: #Verifies that it actually found the data 
            location = location[0]  #array to single value
            if first_column[location+3] == 'Date': #Verifies that data structure is as anticipated
                target_data = rawdata.iloc[location+3:,:]
                target_data.reset_index(drop=True, inplace=True) #optional, zeros the index column
                return target_data
            else:
                return None
        else: 
            return None

    def flatten(self,data):
        """Converts a 2D TCEQ array into a linear array.(DataFrame)"""
        values = np.array(data.iloc[1:,1:]).flatten()
        dates = np.array(data.iloc[1:,0])
        hours = np.array(data.iloc[0,1:])
        timestamp = []
        for date in dates:
            for hour in hours:
                timestamp.append(date+' '+hour)
        timestamp = np.array(timestamp)
        return pd.DataFrame([timestamp,values]).transpose()

    def str2num(self,data):
        '''Converts column of strings to float values'''
        data = np.array(data.replace('AQI',np.nan)
                        .replace('QAS',np.nan)
                        .astype(float))
        return data


if __name__ == '__main__':
    sample = TCEQfile('input\\archive\\tceq2.csv')
    
# # %% Nan remover
# p2 = pm_vector[~np.isnan(temp_vector)]
# p2 = p2[~np.isnan(pm_vector)]
# t2 = temp_vector[~np.isnan(temp_vector)]
# t2 =  t2[~np.isnan(pm_vector)]
# pm_vector = p2
# temp_vector = t2

# # %%
# plt.figure()
# t = temp_vector-np.min(temp_vector)
# p = pm_vector-np.min(pm_vector)
# plt.plot(abs((t)/np.max(t)),abs(p/np.max(p)),'.')
# a = np.linspace(0,1,100)
# plt.plot(a,a)



# %% Linear Regression

# #https://towardsdatascience.com/simple-and-multiple-linear-regression-in-python-c928425168f9
# X = temp_vector ## X usually means our input variables (or independent variables)
# y = pm_vector ## Y usually means our output/dependent variable
# X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# # Note the difference in argument order
# model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
# predictions = model.predict(X)

# # Print out the statistics
# model.summary()

# plt.figure()
# plt.plot(abs(predictions/np.max(predictions)),abs(pm_vector/np.max(pm_vector)),'.')
# a = np.linspace(0,1,100)
# plt.plot(a,a)


    