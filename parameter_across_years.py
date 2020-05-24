# -*- coding: utf-8 -*-
"""
Created on Sat May 23 15:09:54 2020

@author: CalvinL2
"""
# %% Setup
import pandas as pd

from plotly.offline import plot
import plotly.graph_objects as go

def replace_strings(pd_series):
    """ Numbers only please """
    return pd.to_numeric(pd_series, errors='coerce')

def to_datetimeindex(df, column='Time', tz='US/Central'):
    """ Time column to datetimeindex """
    df[column] = pd.to_datetime(df[column])
    df = df.set_index(column).tz_convert(tz)
    
    return df

def replace_year(df, column='Time'):
    """ Shifts all data to 2020 """
    df[column] = df[column].apply(lambda s: s.replace('2018', '2020').replace('2019', '2020'))
    return df

def process_data(years, column):
    """ Clean, resample, and roll """
    for k,v in years.items():
        years[k][column] = replace_strings(v[column])
        v = replace_year(v)
        years[k] = to_datetimeindex(v)

    for k, v in years.items():
        years[k] = v.resample('D').mean().rolling(7, center=True).mean()

    return years

def create_fig(years, column, mode='lines'):
    """ Drawing the lines and stuff """
    fig = go.Figure()
        
    for k,df in years.items():
        fig.add_trace(go.Scattergl(x=df.index, y=df[column],
                                   mode=mode, name=k))
    
    fig.update_layout(xaxis=dict(tickformat="%b",
                                 tick0="2020-01-02",
                                 dtick=30.42 * 24 * 60 * 60 * 1000))
    
    fig.update_xaxes(range=["2020-01-01","2020-12-31"])
    
    return fig

def label_plot(fig, title, xtitle, ytitle):
    """ It's in the name """
    fig.update_layout(title=title, xaxis_title=xtitle, yaxis_title=ytitle)
    

def highlight_covid(fig):
    """ That time everyone went on the month-long staycation. """
    fig.update_layout(
        shapes=[
            dict(
                type="rect",
                xref="x",
                yref="paper",
                x0="2020-3-24",
                y0=0,
                x1="2020-5-30",
                y1=1,
                fillcolor="LightSalmon",
                opacity=0.5,
                layer="below",
                line_width=0
                )
            ]
        )
            
# =============================================================================
#  Functions that actually import and plot the data (requesters)
# =============================================================================

# %% Ozone data
def ozone_plot(root):
    column = 'Ozone (ppb)'
    ozone = process_data({'2018': pd.read_csv(f'{root}/2018 Edwards ozone.csv'),
                          '2019': pd.read_csv(f'{root}/2019 Edwards ozone.csv'),
                          '2020': pd.read_csv(f'{root}/2020 Edwards ozone.csv')},
                         column)
    
    fig = create_fig(ozone, column)
    highlight_covid(fig)
    label_plot(fig, 'Ozone Levels in Austin 2018-2020',
                'Month of the Year',
                'Ozone (parts per billion)')
    
    fig.write_image("2018-2020 Austin Ozone.png", scale=1.5)

# %% Oxides of Nitrogen
def NOx_plot(root):
    column = 'NOx (ppb)'
    NOx = process_data({'2018': pd.read_csv(f'{root}/2018 Interstate.csv'),
                       '2019': pd.read_csv(f'{root}/2019 Interstate.csv'),
                       '2020': pd.read_csv(f'{root}/2020 Interstate.csv')},
                      column)
    
    fig = create_fig(NOx, column)
    highlight_covid(fig)
    label_plot(fig, 'NOx Levels in Austin 2018-2020',
                'Month of the Year',
                'NOx (parts per billion)')
    
    fig.write_image("2018-2020 Austin NOx.png", scale=1.5)

# %% Nitrogen Dioxide data
def NO2_plot(root):
    column = 'NO2 (ppb)'
    NO2 = process_data({'2018': pd.read_csv(f'{root}/2018 Interstate.csv'),
                        '2019': pd.read_csv(f'{root}/2019 Interstate.csv'), 
                        '2020': pd.read_csv(f'{root}/2020 Interstate.csv')},
                       column)
    
    fig = create_fig(NO2, column)
    highlight_covid(fig)
    label_plot(fig, 'NO2 Levels in Austin 2018-2020',
                'Month of the Year',
                'NO2 (parts per billion)')
        
    fig.write_image("2018-2020 Austin NO2.png", scale=1.5)

# %% Particulate Matter 2.5 data
def PM_plot(root):
    """ Plots averaged PM2.5 data from TCEQ Webberville and Interstate sensors"""
    column = 'PM 2.5 (ug/m3)'
    PM = process_data({'2018': pd.read_csv(f'{root}/2018 Webberville-Interstate PM 2.5.csv'),
                       '2019': pd.read_csv(f'{root}/2019 Webberville-Interstate PM 2.5.csv'),
                       '2020': pd.read_csv(f'{root}/2020 Webberville-Interstate PM 2.5.csv')},
                      column)
    
    
    fig = create_fig(PM, column)
    highlight_covid(fig)
    label_plot(fig, 'PM 2.5 Levels in Austin 2018-2020',
                'Month of the Year',
                'PM 2.5 (ug/m3)')
    
    fig.write_image("2018-2020 Austin PM 2.5.png", scale=1.5)

# %% Function calls
root = 'data/zolton'

ozone_plot(root)
NOx_plot(root)
NO2_plot(root)
PM_plot(root)
