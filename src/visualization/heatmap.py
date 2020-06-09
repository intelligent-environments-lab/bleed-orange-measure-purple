# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 10:41:44 2020

@author: CalvinL2
"""


# -*- coding: utf-8 -*-
"""
Created on Sat May 23 15:09:54 2020

@author: CalvinL2
"""

# =============================================================================
#  This script imports data located under data/zolton and uses it create plots
#  that compare the differences in a parameter in 2018, 2019, and 2020.
# =============================================================================

# %% Setup
import pandas as pd
import numpy as np

# from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go

from sensors.common.util.importer import Util

def to_numeric(pd_series):
    """ Substitutes TCEQ strings like 'MDL' or 'AQI' with nans """
    return pd.to_numeric(pd_series, errors='coerce')

def set_datetimeindex(df, column='Time', tz='US/Central'):
    """ Time column to datetimeindex """
    df[column] = pd.to_datetime(df[column])
    df = df.set_index(column).tz_convert(tz)

    return df

def shift_year_to_present(df, column='Time'):
    """ Shifts all data to 2020 so that data for all years can be place in the same xrange """
    df[column] = df[column].apply(lambda s: s.replace('2018', '2020').replace('2019', '2020'))
    return df

def process_data(dataset, column):
    """ Clean, resample, and roll """
    dataset = dataset['2020']
    dataset[column] = to_numeric(dataset[column])
    dataset = shift_year_to_present(dataset)
    dataset = set_datetimeindex(dataset)

    dataset = dataset.rolling(24*7, center=True, min_periods=24*3).mean().resample('D').mean()
    
    
    dataset = dataset[dataset.index >= '2020-02-01 00:00:00-06:00']
    dataset = dataset[dataset.index < '2020-05-01 00:00:00-06:00']
    
    gb = dataset.groupby(by=dataset.index.dayofweek)
    z = [day_of_week[1]['Ozone (ppb)'].tolist() for day_of_week in gb]
    
    
    
    return dataset, z

def create_fig(z, column, mode='lines', hide_background=True):
    """ Drawing the lines and stuff """
    if hide_background:
        layout = go.Layout(
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis={'showgrid': False, 'showline': True, 'linecolor': 'black'},
            yaxis={'showgrid': False, 'showline': True, 'linecolor': 'black'})
        fig = go.Figure(layout=layout)
    else:
        fig = go.Figure()
    
    weekdays = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
    fig = go.Figure(data=go.Heatmap(z=z, y=weekdays, hoverongaps=False))

    return fig

def label_plot(fig, title, xtitle, ytitle):
    """ It's in the name """
    fig.update_layout(title=title, xaxis_title=xtitle, yaxis_title=ytitle,
                      annotations=[dict(
                          x=1,
                          y=-0.2,
                          showarrow=False,
                          text="Source: TCEQ",
                          xref="paper",
                          yref="paper"
                          ),])



# =============================================================================
#  Functions to import and plot the data 
# =============================================================================

# %% Ozone data
def ozone_plot(root):
    column = 'Ozone (ppb)'

    # @Util.caching(cachefile='.cache/18-20ozone.cache')
    def _import():
        return process_data({'2020': pd.read_csv(f'{root}/2020 Edwards ozone.csv')},
                            column)
    ozone, percent_diff = _import()
    fig = create_fig(percent_diff, column)
    label_plot(fig, 'Ozone Levels in Austin 2018-2020',
               'Month of the Year',
               'Ozone (parts per billion)')

    fig.write_image("../heatmap.png", scale=1.5)

# %% Oxides of Nitrogen
def NOx_plot(root):
    column = 'NOx (ppb)'

    # @Util.caching(cachefile='.cache/18-20NOx.cache')
    def _import():
        return process_data({'2020': pd.read_csv(f'{root}/2020 Interstate.csv')},
                            column)
    NOx, percent_diff = _import()
    fig = create_fig(percent_diff, column)
    label_plot(fig, 'NOx Levels in Austin 2018-2020',
               'Month of the Year',
               'NOx (parts per billion)')

    fig.write_image("2018-2020 Austin NOx percent change.png", scale=1.5)

# %% Nitrogen Dioxide data
def NO2_plot(root):
    column = 'NO2 (ppb)'

    # @Util.caching(cachefile='.cache/18-20NO2.cache')
    def _import():
        return  process_data({'2020': pd.read_csv(f'{root}/2020 Interstate.csv')},
                             column)
    NO2, percent_diff = _import()
    fig = create_fig(percent_diff, column)
    label_plot(fig, 'NO2 Levels in Austin 2018-2020',
               'Month of the Year',
               'NO2 (parts per billion)')

    fig.write_image("2018-2020 Austin NO2 percent change.png", scale=1.5)

# %% Particulate Matter 2.5 data
def PM_plot(root):
    """ Plots averaged PM2.5 data from TCEQ Webberville and Interstate sensors"""
    column = 'PM 2.5 (ug/m3)'

    # @Util.caching(cachefile='.cache/18-20PM.cache')
    def _import():
        return process_data({'2020': pd.read_csv(f'{root}/2020 Webberville-Interstate PM 2.5.csv')}, column)
    pm, z = _import()
    fig = create_fig(z, column)
    label_plot(fig, 'PM 2.5 Levels in Austin 2018-2020',
               'Month of the Year',
               'PM 2.5 (ug/m3)')

    fig.write_image("../2018-2020 Austin PM 2.5 percent change.png", scale=1.5)

# %% Function calls
def main():
    root = '../data/raw/zolton'
    
    ozone_plot(root)
    # NOx_plot(root)
    # NO2_plot(root)
    # PM_plot(root)
    
if __name__ == '__main__':
    main()
