# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 11:22:43 2020

@author: CalvinL2
"""

import requests
from bs4 import BeautifulSoup

from src.data.helpers.web_requests import AsyncRequest

def create_form(site, param, year):
    """Creates a form to send in a POST request to TCEQ website


    Parameters
    ----------
    site : int
        Numeric CAMS code for the site (e.g. 171).
    param : int
        5-digit AQS air quality parameter code (e.g. 88101).
    year : int
        4-digit year.

    Returns
    -------
    request : dict
        Can be sent in POST requests.

    """


    request = {'submitted':'1',
               'select_site':f'site|||{site}',
               'user_year':f'{year}',
               'user_param':f'{param}',
               'time_format':'24hr',
               'report_format':'comma'}

    return request

def create_forms(sites):
    """Creates multiple forms for the provided years, sites, and parameters


    Parameters
    ----------
    sites : list
        A list of dictionaries with the cams code, parameters, and years for each site.

    Returns
    -------
    forms : list
        A list of dictionaries that can be sent in POST requests.

    """

    forms = []
    for site in sites:
        params = site['params']
        for param in params:
            years = site['years']
            for year in years:
                cams_code = site['cams']
                forms.append(create_form(cams_code, param, year))
    return forms



def extract_data(htmls):
    """
    Locates and returns the datasets within the html source codes

    Parameters
    ----------
    htmls : list
        A list of html strings received in response to the POST requests.

    Returns
    -------
    list
        A list of strings containing the comma delineated datasets.

    """
    def _extract_data(html):
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find('pre')
        if data is None:
            return None
        else:
            return data.text

    datasets = [_extract_data(html) for html in htmls
                if _extract_data(html) is not None]


    return datasets


def export(datasets, save_location=None):
    '''
    Saves the datasets to csv files

    Parameters
    ----------
    datasets : list
        A list of comma delineated dataset strings.
    save_location : str, optional
        The directory location to save the file. The default is None.

    Returns
    -------
    None.

    '''
    for dataset in datasets:
        filename = dataset.partition("\n")[0]+'.csv'
        if save_location is not None:
            filename = f'{save_location}/{filename}'

        with open(filename, 'w', encoding='utf8') as file:
            file.write(dataset)

def main(site, save_location=None):
    """Entry point for this script


    Parameters
    ----------
    site : list
        A list of dictionaries with the cams code, parameters, and years for each site.
    save_location : str, optional
        The directory location to save the file. The default is None.

    Returns
    -------
    None.

    """

    url = 'https://www.tceq.texas.gov/cgi-bin/compliance/monops/yearly_summary.pl'

    forms = create_forms(site)
    responses = AsyncRequest.post_url(url, forms)

    datasets = extract_data(responses)
    export(datasets, save_location)


if __name__ == '__main__':
    sites = [{'cams':171, 'params':[88101], 'years':[2020, 2019, 2018, 2017, 2016, 2015]},
               {'cams': 1605, 'params': [44201], 'years':[2020, 2019, 2018, 2017, 2016, 2015]},
              {'cams': 1068, 'params':[42601, 42602, 88101], 'years':[2020, 2019, 2018, 2017, 2016, 2015]}]

    main(sites, save_location='data/raw/tceq/test')