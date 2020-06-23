#!/usr/bin/env python

# Copyright (C) 2014,2015 K.NAKADA

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@spring8.or.jp"
__copyright__ = "Copyright 2014-2018 Kengo NAKADA"
__license__ = "Apache2"
__status__ = "alpha"

# __version__    = "0.0.1"
# __email__      = "kengo.nakada@gmail.com"
# __license__    = "MIT"

from setuptools import setup, find_packages
import glob

# version = __version__
from StructureAnalysisEnvironment.version import __version__

script = glob.glob("StructureAnalysisEnvironment/bin/*.py")

long_description = 'Structure Analysis Environment'
import os

if os.path.exists('README.md'):
    long_description = open('README.md').read()

package_src_dir = 'StructureAnalysisEnvironment'
files = glob.glob(package_src_dir + '/*.list')
print('*****************************************')
print(files)
print('*****************************************')
#packages = find_packages()
packages = [
    package_src_dir,
    package_src_dir + '.Method',
    package_src_dir + '.gui',
    package_src_dir + '.io',
    package_src_dir + '.io',
    package_src_dir + '.athena',
    package_src_dir + '.fdm',
    package_src_dir + '.hilapw',
    package_src_dir + '.lob',
    package_src_dir + '.mx',
    package_src_dir + '.pf',
    package_src_dir + '.pwscf',
    package_src_dir + '.rmc',
    package_src_dir + '.vasp',
    package_src_dir + '.wien2k'
]
print(packages)
print('*****************************************')

setup(
    name='StructureAnalysisEnvironment',
    # packages=find_packages(),
    packages=packages,
    #       package_dir  = {'':'StructureAnalysisEnvironment'},
    #       include_package_data=True,
    #       package_data = { '': ['LICENSE.txt', 'README.md']},
    data_files=[
        (package_src_dir, files)
    ],
    scripts=script,
    version=__version__,
    description='Structure Analysis Environment',
    long_description=long_description,
    author='K.NAKADA',
    #       author_email = ['kengo.nakada@gmail.com','kengo.nakada@spring8.or.jp'],
    #       author_email = 'kengo.nakada@gmail.com',
    author_email='kengo.nakada@spring8.or.jp',
    license='Apache2.0',
    install_requires=['numpy', 'matplotlib'],
    #       platforms = ['linux','OSX','Window'],
    #       classifiers = [
    #           'Programming Language :: Python :: 2.7',
    #           'Intended Audience :: Science/Research',
    #           'License :: OSI Approved :: MIT License'
    #           ]
)
