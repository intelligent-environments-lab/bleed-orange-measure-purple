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
from plotly.subplots import make_subplots


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
            .resample('D')
            .mean()
        )

    baseline = get_baseline(
        [dataset for year, dataset in years_of_data.items() if year != 2020]
    )
    percent_diff = get_percent_error(baseline, years_of_data[2020][column])

    return years_of_data, percent_diff


def create_fig(hide_background=True):
    # percent_change, column, mode='lines',
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

    fig.update_layout(
        xaxis=dict(
            tickformat="%b", tick0="2020-01-02", dtick=30.42 * 24 * 60 * 60 * 1000
        )
    )

    fig.update_xaxes(range=["2020-02-01", "2020-05-03"])
    # fig.update_yaxes(range=[min(percent_change) - 2, max(percent_change) + 2])
    return fig


def add_trace(fig, percent_change, mode, name='Percent Change'):
    # Only use data from Feb 1-May 1
    percent_change = percent_change[percent_change.index >= '2020-02-01 00:00:00-06:00']
    percent_change = percent_change[percent_change.index < '2020-05-01 00:00:00-06:00']

    fig.add_trace(
        go.Scattergl(
            x=percent_change.index, y=percent_change, mode=mode, name=name, opacity=1,
        )
    )


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


def get_baseline(datasets):
    return pd.concat(datasets, axis=1).mean(axis=1)


def get_percent_error(base, actual):
    return (actual - base) / base * 100


# =============================================================================
#  Functions to import and plot the data
# =============================================================================


def run_param(
    input_file,
    column,
    root='',
    title=None,
    xtitle='Month of the Year',
    ytitle=None,
    out_file='temp_plot.png',
):
    # TODO: Replace O3 with ozone
    assert column is not None
    assert input_file is not None

    def _import():
        data = pd.read_feather(f'{root}/{input_file}')
        data = data.set_index('Time')
        years = [key for key in data.groupby(data.index.year).groups.keys()]
        dataset = {year: data[data.index.year == year] for year in years}
        return process_data(dataset, column)

    ozone, percent_diff = _import()
    percent_diff = percent_diff.rename('error')
    fig = create_fig()
    add_trace(fig, percent_diff, 'lines')
    highlight_covid(fig)
    label_plot(fig, title, xtitle, ytitle)

    fig.write_image(out_file, scale=1.5)


def run_param_combined(
    param_files=None,
    root='',
    title='Percent Change in Air Quality Parameters',
    xtitle='Month of the Year',
    ytitle='Percent Change',
    out_file='temp_plot.png',
):
    assert param_files is not None

    fig = create_fig()
    highlight_covid(fig)
    label_plot(fig, title, xtitle, ytitle)

    for param_name, filename in param_files.items():
        data = pd.read_feather(f'{root}/{filename}').set_index('Time')
        years = [key for key in data.groupby(data.index.year).groups.keys()]
        dataset = {year: data[data.index.year == year] for year in years}
        year_min = [key for key in dataset.keys()][0]
        _, percent_diff = process_data(dataset, dataset[year_min].columns[0])
        percent_diff = percent_diff.rename('error')
        add_trace(fig, percent_diff, 'lines', name=param_name)

    fig.write_image(out_file, scale=1.5)


# %% Function calls
def main():
    root = 'data/processed/tceq'

    run_param(
        'CAMS 1605 Ozone.feather',
        'O3 (ppb)',
        root=root,
        title='Percent Change in Ozone Levels in Austin 2018-2020',
        ytitle='Percent change',
        out_file="2018-2020 Austin Ozone percent change.png",
    )

    run_param(
        'CAMS 1068 Nitrogen Dioxide.feather',
        'NO2 (ppb)',
        root=root,
        title='Percent Change in NO2 Levels in Austin 2018-2020',
        ytitle='Percent Change',
        out_file="a2018-2020 Austin NO2 percent change.png",
    )

    run_param_combined(
        param_files={
            'Ozone': 'CAMS 1605 Ozone.feather',
            'NO2': 'CAMS 1068 Nitrogen Dioxide.feather',
            'PM 2.5': 'CAMS 171_1068 PM-2.5.feather',
        },
        root=root,
        out_file="aaAustin Air Quality Percent Change from 2015 to 2020 subplot.png",
    )

if __name__ == '__main__':
    # Go up one level
    main()