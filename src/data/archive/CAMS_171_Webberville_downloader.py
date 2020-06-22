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
site_field.send_keys('171')
site_field.send_keys(Keys.RETURN)


# %% Select parameters

browser.find_element_by_name('clear_all').click()
browser.find_element_by_name('include88101').click()  # PM2.5 local conditions
browser.find_element_by_name('include62101').click()  # Outdoor temperature

# %% Choose time
browser.find_element_by_css_selector('input[value="24hr"]').click()

browser.find_element_by_css_selector('input[value="comma"]').click()  #Choose comma-delimited

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

# %% Partition per parameter
first_column_values = data.iloc[:,0]
start_indices = data.index[first_column_values=='Date'].values
def has_multiple_words(s):
    return len(s.split()) > 1
bool_array_multiword = first_column_values.apply(has_multiple_words)
diff_array_indices = data.index[bool_array_multiword.diff().fillna(False)]
start_indices = diff_array_indices[0::2]
end_indices = diff_array_indices[1::2]
# %%

def flatten(df):
    dates = np.array(df.iloc[1:,0])
    hours = np.array(df.iloc[0,1:])
    timestamp = np.array([date+' '+hour for date in dates for hour in hours])
            
    values = np.array(df.iloc[1:,1:]).flatten()
    
    df2 = pd.DataFrame([timestamp,values]).transpose()

    metadata = first_column_values.iloc[range(df.index[0]-4,df.index[0])]  
    param_info_loc = metadata.index[metadata.str.contains('POC')][0]
    param_info = metadata[param_info_loc]
    # param_info =  param_info[:param_info.find(' (')]
    
    df2.columns = ['Time', param_info]
    return df2

def format_time(df):
    df['Time'] = pd.to_datetime(df.iloc[:,0], format='%m/%d/%Y %H:%M')\
                    .dt.tz_localize('US/Central', ambiguous='infer', nonexistent='shift_forward')\
                    .dt.tz_convert('UTC')\
                    .dt.strftime('%Y-%m-%d %H:%M:%S %Z')
    return df
df_subsets = [data.iloc[start_indices[count]:end_indices[count],:] 
           for count, _ in enumerate(start_indices)]
df_subsets = [flatten(df) for df in df_subsets]

# %%
df_subsets = [format_time(df).set_index('Time') for df in df_subsets]
# %%
df_subsets2 = [df.iloc[:,0] for df in df_subsets]

# %% Parse data
df_complete = pd.DataFrame(df_subsets2).transpose()

# %% Format datetime

# %% Save data
df_complete.to_csv(data.iloc[0,0]+'.csv', index=False)