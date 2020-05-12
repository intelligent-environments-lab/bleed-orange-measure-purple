# -*- coding: utf-8 -*-
"""
Created on Tue May  5 14:52:18 2020

@author: CalvinL2
"""
import statsmodels.api as sm
import pandas as pd
from sklearn import linear_model

from plotly.offline import plot
import plotly.graph_objects as go

from sensors.pa_datafile import PAfiles
from sensors.TCEQ_pm_datafile import TCEQfile

import matplotlib.pyplot as plt
import numpy as np
def plot_avg_pm2(param='PM2.5_ATM_ug/m3', freq=None):
    
    # A list of series with PM data (non rolling)
    combined_data = [file[:].resample(freq).mean()[param].rename(file.sensorname) 
                      for file in pa_files if file[param] is not None]
    
    
    combined_data =  pd.concat(combined_data, axis=1) #columns = sensors, rows = pm values
    avg_values = combined_data.mean(axis=1)  #average all sensors
    
    return avg_values #panda series

    
if __name__ == "__main__":
    
    # Import data
    pa_files = PAfiles('data/ytd', keepOutliers=False)
    tceq = TCEQfile('data/ytd/tceq.csv')
    tceq_trh = pd.read_csv('data/ytd/tceq_trh.csv')#.set_index('Time')
    
    tceq_trh['Time'] = pd.to_datetime(tceq_trh['Time'], format='%Y-%m-%d %H:%M:%S')
    tceq_trh = tceq_trh.set_index('Time').tz_localize('US/Central', nonexistent='shift_forward')
    
    # Create column with the average pm across all sensors
    pa_avg = plot_avg_pm2(freq='H').rename('PM2.5_ATM_ug/m3')
    pa_avg.index.name = 'Time'
    
    # Combine PA data with tceq trh data in dataframe
    df = pa_avg.append(tceq_trh).rename(columns={0:'PurplePM2.5'})
    df = pd.DataFrame(pa_avg).merge(tceq_trh, how='inner', on='Time')
    df = df.merge(tceq.data.tz_convert('US/Central'), how='inner', on='Time').dropna(how='any')
    
    
    pm_vector = df['PM2.5_ATM_ug/m3']
    X = df[['PM2.5_ATM_ug/m3','Relative Humidity(%)', 'Temperature(F)']] ## X usually means our input variables (or independent variables)
    y = df['PM2.5'] ## Y usually means our output/dependent variable
    X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model
    
    # Note the difference in argument order
    model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
    predictions = model.predict(X)
    
    # Print out the statistics
    model.summary()
    
    plt.figure()
    plt.plot(abs(predictions/np.max(predictions)),abs(y/np.max(y)),'.')
    a = np.linspace(0,1,100)
    plt.plot(a,a)
    
    r1 = np.corrcoef(predictions,y)[0,1]**2
    plt.figure()
    plt.plot(abs(y/np.max(y)),abs(pm_vector/np.max(pm_vector)),'.')
    a = np.linspace(0,1,100)
    plt.plot(a,a)

    r2 = np.corrcoef(pm_vector,y)[0,1]**2

    
    plt.figure(figsize=(20, 10))
    plt.plot_date(df.index, y, '-')
    plt.plot_date(df.index, predictions,'-')
    plt.plot_date(df.index, pm_vector, '-')
    
    plt.savefig('temp-fds.svg')
    
    fig = go.Figure()
    ya=y
    fig.add_trace(go.Scattergl(x=df.index, y=ya,
                               mode='lines', name='TCEQ'))
    fig.add_trace(go.Scattergl(x=df.index, y=pm_vector,
                               mode='lines', name='PA'))
    fig.add_trace(go.Scattergl(x=df.index, y=predictions,
                               mode='lines', name='predict'))
    plot(fig)