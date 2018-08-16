#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 移動原子リスト (通しの原子番号, x, y, z(ang))
# に従い POSCAR 構造の原子を一部(全部)移動する
# リストに記述する単位は ang 単位
#
# 入力はベースとなる POSCAR ファイル
# 直接 RMC_POT 用の cfg ファイルを出力する (VmodifyAtomPosition は POSCAR 出力)
#
################################################################################
#
# 2015.02.27
#  conv_direct2car --> conv_direct2car0
#
# 2014.11.05 1st
#   基本ベースは VmodifyAtomPosition.py (2014.11.05 version)
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
#   cname  = "POSCAR" # OUTPUT BASE filename
    cname  = "igzo"   # OUTPUT BASE filename
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


    ##########################################################################

    # 移動原子リスト読み込み (data,x,y,z)
    name='LIST'
    nlist = SAE.read_list_param(name)

    list_atoms = np.zeros((nlist,4))
    nlist = SAE.read_list4(name,list_atoms)

    # Direct to Cartesian
    if direct:
        ABS=False # for VASP
        scale,direct = SAE.conv_direct2cara(ABS,scale,t,natom,direct,position)

    for i in range(nlist):
        print i, int(list_atoms[i,0]), list_atoms[i,1],list_atoms[i,2],list_atoms[i,3]

    # スケールファクターを 1.0 へ変換
    scale = SAE.conv_scale21a(scale,t)

    # 原子移動(ang) 必要:cartesian-mode
    #    入力list_atom: cartesian-実座標系(ang)
    #    入力position : cartesian-内部座標系(scale)
    #    内部でスケールし直すのでスケールファクターは実はなんでも良い
    SAE.move_atoms0(scale,t,direct,position,nlist,list_atoms)


    ##########################################################################

    # Cartesian to Direct
    if not direct:
        scale,direct = SAE.conv_car2directa(scale,t,natom,direct,position)

#   # POSCAR のファイル標準出力
#   STD=False
#   print_poscar(POSCAR,STD,title,scale,natom,nion,selective,direct,VASP,t,atoms,atoms_index,position,fix)

    # RMC_POT(cfg) 形式への変換 必須:direct-Mode
    scale,direct = SAE.conv_vasp2cfg(scale,t,natom,direct,position)

    # RMC_POT(cfg) 形式への出力(標準出力)
    STD=False
   #STD=True
    SAE.print_cfg(cname,STD,title,t,natom,nion,atoms,position)


    ##########################################################################

    # RMC_POT (*.cfg) 形式から VASP 形式へ変換
    direct = True   # conv_cfg2vasp は direce を想定(in/out)
    scale   = 1.0   # conv_cfg2vasp は scale 1.0 を想定
    scale,direct = SAE.conv_cfg2vaspa(scale,natom,t,direct,position) # 引数版

    # 擬似VASP5 設定
    dummy   = "In Ga Zn O"
    PV5FLAG = True  # 擬似VASP5 出力

    # VASP4+擬似VASP5 出力
    STD=False
   #STD=True
    SAE.print_poscar4(cname,STD,title,scale,natom,nion,\
                      direct,PV5FLAG,t,atoms,dummy,position)


################################################################################

