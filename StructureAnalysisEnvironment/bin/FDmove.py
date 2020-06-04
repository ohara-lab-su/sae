#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDmove
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.06.19 startup
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
__version__    = "0.1.1"
################################################################################

import sys
#import gzip
import os
#import shutil
#import re
import optparse
#import numpy as np
import glob

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
def options():

    parser = optparse.OptionParser()
    parser.add_option('-i','--input', dest='INPUT',)
    parser.add_option('-d', dest='DEST')
    options,args = parser.parse_args()

    fildst = None
    filsrc = None
    inpname = None

    if options.DEST:
        fildst = options.DEST

    if len(args) == 0:
        sys.exit('STOP args < 1 ')

    # $B0z?t(B1: (*.inp $B$N(B filout $B9`L\$,I,?\(B)
    if len(args) == 1:

        if options.INPUT:
            inpname = options.INPUT
        else:
            if os.path.exists('fdmfile.txt'):
                fdmfiletxt = SAE.ReadFdmFdmfile()
                inpname = fdmfiletxt.filout
            else:
                inpname = 'read_pdb.inp'

        if not os.path.exists(inpname) or inpname is None:
            sys.exit(inpname+' file not fount')

        fildst = args[0]

    if len(args) == 2:
        filsrc = args[0]
        fildst = args[1]

    return inpname, filsrc, fildst

################################################################################
if __name__ == '__main__':

    inpname, filsrc, fildst = options()

    if filsrc is None:
        print('inp :', inpname)
        out = SAE.ReadFdmInp(inpname)
        filsrc = out.get_filout()

    print('src :', filsrc)
    print('dst :', fildst)
    print("")

    filelist = [".txt",
                "_bav.txt",
                "_conv.txt"]

    for i  in glob.glob(filsrc+'_sd*.txt'):
        filelist.append(i.replace(filsrc,''))


    for i in filelist:
        if os.path.exists(filsrc+i):
            print("MOVE : " + filsrc + i + " --> " + fildst + i)
            os.rename( filsrc+i, fildst+i )

