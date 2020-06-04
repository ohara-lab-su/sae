#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# position,sort_index_r を与えられたらその内容にしたがって position をソートする
#
#  データー構造の特性上、計算コードを問わない
#
################################################################################
#
# 2015.08.20
#  startup
#
################################################################################
try:
    from .copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import numpy as np


# import copy
# import collections

def sort_position(sort_index_r, position):
    natom = len(position)

    position_s = np.zeros((natom, 3))
    for original in range(natom):
        sort = sort_index_r[original]
        position_s[sort, :] = position[original, :]

    return position_s
