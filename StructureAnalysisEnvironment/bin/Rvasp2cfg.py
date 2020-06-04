#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# convert from VASP-POSCAR to RMC_POT cfg file
#
# 2015.08.24
#    統合化
#
# 2014.10.31
#    関数化 & ライブラリ分離
#
# 2014.10.08
#    1st version
#
################################################################################
from __future__ import print_function

################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.2"
################################################################################

import sys
import os
import optparse

#import numpy as np

import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE

#import re

################################################################################
def options():

    POSCAR = "POSCAR" # INPUT filename
    cname  = "POSCAR" # OUTPUT BASE filename

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT', )
    parser.add_option(  '-o','--output', dest='OUTPUT', )
    options,  args = parser.parse_args()

    if options.INPUT: POSCAR=options.INPUT
    if options.OUTPUT: cname=options.OUTPUT

    #print args,options
    if len(args) > 0:
        #print "script name:",argvs[0]
        cname=args[0]
        POSCAR=args[0]

    if not os.path.exists(POSCAR): sys.exit(POSCAR+" file not found")
    if POSCAR: print("INPUT file name : %s" % str(POSCAR))
    if cname: print("OUTPUT file name: %s" % str(cname+".cfg"))

    return [POSCAR,cname]

################################################################################
if __name__ == '__main__':

    POSCAR,cname = options()

    cell = SAEnv.Read(filename=POSCAR,code='VASP')
    cell.write(outname=cname,code='RMC_POT')

