# Bleed Orange Measure Purple

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub top language](https://img.shields.io/github/languages/top/intelligent-environments-lab/bleed-orange-measure-purple)
[![Test Code](https://github.com/intelligent-environments-lab/bleed-orange-measure-purple/workflows/Test%20Code/badge.svg)](https://github.com/intelligent-environments-lab/bleed-orange-measure-purple/actions?query=workflow%3A%22Test+Code%22)
[![codecov](https://codecov.io/gh/intelligent-environments-lab/bleed-orange-measure-purple/branch/dev/graph/badge.svg)](https://codecov.io/gh/intelligent-environments-lab/bleed-orange-measure-purple)



Bleed Orange Measure Purple project explores the potential uses and benefits of the PurpleAir air quality sensors located on the UT Austin campus through data processing, analysis, and visualization. This repo features a data pipeline with various scripts that handle everything from downloading to visualizing the data. Data from TCEQ sensors is also included in this project to provide regulatory grade reference data. For a more detailed explaination of this project, please refer to the [wiki](https://github.com/intelligent-environments-lab/bleed-orange-measure-purple/wiki).

## Prerequisites


Currently, the plotting library used for the project is Plotly. Their setup instructions can be found [here](https://plotly.com/python/getting-started/). Depending on the ide or export format, different external dependencies may be required (e.g. node for Jupyter, plotly-orca for static image export).
### Plotly

Plotly is plotting engine used in this project. It can be installed via pip/conda and is included in the requirements.txt for this repository. However, there may be additional dependencies that need be installed separately. For instance, node might be required for JupyterLab support.

### Spyder (Anaconda distribution)

This repository is intended to be used with the Spyder IDE. The main reason for this is that the project feature of Spyder makes it easy to add the repo's root directory to sys.path and also set it as the current working directory. If you choose to you another IDE such as VSCode, you will need to either figure how to set these two things in that IDE or correct all the import/file references to work for your IDE.


## Installation
First, clone the repository.
```
git clone https://github.com/intelligent-environments-lab/bleed-orange-measure-purple.git
```

## Components

### src.data.*
**[async_requests.py](src/data/async_request.py):** importable module that allows for [asynchronous](https://realpython.com/async-io-python#async-io-explained) [HTTP GET/POST requests](https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f#6f75) to be made

**[purpleair_data_retriever.py](src/data/purpleair_data_retriever.py):** Runner script, downloads raw realtime PurpleAir data from ThingSpeak and saves it to a csv file with the same headers and metadata as those from [PurpleAir's own website](https://www.purpleair.com/sensorlist?exclude=true&nwlat=30.291268505204116&selat=30.272526603783206&nwlng=-97.7717631299262&selng=-97.72423886855452), uses async_requests.py and thingspeak_keys.json.

**[purpleair_raw_cleaner.py](src/data/purpleair_raw_cleaner.py):** Runner script, serializes raw PurpleAir csv files into parquet files, removes outliers with IQR, merges multiple dataframes into one, converts string dates into datetime objects

**[purpleair_interim_processor.py](src/data/purpleair_interim_processor.py):** Runner script, a mostly trivial conversion of purpleair parquet files to feather files for supposed performance benefits. Will most likely be removed in the future due to preference for a single dataframe with multiindex.

**[tceq_data_retriever.py](src/data/tceq_data_retriever.py):** Runner script, downloads [yearly summary air quality data](https://www.tceq.texas.gov/cgi-bin/compliance/monops/yearly_summary.pl) from the TCEQ website and saves it to a csv file without modification, uses async_requests.py

**[tceq_raw_cleaner.py](src/data/tceq_raw_cleaner.py):** Runner script, serializes raw TCEQ csv files into parquet file, changes data format from matrix to columns, replaces string values with nan, converts date strings to datetime objects, moves negative values to zero, merges dataframes that have the same site and parameter

**[thingspeak_handler.py](src/data/thingspeak_handler.py):** Downloads and saves the [Thingspeak channel and api keys](https://www.purpleair.com/json?exclude=true&key=null&show=null&nwlat=30.291268505204116&selat=30.272526603783206&nwlng=-97.7717631299262&selng=-97.72423886855452) needed for downloading PurpleAir data to a file named ```thingspeak_keys.json```. Relevant sensor metadata is also retained.
