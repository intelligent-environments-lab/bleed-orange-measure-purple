# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 13:49:29 2020

@author: CalvinL2
"""
import os
from os import path
import pickle as pkl
import hashlib

class Util():
    @staticmethod
    def import_with_caching(import_func, *args, cachefile=None, use_cache=True, **kwargs):
        """Imports all PurpleAir files in current directory, uses caching to speed up future runs"""
        def import_data():
            print('Importing data from source...', flush=True, end="")
            output = import_func(*args, **kwargs)
            print('Done', flush=True)
            pkl.dump(output, open(cachefile, 'wb'))
        
        if cachefile is None:
            func_name = import_func.__name__
            hash_str  = func_name + [arg for arg in args if arg != os.getcwd()][0]
            hash_str = hashlib.md5(hash_str.encode('utf-8')).hexdigest()[:8]
            cachefile = '.' + hash_str + f'_{func_name}.cache'
        if not path.exists(cachefile) or not use_cache:
            import_data()
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
    
    
    