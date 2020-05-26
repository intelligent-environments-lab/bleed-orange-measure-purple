# -*- coding: utf-8 -*-
"""
Created on Sat May 16 18:34:12 2020

@author: CalvinL2
"""

# The shortcut for running code cells is Ctrl-Enter

# %% Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd
import numpy as np
# %% User parameters
month = 'May'

# os.popen('taskkill /F /IM chromedriver.exe /T')
# %% Start browser and navigate to TCEQ
browser = webdriver.Chrome()
actions = ActionChains(browser)

# %% Navigate
browser.get('https://www.tceq.texas.gov/cgi-bin/compliance/monops/monthly_summary.pl')
# %% Enter site
site_field =  browser.find_element_by_id('find_site_text')
site_field.send_keys('1068')
site_field.send_keys(Keys.RETURN)


# %% Select parameters

browser.find_element_by_name('clear_all').click()
browser.find_element_by_name('include88101').click()  # PM2.5 local conditions
browser.find_element_by_name('include42603').click()  # Oxides of nitrogen
browser.find_element_by_name('include42602').click()  # Nitrogen dioxide
browser.find_element_by_name('include42601').click()  # Nitrogen oxide
browser.find_element_by_name('include62101').click()  # Outdoor temperature
# %% Choose time
browser.find_element_by_css_selector('input[value="24hr"]').click()
browser.find_element_by_css_selector('input[value="comma"]').click()

# %% Deselect optional statistics
stats = browser.find_elements_by_css_selector('input[name^="print_"')
for stat in stats:
    stat.click()

# %% Select month and year
month_field = Select(browser.find_element_by_name('user_month'))
year_field = Select(browser.find_element_by_name('user_year'))

actions.move_to_element(browser.find_element_by_name('user_month')).perform()

month_field.select_by_visible_text(month)
# input('Verify that the correct month is selected, then press enter in the console to continue:')

# %% Generate report
browser.find_element_by_css_selector('input[value="Generate Report"]').click()

# %% Get data
data = browser.find_element_by_css_selector('pre').text
data = pd.DataFrame([line.split(',') for line in data.split('\n')])

# %% Parse data
dates = np.array(data.iloc[6:,0])
hours = np.array(data.iloc[5,1:])
timestamp = np.array([date+' '+hour for date in dates for hour in hours])
        
values = np.array(data.iloc[6:,1:]).flatten()

data2 = pd.DataFrame([timestamp,values]).transpose()
data2.columns = ['Time','PM2.5']

# %% Format datetime
data2['Time'] = pd.to_datetime(data2.iloc[:,0], format='%m/%d/%Y %H:%M')\
                    .dt.tz_localize('US/Central', ambiguous='infer', nonexistent='shift_forward')\
                    .dt.tz_convert('UTC')\
                    .dt.strftime('%Y-%m-%d %H:%M:%S %Z')
# %% Save data
data2.to_csv(data.iloc[0,0]+'.csv', index=False)