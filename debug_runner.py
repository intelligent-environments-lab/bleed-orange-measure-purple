# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 14:33:55 2020

@author: CalvinL2
"""
import os

import matplotlib.pyplot as plt
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd

from sensors.tceq.TCEQ_pm_datafile import TCEQfile
from sensors.aps.aps_pm_datafile import APSPMfile
from sensors.aps.aps_trh_datafile import APSTRHfile
from sensors.purpleair.pa_datafile import PAfile, PAfiles2
from sensors.common.util.timer import Timer

# sample = TCEQfile('data/tceq_pm_mar.csv')
# sample2 = PAfile('data/pa_covid/PA_II_0D9C (outside) (30.28559 -97.736931) Primary Real Time 03_01_2020 04_08_2020.csv')
# apspm = APSPMfile('data/test3/Test_C_0304.csv')
# apst = APSTRHfile('data/test3/Test_0304_CO_TRH.csv')

sample2 = PAfiles2(os.getcwd()+'/data/monthly')

# %%

# empty = {}
# for file in sample2.files:
#     if file.sensorname in empty:
#         currentfile = empty[file.sensorname]
#         currentfile.data = currentfile.data.append(file.data)
#         empty[file.sensorname] = currentfile
#     else:
#         empty[file.sensorname] = file
# # %%
# for file in empty:
#     empty[file].data.sort_index(inplace=True)
# def plot_TCEQ():
#     fig = go.Figure()
#     fig.add_trace(go.Scattergl(x=sample.time, y=sample.data['PM2.5'],
#                         mode='lines'))
#     plot(fig, filename='TCEQ test.html')


# plt.plot_date(sample.time, sample.pm25, 'o-', xdate=True)
    
# plot_TCEQ()
def block_run():
# %% Debugging Code (To be used in ipython)
# You must be using spyder and already have pa_files created thru another script
    data = pa_files['PA_II_E6D8'].data
    datatypes = data.dtypes
    mem = data.memory_usage()
    header = data.head()
    cols = data.columns