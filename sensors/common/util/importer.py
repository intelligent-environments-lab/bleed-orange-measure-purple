# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 13:49:29 2020

@author: CalvinL2
"""
import os
from os import path
import pickle as pkl
import hashlib
import functools

class Util():
    
    #https://realpython.com/primer-on-python-decorators/#decorators-with-arguments
    @staticmethod
    def caching(_func=None, cachefile='cachefile.cache'):
        def wrap(import_func):
            @functools.wraps(import_func)
            def wrapper(*args, **kwargs):
                def import_data():
                    print('Importing data from source...', flush=True, end="")
                    output = import_func(*args, **kwargs)
                    print('Done', flush=True)
                    pkl.dump(output, open(cachefile, 'wb'))
                    return output
                # if cachefile is None:
                #     func_name = import_func.__name__
                #     hash_str  = func_name + [arg for arg in args if arg != os.getcwd()][0]
                #     hash_str = hashlib.md5(hash_str.encode('utf-8')).hexdigest()[:8]
                #     cachefile = '.' + hash_str + f'_{func_name}.cache'
                if not path.exists(cachefile):
                    output = import_data()
                else:
                    print(f'Loading data from \'{cachefile}\' ... ', flush=True, end="")
                    try:
                        output = pkl.load(open(cachefile, 'rb'))
                    except:
                        print('Error while opening cache file...')
                        import_data()
                    else:
                        print('Done', flush=True)
                return output
            return wrapper
        if _func is None:
            return wrap         #If arguments passed to decorator
        else: 
            return wrap(_func)  #If arguments not passed to decorator


    
    