# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 15:09:32 2020

@author: CalvinL2

Refer to: https://realpython.com/python-timer/

"""
import time

class Timer:
    def __init__(self):
        self.start = None
    
    def __enter__(self):
        self.start = time.perf_counter()
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        end = time.perf_counter()
        print(end-self.start)
