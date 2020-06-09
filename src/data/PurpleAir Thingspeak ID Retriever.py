# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 15:40:39 2020

@author: CalvinL2
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import yaml

def load_json_from_url(url):
    html = urlopen(url).read()
    return json.loads(html)
    

def main():
    purple_air_json = load_json_from_url(config['purple_json_url'])
    
if __name__=='__main__':
    with open('config.yaml') as file:
        config = yaml.full_load(file)
    main()