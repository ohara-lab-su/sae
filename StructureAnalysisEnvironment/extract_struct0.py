# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 単位胞からの部分的な構造抽出コード(フォース情報(VASP)、未対応版)
#
#
# [in/out] scale             : スケールファクター
#
# [in/out] t[3,3]            : 基本並進ベクトル(注意:配列内indexは0から)
#                                    x   y   z
#                              t1 = a11 a21 a31
#                              t2 = a12 a22 a32
#                              t3 = a13 a23 a33
#
# [in]     natom             : もとの内部座標系での総原子数
#
# [in/out] direct            : 内部座標系の記述が direct か cartesian か？
#
# [in/out] position[*,3]     : 内部座標
#                              (注意:VASP 形式が念頭なので cartesian でも
#                                    scale で scale してない座標系)
#
# [in/out] c1(x,y,z)         : リージョン原点c1
# [in/out] c2(x,y,z)         : リージョン原点c2
#                              (注意) 元の direct,scale 指示に基づいて座標系の変換を随時行う
#
#
# [in/(out)] atoms[i]        : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
# [in/(out)] atoms_index[i]  : 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
# [in/(out)] ion[j]          : 通し番号(max=natom)を与えると原子の種類番号を返す
# [in/(out)] ion_local[j]     : 通し番号(max=natom)を与えるとサイト内のローカル通し番号を返す
#
# [in/out] ex_j              : 元セルと extractセルの通し番号対応 index
#
# [in]     ex_natom          : 部分空間の総原子数
# [in/out] ex_atoms[i]       : 部分空間の atoms[i]
# [in/out] ex_atoms_index[i] : 部分空間の atoms_index[i]
#
# [in/out] ex_position[i]    : 部分空間の position[i]
#
# [return]
#
################################################################################
#
# 2018.08.17
#  コメント: 基本的に古いルーチンなので呼び出しているものの仕様が異なるので使ってない
#
# 2015.0216
#  import の名前空間を変更
#
# 2014.11.13 1st
#
################################################################################
from __future__ import print_function
###############################################################################
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

#import sys
#import os

import numpy as np

#from . import conv_direct2car
import StructureAnalysisEnvironment as SAE

#import SpaceGroupEnvironment as SGE

def extract_struct0(scale,t,natom,direct,position,c0,c1,\
                    atoms,atoms_index,ion,ion_local,\
                    ex_j,ex_natom,ex_atoms,ex_atoms_index,ex_position):

    # リージョン選択の座標系の変換
    t1_x = t[0,0]
    t1_y = t[1,0]
    t1_z = t[2,0]

    t2_x = t[0,1]
    t2_y = t[1,1]
    t2_z = t[2,1]

    t3_x = t[0,2]
    t3_y = t[1,2]
    t3_z = t[2,2]

    c0_new = np.zeros(3)
    c0_new[0] = ( t1_x*c0[0] + t2_x*c0[1] + t3_x*c0[2] )*scale
    c0_new[1] = ( t1_y*c0[0] + t2_y*c0[1] + t3_y*c0[2] )*scale
    c0_new[2] = ( t1_z*c0[0] + t2_z*c0[1] + t3_z*c0[2] )*scale

    c1_new = np.zeros(3)
    c1_new[0] = ( t1_x*c1[0] + t2_x*c1[1] + t3_x*c1[2] )*scale
    c1_new[1] = ( t1_y*c1[0] + t2_y*c1[1] + t3_y*c1[2] )*scale
    c1_new[2] = ( t1_z*c1[0] + t2_z*c1[1] + t3_z*c1[2] )*scale

    # cartesian系へ変換
    if direct:
        ABS=False
        scale,direct = SAE.conv_direct2cara(ABS,scale,t,natom,direct,position)

    # 絶対座標系へ変換(引数版)
    SAE.conv_car2carABSa(scale,t,natom,direct,position)

    # リージョン内の原子探索(c軸のリージョンのみ)
    j=0
    for i in range(natom):
        if c0_new[2] <= position[i,2] <= c1_new[2]:
            ex_position[j,0] = position[i,0]
            ex_position[j,1] = position[i,1]
            ex_position[j,2] = position[i,2]
            ex_j[j] = i

            j += 1

    ex_natom = j

    # 原子種の数をカウント (頭が悪そうなループ)
    # (注意) もともと原子種の数でソートされている構造情報を元にしているのが前提
    nion = 0
    tmp = 'ZZ'
    local_atom_index = 0
    for i in range(ex_natom):
        atom0       = int(atoms[int(ion[ex_j[i]])])
        atom_index0 = str(atoms_index[int(ion[ex_j[i]])])
        local_atom_index += 1
        if tmp != atom_index0:
            nion += 1
            if tmp != 'ZZ':
                ex_atoms.append(str(local_atom_index))
                ex_atoms_index.append(str(tmp))
            local_atom_index = 0
        tmp = atom_index0
    ex_nion = nion
    ex_atoms.append(str(local_atom_index))
    ex_atoms_index.append(str(tmp))

    return ex_nion
