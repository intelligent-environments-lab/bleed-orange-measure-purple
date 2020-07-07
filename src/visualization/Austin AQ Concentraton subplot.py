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


def add_subplot_trace(fig, percent_change, column, name=None, num=1, showlegend=True):
    if name is None:
        name = column
    percent_change = percent_change[percent_change.index >= '2020-02-01 00:00:00-06:00']
    percent_change = percent_change[percent_change.index < '2020-05-01 00:00:00-06:00']

    opacity = 1
    width = 3
    if name != 2020:
        opacity = 0.6
        width = 2

    color = {
        2020: '#636EFA',
        2019: '#ef553b',
        2018: '#00cc96',
        2017: '#ab63fa',
        2016: '#ffa15a',
        2015: '#19d3f3',
    }
    showlegend = False
    if num == 2:
        showlegend = True
    fig.add_trace(
        go.Scattergl(
            x=percent_change.index,
            y=percent_change,
            mode='lines',
            name=name,
            legendgroup=name,
            showlegend=showlegend,
            line=dict(width=width, color=color[name]),
            opacity=opacity,
        ),
        row=num,
        col=1,
    )


def run_param_combined_subplots_mean(
    param_files=None,
    root='',
    title='2015-2020 Air Quality Parameters',
    xtitle='Month of the Year',
    ytitle='Percent Change',
    out_file='temp_plot.png',
):
    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        x_title='Month of the Year',
        # y_title='Mean Concentr(%)',
        vertical_spacing=0.0,
    )
    years_in_legend_tracker = []
    count = 1
    for param_name, filename in param_files.items():
        data = pd.read_feather(f'{root}/{filename}').set_index('Time')
        years = [key for key in data.groupby(data.index.year).groups.keys()]
        dataset = {year: data[data.index.year == year] for year in years}
        year_min = [key for key in dataset.keys()][0]
        dataset, percent_diff = process_data(dataset, dataset[year_min].columns[0])
        # percent_diff = percent_diff.rename('error')
        for year, dataset in dataset.items():
            showlegend = True
            if year in years_in_legend_tracker:
                showlegend = False
            add_subplot_trace(
                fig,
                dataset.iloc[:, 0],
                'lines',
                name=year,
                num=count,
                showlegend=showlegend,
            )
            years_in_legend_tracker.append(year)
        # add_subplot_trace(fig, percent_diff, 'lines', name=param_name, num=count)
        count += 1

    fig.write_image(out_file, scale=1.5)
    # Hides the background and grid
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis={
            'showgrid': False,
            'showline': True,
            'linecolor': 'black',
        },  # , 'zeroline':False, 'linewidth': 0.01
        xaxis2={'showgrid': False, 'showline': True, 'linecolor': 'black'},
        xaxis3={'showgrid': False, 'showline': True, 'linecolor': 'black'},
        yaxis={
            'showgrid': False,
            'showline': True,
            'linecolor': 'black',
            'zeroline': True,
            'zerolinecolor': 'black',
            'zerolinewidth': 0.5,
        },
        yaxis2={
            'showgrid': False,
            'showline': True,
            'linecolor': 'black',
            'zeroline': True,
            'zerolinecolor': 'black',
            'zerolinewidth': 0.5,
        },
        yaxis3={
            'showgrid': False,
            'showline': True,
            'linecolor': 'black',
            'zeroline': True,
            'zerolinecolor': 'black',
            'zerolinewidth': 0.5,
        },
    )

    fig.update_yaxes(range=[0, 45], row=1, col=1)
    fig.update_yaxes(range=[0, 30], row=2, col=1)
    fig.update_yaxes(range=[0, 20], row=3, col=1)

    highlight_covid(fig)

    fig.update_layout(title=title, xaxis_tickformat='%b')
    fig.update_yaxes(title_text='Ozone (ppb)', row=1, col=1)
    fig.update_yaxes(title_text='NO2 (ppb)', row=2, col=1)
    fig.update_yaxes(title_text='PM 2.5 (ug/m3)', row=3, col=1)
    fig.update_xaxes(
        dict(tickformat="%b", tick0="2020-01-02", dtick=30.42 * 24 * 60 * 60 * 1000)
    )

    fig.write_html(out_file + '.html')

    fig.write_image(out_file, scale=1.5)


# %% Function calls
def main():
    root = 'data/processed/tceq'

    run_param_combined_subplots_mean(
        param_files={
            'Ozone': 'CAMS 1605 Ozone.feather',
            'NO2': 'CAMS 1068 Nitrogen Dioxide.feather',
            'PM 2.5': 'CAMS 171_1068 PM-2.5.feather',
        },
        root=root,
        out_file="Austin Air Quality Mean Con from 2015 to 2020 subplot.png",
    )


if __name__ == '__main__':
    # Go up one level
    main()
