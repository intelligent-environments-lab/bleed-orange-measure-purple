# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 02:14:56 2020

@author: CalvinL2
"""

import urllib.request 
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()

browser.get('https://www.purpleair.com/sensorlist?exclude=true&nwlat=30.291268505204116&selat=30.272526603783206&nwlng=-97.7717631299262&selng=-97.72423886855452')

browser.implicitly_wait(10)
buttons = browser.find_elements_by_css_selector('button[id$="_download_button"]')
print(buttons)

def primary():
    for button in buttons: 
        if 'Primary' in button.text:
            button.click() 
            
def primary_A():
    for button in buttons: 
        if 'Primary (A)' in button.text:
            button.click() 
        
        