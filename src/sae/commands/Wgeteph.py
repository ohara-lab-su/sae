#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.wien2k.scf import ReadWienScf

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# WIEK2k case.sca
#  エナジーパラメーターのチェック
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.03.31
#  startup
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014,2015 Kengo NAKADA"
__license__ = "MIT"
import os
import re
import optparse

#
################################################################################
#import sys
#import gzip
#import numpy as np
#import SpaceGroupEnvironment as SGE
################################################################################
#case = 'Cu'
if __name__ == "__main__":
    case = re.sub(".*/", "", os.getcwd())
    suffix = "scf"
    parser = optparse.OptionParser(os.getcwd())
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-a", "--atom")
    parser.add_option("-s", "--suffix")
    options, args = parser.parse_args()
    if options.INPUT:
        case = options.INPUT
    if options.atom:
        ion = options.atom
    else:
        ion = "None"
    if options.suffix:
        suffix = options.suffix
    scf = ReadWienScf(case=case, suffix=suffix)
    print("CASE   = ", case)
    print("SUFFIX = ", suffix)
    print("ION    = ", ion)
    scf.write_eph(ion=ion)
