# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 14:33:55 2020

@author: CalvinL2
"""

from plotly.offline import plot
import plotly.graph_objects as go

from TCEQ_pm_datafile import TCEQfile
    
sample = TCEQfile('C:/Users/CalvinLin/My Files/GitHub/bleed-orange-measure-purple/input/tceq_pm_mar.csv')

fig = go.Figure()
fig.add_trace(go.Scattergl(x=sample.data['Time'], y=sample.data['PM2.5'],
                    mode='lines'))

plot(fig, filename='TCEQ test.html')