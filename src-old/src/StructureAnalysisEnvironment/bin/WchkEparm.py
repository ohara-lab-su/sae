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
from __future__ import print_function
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014,2015 Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"
################################################################################

#import sys
import os
import re
#import gzip
#import numpy as np

import optparse

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE


################################################################################
if __name__ == '__main__':

    case = re.sub('.*/','',os.getcwd())
   #case = 'Cu'

    suffix='scf'

    parser = optparse.OptionParser(os.getcwd())
    parser.add_option( '-i','--input', dest='INPUT', )
    parser.add_option( '-a','--atom',)
    parser.add_option( '-o','--orbit',)
    parser.add_option( '-l','--lorbit',)
    parser.add_option( '-s','--suffix',)
    options, args = parser.parse_args()

    if options.INPUT:
        case = options.INPUT

    if options.atom:
        ion = options.atom
    else:
        ion = 'None'

    if options.orbit:
        par = options.orbit
    else:
        par = 'None'

    if options.lorbit:
        par = 'None'
        l = options.lorbit
    else:
        l = 'None'

    if options.suffix:
        suffix = options.suffix

    scf = SAE.ReadWienScf(case=case,suffix=suffix)

    print("CASE   = ",case)
    print("SUFFIX = ",suffix)
    print("ION    = ",ion)
    print("ORBIT  = ",par)

    scf.write_epar(ion=ion,par=par,l=l)

