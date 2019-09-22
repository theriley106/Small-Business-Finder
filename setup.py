#!/usr/bin/env python

from distutils.core import setup

setup(name='sbfinder',
		scripts=['bin/sbfinder'],
      version='2.1',
      description='Using the Yelp Fusion API to Find Local Businesses Without an Online Presense',
      author='Christopher Lambert',
      author_email='lambertcr@outlook.com',
      url='https://github.com/theriley106/SmallBusinessFinder',
      license='MIT',
      packages=['sbfinder'],
      install_requires=['requests', 'bs4', 'lxml', 'urllib3']
     )
