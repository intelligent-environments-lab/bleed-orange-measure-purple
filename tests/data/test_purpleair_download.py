# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 03:19:22 2020

@author: CalvinL2
"""

import os
import unittest

import sys
sys.path.append('../..')

from src.data.purple_data_download import *

class TestPurpleData(unittest.TestCase):
    def test_load_keys(self):
        self.assertGreater(len(main()), 0)
        
if __name__ == '__main__':
    unittest.main()