# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 15:33:13 2020

@author: CalvinL2
"""

def remove_outlier(df, param):
    #Copied from another script pa runner
    # https://stackoverflow.com/questions/34782063/how-to-use-pandas-filter-with-iqr
    Q1 = df[param].quantile(0.25)
    Q3 = df[param].quantile(0.75)
    IQR = Q3-Q1
    mask = df[param].between(Q1-5*IQR, Q3+5*IQR, inclusive=True)
    df = df.loc[mask, :].copy()

    Q1 = df[param].rolling(180, center=True).quantile(0.25)
    Q3 = df[param].rolling(180, center=True).quantile(0.75)
    IQR = Q3-Q1
    mask = (df[param] >= Q1-1.5*IQR)&(df[param] <= Q3+1.5*IQR)
    return df.loc[mask, :]