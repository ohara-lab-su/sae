# -*- coding: utf-8 -*-
##################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# POSCAR の内部座標を direct 系から cartesian 系へ変換
#  ABSモード対応版(殆どおくらゆき)
#
#  (注意) scale ファクターさえ注意すれば POSCAR(VASP) 以外でも使える
#
#
# [in]  ABS
#           True  : 1) スケールファクターを1 にする
#                   2) 内部座標もスケール(絶対座標系)
#
#           False : VASP の cartesian mode
#                   1) 並進ベクトルはスケールしない(別にしても構わないのだが)
#                   2) 内部座標はスケールしない(これをスケールしたらVASPではダメ)
#
#
# [in]     scale0         : 基本並進にかかるスケール(変換前)
#
# [in/out] t[3,3]         : 基本並進ベクトル(注意:配列内indexは0から)
#                                  x   y   z
#                            t1 = a11 a21 a31
#                            t2 = a12 a22 a32
#                            t3 = a13 a23 a33
#
# [in]     natom          : number of atom
# [in]     direct         : 入力のモード(もし Car ならば安全のために止める)
#
# [in/out] position[j,3]  : 通し番号(max=natom)とx,y,z 指定で内部座標
#                           ABS が True 以外は VASP 形式
#                           つまり、scale でスケールしない内部座標系式
#
# [return] scale          : 基本並進にかかるスケール
# [return] direct         : direct = False (変換をしたので direct は False)
#
##################################################################################
#
# 2015.08.24
#  基本ルール変更
#    引数版 conv_direct2carABS --> conv_direct2carABSa
#    戻り値版 conv_direct2darABS1 --> conv_direct2carABS
#
# 2015.02.27
#   引数版
#    conv_direct2car1    (ABS非対応化)
#    conv_direct2carABS1 (ABS対応)
#
#   対応関係をはっきりするために conv_direct2carABS を蔵から出す
#   旧バージョンはそのまま conv_direct2carABS
#
# 2014.11.21
#   ABS 非対応版を conv_direct2car とするために旧版を conv_direct2carABS とする
#   そのためのバージョンとしてブランチ
#    ---> 結局は conv_direct2car を用いているのでお蔵行き
#
# 2014.10.30/31 1st
#
################################################################################
from __future__ import print_function
try:
    from copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import sys
# import os
# import re
# from numpy import *
# from copy import deepcopy

import numpy as np


################################################################################
# 引数版
def conv_direct2carABSa(ABS, scale0, t, natom, direct, position):
    if not direct:
        sys.exit("STOP(conv_direct2car): current is not Direct.")

    ###############################################
    ## 座標系を 1) direct --> cartesian
    ##          2) cartesian のまま
    ##
    ## 変換後に scale して絶対座標にする
    ## (入力がAngstrom 系なので A 単位になる)
    ##
    t1_x = t[0, 0]
    t1_y = t[1, 0]
    t1_z = t[2, 0]

    t2_x = t[0, 1]
    t2_y = t[1, 1]
    t2_z = t[2, 1]

    t3_x = t[0, 2]
    t3_y = t[1, 2]
    t3_z = t[2, 2]

    car = np.zeros((natom, 3))
    for j in range(natom):
        car[j, 0] = t1_x * position[j, 0] + t2_x * position[j, 1] + t3_x * position[j, 2]
        car[j, 1] = t1_y * position[j, 0] + t2_y * position[j, 1] + t3_y * position[j, 2]
        car[j, 2] = t1_z * position[j, 0] + t2_z * position[j, 1] + t3_z * position[j, 2]

    ###############################################
    ## scale0 を掛けて car の絶対座標系へなおす
    ## ABS mode:
    ##     scale=1.0 とするので必須作業 (絶対座標記述の場合)
    ##
    ## non ABS mode:
    ##     VASP 用の POSCAR の car Mode の場合は
    ##     scale に関係なく内部座標は再スケールはない
    ##
    if not ABS:
        # for VASP
        scale = scale0
        scale0 = 1.0
    else:
        # for RMC_POT
        scale = 1.0

    for j in range(natom):
        position[j, 0] = car[j, 0] * scale0
        position[j, 1] = car[j, 1] * scale0
        position[j, 2] = car[j, 2] * scale0

    ###############################################
    ## 基本並進ベクトルをスケールしておく
    ## --> scale=1.0 とするため
    ##
    if ABS:
        t1_x = t1_x * scale0
        t1_y = t1_y * scale0
        t1_z = t1_z * scale0

        t2_x = t2_x * scale0
        t2_y = t2_y * scale0
        t2_z = t2_z * scale0

        t3_x = t3_x * scale0
        t3_y = t3_y * scale0
        t3_z = t3_z * scale0

    t[0, 0] = t1_x
    t[1, 0] = t1_y
    t[2, 0] = t1_z

    t[0, 1] = t2_x
    t[1, 1] = t2_y
    t[2, 1] = t2_z

    t[0, 2] = t3_x
    t[1, 2] = t3_y
    t[2, 2] = t3_z

    scale = scale
    direct = False
    return [scale, direct]


