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

# from plotly.offline import plot
import plotly.graph_objects as go

from sensors.common.util.importer import Util


def shift_year_to_present(df, column='Time'):
    """ Shifts all data to 2020 so that data for all years can be place in the same xrange """
    df.index = df.index.map(lambda t: t.replace(year=2020))
    return df


def process_data(years_of_data, column):
    """ Clean, resample, and roll """
    for year, dataset in years_of_data.items():
        dataset = shift_year_to_present(dataset)

    for year, dataset in years_of_data.items():
        years_of_data[year] = (
            dataset.rolling(24 * 7, center=True, min_periods=24 * 3)
            .mean()
            .resample('3D')
            .mean()
        )

    return years_of_data


def create_fig(years_of_data, column, mode='lines', hide_background=True):
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

    for year, dataset in years_of_data.items():
        if year == 2020:
            opacity = 1
        else:
            opacity = 0.3

        # Only use data from Feb 1-May 1
        dataset = dataset[dataset.index >= '2020-02-01 00:00:00-06:00']
        dataset = dataset[dataset.index < '2020-05-01 00:00:00-06:00']

        fig.add_trace(
            go.Scattergl(
                x=dataset.index,
                y=dataset[column],
                mode=mode,
                name=year,
                opacity=opacity,
            )
        )

    fig.update_layout(
        xaxis=dict(
            tickformat="%b", tick0="2020-01-02", dtick=30.42 * 24 * 60 * 60 * 1000
        )
    )

    fig.update_xaxes(range=["2020-02-01", "2020-05-03"])
    fig.update_yaxes(range=[0, max(dataset[column]) + 2])
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


# =============================================================================
#  Functions to import and plot the data
# =============================================================================


# %% Particulate Matter 2.5 data
def PM_plot(root):
    """ Plots averaged PM2.5 data from TCEQ Webberville and Interstate sensors"""
    column = 'PM 2.5 (ug/m3)'

    @Util.caching(cachefile='.cache/18-20PM.cache')
    def _import():
        return process_data(
            {
                '2020': pd.read_csv(f'{root}/2020 Webberville-Interstate PM 2.5.csv'),
                '2019': pd.read_csv(f'{root}/2019 Webberville-Interstate PM 2.5.csv'),
                '2018': pd.read_csv(f'{root}/2018 Webberville-Interstate PM 2.5.csv'),
            },
            column,
        )

    PM = _import()

    fig = create_fig(PM, column)
    highlight_covid(fig)
    label_plot(
        fig, 'PM 2.5 Levels in Austin 2018-2020', 'Month of the Year', 'PM 2.5 (ug/m3)'
    )

    fig.write_image("../2018-2020 Austin PM 2.5.png", scale=1.5)


def run_param(
    input_file,
    column,
    root=None,
    title=None,
    xtitle='Month of the Year',
    ytitle=None,
    out_file='temp_plot.png',
):
    # TODO: Replace O3 with ozone
    assert root is not None
    assert column is not None
    assert input_file is not None

    def _import():
        data = pd.read_parquet(f'{root}/{input_file}')
        years = [key for key in data.groupby(data.index.year).groups.keys()]
        dataset = {year: data[data.index.year == year] for year in years}
        return process_data(dataset, column)

    param = _import()

    fig = create_fig(param, column)
    highlight_covid(fig)
    label_plot(fig, title, xtitle, ytitle)

    fig.write_image(out_file, scale=1.5)


# %% Function calls
def main():
    root = '../data/interim/tceq'

    run_param(
        'CAMS 1605 Ozone.parquet',
        'O3 (ppb)',
        root=root,
        title='Ozone Levels in Austin 2018-2020',
        ytitle='Ozone (parts per billion)',
        out_file="../aaa2018-2020 Austin Ozone.png",
    )

    run_param(
        'CAMS 1068 Nitrogen Dioxide.parquet',
        'NO2 (ppb)',
        root=root,
        title='NO2 Levels in Austin 2018-2020',
        ytitle='NO2 (parts per billion)',
        out_file="../a2018-2020 Austin NO2.png",
    )

    # run_param(
    #     'CAMS 1068 Nitrogen Dioxide.parquet',
    #     'NOx (ppb)',
    #     root=root,
    #     title='NOx Levels in Austin 2018-2020',
    #     ytitle='NOx (parts per billion)',
    #     out_file="../a2018-2020 Austin NOx percent change.png",
    # )


if __name__ == '__main__':
    main()
