# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# スーパーセル用の
#     1) 基本並進ベクトル
#     2) 原子種数
#
# を作成するモジュール
#
# [in]      super_x
# [in]      super_y
# [in]      super_z
#
# [in/out] atoms[i]   : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
#
# [in]     nion       : 原子種の数
# [in/out] atoms[i]   : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
#
# [in/out] t[3,3]     :  基本並進ベクトル(注意:配列内indexは0から)
#                              x   y   z
#                        t1 = a11 a21 a31
#                        t2 = a12 a22 a32
#                        t3 = a13 a23 a33
#
################################################################################
#
# 2014.10.31
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

import sys
import os
from numpy import *


def make_supercell_param(super_x, super_y, super_z, nion, atoms, t):
    t[0, 0] = t[0, 0] * super_x  # t1_x
    t[1, 0] = t[1, 0] * super_y  # t1_y
    t[2, 0] = t[2, 0] * super_z  # t1_z

    t[0, 1] = t[0, 1] * super_x  # t2_x
    t[1, 1] = t[1, 1] * super_y  # t2_y
    t[2, 1] = t[2, 1] * super_z  # t2_z

    t[0, 2] = t[0, 2] * super_x  # t3_x
    t[1, 2] = t[1, 2] * super_y  # t3_y
    t[2, 2] = t[2, 2] * super_z  # t3_z

    for j in range(nion):
        atoms[j] = int(atoms[j]) * super_x * super_y * super_z
