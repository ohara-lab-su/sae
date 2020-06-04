#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# get E_fermi
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.11.16 startup
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
__version__    = "0.0.1"
################################################################################

import sys
#import gzip
import os
#import re
import optparse
#import numpy as np

import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE

#import matplotlib.pyplot as plt


#################################################################################
def options():

    parser = optparse.OptionParser()
    parser.add_option('-i','--input', dest='INPUT',)
    parser.add_option('--name',)
    options,args = parser.parse_args()

    ###### default inpname 取得
    if options.INPUT:
        inpname = options.INPUT
    else:
        if os.path.exists('fdmfile.txt'):
            fdmfiletxt = SAEnv.ReadFdmFdmfile()
            inpname = fdmfiletxt.filout
        else:
            inpname = 'read_pdb.inp'

    if not os.path.exists(inpname) or inpname is None:
        sys.exit(inpname+' file not fount')

    return inpname,options.name

################################################################################
if __name__ == '__main__':

    inpname, filout = options()

    if not filout:
        inp = SAEnv.ReadFdmInp(inpname)
        filout = inp.filout

    txt = SAEnv.ReadFdmTxt(filout, suffix='.txt')
    bav = SAEnv.ReadFdmBav(filout, suffix = '_bav.txt')

    efermi = txt.E_Fermi
    eedge = txt.E_edge
    edge = bav.edge

    print("E_Fermi")
    print(efermi)
    print("E_Edge ("+edge+")")
    print(eedge)