################################################################################
# ABS 版,戻り値版
#
def conv_direct2carABS(scale0, t, natom, direct, position):
    if not direct:
        sys.exit("STOP(conv_direct2car): current is not Direct.")

    ###############################################
    ## 座標系を 1) direct --> cartesian
    ##          2) cartesian のまま
    ##
    ## 変換後に scale して絶対座標にする
    ## (入力がAngstrom 系なので A 単位になる)
    ##
    t1_x = t[0, 0]
    t1_y = t[1, 0]
    t1_z = t[2, 0]

    t2_x = t[0, 1]
    t2_y = t[1, 1]
    t2_z = t[2, 1]

    t3_x = t[0, 2]
    t3_y = t[1, 2]
    t3_z = t[2, 2]

    car = np.zeros((natom, 3))
    for j in range(natom):
        car[j, 0] = t1_x * position[j, 0] + t2_x * position[j, 1] + t3_x * position[j, 2]
        car[j, 1] = t1_y * position[j, 0] + t2_y * position[j, 1] + t3_y * position[j, 2]
        car[j, 2] = t1_z * position[j, 0] + t2_z * position[j, 1] + t3_z * position[j, 2]

    ###############################################
    ## scale0 を掛けて car の絶対座標系へなおす
    ## ABS mode:
    ##     scale=1.0 とするので必須作業 (絶対座標記述の場合)
    ##
    ## non ABS mode:
    ##     VASP 用の POSCAR の car Mode の場合は
    ##     scale に関係なく内部座標は再スケールはない
    ##
    # if not ABS:
    #    # for VASP
    #    scale  = scale0
    #    scale0 = 1.0
    # else:
    #    # for RMC_POT
    #    scale = 1.0
    scale = 1.0

    for j in range(natom):
        position[j, 0] = car[j, 0] * scale0
        position[j, 1] = car[j, 1] * scale0
        position[j, 2] = car[j, 2] * scale0

    ###############################################
    ## 基本並進ベクトルをスケールしておく
    ## --> scale=1.0 とするため
    ##
    # if ABS:
    t1_x = t1_x * scale0
    t1_y = t1_y * scale0
    t1_z = t1_z * scale0

    t2_x = t2_x * scale0
    t2_y = t2_y * scale0
    t2_z = t2_z * scale0

    t3_x = t3_x * scale0
    t3_y = t3_y * scale0
    t3_z = t3_z * scale0

    t[0, 0] = t1_x
    t[1, 0] = t1_y
    t[2, 0] = t1_z

    t[0, 1] = t2_x
    t[1, 1] = t2_y
    t[2, 1] = t2_z

    t[0, 2] = t3_x
    t[1, 2] = t3_y
    t[2, 2] = t3_z

    scale = scale
    direct = False

    poscar = scale, t, natom, direct, position
    return poscar
