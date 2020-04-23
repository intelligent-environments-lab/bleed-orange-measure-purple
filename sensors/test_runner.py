# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 14:33:55 2020

@author: CalvinL2
"""
import os

from plotly.offline import plot
import plotly.graph_objects as go

from sensors.TCEQ_pm_datafile import TCEQfile
from sensors.pa_datafile import PAfile

sample = TCEQfile('input/tceq_pm_mar.csv')

def plot_TCEQ():
    fig = go.Figure()
    fig.add_trace(go.Scattergl(x=sample.data['Time'], y=sample.data['PM2.5'],
                        mode='lines'))
    plot(fig, filename='TCEQ test.html')