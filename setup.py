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
__script__ = glob.glob("StructureAnalysisEnvironment/bin/*.py")

__long_description__ = "Structure Analysis Environment"

# if os.path.exists('README.md'):
#    long_description = open('README.md').read()

# package_src_dir = "StructureAnalysisEnvironment"
# files = glob.glob(package_src_dir + "/*.list")
# print("*****************************************")
# print(files)
# print("*****************************************")

# パッケージデータ
# .list ファイルをデータファイルとして同梱
__package_data__ = {"StructureAnalysisEnvironment": ["*.list"]}

# パッケージ指定
__packages__ = find_packages("src", exclude=["StructureAnalysisEnvironment.bin"])

setup(
    name="StructureAnalysisEnvironment",
    # packages=find_packages(),
    packages=__packages__,
    #       package_dir  = {'':'StructureAnalysisEnvironment'},
    #       include_package_data=True,
    #       package_data = { '': ['LICENSE.txt', 'README.md']},
    package_data=__package_data__,
    package_dir={"": "src"},
    # data_files=[(package_src_dir, files)],
    scripts=__script__,
    version=__version__,
    description="Structure Analysis Environment",
    long_description=__long_description__,
    author="K.NAKADA",
    #       author_email = ['kengo.nakada@gmail.com','kengo.nakada@spring8.or.jp'],
    #       author_email = 'kengo.nakada@gmail.com',
    # author_email='kengo.nakada@spring8.or.jp',
    author_email="kengo.nakada@gmail.com",
    license="Apache2.0",
    install_requires=["numpy", "matplotlib"],
    #       platforms = ['linux','OSX','Window'],
    #       classifiers = [
    #           'Programming Language :: Python :: 2.7',
    #           'Intended Audience :: Science/Research',
    #           'License :: OSI Approved :: MIT License'
    #           ]
)
