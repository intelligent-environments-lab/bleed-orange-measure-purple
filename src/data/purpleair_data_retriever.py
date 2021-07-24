# -*- coding: utf-8 -*-

"""
Created on Sat Jun 13 01:56:30 2020

@author: CalvinL2
"""
import collections

import json
import pandas as pd
import requests

from src.data.async_requests import AsyncRequest

RAW_FOLDER = '../../../data/raw/purpleair'
RAW_B_FOLDER = '../../../data/raw/purpleair/B'

def build_filename(sensor, start, end, channel, average=None):
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
    channel : str
        Can specify 'primaryA', 'primaryB', 'secondaryA', or 'secondaryB'.
    average : int, optional
        Averaging interval in minutes. The default is None.

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

    # Append 'B' to filename for B sensor, location is 'undefined'
    if 'B' in channel:
        name = name + ' B'
        location_type = 'undefined'

    # Choose primary or secondary
    if 'primary' in channel:
        datatype = 'Primary Real Time'
    else:
        datatype = 'Secondary Real Time'

    # If data is averaged, replace 'real time' with the averaging interval
    if average is not None and int(average) > 0:
        datatype = datatype.replace('Real Time', f'{average}_minute_average')

    # Timestamp to string
    start = start.strftime('%m_%d_%Y')
    end = end.strftime('%m_%d_%Y')

    # Create filename
    filename = f'{name} ({location_type}) ({lat} {lon}) {datatype} {start} {end}.csv'
    return filename


def build_url(channel, api_key, start='', end='', average='', last=False):
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
    average : int, optional
        Averaging interval in minutes. The default is ''.
    last : bool, optional
        If true, retrieves the last entry. Overrides start and end dates. The default is false.

    Returns
    -------
    url : str
        A request url with the included parameters.

    """
    if not last:
        # Timestamps to strings
        start_date = start.strftime('%Y-%m-%d')
        end_date = end.strftime('%Y-%m-%d')

        # If average is not specified or invalid, then clear the variable
        if average is None or ~int(average) > 0:
            average = ''

    if last:
        url = f'https://api.thingspeak.com/channels/{channel}/feeds/last.json?api_key={api_key}&timezone=America/Chicago'
    else:
        url = f'https://api.thingspeak.com/channels/{channel}/feeds.csv?api_key={api_key}&offset=0&average={average}&round=2&start={start_date}%2000:00:00&end={end_date}%2000:00:00'
    
    return url


def chunks(lst, n):
    """ Splits a list into n equally sized chunks"""
    for i in range(0, len(lst), int(len(lst) / n)):
        yield lst[i : i + int(len(lst) / n)]


# TODO: Add secondary headers
def create_dataframes(datasets, channel=None):
    """
    Convert strings to dataframes.

    Parameters
    ----------
    datasets : list
        A list of data strings for each sensor.
    channel : str
        Can specify 'primaryA', 'primaryB', 'secondaryA', or 'secondaryB'.
        The default is None.

    Returns
    -------
    datasets : list
        A list of dataframes for each sensor.

    """
    # Clean up each data fragment
    for num, dataset in enumerate(datasets):
        # Convert string to dataframe
        dataset = pd.DataFrame([line.split(',') for line in dataset.split('\n')])

        # Drop header row, set column names, set index column, drop nan rows
        dataset = dataset.drop(dataset.index[0])
        columns = get_column_headers(channel=channel)
        if len(columns) == (len(dataset.columns) + 1):
            columns.remove('entry_id')
        dataset.columns = columns
        dataset = dataset.set_index('created_at')
        dataset = dataset.dropna(how='all')

        datasets[num] = dataset

    return datasets


def get_api_key(sensor, channel='primaryA'):
    """
    Locates the correct channel_ID and api key for the given sensor.

    Specifically, it traverses the dictionary provided in the variable keys.

    Parameters
    ----------
    sensor : dict
        Dictionary of metadata for one PurpleAir sensor.
    channel : str, optional
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
    if 'A' in channel:
        channel_data = sensor['A']
    else:
        channel_data = sensor['B']

    # Choose primary or secondary
    if 'primary' in channel:
        channel_ID = channel_data['THINGSPEAK_PRIMARY_ID']
        api_key = channel_data['THINGSPEAK_PRIMARY_ID_READ_KEY']
    else:
        channel_ID = channel_data['THINGSPEAK_SECONDARY_ID']
        api_key = channel_data['THINGSPEAK_SECONDARY_ID_READ_KEY']

    return channel_ID, api_key


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


