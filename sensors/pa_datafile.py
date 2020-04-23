# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 09:30:11 2020

@author: CalvinL2
"""

# %% Imports
import os

from datetime import timezone
import pandas as pd

from sensors.common_parent_datafile import CommonFile
from util.importer import Util

# %%
class PAfile(CommonFile):
    """Stores and manipulates data from one file generated by a PurpleAir sensor"""
    
    def __init__(self, filename):
        # BUG Need to discriminate between primary and secondary files
        data = pd.read_csv(filename, index_col=False)

        filename = filename[filename.rfind('/')+1:]

        self._parse_filename(filename)

        # Converts string to datetime object
        timestamps = CommonFile.str2date(data.loc[:, 'created_at'],
                                         '%Y-%m-%d %H:%M:%S %Z',
                                         tzone=timezone.utc)

        # Creates datetime column and makes it the index for the df,
            #use df.index.values or df.index.name to access
        data.insert(0, 'time', timestamps)
        data = data.set_index('time')

        # Defining instance variables for the object
        self.filename = filename
        super().__init__(data)

    def _parse_filename(self, filename):
        # Some adjustments to format to make parsing easier
        filename = filename[filename.rfind('\\')+1:]
        filename = filename.replace(' B', '[B]')
        filename = filename.replace('(', '').replace(')', '')
        filename = filename.replace('.csv', '')

        filename = filename.split(' ')
        # Uses iterate function to extract data from the filename

        self.sensorname = filename[0]
        self.sensor_environment = filename[1]
        self.latitude = float(filename[2])
        self.longitude = float(filename[3])

    @staticmethod
    def import_pa_files(cwd, file_dir):
        """Returns a list of PAfile for every PurpleAir csv in the specified directory"""
        return [PAfile(file_dir+'\\'+filename)
                for filename in os.listdir(cwd+'\\'+file_dir)
                if filename.endswith(".csv") and filename.startswith("PA")]

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
    def __init__(self, file_dir):
        files = Util.import_with_caching(PAfile.import_pa_files, os.getcwd(), file_dir)
        self.files = {file.sensorname:file for file in files}

    def __getitem__(self, key):
        return self.files[key]

    def __iter__(self):
        return (file for file in self.files.values())
