# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 09:30:11 2020

@author: CalvinL2
"""

# %% Imports
import os

import pandas as pd

from sensors.common_parent_datafile import CommonFile
from util.importer import Util

# %%
class PAfile(CommonFile):
    """Stores and manipulates data from one file generated by a PurpleAir sensor"""

    def __init__(self, filename):
        # BUG Need to discriminate between primary and secondary files
        data = pd.read_csv(filename, index_col=False)

        self.filename = filename[filename.rfind('/')+1:]

        def _parse_filename(filename):
            filename = filename[filename.rfind('\\')+1:]
            filename = filename.replace(' B', '[B]')
            filename = filename.replace('(', '').replace(')', '')
            filename = filename.replace('.csv', '')

            filename = filename.split(' ')

            self.sensorname = filename[0]
            self.sensor_environment = filename[1]
            self.latitude = float(filename[2])
            self.longitude = float(filename[3])

        _parse_filename(self.filename)

        timestamps = CommonFile.to_datetime(data['created_at'], '%Y-%m-%d %H:%M:%S %Z')
        data.insert(0, 'time', timestamps)
        data = data.set_index('time')

        super().__init__(data)

    @property
    def pm25(self):
        """Returns PM 2.5 values in a panda series."""
        return self['PM2.5_ATM_ug/m3']

    @property
    def temperature(self):
        """Returns temperature values in a panda series."""
        return self['Temperature_F']

    @property
    def humidity(self):
        """Returns temperature values in a panda series."""
        return self['Humidity_%']


class PAfiles():
    """An object to import and store multiple PAfile objects"""
    def __init__(self, file_dir):
        files = Util.import_with_caching(PAfiles.import_pa_files, os.getcwd(), file_dir)
        self.files = {file.sensorname:file for file in files}

    def __getitem__(self, key):
        return self.files[key]

    def __iter__(self):
        return (file for file in self.files.values())
    
    def __str__(self):
        return str(self.files)
    
    @staticmethod
    def import_pa_files(cwd, file_dir):
        """Returns a list of PAfile for every PurpleAir csv in the specified directory"""
        return [PAfile(file_dir+'\\'+filename)
                for filename in os.listdir(cwd+'\\'+file_dir)
                if filename.endswith(".csv") and filename.startswith("PA")]
