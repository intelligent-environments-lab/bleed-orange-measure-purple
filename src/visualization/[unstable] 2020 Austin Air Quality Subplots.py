# -*- coding: utf-8 -*-
"""
Created on Mon May 25 16:37:40 2020

@author: CalvinL2
"""
import pandas as pd

from plotly.offline import plot
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from sensors.common.util.importer import Util


def process_data(year, column):
    year[column] = replace_strings(year[column])
    year = to_datetimeindex(year)
    year = (
        year.rolling(24 * 7, center=True, min_periods=24 * 3)
        .mean()
        .resample('D')
        .mean()
    )

    return year


# %% Particulate Matter 2.5 data
@Util.caching(cachefile='.cache/2020PM.cache')
def PM_plot(root):
    """ Plots averaged PM2.5 data from TCEQ Webberville and Interstate sensors"""
    column = 'PM 2.5 (ug/m3)'
    return process_data(
        pd.read_csv(f'{root}/2020 Webberville-Interstate PM 2.5.csv'), column
    )


@Util.caching(cachefile='.cache/2020PAPM.cache')
def PA_PM_plot(root):
    column = 'Corrected PM 2.5 (ug/m3)'
    return process_data(
        pd.read_csv(f'{root}/2020 PurpleAir PM 2.5 corrected.csv'), column
    )


def add_subplot_trace(fig, dataset, column, name=None, num=1):
    if name is None:
        name = column
    dataset = dataset[dataset.index >= '2020-02-01 00:00:00-06:00']
    dataset = dataset[dataset.index < '2020-05-01 00:00:00-06:00']

    fig.add_trace(
        go.Scattergl(x=dataset.index, y=dataset[column], mode='lines', name=name),
        row=num,
        col=1,
    )


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
                x1="2020-5-22",
                y1=1,
                fillcolor="LightSalmon",
                opacity=0.5,
                layer="below",
                line_width=0,
            )
        ]
    )
    # fig['layout']['annotations'][0].update(text='your text here');


# %% Function calls
root = '../data/raw/zolton'

data = {
    'ozone': ozone_plot(root),
    'NOx': NOx_plot(root),
    'PM': PM_plot(root),
    'PA_PM': PA_PM_plot(root),
}


fig = make_subplots(
    rows=2, cols=1, shared_xaxes=True, x_title='Month of the Year', vertical_spacing=0.0
)

# Hides the background and grid
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis={'showgrid': False, 'showline': True, 'zeroline': False, 'linewidth': 0.01},
    xaxis2={'showgrid': False, 'showline': True, 'linecolor': 'black'},
    yaxis={'showgrid': False, 'showline': True, 'linecolor': 'black'},
    yaxis2={'showgrid': False, 'showline': True, 'linecolor': 'black'},
)


fig.update_yaxes(
    range=[0, max([data['PA_PM'].max()[0], data['PM'].max()[0]]) + 2], row=1, col=1
)
fig.update_yaxes(
    range=[0, max([data['NOx'].max()[0], data['ozone'].max()[0]]) + 5], row=2, col=1
)

add_subplot_trace(fig, data['PM'], 'PM 2.5 (ug/m3)', name='PM 2.5 (TCEQ)')
add_subplot_trace(
    fig, data['PA_PM'], 'Corrected PM 2.5 (ug/m3)', name='PM 2.5 (PurpleAir)'
)
# add_subplot_trace(fig, data['ozone'], 'Ozone (ppb)')
add_subplot_trace(fig, data['ozone'], 'Ozone (ppb)', name='Ozone', num=2)
add_subplot_trace(fig, data['NOx'], 'NOx (ppb)', name='NOx', num=2)
highlight_covid(fig)


fig.update_layout(title='2020 Austin Air Quality', xaxis_tickformat='%b')
fig.update_yaxes(title_text='PM 2.5 (ug/m3)', row=1, col=1)
fig.update_yaxes(title_text='parts per billion', row=2, col=1)
fig.update_xaxes(dict(tickformat="%b"))

fig.write_image("../2020 Austin Air Quality.png", scale=1.5)
