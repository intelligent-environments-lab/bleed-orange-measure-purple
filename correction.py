# -*- coding: utf-8 -*-
"""
Created on Tue May  5 14:52:18 2020

@author: CalvinL2
"""
import statsmodels.api as sm
import pandas as pd
from sklearn import linear_model

from sensors.purpleair.pa_datafile import PAfiles
from sensors.tceq.TCEQ_pm_datafile import TCEQfile


def plot_avg_pm(param='PM2.5_ATM_ug/m3', freq=None):
    
    # A list of series with PM data (non rolling)
    combined_data = [file[:].resample(freq).mean()[param].rename(file.sensorname) 
                      for file in pa_files if file[param] is not None]
    
    
    combined_data =  pd.concat(combined_data, axis=1) #columns = sensors, rows = pm values
    avg_values = combined_data.mean(axis=1)  #average all sensors
    
    return avg_values #panda series

    
if __name__ == "__main__":
    pa_files = PAfiles('data/ytd', keepOutliers=False)
    tceq = TCEQfile('data/ytd/tceq.csv')
    tceq_trh = pd.read_csv('data/ytd/tceq_trh.csv').set_index('Time')
    
    pa_avg = plot_avg_pm(freq='H').rename('PM2.5_ATM_ug/m3')
    df = pa_avg.append(tceq_trh)
    
    
    
    
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


