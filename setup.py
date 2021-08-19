from setuptools import setup, version, find_packages

setup(
    name='iel-bomp',
    version='0.2.0',
    author='Calvin J Lin',
    author_email='calvin.lin@utexas.edu',
    packages=find_packages(),
    package_data={'bomp':['data/thingspeak_keys.json']},
    entry_points = {'console_scripts':['bomp=bomp.__main__:main']},
    description='Package that can download data from UT\'s PurpleAir netork'
)