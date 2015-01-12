#!/usr/bin/env python

PROJECT = 'coldframe'
VERSION = '0.1'

from setuptools import setup, find_packages


long_description = ''

setup(
    name=PROJECT,
    version=VERSION,
    description='flask webapp for monitoring cold frame temperature',
    long_description=long_description,
    author='Kyle Marsh',
    author_email='kyle@kmarsh.net',
    url='...',
    download_url='...',
    scripts=[],
    provides=[],
    install_requires=['flask>=0.10.1', 'flask-restful', 'flask-influxdb', 'requests'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    )
