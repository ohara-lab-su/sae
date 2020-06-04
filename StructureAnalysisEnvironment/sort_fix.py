#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# fix,sort_index_r を与えられたらその内容にしたがって fix をソートする
#
#  データー構造の特性上、計算コードを問わない
#
# sort_position との違いはデータータイプの違いだけ
#
################################################################################
#
# 2015.08.20
#  startup
#
################################################################################
from copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import numpy as np


# import copy
# import collections

def sort_fix(sort_index_r, fix):
    natom = len(fix)

    fix_s = np.zeros((natom, 3), dtype='S')
    for original in range(natom):
        sort = sort_index_r[original]
        fix_s[sort, :] = fix[original, :]

    return fix_s
