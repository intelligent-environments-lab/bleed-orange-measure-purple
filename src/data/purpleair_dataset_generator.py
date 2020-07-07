# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 01:56:30 2020

@author: CalvinL2
"""

import requests
import json
import aiohttp
import asyncio

import pandas as pd
import nest_asyncio

nest_asyncio.apply()

from src.data.helpers.web_requests import AsyncRequest

# TODO: add autogeneration of folder directory, anticipate asyncio instability,
#   handle secondary headers


def import_json(filename):
    with open(filename, 'r', encoding='utf8') as file:
        filedata = json.load(file)
    return filedata


def get_key(keys, sensor_name, mode='primaryA'):
    channel = keys[sensor_name]
    if 'A' in mode:
        channel = channel['A']
    else:
        channel = channel['B']

    if 'primary' in mode:
        channel_ID = channel['THINGSPEAK_PRIMARY_ID']
        api_key = channel['THINGSPEAK_PRIMARY_ID_READ_KEY']
    else:
        channel_ID = channel['THINGSPEAK_SECONDARY_ID']
        api_key = channel['THINGSPEAK_SECONDARY_ID_READ_KEY']

    return channel_ID, api_key


def build_url(channel, api_key, start=None, end=None):
    start_date = start.strftime('%Y-%m-%d')
    end_date = end.strftime('%Y-%m-%d')
    url = f'https://api.thingspeak.com/channels/{channel}/feeds.csv?api_key={api_key}&start={start_date}%2000:00:00&end={end_date}%2000:00:00'
    return url


def build_filename(metadata_sets, sensor_name, start_date, end_date, mode):
    metadata = metadata_sets[sensor_name]

    location_type = metadata['DEVICE_LOCATIONTYPE']
    lat = metadata['Lat']
    lon = metadata['Lon']

    if 'primary' in mode:
        datatype = 'Primary Real Time'
    else:
        datatype = 'Secondary Real Time'

    start_date = start_date.strftime('%m_%d_%Y')
    end_date = end_date.strftime('%m_%d_%Y')

    filename = f'{sensor_name} ({location_type}) ({lat} {lon}) {datatype} {start_date} {end_date}.csv'
    return filename


def combine_and_export(datasets, sensor_name, metadata, filename):
    columns = [
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
    # if type(datasets[0]) is bytes:
    #     datasets = [data.decode('utf8') for data in datasets]
    frames = [
        pd.DataFrame([line.split(',') for line in data.split('\n')])
        for data in datasets
    ]
    frames = [
        frame.drop(frame.index[0]).set_index(0).dropna(how='all') for frame in frames
    ]
    single_file = pd.concat(frames)
    single_file.index.name = 'created_at'
    single_file.columns = columns
    single_file.to_csv(filename)


def run_request(start_date, end_date, mode='primaryA', keys=None, save_location=None):
    start_date = pd.to_datetime(
        start_date, format='%Y-%m-%d', infer_datetime_format=True
    )
    end_date = pd.to_datetime(
        end_date, format='%Y-%m-%d', infer_datetime_format=True
    ) + pd.Timedelta('1d')
    delta = pd.Timedelta('11d')
    for name, metadata in keys.items():
        print(f'\nDownloading data for {name}')
        channel_ID, api_key = get_key(keys, name, mode=mode)
        file_start = start_date
        file_end = start_date + delta
        urls = []
        while True:
            # print(f'From {file_start} to {file_end}')
            urls.append(build_url(channel_ID, api_key, file_start, file_end))
            file_start = file_end
            file_end = file_start + delta
            if file_end > end_date:
                file_end = end_date
            if file_start >= end_date or file_start >= file_end:
                break
        responses = AsyncRequest.get_urls(urls)

        filename = build_filename(keys, name, start_date, end_date, mode)
        if save_location is not None:
            filename = save_location + '/' + filename
        combine_and_export(responses, name, metadata, filename)


def main():
    thingkeys = import_json('src/data/thingspeak_keys.json')
    run_request(
        '2020-1-1', '2020-6-1', keys=thingkeys, save_location='data/raw/purpleair/test'
    )


if __name__ == '__main__':
    main()
