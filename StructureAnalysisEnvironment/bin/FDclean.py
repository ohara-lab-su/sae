#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDclean
# *.in ファイルを読み込んで Filout タグから名前を取得し
# Filout* ファイルを消す
#
################################################################################
#
# 2020.08.11: filout 処理でのセーフティーを導入
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
#import re
import optparse
#import numpy as np
import glob

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
def options():

#   name = 'read_pdb.inp'
#   name = 'POSCAR.inp'

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT',)
    options,args = parser.parse_args()

    ###### default inpname �擾
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

    if len(args) > 0:
        inpname=args[0]

    return inpname


if __name__ == '__main__':

    name = options()
    out = SAE.ReadFdmInp(name)

    filout = out.get_filout()
    print('fileout :',filout)

    if filout == '':
        print('fileout is None')
        sys.exit(-1)

#   filelist = glob.glob(filout+'*.txt')
    filelist = ['fdmnes_error.txt',
                filout+".txt",
                filout+"_bav.txt",
                filout+"_conv.txt"]

    filelist.extend(glob.glob(filout+'_sd*.txt'))

#   print ""
    for i in filelist:
        if os.path.exists(i):
            print("DELETE : "+i)
            os.remove(i)

    if os.path.exists('fdm.out'):
        print("DELETE : fdm.out")
        os.remove('fdm.out')

    if os.path.exists('PBS_log'):
        print("DELETE : PBS_log")
        os.remove('PBS_log')

