#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# PWscf *.in --> POSCAR 変換出力
#
################################################################################
#
# 2015.08.24
#  統合化への大改修
#
# 2015.05.13 startup
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"
################################################################################

#import sys
#import gzip
#import os
#import re
import optparse
#import numpy as np

import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE

################################################################################
def options():
    name = 'scf.in'

    parser = optparse.OptionParser()

    parser.add_option(  '-i','--input', dest='INPUT', default=name,)
    options,args = parser.parse_args()

    if options.INPUT: name=options.INPUT
    if len(args) > 0: name=args[0]

    return name

################################################################################
if __name__ == '__main__':

    name = options()
    pwin = SAEnv.Read(filename=name,code='PWscf')
    pwin.write(outname=name,code='VASP')