def get_column_headers(channel):
    """
    Return a list of headers for the specified PurpleAir data channel.

    Parameters
    ----------
    channel : str
        Can specify 'primaryA','primaryB','secondaryA', and 'secondaryB'.

    Returns
    -------
    list
        A list of column names (strings).

    """
    channel_columns = {
        'primaryA': [
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
        ],
        'secondaryA': [
            'created_at',
            'entry_id',
            '>=0.3um/dl',
            '>=0.5um/dl',
            '>1.0um/dl',
            '>=2.5um/dl',
            '>=5.0um/dl',
            '>=10.0um/dl',
            'PM1.0_ATM_ug/m3',
            'PM10_ATM_ug/m3',
        ],
        'primaryB': [
            'created_at',
            'entry_id',
            'PM1.0_CF1_ug/m3',
            'PM2.5_CF1_ug/m3',
            'PM10.0_CF1_ug/m3',
            'UptimeMinutes',
            'ADC',
            'Pressure_hpa',
            'IAQ',
            'PM2.5_ATM_ug/m3',
        ],
        'secondaryB': [
            'created_at',
            'entry_id',
            '>=0.3um/dl',
            '>=0.5um/dl',
            '>1.0um/dl',
            '>=2.5um/dl',
            '>=5.0um/dl',
            '>=10.0um/dl',
            'PM1.0_ATM_ug/m3',
            'PM10_ATM_ug/m3',
        ],
    }
    return channel_columns[channel]

def live_data():
    thingkeys_json = import_json('thingspeak_keys.json')

    thingkeys = collections.OrderedDict()
    for sensor in thingkeys_json:
        thingkeys[sensor['Label']] = sensor

    urls = {}
    for name, sensor in thingkeys.items():
        channel_ID, api_key = get_api_key(sensor, channel='primaryA')
        url = build_url(channel=channel_ID, api_key=api_key, last=True)
        urls[name]=url
    
    for name, url in urls.items():
        row = pd.DataFrame(json.loads(requests.get(url).content), index=[0])
        row['Lat'] = thingkeys[name]['Lat']
        row['Lon'] = thingkeys[name]['Lon']
        urls[name] = row

    df = pd.concat(list(urls.values())).reset_index(drop=True)
    df.columns = get_column_headers('primaryA')+['Lat','Lon']
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['sensor'] = list(urls.keys())
    df = df[['sensor']+[col for col in df.columns if col not in ['sensor']]]
    return df

