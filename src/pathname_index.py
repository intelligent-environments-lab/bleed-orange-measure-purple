# -*- coding: utf-8 -*-

index = {
    'purpleair': {
        'raw':'data/raw/purpleair',
        'rawB':'data/raw/purpleair',
        'interim':'data/interim/PurpleAir_realtime.parquet',
        'interimB':'data/interim/PurpleAir_B_realtime.parquet',
        'processed_daily':'data/processed/PurpleAir_daily.parquet'
        }
    }


pa_index = index['purpleair']
pa_raw = pa_index['raw']
pa_rawB = pa_index['rawB']
pa_int_real = pa_index['interim']
pa_intB_real = pa_index['interimB']
pa_pro_daily = pa_index['processed_daily']