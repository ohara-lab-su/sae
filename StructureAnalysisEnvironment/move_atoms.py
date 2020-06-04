# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# カーテシアンモードになっている必要がある
#  list_atoms に従い原子を動かす(単位は Ang )
#
#  入力はcartesian-実座標系
#  プログラム中で cartesian-position系(内部座標系)に変換する
#  スケールファクターはなんでも良い(positionと同じファクターであれば良い)
#
#  原子移動時に衝突のチェックはしてないので注意
#
# [in]     scale          : スケーリングファクター
# [in/out] t[3,3]         :  基本並進ベクトル(注意:配列内indexは0から)
#                                  x   y   z
#                            t1 = a11 a21 a31
#                            t2 = a12 a22 a32
#                            t3 = a13 a23 a33
#
# [in]     direct          : direct or cartesian
#
# [in/out] position(i,3)  : 内部座標
# [in/out] move_atoms(i,4) : 移動原子リスト(原子の番号,移動距離Ang_x, Ang_y, Ang_z)
#
# [return] scale
#
################################################################################
#
# 2014.11.05 1st
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
import os
import re
from numpy import *


## スケールファクターでリスケールしている
## [カーテシアン＋スケールファクター有り]の場合実座標化
##
def move_atoms1(scale, t, direct, position, nlist, list_atoms):
    if direct:
        sys.exit("STOP: direct mode")

    for i in range(nlist):
        # 実座標系 list_atom を内部座標系 new_{x,y,z} に直すために 1/scale を掛ける
        atom = int(list_atoms[i, 0]) - 1
        new_x = list_atoms[i, 1] / scale
        new_y = list_atoms[i, 2] / scale
        new_z = list_atoms[i, 3] / scale

        # 内部座標系 position + 内部座標系 new_{x,y,z}
        position[atom, 0] = position[atom, 0] + new_x
        position[atom, 1] = position[atom, 1] + new_y
        position[atom, 2] = position[atom, 2] + new_z

    return scale


## リスケールなし (そのまま)
def move_atoms0(scale, t, direct, position, nlist, list_atoms):
    if direct:
        sys.exit("STOP: direct mode")

    for i in range(nlist):
        # 実座標系 list_atom を内部座標系 new_{x,y,z} に直すために 1/scale を掛ける
        atom = int(list_atoms[i, 0]) - 1
        new_x = list_atoms[i, 1]
        new_y = list_atoms[i, 2]
        new_z = list_atoms[i, 3]

        # 内部座標系 position + 内部座標系 new_{x,y,z}
        position[atom, 0] = position[atom, 0] + new_x
        position[atom, 1] = position[atom, 1] + new_y
        position[atom, 2] = position[atom, 2] + new_z

    return scale
