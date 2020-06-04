# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# scale ファクターフリー(VASP形式) の cartesian 形式から
# scale でスケールした cartesian 形式(scale=1.0) へ変換する
#
#  1) スケールファクター を 1 にする
#  2) 内部座標もスケール(絶対座標系)
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
#
################################################################################
#
# 2015.08.24
#  関数名のるーるを再統一化
#   引数版   conv_car2carABS  --> conv_car2carABSa
#   戻り値版 conv_car2carABS1 --> conv_car2carABS
#
#
# 2015.03.09
#  戻り値のルールを変更したバージョン conv_car2carABS1 を用意
#
# 2014.11.12 1st
#
################################################################################
from __future__ import print_function

try:
    from .copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import sys
# import os
# import re
import numpy as np


# from copy import deepcopy


################################################################################
# 引数版
def conv_car2carABSa(scale0, t, natom, direct, position):
    if direct:
        sys.exit("STOP: current is Direct.")

    t1_x = t[0, 0]
    t1_y = t[1, 0]
    t1_z = t[2, 0]

    t2_x = t[0, 1]
    t2_y = t[1, 1]
    t2_z = t[2, 1]

    t3_x = t[0, 2]
    t3_y = t[1, 2]
    t3_z = t[2, 2]

    # スケールファクターを 1.0 にする
    scale = 1.0

    # 内部座標のスケール
    for j in range(natom):
        position[j, 0] = position[j, 0] * scale0
        position[j, 1] = position[j, 1] * scale0
        position[j, 2] = position[j, 2] * scale0

    # 基本並進ベクトルのスケール
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

    return scale


################################################################################
# 戻り値版
#
def conv_car2carABS(scale0, t, natom, direct, position):
    if direct:
        sys.exit("STOP: current is Direct.")

    t1_x = t[0, 0]
    t1_y = t[1, 0]
    t1_z = t[2, 0]

    t2_x = t[0, 1]
    t2_y = t[1, 1]
    t2_z = t[2, 1]

    t3_x = t[0, 2]
    t3_y = t[1, 2]
    t3_z = t[2, 2]

    # スケールファクターを 1.0 にする
    scale = 1.0

    # 内部座標のスケール
    p = np.zeros((natom, 3))
    for j in range(natom):
        p[j, 0] = position[j, 0] * scale0
        p[j, 1] = position[j, 1] * scale0
        p[j, 2] = position[j, 2] * scale0

    # 基本並進ベクトルのスケール
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

    return [scale, t, natom, direct, p]
