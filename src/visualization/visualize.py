# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 00:57:11 2020

@author: Calvin J Lin
"""
import pandas as pd

def update_layout(fig, no_bg=True, short_xticklabel=True, fontsize=None, nticks=None):
    """Updates layout of plotly graphs"""
    if fontsize is not None:
        fig.update_layout(
            font=dict(size=fontsize)
        )
    if no_bg:
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        for update_axes in [fig.update_xaxes, fig.update_yaxes]:
            update_axes(
                zeroline=True,
                linecolor='black'
            )

    if short_xticklabel:
        fig.update_xaxes(
            tickangle=45,
            tickformat="%m-%y",
            nticks=nticks,
        )
    return fig

def truncate_sensor_name(df):
    """ Remove PA_II_ from sensor name"""
    for i, value in enumerate(df['sensor_name']):
        df.loc[i, 'sensor_name'] = value.replace("PA_II_", "")
    return df

def resample_by_sensor(df,fq):
    """Resample on level two values of multiindex"""
    data = df.groupby([pd.Grouper(level='sensor_name'),pd.Grouper(level='created_at',freq=fq)]).mean()
    return data