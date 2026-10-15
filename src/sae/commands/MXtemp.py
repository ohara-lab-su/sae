#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.common.paths import FileDiscovery
from sae.openmx.md import ReadMd

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# MXtemp.py
#
#   *.md から temperature と given Temp と Total Energy を抜き出す
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.03.03
#   startup
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import optparse

#
################################################################################
#import re
#import numpy as np
#from pylab import *
#import matplotlib.pyplot as plt
#import SpaceGroupEnvironment as SGE 
################################################################################
# オプション処理(指定したファイルが存在してない時はsuffixをつけてみる)
# デフォルト名 or 入力名が存在しない時の入力ファイル名自動探索
if __name__ == "__main__":
    name = "openmx"
    suffix = "md"
    mdname = name + "." + suffix
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    if options.INPUT:
        mdname = options.INPUT
        if not os.path.exists(mdname):
            mdname = mdname + "." + suffix
    if not os.path.exists(mdname):
        mdname0 = FileDiscovery().find_datfile(suffix)
        if mdname0 != None:
            mdname = mdname0 + "." + suffix
        else:
            sys.exit("STOP: " + mdname + " not found.")
    print("INPUT:", mdname)
    md = ReadMd(mdname)
    natom = md.get_natom()
    nion = md.get_nion()
    nloop = md.get_nloop()
    energy = md.get_energy_loop()
    temp = md.get_temp_loop()
    given = md.get_temp_given_loop()
    for i in range(nloop):
        print("%5d  %8.3f  %8.3f  %15.8f" % (i + 1, temp[i], given[i], energy[i]))
