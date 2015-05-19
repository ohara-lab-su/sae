#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# POSCAR の direct 変換
#
# 2014.10.31
#   関数化 & ライブラリ化 テスト用テストプログラム
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
__version__    = "0.0.1"
################################################################################

import sys
import os
import optparse

import numpy as np
import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

#import re
#from copy import deepcopy
#from numpy import *

#from LIB_vasp import read_poscar_param
#from LIB_vasp import read_poscar
#from LIB_vasp import conv_direct2car
#from LIB_vasp import print_poscar
#from LIB_vasp import *

#from LIB_vasp.read_poscar_param import *
#from LIB_vasp.read_poscar import *
#from LIB_vasp.conv_direct2car import *
#from LIB_vasp.conv_car2direct import *
#from LIB_vasp.print_poscar import *

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

    if options.INPUT:
        POSCAR=options.INPUT
        cname=options.INPUT

    if options.OUTPUT:
        cname=options.OUTPUT

    #print args,options
    if len(args) > 0:
        #print "script name:",argvs[0]
        #POSCAR=argv[0]
        #distance = float(args[0])
        cname=args[0]
        POSCAR=args[0]

    if not os.path.exists(POSCAR):
        if os.path.exists(POSCAR+".vasp"):
            POSCAR="POSCAR.vasp"
            cname=POSCAR
        else:
            sys.exit(POSCAR+" file not found")

    print "INPUT file name    :",POSCAR
    print "OUTPUT file name   :",cname+".vasp"

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
    ion         = np.zeros(natom)
    ion_local   = np.zeros(natom)
    position    = np.zeros((natom,3))
    fix         = np.zeros((natom,3),dtype='S')

    # POSCAR の読み込み
    title,scale,selective,direct = \
       SAE.read_poscar(POSCAR,VASP,t,atoms,atoms_index,ion,ion_local,position,fix)

    # Cartesian to Direct
    if not direct:
        scale,direct = SAE.conv_car2direct(scale,t,natom,direct,position)
        src_mode="Cartesian"
    else:
        src_mode="Direct"
        print "CURRENT MODE       :",src_mode
        sys.exit("don't need to convert")

    print "CURRENT MODE       :",src_mode

    # POSCAR の標準出力
    print ""
    STD=True
    SAE.print_poscar(cname,STD,title,scale,natom,nion,\
                     selective,direct,VASP,t,atoms,atoms_index,position,fix)

    # POSCAR のファイル出力
    STD=False
    SAE.print_poscar(cname,STD,title,scale,natom,nion,\
                     selective,direct,VASP,t,atoms,atoms_index,position,fix)

################################################################################
