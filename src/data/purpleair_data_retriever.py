# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 01:56:30 2020

@author: CalvinL2
"""

import json

import pandas as pd

from src.data.helpers.web_requests import AsyncRequest

# TODO: add autogeneration of folder directory, anticipate asyncio instability,
#   handle secondary headers

# =============================================================================
#  Thingspeak file import/read functions
# =============================================================================

def import_json(filename):
    """
    Load a json file.

    Parameters
    ----------
    filename : str
        Filename or relative path to file.

    Returns
    -------
    filedata : dict
        Data in json file.

    """
    with open(filename, 'r', encoding='utf8') as file:
        filedata = json.load(file)
    return filedata


def get_key(keys, sensor, mode='primaryA'):
    """
    Locates the correct channel_ID and api key for the given sensor.

    Specifically, it traverses the dictionary provided in the variable keys.

    Parameters
    ----------
    keys : dict
        Data loaded from json file.
    sensor : dict
        Dictionary of metadata for one PurpleAir sensor.
    mode : str, optional
        Can specify primaryA, primaryB, secondaryA, or secondaryB.
        The default is 'primaryA'.

    Returns
    -------
    channel_ID : str
        Thingspeak channel ID for the given sensor.
    api_key : str
        Thingspeak api key for the given sensor.

    """
    # Choose A or B
    if 'A' in sensor:
        channel = sensor['A']
    else:
        channel = sensor['B']

    # Choose primary or secondary
    if 'primary' in sensor:
        channel_ID = channel['THINGSPEAK_PRIMARY_ID']
        api_key = channel['THINGSPEAK_PRIMARY_ID_READ_KEY']
    else:
        channel_ID = channel['THINGSPEAK_SECONDARY_ID']
        api_key = channel['THINGSPEAK_SECONDARY_ID_READ_KEY']

    return channel_ID, api_key

# =============================================================================
# Code that actually handles downloading PurpleAir data
# =============================================================================

# TODO: function might not handle a none value correctly
def build_url(channel, api_key, start=None, end=None):
    """
    Create a thingspeak.com url that can be used to access the target data.

    Parameters
    ----------
    channel : str
        Thingspeak channel ID.
    api_key : str
        Thingspeak api key.
    start : Timestamp, optional
        Starting date. The default is None.
    end : Timestamp, optional
        Ending date. The default is None.

    Returns
    -------
    url : str
        A request url with the included parameters.

    """
    # Timestamps to strings
    start_date = start.strftime('%Y-%m-%d')
    end_date = end.strftime('%Y-%m-%d')

    url = f'https://api.thingspeak.com/channels/{channel}/feeds.csv?api_key={api_key}&start={start_date}%2000:00:00&end={end_date}%2000:00:00'
    return url


def build_filename(sensor, start, end, mode):
    """
    Create a filename (string) based on sensor and data parameters.

    Parameters
    ----------
    sensor : dict
        Dict of metadata for one sensor.
    start : Timestamp
        Start date of data.
    end : Timestamp
        End date of data.
    mode : str
        Can specify 'primaryA', 'primaryB', 'secondaryA', or 'secondaryB'.

    Returns
    -------
    filename : str
        A filename for the given datafile.

    """
    # More convenient local variables
    name = sensor['Label']
    location_type = sensor['DEVICE_LOCATIONTYPE']
    lat = sensor['Lat']
    lon = sensor['Lon']

    # Append 'B' to filename for B sensor
    if 'B' in mode:
        name = name + ' B'

    # Choose primary or secondary
    if 'primary' in mode:
        datatype = 'Primary Real Time'
    else:
        datatype = 'Secondary Real Time'

    # Timestamp to string
    start = start.strftime('%m_%d_%Y')
    end = end.strftime('%m_%d_%Y')

    # Create filename
    filename = f'{name} ({location_type}) ({lat} {lon}) {datatype} {start} {end}.csv'
    return filename

# TODO: Add secondary headers
def create_dataframes(datasets):
    """
    Convert strings to dataframes.

    Parameters
    ----------
    datasets : list
        A list of data strings for each sensor.

    Returns
    -------
    datasets : list
        A list of dataframes for each sensor.

    """
    columns = [
        'created_at',
        'entry_id',
        'PM1.0_CF1_ug/m3',
        'PM2.5_CF1_ug/m3',
        'PM10.0_CF1_ug/m3',
        'UptimeMinutes',
        'RSSI_dbm',
        'Temperature_F',
        'Humidity_%',
        'PM2.5_ATM_ug/m3',
    ]

    # Clean up each data fragment
    for num, dataset in enumerate(datasets):
        # Convert string to dataframe
        dataset = pd.DataFrame([line.split(',') for line in dataset.split('\n')])

        dataset.columns = columns

        # Drop header row, set column names, set index column, drop nan rows
        dataset = dataset.drop(dataset.index[0])
        dataset.columns = columns
        dataset = dataset.set_index('created_at')
        dataset = dataset.dropna(how='all')

        datasets[num] = dataset

    return datasets


def main(start, end, mode='primaryA', thingspeak='src/data/thingspeak_keys.json', save_location=None):
    """
    Download data from PurpleAir.

    This script downloads raw data from PurpleAir with the same output file as
    using their website. However, it is much faster since it retrieves more data
    of each url GET request, and it uses asyncio to download files simultaneously.

    This function can only access one 'mode' of the available data from UT's
    sensors at a time.

    Parameters
    ----------
    start : str
        Start date of data formatted as is %Y-%m-%d (inclusive).
    end : str
        End date of data formatted as %Y-%m-%d (inclusive).
    mode : str, optional
        The type and channel of data to be retrieve from the sensors. Valid values
        include 'primaryA', 'primaryB', 'secondaryA', and 'secondaryB'.
        The default is 'primaryA'.
    thingspeak : str, optional
        The name/path of the file with Thingspeak metadata, channel IDs, and api keys.
        The default is 'src/data/thingspeak_keys.json'.
    save_location : str, optional
        Directory where the output data files should be saved. The default is None.

    Returns
    -------
    None.

    """
    # Convert string dates to pandas datetimes. Add one date to end date to make inclusive.
    start = pd.to_datetime(start, format='%Y-%m-%d')
    end = pd.to_datetime(end, format='%Y-%m-%d') + pd.Timedelta('1d')

    # A single url request to Thingspeak can retrieve 8000 entries. At PurpleAir's
    # raw frequency of 2 min, this equates to slightly more than 11 days
    url_delta = pd.Timedelta('11d')

    # Load Thingspeak keys and metadata from file
    thingkeys = import_json(thingspeak)

    # Downloads and saves a datafile for each sensor
    for sensor in thingkeys:
        name = sensor['Label']
        print(f'\nDownloading data for {name}')

        # Get Thingspeak ID and API key for current sensor
        channel_ID, api_key = get_key(thingkeys, sensor, mode=mode)

        # Start and end date for each url request
        url_start = start
        url_end = start + url_delta

        # Creates urls representing each fragment of data for a sensor
        urls = []
        while True:
            urls.append(build_url(channel_ID, api_key, url_start, url_end))

            # Move time window forward
            url_start = url_end
            url_end = url_start + url_delta

            # When approaching end date, adjust request time window to fit
            if url_end > end:
                url_end = end

            # Exit this loop when all urls for this sensor are created
            if url_start >= end or url_start >= url_end:
                break

        # Asynchronously download the data
        responses = AsyncRequest.get_urls(urls)

        # Create filename
        filename = build_filename(sensor, start, end, mode)

        # If save path specified, append it to beginning of filename
        if save_location is not None:
            filename = save_location + '/' + filename

        datasets = create_dataframes(responses)

        # Merge datasets
        combined_dataset = pd.concat(datasets)

        # Export
        combined_dataset.to_csv(filename)


if __name__ == '__main__':
    main('2020-1-1', '2020-7-1', save_location='data/raw/purpleair')
