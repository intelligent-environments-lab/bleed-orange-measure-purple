# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 11:22:43 2020

@author: CalvinL2
"""

import requests
from bs4 import BeautifulSoup

def create_form(cams_site, year, param):
    """ Creates a form to send in a POST request to TCEQ website"""
    
    request = {'submitted':'1',
               'select_site':f'site|||{cams_site}',
               'user_year':f'{year}',
               'user_param':f'{param}',
               'time_format':'24hr',
               'report_format':'comma'}
    
    return request

def create_forms(years, sites):
    """ Creates multiple forms for the provided years, sites, and parameters"""
    forms = []
    for year in years:
        for _, site in sites.items():
            for param in site['params']:
                forms.append(create_form(site['cams'], year, param))
    return forms

def extract_data_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find('pre')
    return data.text

def export_to_file(data, filename):
    """ Writes data string to file """
    with open(filename, 'w', encoding='utf8') as file:
        file.write(data)
        
def main():
    """ Entry point for the program """
    request_url = 'https://www.tceq.texas.gov/cgi-bin/compliance/monops/yearly_summary.pl'
    years = [2020, 2019, 2018, 2017, 2016]
    sites = {'Webberville':{'cams':171,
                            'params':[88101]},
             'Edwards':{'cams': 1605,
                        'params': [44201]},
             'Interstate':{'cams': 1068,
                           'params':[42601, 42602, 88101]}
             }
    request = create_form('0171', '2020', '88101')
    res = create_forms(years, sites)
    response = requests.post(request_url, data=request)
    data = extract_data_from_html(response.text)
    print(response.text)
    
if __name__ == '__main__':
    main()