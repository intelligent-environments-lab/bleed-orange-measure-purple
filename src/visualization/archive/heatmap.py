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


def create_fig(z, column, mode='lines', hide_background=True):
    """ Drawing the lines and stuff """
    if hide_background:
        layout = go.Layout(
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis={'showgrid': False, 'showline': True, 'linecolor': 'black'},
            yaxis={'showgrid': False, 'showline': True, 'linecolor': 'black'},
        )
        fig = go.Figure(layout=layout)
    else:
        fig = go.Figure()

    weekdays = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
    fig = go.Figure(data=go.Heatmap(z=z, y=weekdays, hoverongaps=False))

    return fig


def label_plot(fig, title, xtitle, ytitle):
    """ It's in the name """
    fig.update_layout(
        title=title,
        xaxis_title=xtitle,
        yaxis_title=ytitle,
        annotations=[
            dict(
                x=1,
                y=-0.2,
                showarrow=False,
                text="Source: TCEQ",
                xref="paper",
                yref="paper",
            ),
        ],
    )


def process_data(dataset, column):
    """ Clean, resample, and roll """

    dataset = (
        dataset.rolling(24 * 7, center=True, min_periods=24 * 3)
        .mean()
        .resample('D')
        .mean()
    )

    dataset = dataset[dataset.index >= '2020-02-01 00:00:00-06:00']
    dataset = dataset[dataset.index < '2020-05-01 00:00:00-06:00']

    gb = dataset.groupby(by=dataset.index.dayofweek)
    z = [day_of_week[1][column].tolist() for day_of_week in gb]

    return dataset, z


def main():
    """ Plots averaged PM2.5 data from TCEQ Webberville and Interstate sensors"""

    root = 'data/processed/purpleair'
    column = 'PM2.5 (ug/m3)'

    dataset = pd.read_feather(f'{root}/PA_combined_hourly_average.feather')
    dataset = dataset.set_index('Time')

    pm, z = process_data(dataset, column)
    fig = create_fig(z, column)
    label_plot(
        fig, 'PM 2.5 Levels in Austin 2018-2020', 'Month of the Year', 'PM 2.5 (ug/m3)'
    )

    fig.write_image("reports/working/Austin PM 2.5 Heatmap.png", scale=1.5)


if __name__ == '__main__':
    main()
