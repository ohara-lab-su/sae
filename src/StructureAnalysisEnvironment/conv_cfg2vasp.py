# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# RMC_POT 形式の座標系からVASP形式の座標系へ変換
#   VASP 以外でも同じ、cartesian 系の並進＆内部座標系
#   基本並進ベクトル＆内部座標
#   scale factor は自動的に 1.0 になる( 1.0 としている)
#
#   RMC_POT 形式は direct mode のみ(のはず)
#
# [in]     scale          : scale
# [in]     natom          : number of atom
#
# [in]     direct         : Direct モードのみ対応なのは前提なので必要ない
#                           ただし、他のライブラリとの整合性のためにこの引数を入れる
#
# [in/out] t[3,3]         : 基本並進ベクトル(注意:配列内indexは0から)
#                                  x   y   z
#                            t1 = a11 a21 a31
#                            t2 = a12 a22 a32
#                            t3 = a13 a23 a33
#
# [in/out] position[j,3]  : 通し番号(max=natom)とx,y,z 指定で内部座標
#
# [return] scale          : scale
# [return] direct         : Direct mode は Trune を返す(一応)
#
################################################################################
#
# 2015.08.24
#  戻り値版と引数版のルールの再統一に合わせる
#    引数版 conv_cfg2vasp()  --> conv_cfg2vaspa()
#
# 2014.10.31 bug fix
# 2014.10.30 1st
#
################################################################################
from __future__ import print_function

from sae.errors import legacy_error as _legacy_error
try:
    from .copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import sys
import os
import re
import optparse
from numpy import *


# 戻り値版 (cfg2vaspa() <---> cfg2vasp() )
def conv_cfg2vaspa(scale, t, natom, direct, position):
    """
    :param scale:
    :param t:
    :param natom:
    :param direct:
    :param position:
    :return:
    """
    if not direct:
        _legacy_error("STOP: input file is not direct mode")

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
    ## DATA convert (RMC_POT to VASP )
    ##
    t1_x = t1_x * 2
    t1_y = t1_y * 2
    t1_z = t1_z * 2

    t2_x = t2_x * 2
    t2_y = t2_y * 2
    t2_z = t2_z * 2

    t3_x = t3_x * 2
    t3_y = t3_y * 2
    t3_z = t3_z * 2

    x_offset = 0.5
    y_offset = 0.5
    z_offset = 0.5

    # for Direct
    for i in range(int(natom)):
        position[i, 0] = position[i, 0] / 2 + x_offset
        position[i, 1] = position[i, 1] / 2 + y_offset
        position[i, 2] = position[i, 2] / 2 + z_offset

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
    direct = True
    return scale, direct
