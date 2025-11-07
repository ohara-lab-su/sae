#!/usr/bin/env python

# Copyright (C) 2014,2015 K.NAKADA

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
# __email__ = "kengo.nakada@spring8.or.jp"
__copyright__ = "Copyright 2014-2018 Kengo NAKADA"
__license__ = "Apache2"
__status__ = "alpha"

# __version__    = "0.0.1"
# __license__    = "MIT"

from setuptools import setup, find_packages
import glob
import re


# version = __version__
# from StructureAnalysisEnvironment import __version__
def read_version_from_toml() -> str:
    with open("pyproject.toml", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("version"):
                m = re.search(r'version\s*=\s*["\']([^"\']+)["\']', line)
                if m:
                    return m.group(1)
    raise RuntimeError("version not found in pyproject.toml")


__version__ = read_version_from_toml()

# スクリプト指定
script = glob.glob("StructureAnalysisEnvironment/bin/*.py")

description = "Structure Analysis Environment"
long_description = "Structure Analysis Environment"

# パッケージデータ
# .list ファイルをデータファイルとして同梱
package_data = {"StructureAnalysisEnvironment": ["*.list"]}
package_dir = {"": "src"}

# パッケージ指定
packages = find_packages(
    "src",
    exclude=["StructureAnalysisEnvironment.bin"],
)

setup(
    name="StructureAnalysisEnvironment",
    packages=packages,
    # package_dir  = {'':'StructureAnalysisEnvironment'},
    # include_package_data=True,
    # package_data = { '': ['LICENSE.txt', 'README.md']},
    package_data=package_data,
    package_dir=package_dir,
    # data_files=[(package_src_dir, files)],
    scripts=script,
    version=__version__,
    description=description,
    long_description=long_description,
    author=__author__,
    # author_email = ['kengo.nakada@gmail.com','kengo.nakada@spring8.or.jp'],
    # author_email='kengo.nakada@spring8.or.jp',
    author_email=__email__,
    license=__license__,
    install_requires=[
        "pandas",
        "ase",
        "numpy",
        "matplotlib",
    ],
    #       platforms = ['linux','OSX','Window'],
    #       classifiers = [
    #           'Programming Language :: Python :: 2.7',
    #           'Intended Audience :: Science/Research',
    #           'License :: OSI Approved :: MIT License'
    #           ]
)
