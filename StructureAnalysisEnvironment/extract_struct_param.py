# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 単位胞からの部分的な構造抽出コードの前哨戦
#   部分空間の原子数確認ルーチン
#
# [in/out] scale          : スケールファクター
#
# [in/out] t[3,3]         : 基本並進ベクトル(注意:配列内indexは0から)
#                                 x   y   z
#                           t1 = a11 a21 a31
#                           t2 = a12 a22 a32
#                           t3 = a13 a23 a33
#
# [in]     natom          : もとの内部座標系での総原子数
#
# [in/out] direct         : 内部座標系の記述が direct か cartesian か？
#
# [in/out] position[*,3]  : 内部座標
#                           (注意:VASP 形式が念頭なので cartesian でも
#                                 scale で scale してない座標系)
#
# [in/out] c1(x,y,z)      : リージョン原点c1
# [in/out] c2(x,y,z)      : リージョン原点c2
#                           (注意) 元の direct,scale 指示に基づいて座標系の変換を随時行う
#
# [return] scale
# [return] direct
# [return] extract_natom  : 抽出した原子の数
#
#
################################################################################
#
# 2018.08.17
#  コメント: 基本的に古いルーチンなので呼び出しているものの仕様が異なるので使ってない
#
# 2015.02.16
#  import の名前空間を変更
#
# 2014.11.12 1st
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

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

def extract_struct_param(scale,t,natom,direct,position,c0,c1):

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

    # 絶対座標系へ変換
    SAE.conv_car2carABS(scale,t,natom,direct,position)

    # リージョン内の原子探索(c軸のリージョンのみ)
    j=0
    for i in range(natom):
        if position[i,2] >= c0_new[2] and position[i,2] <= c1_new[2]:
            j += 1

    extract_natom = j

    return [scale,direct,extract_natom]
