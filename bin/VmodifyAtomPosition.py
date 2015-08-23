#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 移動原子リスト (通しの原子番号, x, y, z(ang))
# に従い POSCAR 構造の原子を一部(全部)移動する
# リストに記述する単位は ang 単位
#
# POSCAR ベース入力、POSCAR 形式での出力
#
################################################################################
#
# 2015.02.27
#  conv_direct2car --> conv_direct2car0
#
# 2014.11.05 1st
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
        #POSCAR=argv[0]
        #distance = float(args[0])
        cname=args[0]

    if not os.path.exists(POSCAR):
        if os.path.exists(POSCAR+".vasp"):
            POSCAR="POSCAR.vasp"
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

    direct0 = direct

    # 移動原子リスト読み込み (data,x,y,z)
    name='LIST'
    nlist = SAE.read_list_param(name)

    list_atoms = np.zeros((nlist,4))
    nlist = SAE.read_list4(name,list_atoms)

    # Direct to Cartesian
    if direct0:
        ABS=False # for VASP
       #ABS=True  # for SuperCell
        scale,direct = SAE.conv_direct2cara(ABS,scale,t,natom,direct,position)

    # 原子移動(ang) 必要:カーテシアンmode
    SAE.move_atoms0(scale,t,direct,position,nlist,list_atoms)

    # Cartesian to Direct
    if direct0:
        scale,direct = SAE.conv_car2directa(scale,t,natom,direct,position)

    # POSCAR のファイル標準出力
    STD=False
    SAE.print_poscar(cname,STD,title,scale,natom,nion,\
                     selective,direct,VASP,t,atoms,atoms_index,position,fix)

#   # POSCAR の標準出力
#   print ""
#   STD=True
#   print_poscar(cname,STD,title,scale,natom,nion,selective,direct,VASP,t,atoms,atoms_index,position,fix)

################################################################################