def main(
    start=None,
    end=None,
    channel='primaryA',
    average=None,
    thingkeys='src/data/thingspeak_keys.json',
    save_location='data/raw',
):
    """
    Download data from PurpleAir.

    This script downloads raw data from PurpleAir with the same output file as
    using their website. However, it is much faster since it retrieves more data
    of each url GET request, and it uses asyncio to download files simultaneously.

    This function can only access one 'channel' of the available data from UT's
    sensors at a time.

    Parameters
    ----------
    start : str
        Start date of data formatted as is %Y-%m-%d (inclusive).
    end : str
        End date of data formatted as %Y-%m-%d (inclusive).
    average : int, optional
        Averaging interval in minutes. The default is None.
    channel : str, optional
        The type and channel of data to be retrieve from the sensors. Valid values
        include 'primaryA', 'primaryB', 'secondaryA', and 'secondaryB'.
        The default is 'primaryA'.
    thingkeys : str, optional
        The name/path of the file with Thingspeak metadata, channel IDs, and api keys.
        The default is 'src/data/thingspeak_keys.json'.
    save_location : str, optional
        Directory where the output data files should be saved. The default is None.

    Returns
    -------
    None.

    """
    if (start is None) or (end is None):
        raise ValueError('Start and end dates must be specified')

    # Convert string dates to pandas datetimes. Add one day to end date to make inclusive.
    start = pd.to_datetime(start, format='%Y-%m-%d')
    end = pd.to_datetime(end, format='%Y-%m-%d') + pd.Timedelta('1d')

    # A single url request to Thingspeak can retrieve 8000 entries. At PurpleAir's
    # raw frequency of 2 min, this equates to slightly more than 11 days
    url_delta = pd.Timedelta('11d')

    # Load Thingspeak keys and metadata from file
    thingkeys_json = import_json(thingkeys)

    # Convert to dictionary with label as key
    # thingkeys = {sensor['Label']:sensor for sensor in thingkeys}

    thingkeys = collections.OrderedDict()
    for sensor in thingkeys_json:
        thingkeys[sensor['Label']] = sensor

    # Downloads and saves a csv file for each sensor
    for name, sensor in thingkeys.items():
        # name = sensor['Label']
        # print(f'\nDownloading data for {name}')

        # Create filename using metadata and PurpleAir's format,
        # remove one day from end to get back to original input end date
        filename = build_filename(
            sensor, start, end - pd.Timedelta('1d'), channel, average=average
        )

        # Get Thingspeak ID and API key for current sensor
        channel_ID, api_key = get_api_key(sensor, channel=channel)

        # Create variables for start and end date for each url request (moving window)
        url_start = start
        url_end = start + url_delta

        # Creates urls representing each fragment of data for a sensor
        urls = []
        while True:
            urls.append(
                build_url(channel_ID, api_key, url_start, url_end, average=average)
            )

            # Move time window forward
            url_start = url_end
            url_end = url_start + url_delta

            # When approaching end date, adjust request time window to fit
            if url_end > end:
                url_end = end

            # Exit this loop when all urls for this sensor are created
            if url_start >= end or url_start >= url_end:
                break

        # Saves url to sensor dict
        thingkeys[name]['urls'] = urls

    # Creates a flat list of urls for all sensor data and downloads the data asynchronously
    bulk_urls = [url for _, sensor in thingkeys.items() for url in sensor['urls']]
    response_a = AsyncRequest.get_urls(bulk_urls)

    # Unflattens downloaded data, grouping data for each sensor
    response_a = list(chunks(response_a, len(thingkeys)))

    # Inserts downloaded data into dict so that its in the same place as metadata
    count = 0
    for name, sensor in thingkeys.items():
        thingkeys[name]['responses'] = response_a[count]
        count += 1

    # Old download method
    # for name, sensor in thingkeys.items():
    #     print(f'\nDownloading data for {name}')
    #     # Asynchronously download the data using generated urls
    #     thingkeys[name]['responses'] = AsyncRequest.get_urls(sensor['urls'])

    for name, sensor in thingkeys.items():
        # Create filename using metadata and PurpleAir's format,
        # remove one day from end to get back to original input end date
        filename = build_filename(
            sensor, start, end - pd.Timedelta('1d'), channel, average=average
        )

        # If save path specified, append it to beginning of filename
        if save_location is not None:
            filename = save_location + '/' + filename

        # Store the data into dataframes and make modifications such as adding column headers
        datasets = create_dataframes(sensor['responses'], channel=channel)

        # Merge datasets for each sensor channel
        combined_dataset = pd.concat(datasets)

        # Export to csv
        combined_dataset.to_csv(filename)


if __name__ == '__main__':
    #live_data()
    main(
        start='2020-1-1',
        end='2020-9-15',
        channel='primaryA',
        save_location=RAW_FOLDER,
    )
    main(
        start='2020-1-1',
        end='2020-9-15',
        channel='primaryB',
        save_location=RAW_B_FOLDER,
    )
