#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# VfindBond.py
#  原子のボンドを調べるための関数のテストを兼ねたプログラム
#   ボンド一覧はゾーンバウンダリーは考えない(一つのセル内だけ)
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.02.27
#   conv_direct2car --> conv_direct2car0
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

#import os
#import re
import sys
#import optparse

import numpy as np
#from copy import deepcopy

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
def options():

    POSCAR = "POSCAR" # INPUT (BASE) filename

    atom1    = 1    # 検索する原子の種類番号(1) default
    atom2    = 4    # 検索する原子の種類番号(2) default
    distance = 2.4  # ボンドを検索する範囲(ang) default


    return [POSCAR,atom1,atom2,distance]

################################################################################
if __name__ == '__main__':

    # Default & OptionParser
    POSCAR,atom1,atom2,distance = options()

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

    # Direct to Cartesian
    if direct:
        ABS=False # for VASP
       #ABS=True  # for SuperCell
        scale,direct = SAE.conv_direct2cara(ABS,scale,t,natom,direct,position)

    scale = SAE.conv_car2carABSa(scale,t,natom,direct,position) # 引数版

    if direct:
        sys.exit("Error: current mode is Direct")

    if nion <  atom1 or nion < atom2 :
        sys.exit("Error: nion < atom1 or atom2")

    # atom1 と atom2 が discance 以内でボンドしている数を入手
    # ZB は超えない
    bondnum  = SAE.get_bond_info_param(atom1,atom2,distance,nion,atoms,position)
    if bondnum != 0:
        print(bondnum)

    bondr = np.zeros((bondnum))
    bond1 = np.zeros((bondnum),dtype=int)
    bond2 = np.zeros((bondnum),dtype=int)

    # atom1 と atom2 が distance 以下の時に bond しているとして情報を返す。
    # (1) bond している原子番号(通し坂東での記述)
    # (2) bond 距離
   #get_bond_info(atom1,atom2,distance,nion,\
   #              ion,atoms,atoms_index,position,bondr,bond1,bond2)
    SAE.get_bond_info(atom1,atom2,distance,nion,\
                      atoms,atoms_index,position,bondr,bond1,bond2)

    for num in range(bondnum):

        x1 = position[bond1[num],0]
        y1 = position[bond1[num],1]
        z1 = position[bond1[num],2]

        x2 = position[bond2[num],0]
        y2 = position[bond2[num],1]
        z2 = position[bond2[num],2]

        r1 = bondr[num]

       #print num, bond1[num],"("+str(atoms_index[ion[bond1[num]]])+") -",\
       #           bond2[num],"("+str(atoms_index[ion[bond2[num]]])+")"  ,\
       #           " %10.7f   %11.8f %11.8f %11.8f   %11.8f %11.8f %11.8f" \
       #           % ( r1, x1,y1,z1, x2,y2,z2)

        print("%d %d (%s) - %s (%s)   %10.7f   %11.8f %11.8f %11.8f   %11.8f %11.8f %11.8f"
              % ( num, bond1[num], str(atoms_index[ion[bond1[num]]]),
                       bond2[num], str(atoms_index[ion[bond2[num]]]),
                       r1,  x1,y1,z1, x2,y2,z2))


