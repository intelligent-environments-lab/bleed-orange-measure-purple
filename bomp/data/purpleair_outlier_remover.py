# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 00:14:12 2020

@author: Calvin J Lin
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import bomp.pathname_index as pni

def mark_outliers(df):
    """
    Compares A and B channel data to determine outliers and adds column indicating results.

    Parameters
    ----------
    df : DataFrame
        DataFrame with both A and B data present as columns.

    Returns
    -------
    df : DataFrame
        Same dataframe, but with a new 'outlier' column with True/False values.

    """
    diff = abs(df['Channel A PM2.5 (ug/m3)'] - df['Channel B PM2.5 (ug/m3)'])
    pct_error = diff * 100 / df['Channel A PM2.5 (ug/m3)']
    df['outlier'] = (diff > 5) & (
        pct_error > 16
    )  # Is outlier if A/B differ by > 5 ug/m3 or 16% error
    return df


def remove_marked_outliers(data):
    """
    Removes rows of dataframe that have the value True for the 'outlier' column.

    """
    data_cleaned = data.loc[~data.loc[:, 'outlier']]
    return data_cleaned


# https://stackoverflow.com/questions/15799162/resampling-within-a-pandas-multiindex
def resample_by_sensor(df, freq='H'):
    """
    Groupby sensor, then resample

    Parameters
    ----------
    df : DataFrame
        Original realtime dataframe with multiindex.

    Returns
    -------
    data_averaged : DataFrame
        Dataframe with new time frequency, retains multiindex.

    """
    grouper = df.groupby(
        [pd.Grouper(level='sensor_name'), pd.Grouper(level='created_at', freq=freq)]
    )
    df_averaged = grouper.mean()

    # This part doesn't work, creates nans but they're ignored by pd during error calc
    # insufficient_timepoints = grouper.count() < grouper.count().max()*0.9
    # data = data_averaged[~insufficient_timepoints]
    return df_averaged


def scatter_facet_grid(
    df,
    x_col='Channel B PM2.5 (ug/m3)',
    y_col='Channel A PM2.5 (ug/m3)',
    hue='outlier',
    bound=150,
):
    """
    Create a grid of A/B correlation plots for each sensor.

    Parameters
    ----------
    df : DataFrame
        Multi-index dataframe with data for all sensors, including A/B data.
    x_col : str, optional
        Name of column with x-axis data. The default is 'Channel B PM2.5 (ug/m3)'.
    y_col : str, optional
        Name of column with y-axis data. The default is 'Channel A PM2.5 (ug/m3)'.
    hue : str, optional
        Name of column with values to determine dat point colors. The default is 'outlier'.
    bound : int, optional
        View limit for x and y axes. The default is 150.

    Returns
    -------
    None.

    """
    df = df.loc[(df[y_col] < bound) & (df[x_col] < bound)]
    g = sns.FacetGrid(
        df.reset_index().set_index('created_at'),
        col="sensor_name",
        hue=hue,
        palette=['blue', 'red'],
        col_wrap=5,
    )
    g.map(sns.scatterplot, x_col, y_col)


def main(A_file=None, B_file=None, save_file=None, freq='H'):
    """
    Uses A and B channel data to identify and remove outliers.

    Parameters
    ----------
    A_file : str
        Parquet file with data from the A channel of the PurpleAir sensor.
    B_file : str
        Parquet file with data from the A channel of the PurpleAir sensor.
    save_file : str
        Location to save parquet file.

    Returns
    -------
    None.

    """
    if (A_file is None) or (B_file is None):
        raise ValueError('Both A and B file must be specified')
    if save_file is None:
        raise ValueError('Please specify a filename for the save_file')

    # Import the data
    print('Importing data...')
    data_A = pd.read_parquet(A_file).drop(columns=['entry_id'])
    data_B = pd.read_parquet(B_file)[['PM2.5_ATM_ug/m3']]

    print('Resampling...')
    data_A = resample_by_sensor(data_A, freq=freq).rename(
        columns={'PM2.5_ATM_ug/m3': 'Channel A PM2.5 (ug/m3)'}
    )
    data_B = resample_by_sensor(data_B, freq=freq).rename(
        columns={'PM2.5_ATM_ug/m3': 'Channel B PM2.5 (ug/m3)'}
    )
    data = pd.concat([data_A, data_B], axis=1, join='inner')

    print('Removing outliers...')
    marked_data = mark_outliers(data)
    data_cleaned = remove_marked_outliers(marked_data)

    print('Plotting...')
    scatter_facet_grid(data_cleaned)
    plt.show()

    print(f'Saving to {save_file}')
    data_cleaned.drop(columns='outlier').to_parquet(save_file)


if __name__ == '__main__':
    main(
        A_file=pni.pa_int_real,
        B_file=pni.pa_intB_real,
        save_file=pni.pa_pro_daily,
        freq='D',
    )
