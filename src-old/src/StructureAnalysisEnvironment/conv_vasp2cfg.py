# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# VPAS 形式での座標から RMC_POT 形式の座標系への変換
#   基本並進ベクトル＆内部座標
#
# [in]     scale          : スケールファクター
# [in/out] t[3,3]         : 基本並進ベクトル(注意:配列内indexは0から)
#                                  x   y   z
#                            t1 = a11 a21 a31
#                            t2 = a12 a22 a32
#                            t3 = a13 a23 a33
#
# [in]     natom          : number of atom
# [in/out] position[j,3]  : 通し番号(max=natom)とx,y,z 指定で内部座標
#
# [return] scale          : direct mode は True を返す
# [return] direct         : direct mode は True を返す
#
################################################################################
#
# 2015.08.24
#  戻り値版と引数版のルールの再統一に合わせる
#   引数版   conv_vasp2cfg()  --> conv_vasp2cfga()
#   戻り値版 conv_vasp2cfg1() --> conv_vasp2cfg()
#
# 2015.03.10
#  戻り値と引数を1:1にしたバージョンの関数を作成
#   conv_vasp2cfg
#
# 2014.10.31 bug fix
# 2014.10.30 1st
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
# import optparse
# from numpy import *


################################################################################
# 引数版
def conv_vasp2cfga(scale0, t, natom, direct, position):
    if not direct:
        sys.exit("STOP: input file is not direct mode")

    t1_x = t[0, 0]
    t1_y = t[1, 0]
    t1_z = t[2, 0]

    t2_x = t[0, 1]
    t2_y = t[1, 1]
    t2_z = t[2, 1]

    t3_x = t[0, 2]
    t3_y = t[1, 2]
    t3_z = t[2, 2]

    ###############################################
    ## data convert for cfg (RMC_POT) format
    ## from direct to direct coordinate
    ##
    t1_x = scale0 * t1_x / 2.0
    t1_y = scale0 * t1_y / 2.0
    t1_z = scale0 * t1_z / 2.0
    t2_x = scale0 * t2_x / 2.0
    t2_y = scale0 * t2_y / 2.0
    t2_z = scale0 * t2_z / 2.0
    t3_x = scale0 * t3_x / 2.0
    t3_y = scale0 * t3_y / 2.0
    t3_z = scale0 * t3_z / 2.0

    x_offset = 0.5
    y_offset = 0.5
    z_offset = 0.5

    for j in range(int(natom)):
        position[j, 0] = (position[j, 0] - x_offset) * 2.0
        position[j, 1] = (position[j, 1] - y_offset) * 2.0
        position[j, 2] = (position[j, 2] - z_offset) * 2.0
    # print " %16.12f %16.12f %16.12f" %(position[j,0],position[j,1],position[j,2])

    t[0, 0] = t1_x
    t[1, 0] = t1_y
    t[2, 0] = t1_z

    t[0, 1] = t2_x
    t[1, 1] = t2_y
    t[2, 1] = t2_z

    t[0, 2] = t3_x
    t[1, 2] = t3_y
    t[2, 2] = t3_z

    scale = 1.0
    direct = True
    return [scale, direct]


################################################################################
# 戻り値版
#
def conv_vasp2cfg(scale0, t, natom, direct, position):
    if not direct:
        sys.exit("STOP: input file is not direct mode")

    t1_x = t[0, 0]
    t1_y = t[1, 0]
    t1_z = t[2, 0]

    t2_x = t[0, 1]
    t2_y = t[1, 1]
    t2_z = t[2, 1]

    t3_x = t[0, 2]
    t3_y = t[1, 2]
    t3_z = t[2, 2]

    ###############################################
    ## data convert for cfg (RMC_POT) format
    ## from direct to direct coordinate
    ##
    t1_x = scale0 * t1_x / 2.0
    t1_y = scale0 * t1_y / 2.0
    t1_z = scale0 * t1_z / 2.0
    t2_x = scale0 * t2_x / 2.0
    t2_y = scale0 * t2_y / 2.0
    t2_z = scale0 * t2_z / 2.0
    t3_x = scale0 * t3_x / 2.0
    t3_y = scale0 * t3_y / 2.0
    t3_z = scale0 * t3_z / 2.0

    x_offset = 0.5
    y_offset = 0.5
    z_offset = 0.5

    for j in range(int(natom)):
        position[j, 0] = (position[j, 0] - x_offset) * 2.0
        position[j, 1] = (position[j, 1] - y_offset) * 2.0
        position[j, 2] = (position[j, 2] - z_offset) * 2.0
    # print " %16.12f %16.12f %16.12f" %(position[j,0],position[j,1],position[j,2])

    t[0, 0] = t1_x
    t[1, 0] = t1_y
    t[2, 0] = t1_z

    t[0, 1] = t2_x
    t[1, 1] = t2_y
    t[2, 1] = t2_z

    t[0, 2] = t3_x
    t[1, 2] = t3_y
    t[2, 2] = t3_z

    scale = 1.0
    direct = True
    return scale, t, natom, direct, position
