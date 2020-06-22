# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 11:22:43 2020

@author: CalvinL2
"""

import requests
from bs4 import BeautifulSoup

def create_form(site, param, year):
    """Creates a form to send in a POST request to TCEQ website


    Parameters
    ----------
    site : int
        CAMS code for the site.
    param : int
        5-digit AQS air quality parameter code.
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
    """ Creates multiple forms for the provided years, sites, and parameters"""

    forms = []
    for site in sites:
        params = site['params']
        for param in params:
            years = site['years']
            for year in years:
                cams_code = site['cams']
                forms.append(create_form(cams_code, param, year))
    return forms

def extract_data_from_html(html):
    """Extracts the csv data table from the html page source


    Parameters
    ----------
    html : str
        Page source code in its entirety.

    Returns
    -------
    str
        Raw unformatted csv data including the metadata rows.

    """
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find('pre')
    if data is None:
        return None
    else:
        return data.text

def extract_data_from_htmls(htmls):

    datasets = [extract_data_from_html(html) for html in htmls
                if extract_data_from_html(html) is not None]
    return datasets

def export_to_file(data, filename='temp_file.csv'):
    """Produces a csv file that contains the provided data


    Parameters
    ----------
    data : str
        Data string to be written to file.
    filename : str
        Name for the output file, can also include relative path from working directory.

    Returns
    -------
    None.

    """
    with open(filename, 'w', encoding='utf8') as file:
        file.write(data)

def post_requests(url, forms):
    print(f"Posting {len(forms)} requests...")
    responses = [requests.post(url, data=form).text for form in forms]
    print("Posting complete")
    return responses


def main(site, param=None, years=None, save_location=None):
    """ Entry point for the program """
    request_url = 'https://www.tceq.texas.gov/cgi-bin/compliance/monops/yearly_summary.pl'

    # request = create_form(site, param, years)
    forms = create_forms(site)
    responses = post_requests(request_url, forms)
    datasets = extract_data_from_htmls(responses)

    for dataset in datasets:
        filename = dataset.partition("\n")[0]+'.csv'
        if save_location is not None:
            filename = f'{save_location}/{filename}'
        export_to_file(dataset, filename)
    print()
    # response = requests.post(request_url, data=request)
    # data = extract_data_from_html(response.text)

if __name__ == '__main__':

    sites = [{'cams':171, 'params':[88101], 'years':[2020, 2019, 2018, 2017, 2016]},
               {'cams': 1605, 'params': [44201], 'years':[2020, 2019, 2018, 2017, 2016]},
              {'cams': 1068, 'params':[42601, 42602, 88101], 'years':[2020, 2019, 2018, 2017, 2016]}]
    main(sites, save_location='data/raw/tceq')