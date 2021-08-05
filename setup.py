from setuptools import setup, version, find_packages

setup(
    name='bomp',
    version='0.1.0',
    author='Calvin J Lin',
    author_email='calvin.lin@utexas.edu',
    packages=['bomp'],
    entry_points = {'console_scripts':['bomp=bomp.__main__:main']},
    description='Package that can download data from UT\'s PurpleAir netork'
)