# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#
# 入力した原子種の通し番号の下限と上限を返す
# 入力する原子種の種別番号は 1 からスタート
#
# 一応VASP(POSCAR) 用だが、ion[j] のフォーマットが共通ならば全てのプログラムで使える
#
# [in]     atom1   : 原子種の種別番号（POSCAR の種別番号: 1から始まる--> サイト番号)
# [in]     nion    : 原子の種類数
#
# [in/out] atoms[i]: 原子の種類番号(max=nion)を与えると、その原子種の数を返す
#
# [return] start
# [return] end
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
from numpy import *


def get_atom_start(atom1, nion, atoms):
    atom1_0 = atom1 - 1

    k = 0
    for i in range(nion):
        if atom1 < 1:
            _legacy_error("STOP: unknown number, atom1 = " + str(atom1))
        if i == (atom1_0):
            start = k
            end = k + int(atoms[i]) - 1
        k = k + int(atoms[i])

    #   print "==="
    #   print "k_start", start
    #   print "k_end",   end
    #   print "k_last", k

    return [start, end]
