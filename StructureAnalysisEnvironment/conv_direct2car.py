# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# POSCAR の内部座標を direct 系から cartesian 系へ変換
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
################################################################################
#
# 2015.08.24
#  戻り値版と引数版の名前センスを他に統一(引数版*a, 戻り値版)
#  conv_direct2car0 --> conv_direct2cara  (引数版)
#  conv_direct2car1 --> conv_direct2car   (戻り値版)
#
#
# 2015.02.27
#  旧バージョン(引数版) を conv_direct2car0 へ名前変更
#  新バージョン(戻り値版) を conv_direct2car1 へ名前変更
#
#  2015.02.27 の時点で影響があるルーチン
#
# Vdirect2car.py:              scale,direct = SAE.conv_direct2car(ABS,scale,t,natom,direct,position)
# VfindBond.py:                scale,direct = SAE.conv_direct2car(ABS,scale,t,natom,direct,position)
# Vforce2md.py:                scale,direct = np.conv_direct2car(ABS,scale,t,natom,direct,position0)
# VmakeSuperCell2.py:          scale,direct = SAE.conv_direct2car(ABS,scale,t,natom,direct,position)
# VmodifyAtomPosition.py:      scale,direct = SAE.conv_direct2car(ABS,scale,t,natom,direct,position)
# Vplot_Crystal.py:            scale,direct = SAE.conv_direct2car(ABS,scale,t,natom,direct,position)
# Vplot_CrystalAnimePOSCAR.
#
# Rmove.py:                    scale,direct = SAE.conv_direct2car(ABS,scale,t,natom,direct,position)
# Rmove1.py:                   scale,direct = SAE.conv_direct2car(ABS,scale,t,natom,direct,position)
# RplotCrystal0.py:            SAE.conv_direct2car(ABS,scale,t,natom,direct,position)
# Rplot_Crystal.py:            scale,direct = SAE.conv_direct2car(ABS,scale,t,natom,direct,position)
# Rplot_CrystalAnimeCFG.py:    SAE.conv_direct2car(ABS,scale,t,natom,direct,position)
# VfindNN1_library1.py:        scale,direct = SAE.conv_direct2car(ABS,scale,t,natom,direct,position)py
#
# 2015.02.27
# conv_direct2car_return.py を作成
#
# 2015.02.27
#  numpy の import を from 仕様をやめて import * as * に変更
#
# 2014.10.30/31 1st
#
################################################################################
from __future__ import print_function
try:
    from .copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.2"

################################################################################

import sys
# import os
# import re
# from numpy import *
# from copy import deepcopy
import numpy as np


################################################################################
# 引数はリストのリファレンスで受け取り、引数で配列の内容を[in/out]する仕様
# 少メモリ/高速仕様
#  注意) 2015.02.27: conv_direct2car --> conv_direct2car0 名前変更
#
def conv_direct2cara(ABS, scale0, t, natom, direct, position):
    """

    :param ABS:
    :param scale0:
    :param t:
    :param natom:
    :param direct:
    :param position:
    :return:
    """
    if not direct:
        sys.exit("STOP(conv_direct2car): current is not Direct.")

    ###############################################
    # 座標系を 1) direct --> cartesian
    #          2) cartesian のまま
    #
    # 変換後に scale して絶対座標にする
    # (入力がAngstrom 系なので A 単位になる)
    #
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
    # scale0 を掛けて car の絶対座標系へなおす
    # ABS mode:
    #     scale=1.0 とするので必須作業 (絶対座標記述の場合)
    #
    # non ABS mode:
    #     VASP 用の POSCAR の car Mode の場合は
    #     scale に関係なく内部座標は再スケールはない
    #     もし、VASPで scale=1.0 としてかえれば conv_scale21() を用いて scale=1.0 としてから
    #     direct to car を実行する
    #
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
    # 基本並進ベクトルをスケールしておく
    # --> scale=1.0 とするため
    #
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
# 引数はあくまで入力で、戻り値でアップデートした値を手にする方法論
# メモリ使用量が倍かかるし、その都度配列を作り直すので少し遅い
#
# conv_direct2car と同一仕様(戻り値が異なる)
#  ただし、ABS 仕様は消す
#
def conv_direct2car(scale0, t, natom, direct, position):
    if not direct:
        sys.exit("STOP(conv_direct2car): current is not Direct.")

    ###############################################
    # 座標系を 1) direct --> cartesian
    #          2) cartesian のまま
    #
    # 変換後に scale して絶対座標にする
    # (入力がAngstrom 系なので A 単位になる)
    #
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
    # scale0 を掛けて car の絶対座標系へなおす
    # ABS mode:
    #     scale=1.0 とするので必須作業 (絶対座標記述の場合)
    #
    # non ABS mode:
    #     VASP 用の POSCAR の car Mode の場合は
    #     scale に関係なく内部座標は再スケールはない
    #
    # if not ABS:
    #    # for VASP
    #    scale  = scale0
    #    scale0 = 1.0
    # else:
    #    # for RMC_POT
    #    scale = 1.0
    scale = scale0
    scale0 = 1.0

    for j in range(natom):
        position[j, 0] = car[j, 0] * scale0
        position[j, 1] = car[j, 1] * scale0
        position[j, 2] = car[j, 2] * scale0

    ###############################################
    ## 基本並進ベクトルをスケールしておく
    ## --> scale=1.0 とするため
    ##
    # if ABS:
    #    t1_x = t1_x*scale0
    #    t1_y = t1_y*scale0
    #    t1_z = t1_z*scale0
    #
    #    t2_x = t2_x*scale0
    #    t2_y = t2_y*scale0
    #    t2_z = t2_z*scale0
    #
    #    t3_x = t3_x*scale0
    #    t3_y = t3_y*scale0
    #    t3_z = t3_z*scale0

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

    # poscar = ABS,scale,t,natom,direct,position
    poscar = scale, t, natom, direct, position
    return poscar
