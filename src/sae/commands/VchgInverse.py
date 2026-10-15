#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.structure.base import Method
from sae.vasp.chgcar import ReadVaspChgcar
import sys
import os
import re
import math
import numpy as np

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
################################################################################
# CHGCAR/ELFCAR 読み込み class
#
# 先頭部分は POSCAR と同じなので以下は同じ
#
# t[3,3]            :  基本並進ベクトル(注意:配列内indexは0から)
#
#                              x   y   z
#                        t1 = a11 a21 a31  ! lattice vector t1
#                        t2 = a12 a22 a32  ! lattice vector t2
#                        t3 = a13 a23 a33  ! lattice vector t3
# 注意)
#    t(基本並進行列)
#                             t11, t12, t13
#                             t21, t22, t23
#                             t31, t32, t33
#
# atoms[i]          : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
# atoms_index[i]    : 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
# atoms_index_j[i]  : 通し番号(max=natom)を与えると、原子種の元素記号を返す
# ion[j]            : 通し番号(max=natom)を与えると原子の種類番号を返す
# ion_local[j]      : 通し番号(max=natom)を与えるとサイト内のローカル通し番号を返す
#
# position[j,3]     : 通し番号(max=natom)とx,y,z 指定で内部座標
# fix[j,3]          : 通し番号(max=natom)とx,y,z 指定でForceのFix/non-Fix 指定
#
# title             : タイトル
# scale             : 格子定数(スケールファクター)
# selective         : selective mode
# direct            : direct or cartesian
#
################################################################################
# 2018.08.18 新インスタンス変数
#
# t1_len         : 格子定数a
# t2_len         : 格子定数b
# t3_len         : 格子定数c
#
# 2018.08.18 新Method
#
# get_lattice_a()
# get_lattice_b()
# get_lattice_c()
#
# get_t1_len()
# get_t2_len()
# get_t3_len()
#
################################################################################
#
# 1) 基本構造情報読み込み Method : get_*()
#
# 2) 並進ベクトル回転Method
#     conv_rot_euler(self,alpha,beta,gamma)
#
# 3) POSCAR print method
#     print_poscar()
#
# 4) conv Direct --> Cartesian
#     conv_direct2car()
#
# 5) makes SuperCell method
#     conv_supercell()
#
################################################################################
#
# 2018.08.17
#  startup
#
################################################################################
try:
    Method = Method
except ImportError:
    Method = Method
################################################################################
# import gzip
# sys.path.append('../..')
# import SpaceGroupEnvironment as SGE
# from numba import jit
# name = 'POSCAR'
# 反転した CHGCAR を作る
if __name__ == "__main__":
    import optparse

    name = "CHGCAR"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT", default=name)
    options, args = parser.parse_args()
    name = options.INPUT
    chgcar = ReadVaspChgcar(name)
    max = chgcar.chgdata.max()
    min = chgcar.chgdata.min()
    print("origin CHGCAR max = %s" % max)
    print("origin CHGCAR min = %s" % min)
    print("offset            = %s" % max)
    inv_chg = chgcar.inverse_chgcar(offset=max)
    print("origin CHGCAR Inverse max = %s" % inv_chg.max())
    print("origin CHGCAR Inverse min = %s" % inv_chg.min())
    chgcar.print_chgcar(chgcar=inv_chg, outname="CHGCAR_INVERSE")
