#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# convert from RMC_POT cfg file to VASP POSCAR file
#
################################################################################
#
# 2015.07.16
#    関数版を駆逐(class版を使う)
#
# 2014.10.31
#    関数化 & ライブラリ分離
#
# 2014.10.08
#    Rvasp2cfg.py に仕様を合わせる
#    --> オプション関係を追加
#
# 2014.10.01
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
__version__    = "0.0.3"
################################################################################

import sys
import os
import optparse
#import numpy as np

import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE

################################################################################
def options():

    cname="igzo" # INPUT BASE filename

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT',)
    options,  args = parser.parse_args()
    if options.INPUT: cname=options.INPUT

    if len(args) > 0: cname=args[0]

    if cname:
        print "INPUT file name :",cname+".cfg"
        print "OUTPUT file name:",cname+".vasp"

    if not os.path.exists(cname+".cfg"):
        sys.exit(cname+".cfg file not found")

    return cname


################################################################################
if __name__ == '__main__':

    cname = options()
    filename = cname+".cfg"
    outname = cname

    dummy=['In','Ga','Zn','O']

    cell = SAEnv.Read(filename=filename,code='RMC',atoms_index=dummy)
    cell.write(outname=outname,code='VASP')

