# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 22:02:26 2020

@author: Calvin J Lin
"""
def test_build():
    # import src.data.purpleair_data_retriever as pdr

    # pdr.main(start='2020-1-1', end='2020-9-15', channel='primaryA', save_location='data/raw/purpleair')
    # pdr.main(start='2020-1-1', end='2020-9-15', channel='primaryB', save_location='data/raw/purpleair/B')
    
    import src.pathname_index as pni
    import src.data.purpleair_raw_cleaner as pc

    pc.main(path=pni.pa_raw, save_location=pni.pa_int_real)
    pc.main(path=pni.pa_rawB, save_location=pni.pa_intB_real)
    
    import src.data.purpleair_outlier_remover as por
    
    por.main(A_file=pni.pa_int_real,
             B_file=pni.pa_intB_real,
             save_file=pni.pa_pro_daily,
             freq='D')

