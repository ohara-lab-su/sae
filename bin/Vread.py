#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
################################################################################
#
# 2015.01.20
#   read_poscar.py and read_poscar_param.py の GZIP 対応に合わせて
#   options 関係のルーチンを少し修正
#
# 2014.10.30/31
#    関数化 & ライブラリ化 テスト用テストプログラム
#
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
import numpy as np

#import re
#from copy import deepcopy

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
def options():

    ###############################################
    ## default parameter
    ##
    cname  = "POSCAR" # OUTPUT BASE filename
    POSCAR = "POSCAR" # INPUT (BASE) filename

    ###############################################
    ## optparse
    ##
    parser = optparse.OptionParser()

    parser.add_option(  '-i','--input', dest='INPUT',)
    parser.add_option(  '-o','--output', dest='OUTPUT',)
    options,  args = parser.parse_args()

    if options.INPUT: POSCAR=options.INPUT
    if options.OUTPUT: cname=options.OUTPUT

    #print args,options
    if len(args) > 0:
        #print "script name:",argvs[0]
        #POSCAR=argv[0]
        #distance = float(args[0])
        cname=args[0]

    if not os.path.exists(POSCAR):
        if not os.path.exists(POSCAR+".gz"):
            if os.path.exists(POSCAR+".vasp"):
                POSCAR="POSCAR.vasp"
            else:
                sys.exit(POSCAR+" file not found")

    print "INPUT file name    :",POSCAR
    print "OUTPUT file name   :",cname+".vasp"
    print ""

    return [POSCAR,cname]


################################################################################
if __name__ == '__main__':

    # Default & OptionParser
    POSCAR,cname = options()

    # POSCAR の事前読み込み
    nion,natom,VASP = SAE.read_poscar_param(POSCAR)

    # POSCAR 読み込みのための準備
    t           = np.zeros((3,3))
    atoms       = []
    atoms_index = []
    ion         = np.zeros(natom,dtype=int)
    ion_local   = np.zeros(natom,dtype=int)
    position    = np.zeros((natom,3))
    fix         = np.zeros((natom,3),dtype='S')

    # POSCAR の読み込み
    title,scale,selective,direct = \
       SAE.read_poscar(POSCAR,VASP,t,atoms,atoms_index,ion,ion_local,position,fix)

    # POSCAR の標準出力
   #STD=False
    STD=True
    SAE.print_poscar(cname,STD,title,scale,natom,nion,\
                 selective,direct,VASP,t,atoms,atoms_index,position,fix)


################################################################################

