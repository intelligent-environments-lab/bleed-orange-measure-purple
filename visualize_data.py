# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 10:22:24 2020

@author: CalvinL2
"""
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from datetime import timezone, timedelta

def plot_timeseries(time,y,fmt='o',**kwargs):
    # TODO verify that timezone works correctly
    # TODO adjust appearance of dates on x axis
    # General function to create timeseries graph with plot_date function

    # central = timezone(timedelta(hours=-6))
    # plt.plot_date(date2num(time),y,fmt,tz=central,xdate=True,**kwargs)
    plt.plot_date(date2num(time),y,fmt,xdate=True,**kwargs)
    #date2num converts datetime to plt dates
    
    # fig.autofmt_xdate()
    # plt.xlabel(time.name)
    plt.xlabel('time')
    plt.ylabel(y.name)
    for key,value in kwargs.items():   #If kwargs are specified
        if key == 'title':
            plt.title(value)
        elif key == 'xlabel':
            plt.xlabel(value)
        elif key == 'ylabel':
            plt.ylabel(value)
        elif key == 'filename':
            plt.savefig(value)

# def plot(x,y,fmt='o',**kwargs):
#     # Plot function with bundled capabilities in **kwargs
    
#     fig = plt.figure()
#     plt.plot_date(x,y,fmt)
#     fig.autofmt_xdate()
    
#     for key,value in kwargs.items():
#         if key == 'title':
#             plt.title(value)
#         elif key == 'xlabel':
#             plt.xlabel(value)
#         elif key == 'ylabel':
#             plt.ylabel(value)
#         elif key == 'filename':
#             plt.savefig(value)

def violin_plot(y):
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    bp = ax.violinplot(y)
    violin_plot(file.get_pm())
    return bp
    