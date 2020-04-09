# Bleed Orange Measure Purple
The Bleed Orange Measure Project is aimed to learn more about the particulate matter sources, fate, and transport across UT's campus using a low-cost sensor network.

## Purple Air Sensors
[Purple Air](https://www2.purpleair.com) is a company that provides low-cost particulate matter sensors for indoor and outdoor applications. The company uses sensors developed by [Plantower](http://plantower.com/en/) and provides a [map](https://www.purpleair.com/map?mylocation) for real-time viewing of data gathered by publicly-registered sensors. Data are available to download from any publicly-registered device. 

For this project, we are using the [PA-II](https://www2.purpleair.com/products/purpleair-pa-ii) outdoor sensors to gather particulate matter, temperature, and relative humidty data on campus.

![pa-ii](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fs.w-x.co%2Fwu%2Fpurpleair-device2x.jpeg&f=1&nofb=1)

## Sensor Network
We currently have 16 sensors on the University of Texas at Austin's campus. These sensors are provided with constant power from the emergency help poles they are installed on and are connected to UT's IoT network.

![sensor locations](https://github.com/intelligent-environments-lab/bleed-orange-measure-purple/blob/master/images/sensor_locations.png)

## Python Script Description
**main_comparison_runner.py**: Run this file to compare PurpleAir and APS for test 3  
**common_parent_datafile.py**: Superclass of other datafile scripts  
**..datafile.py**: Defines objects with functions and variables for different sensors, used in 'runner' scripts  
  
**pa_covid_runner.py**(New): Looks at data for all 16 of UT's PurpleAir sensors for the time period from Mar 1 - Apr 8, and creates a     scatter plot of hourly averages. This code is not optimized and may take one or two minutes to execute.
  
**multi_pa_runner.py**: Used to test pa_datafile.py  
**visualize_data.py**: for reference only/deprecated  
