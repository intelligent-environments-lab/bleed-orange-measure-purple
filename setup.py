from setuptools import setup, version, find_packages

setup(
    name='bomp',
    version='0.1.0',
    author='Calvin J Lin',
    author_email='calvin.lin@utexas.edu',
    packages=['src'],
    entry_points = {'console_scripts':['bomp=src.__main__:main']},
    description='Package that can download data from UT\'s PurpleAir netork'
)