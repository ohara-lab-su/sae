#!/usr/bin/env python

# Copyright (C) 2014,2015 K.NAKADA
# MIT LICENSE

from setuptools import setup, find_packages
import glob

version = '0.0.1'

script =  glob.glob("bin/*.py")

setup(
        name = 'StructureAnalysisEnvironment',
        packages = find_packages(),
        scripts = script,
#       packages = find_packages('StructureAnalysisEnvironment'),
#       package_dir  = {'':'StructureAnalysisEnvironment'},
        version = version,
        author = 'K.NAKADA',
        author_email = ['kengo.nakada@gmail.com','kengo.nakada@spring8.or.jp'],
        license = 'MIT',
#       platforms = ['linux','OSX'],
)

