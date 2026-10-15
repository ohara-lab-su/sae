# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#
# 入力した原子種番号(サイト番号) 通しのボンドを情報を返す
# 入力する原子種番号は 1 からスタート
#
# [in] atom1          : ボンドを考える原子1
# [in] atom2          : ボンドを考える原子2 (atom1-atom2のボンドを考える)
# [in] distance       : ボンドとみなす距離
#
# [in] nion           : 原子の種類数
# [in] position       : セルの内部座標(絶対座標に変換してあるのが前提)
#
# [return] num        : ボンド数
#
# [in/out] bond1[num] : ボンドしている原子の通し番号が記述されている
# [in/out] bond2[num] : ボンドしている原子の通し番号が記述されている
# [in/out] bondr[num] : ボンドしている距離
#
################################################################################
from __future__ import print_function

try:
    from .copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################
#
# 2015.02.16
#   import の名前空間を変更
#   無駄な import の廃止
#
################################################################################

# import sys
# import os
# import re
import numpy as np

import StructureAnalysisEnvironment as SAE


# import SpaceGroupEnvironment as SGE

####################################################
## distanceでatom1とatom2がボンドしている数を返す
## ゾーンバウンダリーを超えない
##
def get_bond_info_param(atom1, atom2, distance, nion, atoms, position):
    # 入力原子 atom1 の原子種を確認
    #   atom1   = 1
    #   atom2   = 4

    # 入力した原子種の通し番号の下限と上限を返す
    # 入力する原子種の種別番号は 1 からスタート
    start1, end1 = SAE.get_atom_start(atom1, nion, atoms)
    if atom1 != atom2:
        start2, end2 = SAE.get_atom_start(atom2, nion, atoms)

    # 入力した原子のサイト内ループを通し番号で記述
    atom1_0 = atom1 - 1
    # for i in range(int(atoms[atom1_0])):
    # print i

    num = 0
    if atom1 != atom2:
        for i in range(start1, end1 + 1, 1):
            x1 = position[i, 0]
            y1 = position[i, 1]
            z1 = position[i, 2]
            for j in range(start2, end2 + 1, 1):
                if j != i:
                    x2 = position[j, 0]
                    y2 = position[j, 1]
                    z2 = position[j, 2]

                    r0 = np.fabs((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) + (z2 - z1) * (z2 - z1))
                    r1 = np.sqrt(r0)
                    if r1 < distance:
                        num += 1
    else:
        for i in range(start1, end1 + 1, 1):
            x1 = position[i, 0]
            y1 = position[i, 1]
            z1 = position[i, 2]
            for j in range(i, end1 + 1, 1):
                if j != i:
                    x2 = position[j, 0]
                    y2 = position[j, 1]
                    z2 = position[j, 2]

                    r0 = np.fabs((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) + (z2 - z1) * (z2 - z1))
                    r1 = np.sqrt(r0)
                    if r1 < distance:
                        num += 1

    return num


####################################################
## distanceでatom1とatom2がボンドしている数を返す
## ゾーンバウンダリーを超えない
##
## 注意) 引数の ion はデバッグ用(print用)
##       それ以外ではルーチンの中では使わないので基本は省いておく
##
def get_bond_info(atom1, atom2, distance, nion, atoms, atoms_index, position, bondr, bond1, bond2):
    # def get_bond_info(atom1,atom2,distance,nion,ion,atoms,atoms_index,position,bondr,bond1,bond2):

    # 入力原子 atom1 の原子種を確認
    #   atom1   = 1
    #   atom2   = 4

    # 入力した原子種の通し番号の下限と上限を返す
    # 入力する原子種の種別番号は 1 からスタート
    start1, end1 = SAE.get_atom_start(atom1, nion, atoms)
    if atom1 != atom2:
        start2, end2 = SAE.get_atom_start(atom2, nion, atoms)

    # 入力した原子のサイト内ループを通し番号で記述
    atom1_0 = atom1 - 1
    # for i in range(int(atoms[atom1_0])):
    # print i

    num = 0
    if atom1 != atom2:
        for i in range(start1, end1 + 1, 1):
            x1 = position[i, 0]
            y1 = position[i, 1]
            z1 = position[i, 2]
            for j in range(start2, end2 + 1, 1):
                if j != i:
                    x2 = position[j, 0]
                    y2 = position[j, 1]
                    z2 = position[j, 2]

                    r0 = np.fabs((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) + (z2 - z1) * (z2 - z1))
                    r1 = np.sqrt(r0)
                    if r1 < distance:
                        # print num, i,"("+str(atoms_index[ion[i]])+") -",\
                        #           j,"("+str(atoms_index[ion[j]])+")"  ,\
                        #           " %8.5f   %11.8f %11.8f %11.8f   %11.8f %11.8f %11.8f" \
                        #           % ( r1, x1,y1,z1, x2,y2,z2)
                        bondr[num] = r1
                        bond1[num] = i
                        bond2[num] = j
                        num += 1

    # atom1 = atom2
    else:
        for i in range(start1, end1 + 1, 1):
            x1 = position[i, 0]
            y1 = position[i, 1]
            z1 = position[i, 2]
            for j in range(i, end1 + 1, 1):
                if j != i:
                    x2 = position[j, 0]
                    y2 = position[j, 1]
                    z2 = position[j, 2]

                    r0 = np.fabs((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) + (z2 - z1) * (z2 - z1))
                    r1 = np.sqrt(r0)
                    if r1 < distance:
                        # print num, i,"("+str(atoms_index[ion[i]])+") -",\
                        #           j,"("+str(atoms_index[ion[j]])+")"  ,\
                        #           " %8.5f   %11.8f %11.8f %11.8f   %11.8f %11.8f %11.8f" \
                        #           % ( r1, x1,y1,z1, x2,y2,z2)
                        bondr[num] = r1
                        bond1[num] = i
                        bond2[num] = j
                        num += 1
