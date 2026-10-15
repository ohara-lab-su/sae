#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
##########################################################################
from __future__ import print_function
from sae.common.text import TextFiles
from sae.geometry.coordinates import CoordinateTransforms
from sae.rmcpot.cfg_writer import RmcConfigWriter
from sae.rmcpot.conversion import RmcConversions
from sae.vasp.poscar_fields import PoscarFields
from sae.vasp.poscar_writer import PoscarWriter

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
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import numpy as np


#
################################################################################
#import SpaceGroupEnvironment as SGE
#import re
#import optparse
#from copy import deepcopy
################################################################################
def options():
    # OUTPUT BASE filename
    cname = "igzo"
    # INPUT (BASE) filename
    POSCAR = "POSCAR"
    # 計算する格子リスト
    lname = "lattice.list"
    if not os.path.exists(POSCAR):
        sys.exit("STOP: " + POSCAR + " file not found")
    if not os.path.exists(cname + ".dat"):
        sys.exit("STOP: " + cname + ".dat file not found")
    if not os.path.exists(lname):
        sys.exit("STOP: " + lname + " file not found")
    print("INPUT file name :", POSCAR)
    print("OUTPUT file name:", cname + ".cfg")
    return [POSCAR, cname, lname]


################################################################################
# Default & OptionParser
# POSCAR の事前読み込み
# POSCAR 読み込みのための準備
# POSCAR の読み込み
##########################################################################
# リスト読み込み (data)
# スケールファクターを 1.0 へ変換
if __name__ == "__main__":
    POSCAR, cname, lname = options()
    nion, natom, VASP = PoscarFields().read_poscar_param(POSCAR)
    t = np.zeros((3, 3))
    # 原子の種類番号(max=nion)を与えると、その原子種の数を返す
    atoms = []
    # 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
    atoms_index = []
    # 通し番号(max=natom)を与えると原子の種類番号を返す
    ion = np.zeros(natom)
    # 通し番号(max=natom)を与えるとサイト内のローカル通し番号を返す
    ion_local = np.zeros(natom)
    position = np.zeros((natom, 3))
    fix = np.zeros((natom, 3), dtype="S")
    title, scale, selective, direct = PoscarFields().read_poscar(
        POSCAR, VASP, t, atoms, atoms_index, ion, ion_local, position, fix
    )
    nlist = TextFiles().read_list_param(lname)
    list_lattice = np.zeros(nlist, dtype=float)
    nlist = TextFiles().read_list1(lname, list_lattice)
    scale = CoordinateTransforms().conv_scale21a(scale, t)
    lattice_org = t[0, 0]
    # for RMC_POT
    cell_org = t[0, 0] / 2
    density = np.zeros(nlist, dtype=float)
    cell = np.zeros(nlist, dtype=float)
    print("")
    print("NATOM             = ", natom)
    print("ORIGINA LATTICE a = ", lattice_org)
    print("")
    # Cartesian to Direct
    # RMC_POT(cfg) 形式への変換 必須:direct-Mode
    # *.dat (RMC_POT) の density を置換して出力
    # RMC_POT(cfg) 形式への出力(標準出力)
    #STD=True
    #SAE.print_cfg(outname,STD,title,t,natom,nion,atoms,position)
    ############## VASP 形式の*.vasp への出力(構造確認用)
    ##
    # RMC_POT (*.cfg) 形式から VASP 形式へ変換
    # 引数版
    # 擬似VASP5 設定
    # VASP4+擬似VASP5 出力
    #STD=True
    for i in range(nlist):
        print("====================")
        density[i] = natom / (lattice_org * list_lattice[i]) ** 3
        cell[i] = lattice_org * list_lattice[i] / 2
        print("  LATTICE RATE    = ", list_lattice[i])
        print("  LATTICE         = ", lattice_org * list_lattice[i])
        print("  CELL            = ", cell[i])
        print("  DENSITY         = ", density[i])
        if not direct:
            scale, direct = CoordinateTransforms().conv_car2directa(
                scale, t, natom, direct, position
            )
        scale, direct = RmcConversions().conv_vasp2cfg(
            scale, t, natom, direct, position
        )
        t[0, 0] = cell[i]
        t[1, 1] = cell[i]
        t[2, 2] = cell[i]
        outname = cname + "_" + str(list_lattice[i])
        print("  OUTPUT DAT      = ", outname + ".dat")
        STD = False
        RmcConversions().change_density(STD, cname, outname, density[i])
        print("  OUTPUT CFG-FILE = ", outname + ".cfg")
        STD = False
        RmcConfigWriter().print_rmcpot_cfg(
            outname, STD, title, t, natom, nion, atoms, position
        )
        print("  OUTPUT POSCAR   = ", outname + ".vasp")
        # conv_cfg2vasp は direce を想定(in/out)
        direct = True
        # conv_cfg2vasp は scale 1.0 を想定
        scale = 1.0
        scale, direct = RmcConversions().conv_cfg2vaspa(
            scale, t, natom, direct, position
        )
        dummy = "In Ga Zn O"
        # 擬似VASP5 出力
        PV5FLAG = True
        STD = False
        PoscarWriter().print_poscar4(
            outname,
            STD,
            title,
            scale,
            natom,
            nion,
            direct,
            PV5FLAG,
            t,
            atoms,
            dummy,
            position,
        )
        print("")
