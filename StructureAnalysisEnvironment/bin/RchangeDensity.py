#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#
# 入力(1) POSCAR
# 入力(2) lattice.list
# 入力(3) igzo.dat
#
# 出力(1) igzo.cfg (構造,lattice変更)
# 出力(2) igzo.dat (密度変更)
#
#
################################################################################
#
# --> ファイルから 基準となる格子定数の比率リスト
#     0.8
#     0.9
#
# を入力して
#
# 1) 格子定数を変更 (*.cfg 変更)
# 2) 電子密度を変更 (*.dat 変更)
#
# の作成を連続的に行う。python 版
# shell-script の代わりに使った時の、開発効率のテストも兼ねている
#
# 結果は画面にも出力するが、*.dat (密度情報) および *.cfg (構造情報) を
# ファイル単位で出力する
#
# 汎用性は微妙、たぶん無い
#
# 基準となる格子定数(および計算密度)は、ベースとなる POSCAR から取得する
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2014.11.07
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

    cname   = "igzo"        # OUTPUT BASE filename
    POSCAR  = "POSCAR"      # INPUT (BASE) filename
    lname   = "lattice.list" # 計算する格子リスト

    if not os.path.exists(POSCAR):
        sys.exit("STOP: "+POSCAR+" file not found")

    if not os.path.exists(cname+".dat"):
        sys.exit("STOP: "+cname+".dat file not found")

    if not os.path.exists(lname):
        sys.exit("STOP: "+lname+" file not found")

    print("INPUT file name :",POSCAR)
    print("OUTPUT file name:",cname+".cfg")

    return [POSCAR,cname,lname]


################################################################################
if __name__ == '__main__':

    # Default & OptionParser
    POSCAR,cname,lname = options()

    # POSCAR の事前読み込み
    nion,natom,VASP = SAE.read_poscar_param(POSCAR)

    # POSCAR 読み込みのための準備
    t           = np.zeros((3,3))
    atoms       = []                  # 原子の種類番号(max=nion)を与えると、その原子種の数を返す
    atoms_index = []                  # 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
    ion         = np.zeros(natom)     # 通し番号(max=natom)を与えると原子の種類番号を返す
    ion_local   = np.zeros(natom)     # 通し番号(max=natom)を与えるとサイト内のローカル通し番号を返す
    position    = np.zeros((natom,3))
    fix         = np.zeros((natom,3),dtype='S')

    # POSCAR の読み込み
    title,scale,selective,direct = \
       SAE.read_poscar(POSCAR,VASP,t,atoms,atoms_index,ion,ion_local,position,fix)

    ##########################################################################

    # リスト読み込み (data)
    nlist = SAE.read_list_param(lname)

    list_lattice = np.zeros(nlist,dtype=float)
    nlist = SAE.read_list1(lname,list_lattice)

    # スケールファクターを 1.0 へ変換
    scale = SAE.conv_scale21a(scale,t)

    lattice_org = t[0,0]
    cell_org    = t[0,0]/2  # for RMC_POT
    density     = np.zeros(nlist,dtype=float)
    cell        = np.zeros(nlist,dtype=float)

    print("")
    print("NATOM             = ", natom)
    print("ORIGINA LATTICE a = ", lattice_org)
    print("")

    for i in range(nlist):
        print("====================")

        density[i] = natom/((lattice_org*list_lattice[i])**3)
        cell[i]    = (lattice_org*list_lattice[i])/2

        print("  LATTICE RATE    = ", list_lattice[i])
        print("  LATTICE         = ", lattice_org*list_lattice[i])
        print("  CELL            = ", cell[i])
        print("  DENSITY         = ", density[i])

        # Cartesian to Direct
        if not direct:
            scale,direct = SAE.conv_car2directa(scale,t,natom,direct,position)

        # RMC_POT(cfg) 形式への変換 必須:direct-Mode
        scale,direct = SAE.conv_vasp2cfg(scale,t,natom,direct,position)

        t[0,0] =  cell[i]
        t[1,1] =  cell[i]
        t[2,2] =  cell[i]

        outname = cname+"_"+str(list_lattice[i])

        # *.dat (RMC_POT) の density を置換して出力
        print("  OUTPUT DAT      = ", outname+'.dat')
        STD=False
        SAE.change_density(STD,cname,outname,density[i])

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




