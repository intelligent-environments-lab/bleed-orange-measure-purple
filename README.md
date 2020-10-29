# Bleed Orange Measure Purple

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub top language](https://img.shields.io/github/languages/top/intelligent-environments-lab/bleed-orange-measure-purple)
[![Test Code](https://github.com/intelligent-environments-lab/bleed-orange-measure-purple/workflows/Build/badge.svg)](https://github.com/intelligent-environments-lab/bleed-orange-measure-purple/actions?query=workflow%3A%22Build%22)
[![codecov](https://codecov.io/gh/intelligent-environments-lab/bleed-orange-measure-purple/branch/dev/graph/badge.svg)](https://codecov.io/gh/intelligent-environments-lab/bleed-orange-measure-purple)

Bleed Orange Measure Purple project explores the potential uses and benefits of the PurpleAir air quality sensors located on the UT Austin campus through data processing, analysis, and visualization. This repo features a data pipeline with various scripts that handle everything from downloading to visualizing the data. Data from TCEQ sensors is also included in this project to provide regulatory grade reference data. For a more detailed explaination of this project, please refer to the [wiki](https://github.com/intelligent-environments-lab/bleed-orange-measure-purple/wiki).

## Prerequisites

<!--
### Plotly

Plotly is plotting engine used in this project. Their setup instructions can be found [here](https://plotly.com/python/getting-started/). Plotly can be installed via pip/conda and is included in the ```environment.yml``` file for this repository. However, there may be additional dependencies that need be installed separately. For instance, node might be required for JupyterLab support.
-->
### Anaconda (Python Distribution)

[Anaconda](https://www.anaconda.com/products/individual) is highly recommended for use with this repo. It comes bundled with the Spyder and Jupyter IDEs which are used to run the Python scripts and IPython notebooks in this repo, and it also includes the conda package manager which makes it easier to install the necessary packages and dependencies for this repo.

## Installation
First, clone the repository by downloading the repo as zip, using [GitHub Desktop](https://desktop.github.com/) (green button at top of this page) or the following git command:
```
git clone https://github.com/intelligent-environments-lab/bleed-orange-measure-purple.git
```
Note the folder location where the repo was copied to. You will need it for the next step.

To setup the conda environment and install package dependencies, open Anaconda Prompt. Then, change the current folder or directory of the prompt to the root folder/directory of this repo (```(base) C:\\...some user path...\bleed-orange-measure-purple>```) so that the command below can find the ```environment.yml``` file. Then, run the following command using the ```environment.yml``` file to install the conda environment and associated packages(may take a few minutes):
```
conda env create -f environment.yml
```
After the command completes, you should have a conda environment named ```bomp``` that you can activate with the command ```activate bomp```.
<!--
Launch Spyder and create a new Spyder project in the root directory of the repository. 

Check that the repository's root directory is in both ```os.getcwd()``` and ```sys.path``` in order to avoid import or file not found errors.

Also when you hit run on any of the scripts below, you wil need to make sure that the configuration is set to run in the current working directory.
-->

## Usage
To start the Jupyter IDE, open Anaconda Prompt, and type the following command:
```
activate bomp && jupyter lab
```
Jupyter Lab should start in your browser, and then you can start using it. The ```main.ipynb``` is a good starting point to run the program since it downloads PurpleAir data in csv format. 

Spyder can be used to view and run the ```.py``` files individually, but the setup is trickier (involves changing the python interpreter to ```...anaconda3\envs\bomp\python.exe```, and the file must be run from the top-level ```bleed-orange-measure-purple``` directory). For non-technical users, it is easier just to import the ```.py``` scripts into ```main.ipynb``` and run it using Jupyter.

## Components

### src.data.*
**[async_requests.py](src/data/async_requests.py):** importable module that allows for [asynchronous](https://realpython.com/async-io-python#async-io-explained) [HTTP GET/POST requests](https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f#6f75) to be made, significantly reduces time needed to download the data for this project

**[purpleair_data_retriever.py](src/data/purpleair_data_retriever.py):** Downloads raw realtime PurpleAir data from ThingSpeak and saves it to a csv file with the same headers and metadata as those from [PurpleAir's own website](https://www.purpleair.com/sensorlist?exclude=true&nwlat=30.291268505204116&selat=30.272526603783206&nwlng=-97.7717631299262&selng=-97.72423886855452), uses async_requests.py and thingspeak_keys.json.

**[purpleair_raw_cleaner.py](src/data/purpleair_raw_cleaner.py):** Serializes raw PurpleAir csv files into parquet files, merges multiple dataframes into one, converts string dates into datetime objects

**[purpleair_outlier_remover.py](src/data/purpleair_outlier_remover.py):** Compares A and B channel data to identify outliers which exceed a difference of 5 ug/m3 or a percent error of 16%

**[tceq_data_retriever.py](src/data/tceq_data_retriever.py):** Runner script, downloads [yearly summary air quality data](https://www.tceq.texas.gov/cgi-bin/compliance/monops/yearly_summary.pl) from the TCEQ website and saves it to a csv file without modification, uses async_requests.py

**[tceq_raw_cleaner.py](src/data/tceq_raw_cleaner.py):** Runner script, serializes raw TCEQ csv files into parquet file, changes data format from matrix to columns, replaces string values with nan, converts date strings to datetime objects, moves negative values to zero, merges dataframes that have the same site and parameter

**[tceq_interim_processor](src/data/tceq_interim_processor.py):** Runner script, another somewhat pointless parquet to feather converter

**[thingspeak_handler.py](src/data/thingspeak_handler.py):** Runner script, downloads and saves the [Thingspeak channel and api keys](https://www.purpleair.com/json?exclude=true&key=null&show=null&nwlat=30.291268505204116&selat=30.272526603783206&nwlng=-97.7717631299262&selng=-97.72423886855452) needed for downloading PurpleAir data to a file named ```thingspeak_keys.json```. Relevant sensor metadata is also retained.
