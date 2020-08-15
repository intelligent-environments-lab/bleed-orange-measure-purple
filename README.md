# Bleed Orange Measure Purple

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub top language](https://img.shields.io/github/languages/top/intelligent-environments-lab/bleed-orange-measure-purple)
![Test Code](https://github.com/intelligent-environments-lab/bleed-orange-measure-purple/workflows/Test%20Code/badge.svg)
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
