"""Setup program for hexprint CLI tool
"""
from setuptools import setup

setup(
    name='Hexprint',
    version='1.0',
    license='MIT License',
    author='Doug Mahugh',
    py_modules=['hexprint'],
    install_requires=[
        'Click', 'Colorama',
    ],
    entry_points='''
        [console_scripts]
        hexprint=hexprint:cli
    '''
)