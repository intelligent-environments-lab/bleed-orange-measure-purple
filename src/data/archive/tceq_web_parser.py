# -*- coding: utf-8 -*-
"""
Created on Sat May 23 13:09:11 2020

@author: CalvinL2
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd
import numpy as np


def get_site(browser):
    browser.get(
        'https://www.tceq.texas.gov/cgi-bin/compliance/monops/yearly_summary.pl'
    )
    site_field = browser.find_element_by_id('find_site_text')
    site_field.send_keys('1068')
    site_field.send_keys(Keys.RETURN)


def flatten(df, data):
    dates = np.array(df.iloc[1:, 0])
    hours = np.array(df.iloc[0, 1:])
    timestamp = np.array([date + ' ' + hour for date in dates for hour in hours])

    values = np.array(df.iloc[1:, 1:]).flatten()

    df2 = pd.DataFrame([timestamp, values]).transpose()

    first_column_values = data.iloc[:, 0]

    metadata = first_column_values.iloc[range(df.index[0] - 4, df.index[0])]
    param_info_loc = metadata.index[metadata.str.contains('POC')][0]
    param_info = metadata[param_info_loc]
    # param_info =  param_info[:param_info.find(' (')]

    df2.columns = ['Time', param_info]
    return df2


def format_time(df):
    df['Time'] = (
        pd.to_datetime(df.iloc[:, 0], format='%m/%d/%Y %H:%M')
        .dt.tz_localize(
            'US/Central',
            ambiguous=np.repeat(False, df.shape[0]),
            nonexistent='shift_forward',
        )
        .dt.tz_convert('UTC')
        .dt.strftime('%Y-%m-%d %H:%M:%S %Z')
    )
    return df


def replace_strings(pd_series):
    """ Numbers only please """
    return pd.to_numeric(pd_series, errors='coerce')


# %% Start parsing
def deselect_stats():
    stats = browser.find_elements_by_css_selector('input[name^="print_"')
    for stat in stats:
        stat.click()


def select_format():
    browser.find_element_by_css_selector('input[value="24hr"]').click()
    browser.find_element_by_css_selector('input[value="comma"]').click()


def parse():
    data = browser.find_element_by_css_selector('pre').text
    data = pd.DataFrame([line.split(',') for line in data.split('\n')])

    first_column_values = data.iloc[:, 0]
    start_indices = data.index[first_column_values == 'Date'].values[0]

    d2 = data.iloc[start_indices:, 0:]
    d2 = flatten(d2, data)
    d2 = format_time(d2)

    col_name = d2.columns[1]
    d2[col_name] = replace_strings(d2[col_name])

    # %% Save csv
    d2.to_csv('2020 Camp Mabry RH.csv', index=False)


def main():
    get_site(browser)
    deselect_stats()
    select_format()


if __name__ == '__main__':
    browser = webdriver.Chrome()
    actions = ActionChains(browser)
    main()
