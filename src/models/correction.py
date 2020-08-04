 # -*- coding: utf-8 -*-
"""
Created on Tue May  5 14:52:18 2020

@author: CalvinL2
"""

import os

import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd

# from sklearn import linear_model

from plotly.offline import plot
import plotly.graph_objects as go


import matplotlib.pyplot as plt
import numpy as np


def list_files(path):
    """
    Create a list of files in the provided directory.

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

if __name__ == "__main__":
    # TODO: Replace with UT weather
    # %% Import data from csvs
    tceq_pm = pd.read_feather('data/processed/tceq/CAMS 171_1068 PM-2.5.feather')
    tceq_pm = tceq_pm.set_index('Time')
    tceq_t = pd.read_parquet('data/interim/tceq/CAMS 5002 Outdoor Temperature.parquet')
    tceq_rh = pd.read_parquet('data/interim/tceq/CAMS 5002 Relative Humidity.parquet')
    pa_avg = pd.read_feather('data/processed/purpleair/PA_combined_hourly_average.feather')
    pa_avg = pa_avg.set_index('Time')

    # Find intersecting index
    intersect = tceq_pm.index.intersection(tceq_t.index).intersection(tceq_rh.index)
    intersect = intersect.intersection(pa_avg.index)

    # Limit data to intersecting
    tceq_pm = tceq_pm.loc[intersect]
    tceq_t = tceq_t.loc[intersect]
    pa_avg = pa_avg.loc[intersect]
    tceq_rh = tceq_rh.loc[intersect]

    # X = df[
    #     ['PM2.5_ATM_ug/m3', 'Relative Humidity (%)', 'Temperature (F)']
    # ]  ## X usually means our input variables (or independent variables)
    # y = df['PM 2.5 (ug/m3)']  ## Y usually means our output/dependent variable
    # X = sm.add_constant(X)  ## let's add an intercept (beta_0) to our model

    # Note the difference in argument order
    # model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
    # predictions = model.predict(X)

# =============================================================================
#     Quadratic Regression
# =============================================================================
    data = {
        'temp': tceq_t['Temperature (F)'],
        'r': tceq_rh['Relative Humidity (%)'],
        'purple': pa_avg['PM2.5 (ug/m3)'],
        'tceq': tceq_pm['PM2.5 (ug/m3)'],
    }

    dewpoint = ((data['temp'] - 32) * 5 / 9 + ((100 - data['r']) / 5)) * 9 / 5 + 32
    data['dp'] = dewpoint

    # I() is used to get it to do quadratic regression properly
    model = smf.ols(
        formula='tceq ~ temp + r + purple + I(r**2) + I(temp**2) + I(purple**2) + I(r*temp) + I(purple*temp) + I(r*purple)',
        data=data,
    ).fit()

    # model = smf.ols(formula='tceq ~ temp + r + purple + dp', data=data).fit()

    data1 = {
        'temp': tceq_t['Temperature (F)'],
        'r': tceq_rh['Relative Humidity (%)'],
        'purple': pa_avg['PM2.5 (ug/m3)'],
    }
    predictions = model.predict(data)
    # Print out the statistics
    print(model.summary())


    # r2_predict = np.corrcoef(predictions, y)[0, 1] ** 2
    # plt.figure()
    # plt.plot(abs(y / np.max(y)), abs(pm_vector / np.max(pm_vector)), '.')
    # a = np.linspace(0, 1, 100)
    # plt.plot(a, a)

    # plt.figure()
    # plt.plot(abs(predictions / np.max(predictions)), abs(y / np.max(y)), '.')
    # a = np.linspace(0, 1, 100)
    # plt.plot(a, a)

    # r2_original = np.corrcoef(pm_vector, y)[0, 1] ** 2

    # plt.figure(figsize=(20, 10))
    # plt.plot_date(df.index, y, '-')
    # plt.plot_date(df.index, predictions, '-')
    # plt.plot_date(df.index, pm_vector, '-')


    # fig = go.Figure()
    # ya = y
    # fig.add_trace(go.Scattergl(x=df.index, y=ya, mode='lines', name='TCEQ'))
    # fig.add_trace(go.Scattergl(x=df.index, y=pm_vector, mode='lines', name='PA'))
    # fig.add_trace(go.Scattergl(x=df.index, y=predictions, mode='lines', name='predict'))
    # plot(fig)

    # predictions.index = predictions.index.strftime('%Y-%m-%d %H:%M:%S %Z')
    # predictions.to_csv('2020 PurpleAir PM 2.5 corrected.csv')
