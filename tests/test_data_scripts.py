# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 01:19:43 2020

@author: CalvinL2
"""

#import yaml

import src.data.purpleair_data_retriever
import src.data.purpleair_raw_cleaner
import src.data.thingspeak_handler
#from src.data.tceq_dataset_generator import main as main4
#from src.data.tceq_interim_processor import main as main5
#from src.data.tceq_raw_cleaner import main as main6


#def test_pa_data_gen():
 #   main1()


def test_purpleair_data_retriever():
    src.data.purpleair_data_retriever.main()


def test_thingspeak_handler():
    src.data.thingspeak_handler.main()

def test_purpleair_raw_cleaner():
    src.data.purpleair_raw_cleaner.main()
    
#def test_tceq_data_gen():
 #   sites = [
  #      {'cams': 171, 'params': [88101], 'years': [2020, 2019]},
   #     {'cams': 1605, 'params': [44201], 'years': [2020]},
    #    {'cams': 1068, 'params': [42601, 42602], 'years': [2020]},
    #]

    #main4(sites, save_location='tests/output')


#def test_tceq_interim_processor():
#    main5()


#def test_tceq_raw_clean():
#    main6('data/raw/tceq', save_location='tests/output')
