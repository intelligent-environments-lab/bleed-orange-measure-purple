# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 23:44:24 2020

@author: Calvin Lin
"""
from collections import OrderedDict
import json

import requests

PURPLEAIR_KEY_URL = 'https://www.purpleair.com/json?exclude=true&key=null&show=null&nwlat=30.291268505204116&selat=30.272526603783206&nwlng=-97.7717631299262&selng=-97.72423886855452'

def extract_key_info(pa_json):
    """
    Extract key-value pairs of interest and puts them in a new dict.

    Parameters
    ----------
    pa_json : dict
        The 'results' section of the json file retrieved from PurpleAir.

    Returns
    -------
    data_json : dict
        A dict with only the values of interest.

    """
    target_keys = [
        'ID',
        'Label',
        'ParentID',
        'Lat',
        'Lon',
        'DEVICE_LOCATIONTYPE',
        'THINGSPEAK_PRIMARY_ID',
        'THINGSPEAK_PRIMARY_ID_READ_KEY',
        'THINGSPEAK_SECONDARY_ID',
        'THINGSPEAK_SECONDARY_ID_READ_KEY',
    ]

    data_json = {key: value for key, value in pa_json.items() if key in target_keys}

    return data_json


def sort_ab_channels(pa_json):
    """
    Sorts key-value pairs into A/B channel and associated them with the sample sensor name.

    Parameters
    ----------
    pa_json : list
        A list of dictionaries for each sensor.

    Returns
    -------
    sensors : list
        A list of dictionaries for each sensor (after reorganizing/rearranging).

    """
    # In the end, sensor_b will be a subset of sensors
    sensors = OrderedDict()
    sensors_b = []

    for sensor in pa_json:

        # Extracts the thingspeak keys from the json
        thingspeak_keys = OrderedDict(
            [
                ('THINGSPEAK_PRIMARY_ID', sensor.pop('THINGSPEAK_PRIMARY_ID')),
                (
                    'THINGSPEAK_PRIMARY_ID_READ_KEY',
                    sensor.pop('THINGSPEAK_PRIMARY_ID_READ_KEY'),
                ),
                ('THINGSPEAK_SECONDARY_ID', sensor.pop('THINGSPEAK_SECONDARY_ID')),
                (
                    'THINGSPEAK_SECONDARY_ID_READ_KEY',
                    sensor.pop('THINGSPEAK_SECONDARY_ID_READ_KEY'),
                ),
            ]
        )

        # Sorts thingspeak keys into channel A or B
        if 'ParentID' in sensor:
            thingspeak_keys['ID'] = sensor['ParentID']
            sensor['B'] = thingspeak_keys
            sensors_b.append(sensor)
        else:
            thingspeak_keys['ID'] = sensor['ID']
            sensor['A'] = thingspeak_keys
            sensors[sensor['ID']] = sensor

        # Use OrderedDict to move 'ID' to top of each channel's values
        thingspeak_keys.move_to_end('ID', last=False)

    # Merges the two channels into one entry
    for sensor in sensors_b:
        sensors[sensor['ParentID']]['B'] = sensor['B']

    # Removes top level 'ID' because it's already stored for each A/B channel
    for sensor in sensors.values():
        sensor.pop('ID')

    # Convert top-level dict to list
    sensors = list(sensors.values())

    return sensors


def export_json(pa_json, filename='src/data/thingspeak_keys.json'):
    """Write json data to json file."""
    with open(filename, 'w', encoding='utf8') as file:
        json.dump(pa_json, file, indent=4, ensure_ascii=False)
        print(f'Thingspeak keys saved to {filename}')


def main():
    """
    Create and save Thingspeak IDs, keys, and metadata to file.

    This script creates a thingspeak json file, which contains values needed in
    order to download PurpleAir data.

    Returns
    -------
    None.

    """

    url = PURPLEAIR_KEY_URL
    # Send internet request and load response as json
    data = requests.get(url).text
    data_json = json.loads(data)['results']


    # Extract and transform useful json data
    purpleair_ids = [extract_key_info(sensor) for sensor in data_json]
    purpleair_ids = sort_ab_channels(purpleair_ids)

    # Save to file
    export_json(purpleair_ids)


if __name__ == '__main__':
    main()
