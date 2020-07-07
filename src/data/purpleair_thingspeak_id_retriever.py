# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 15:40:39 2020

@author: CalvinL2
"""

from urllib.request import urlopen
import requests
import json

import yaml


def load_json_from_url(url):
    html = urlopen(url).read()
    return json.loads(html)

def get_json_from_url(url):
    html = requests.get(url)

def extract_key_info(pa_json):
    thingspeak = {
        'THINGSPEAK_PRIMARY_ID': pa_json['THINGSPEAK_PRIMARY_ID'],
        'THINGSPEAK_PRIMARY_ID_READ_KEY': pa_json['THINGSPEAK_PRIMARY_ID_READ_KEY'],
        'THINGSPEAK_SECONDARY_ID': pa_json['THINGSPEAK_SECONDARY_ID'],
        'THINGSPEAK_SECONDARY_ID_READ_KEY': pa_json['THINGSPEAK_SECONDARY_ID_READ_KEY'],
    }

    sensor = {'ID': pa_json['ID'], 'Label': pa_json['Label']}

    if 'ParentID' in pa_json:
        sensor['ParentID'] = pa_json['ParentID']
        thingspeak['ID'] = pa_json['ID']
        thingspeak2 = {'ID': pa_json['ID']}
        thingspeak2.update(thingspeak)
        sensor['B'] = thingspeak2
    else:
        sensor['DEVICE_LOCATIONTYPE'] = pa_json['DEVICE_LOCATIONTYPE']
        sensor['Lat'] = pa_json['Lat']
        sensor['Lon'] = pa_json['Lon']
        thingspeak2 = {'ID': pa_json['ID']}
        thingspeak2.update(thingspeak)
        sensor['A'] = thingspeak2

    return sensor


def associate_ab_channels(pa_json):
    sensors = {sensor['ID']: sensor for sensor in pa_json if 'ParentID' not in sensor}
    channel_b = [sensor for sensor in pa_json if 'ParentID' in sensor]

    for channel in channel_b:
        sensors[channel['ParentID']]['B'] = channel['B']

    for _, sensor in sensors.items():
        sensor.pop('ID')
    return sensors


def export_json(pa_json):
    with open('thingspeak_keys_test.json', 'w', encoding='utf8') as file:
        json.dump(pa_json, file, indent=4, ensure_ascii=False)


def main():
    with open('src/data/config.yaml') as file:
        config = yaml.full_load(file)
    url = config['purple_json_url']
    purple_air_json = load_json_from_url(url)
    purple_air_json = purple_air_json['results']
    purpleair_ids = [extract_key_info(sensor) for sensor in purple_air_json]
    purpleair_ids = associate_ab_channels(purpleair_ids)
    purpleair_ids = {sensor['Label']: sensor for _, sensor in purpleair_ids.items()}
    for _, entry in purpleair_ids.items():
        entry.pop('Label')
    export_json(purpleair_ids)


if __name__ == '__main__':
    main()
