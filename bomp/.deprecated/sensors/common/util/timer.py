# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 15:09:32 2020

@author: CalvinL2

Refer to: https://realpython.com/python-timer/

"""
import time
import functools


class Timer:
    """A timer class to be used with the 'with' statement"""

    def __init__(self, msg=''):
        self.start = None
        self.msg = msg

    def __enter__(self):
        self.start = time.perf_counter()

    def __exit__(self, exc_type, exc_value, exc_tb):
        end = time.perf_counter()
        print(f'{self.msg}{float(int((end-self.start)*1000))/1000} secs')


def timeit(func):
    """Timer decorator: put @timeit before any function to time it in seconds"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        value = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start
        print(f'Elapsed time:{elapsed:0.4f} seconds')
        return value

    return wrapper
