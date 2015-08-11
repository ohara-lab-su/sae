#!/usr/bin/env python

# Copyright (C) 2014,2015 K.NAKADA
# MIT LICENSE
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014,2015 Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"


from setuptools import setup, find_packages
import glob

version = __version__

script =  glob.glob("bin/*.py")

setup(
        name = 'StructureAnalysisEnvironment',
        packages = find_packages(),
        scripts = script,
#       packages = find_packages('StructureAnalysisEnvironment'),
#       package_dir  = {'':'StructureAnalysisEnvironment'},
        version = version,
        author = 'K.NAKADA',
#       author_email = ['kengo.nakada@gmail.com','kengo.nakada@spring8.or.jp'],
        author_email = 'kengo.nakada@gmail.com',
        license = 'MIT',
#       platforms = ['linux','OSX','Window'],
)

