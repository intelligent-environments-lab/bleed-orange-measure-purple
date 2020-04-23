# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 15:09:32 2020

@author: CalvinL2

Refer to: https://realpython.com/python-timer/

"""
import time

class Timer:
    def __init__(self, msg=''):
        self.start = None
        self.msg = msg
    
    def __enter__(self):
        self.start = time.perf_counter()
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        end = time.perf_counter()
        print(f'{self.msg}{float(int((end-self.start)*1000))/1000} secs')
