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


def find_dewpoint(temperature, relative_humidity):
    """
    Calculate dewpoint from temperature and relative humidity.

    Parameters
    ----------
    temperature : Series
        Temperature in Farenheit.
    relative_humidity : Series
        Humidity as a percentage.

    Returns
    -------
    dewpoint : Series
        Dewpoint in Farenheit.

    """
    dewpoint = (
        (temperature - 32) * 5 / 9 + ((100 - relative_humidity) / 5)
    ) * 9 / 5 + 32
    return dewpoint


def intersect(dataframes):
    """
    Perform a boolean intersect operation on dataframes based on index.

    Parameters
    ----------
    dataframes : list
        Dataframes to be intersected.

    Returns
    -------
    index : DatetimeIndex
        Index column shared by all dataframes.
    dataframes : list
        Dataframes with a common index.

    """
    # Got to start somewhere
    index = dataframes[0].index

    # Find common index
    for df in dataframes[1:]:
        index = index.intersection(df.index)

    # Apply common index to dataframes
    for num, df in enumerate(dataframes):
        dataframes[num] = df.loc[index]

    return index, dataframes


def main():
    # =============================================================================
    #     Import data
    # =============================================================================
    # TODO: Replace with UT weather
    # %% Import data from csvs
    tceq_pm = pd.read_feather('data/processed/tceq/CAMS 171_1068 PM-2.5.feather')
    tceq_pm = tceq_pm.set_index('Time')
    tceq_t = pd.read_parquet('data/interim/tceq/CAMS 5002 Outdoor Temperature.parquet')
    tceq_rh = pd.read_parquet('data/interim/tceq/CAMS 5002 Relative Humidity.parquet')
    pa_avg = pd.read_feather(
        'data/processed/purpleair/PA_combined_hourly_average.feather'
    )
    pa_avg = pa_avg.set_index('Time')

    # Only keep indices that appear in all dataframes
    _, dataframes = intersect([tceq_pm, tceq_rh, tceq_t, pa_avg])
    tceq_pm, tceq_rh, tceq_t, pa_avg = dataframes

    # =============================================================================
    #     Quadratic Regression
    # =============================================================================
    data = {
        'temp': tceq_t['Temperature (F)'],
        'r': tceq_rh['Relative Humidity (%)'],
        'purple': pa_avg['PM2.5 (ug/m3)'],
        'tceq': tceq_pm['PM2.5 (ug/m3)'],
    }

    # Calulates and adds dewpoint as a predictor
    data['dp'] = find_dewpoint(data['temp'], data['r'])

    # I() is used to get it to do quadratic regression properly
    model = smf.ols(
        formula='tceq ~ temp + r + purple + I(r**2) + I(temp**2) + I(purple**2) + I(r*temp) + I(purple*temp) + I(r*purple)',
        data=data,
    ).fit()

    # model = smf.ols(formula='tceq ~ temp + r + purple + dp', data=data).fit()

    data1 = {
        'temp': tceq_t['Tempera ture (F)'],
        'r': tceq_rh['Relative Humidity (%)'],
        'purple': pa_avg['PM2.5 (ug/m3)'],
    }
    predictions = model.predict(data)
    # Print out the statistics
    print(model.summary())


if __name__ == "__main__":
    main()

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
