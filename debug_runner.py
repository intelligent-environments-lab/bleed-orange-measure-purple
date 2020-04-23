# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 14:33:55 2020

@author: CalvinL2
"""
import os

import matplotlib.pyplot as plt
from plotly.offline import plot
import plotly.graph_objects as go

from sensors.TCEQ_pm_datafile import TCEQfile
from sensors.pa_datafile import PAfile
from util.timer import Timer

sample = TCEQfile('data/tceq_pm_mar.csv')
sample2 = PAfile('data/pa_covid/PA_II_0D9C (outside) (30.28559 -97.736931) Primary Real Time 03_01_2020 04_08_2020.csv')
def plot_TCEQ():
    fig = go.Figure()
    fig.add_trace(go.Scattergl(x=sample.time, y=sample.data['PM2.5'],
                        mode='lines'))
    plot(fig, filename='TCEQ test.html')


plt.plot_date(sample.time, sample.pm25, 'o-', xdate=True)
plot_TCEQ()
