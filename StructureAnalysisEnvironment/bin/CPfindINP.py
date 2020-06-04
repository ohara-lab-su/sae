#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# CPfindINP
#
#  指定suffixのファイルがカレントに一つの時はそのファイル名を返すルーチンへ
#  変更
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.03.16
#  ライブラリの find_datfile.py を超つ使うのを変更して、CP2K 専用型に変更
#
################################################################################
from __future__ import print_function
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.6"
################################################################################

#import sys
#import os
#import gzip

#import re
#import glob
import optparse

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
if __name__ == '__main__':

    suffix = 'inp'
    parser = optparse.OptionParser()
    parser.add_option( '-s','--suffix',)
    options, args = parser.parse_args()

    if len(args) >0:
        suffix = args[0]

    if options.suffix:
        suffix = options.suffix

    try:
        datname = SAE.find_datfile(suffix)
        print(datname)
    except:
        pass

