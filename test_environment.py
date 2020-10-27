# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 22:02:26 2020

@author: Calvin J Lin
"""
def test_build():
    # import src.data.purpleair_data_retriever as pdr

    # pdr.main(start='2020-1-1', end='2020-9-15', channel='primaryA', save_location='data/raw/purpleair')
    # pdr.main(start='2020-1-1', end='2020-9-15', channel='primaryB', save_location='data/raw/purpleair/B')
    
    import src.data.purpleair_raw_cleaner as pc

    pc.main(path='data/raw/purpleair', save_location='data/interim/PurpleAir_realtime.parquet')
    pc.main(path='data/raw/purpleair/B', save_location='data/interim/PurpleAir_B_realtime.parquet')
    
    import src.data.purpleair_outlier_remover as por
    
    por.main(A_file='data/interim/PurpleAir_realtime.parquet',
             B_file='data/interim/PurpleAir_B_realtime.parquet',
             save_file='data/processed/PurpleAir_daily.parquet',
             freq='D')

