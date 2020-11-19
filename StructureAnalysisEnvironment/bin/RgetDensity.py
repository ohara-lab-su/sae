#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 基本となる POSCAR ファイルから密度を求める
# (あくまで格子定数と原子数から求められる密度)
#
# 入力 POSCAR
#
# 出力(1) 標準出力
# 出力(2) POSCAR.cfg
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2014.11.13 1st
#
#  RchangeDnsity.py (2014.11.07 版)
#  Rvasp2cfg.py (2014.10.31 版)
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
import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

#import re
#import optparse
#from copy import deepcopy

################################################################################
def options():

    cname   = "POSCAR"        # OUTPUT BASE filename
    POSCAR  = "POSCAR"      # INPUT (BASE) filename

    if not os.path.exists(POSCAR):
        sys.exit("STOP: "+POSCAR+" file not found")

    print("INPUT file name :",POSCAR)
    print("OUTPUT file name:",cname+".cfg")

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
    title,scale,selective,direct = SAE.read_poscar(POSCAR,VASP,t,atoms,atoms_index,ion,ion_local,position,fix)

    ##########################################################################

    # スケールファクターを 1.0 へ変換
    scale = SAE.conv_scale21a(scale,t)

    lattice     = t[0,0]
    cell        = t[0,0]/2  # for RMC_POT
    density     = natom/(lattice**3)

    print("")
    print("  NATOM           = ", natom)
    print("  LATTICE         = ", lattice)
    print("  CELL (RMC.cfg)  = ", cell)
    print("")
    print("  DENSITY         = ", density)
    print("")

    # Cartesian to Direct
    if not direct:
        scale,direct = SAE.conv_car2directa(scale,t,natom,direct,position)

    # RMC_POT(cfg) 形式への変換 必須:direct-Mode
    scale,direct = SAE.conv_vasp2cfg(scale,t,natom,direct,position)

    t[0,0] =  cell
    t[1,1] =  cell
    t[2,2] =  cell

    outname = cname

    # RMC_POT(cfg) 形式への出力(標準出力)
    print("  OUTPUT CFG-FILE = ", outname+'.cfg')
    STD=False
   #STD=True
    SAE.print_cfg(outname,STD,title,t,natom,nion,atoms,position)

    ############## VASP 形式の*.vasp への出力(構造確認用)
    ##
    print("  OUTPUT POSCAR   = ", outname+'.vasp')
    # RMC_POT (*.cfg) 形式から VASP 形式へ変換
    direct = True   # conv_cfg2vasp は direce を想定(in/out)
    scale   = 1.0   # conv_cfg2vasp は scale 1.0 を想定
    scale,direct = SAE.conv_cfg2vaspa(scale,t,natom,direct,position) # 引数版

    # 擬似VASP5 設定
    dummy   = "In Ga Zn O"
    PV5FLAG = True  # 擬似VASP5 出力

    # VASP4+擬似VASP5 出力
    STD=False
   #STD=True
    SAE.print_poscar4(outname,STD,title,scale,natom,nion,\
                      direct,PV5FLAG,t,atoms,dummy,position)

    print("")

    ##########################################################################




