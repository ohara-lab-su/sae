#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# convert from VASP-POSCAR to RMC_POT cfg file
#
# 2014.10.31
#    関数化 & ライブラリ分離
#
# 2014.10.08
#    1st version
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

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

#import re

################################################################################
def options():

    ###############################################
    ## default name
    ##
    POSCAR = "POSCAR" # INPUT filename
    cname  = "POSCAR" # OUTPUT BASE filename

    ###############################################
    ## optparse
    ##
    parser = optparse.OptionParser()

    parser.add_option(  '-i','--input',
                        dest='INPUT',
                        default=POSCAR,
    )
    parser.add_option(  '-o','--output',
                        dest='OUTPUT',
                        default=cname,
    )
    options,  args = parser.parse_args()

    if options.INPUT:
        POSCAR=options.INPUT

    if options.OUTPUT:
        cname=options.OUTPUT

    #print args,options
    if len(args) > 0:
        #print "script name:",argvs[0]
        cname=args[0]
        POSCAR=args[0]

    if not os.path.exists(POSCAR):
        sys.exit(POSCAR+" file not found")

    if POSCAR:
        print "INPUT file name :",POSCAR

    if cname:
        print "OUTPUT file name:",cname+".cfg"

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

#   # Direct to Cartesian
#   if direct:
#      #ABS=False # for VASP
#       ABS=True  # for RMC_POT
#       scale,direct = conv_direct2cara(ABS,scale,t,natom,position)
#       mode="Direct"
#   else:
#       mode="Cartesian"

    # スケールファクターを 1.0 へ変換
    scale = SAE.conv_scale21a(scale,t)

    # Cartesian to Direct
    if not direct:
        scale,direct = SAE.conv_car2directa(scale,t,natom,direct,position)
        src_mode="Cartesian"
    else:
        src_mode="Direct"


    print "CURRENT MODE    :",src_mode

   ## TEST POSCAR の標準出力
   #STD=True
   #print_poscar(cname,STD,title,scale,natom,nion,selective,direct,VASP,t,atoms,atoms_index,position,fix)

    # RMC_POT(cfg) 形式への変換
    scale,direct = SAE.conv_vasp2cfg(scale,t,natom,direct,position)

    # RMC_POT(cfg) 形式への出力(標準出力)
   #print ""
    STD=False
   #STD=True
    SAE.print_cfg(cname,STD,title,t,natom,nion,atoms,position)

################################################################################




