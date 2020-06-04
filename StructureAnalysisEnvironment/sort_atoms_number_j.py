#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# atoms_number_j を与えられたらその内容をグルーピングして
#
#  1) atoms および atoms_number, atoms_index を作成
#  2) グルーピング前の atoms_number_j と グルーピング後の atoms_number
#     の対応 index 情報を作る
#
#     sort_index   : sort_index --> original_index
#     sort_index_r : original_index --> sort_index
#
#  データー構造の特性上、計算コードを問わない
#
################################################################################
#
# 2015.08.20
#  startup
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

import numpy as np
# import copy
import collections

import StructureAnalysisEnvironment as SAEnv


################################################################################
#
def sort_atom_number_j(atoms_number_j):
    natom = len(atoms_number_j)

    # ION 数および atoms, atoms_index の作成
    counter = collections.Counter(atoms_number_j)
    nion = len(counter)
    atoms = np.zeros(nion, dtype=int)
    atoms_index = []
    atoms_number = np.zeros(nion, dtype=int)
    i = 0
    for number, cnt in counter.most_common():
        atoms_index.append(SAEnv.get_atomic_symbol0(int(number)))
        atoms_number[i] = int(number)
        atoms[i] = cnt
        i += 1

    # ソート用のindexの作成
    sort_index = np.zeros(natom, dtype=int)  # sort_index --> original_index
    sort_index_r = np.zeros(natom, dtype=int)  # original_index --> sort_index
    for i in range(natom):
        index = 0  # sort+index
        for k in range(nion):
            for j in range(natom):  # original_index
                if atoms_number[k] == atoms_number_j[j]:
                    sort_index[index] = j
                    sort_index_r[j] = index
                    index += 1

    #   print sort_index
    #   print sort_index_r

    #   position_s = np.zeros((natom,3))
    #   for original in range(natom):
    #       sort = sort_index_r[original]
    #       position_s[sort,:] = position[original,:]

    atoms_number_js = np.zeros(natom, dtype=float)
    for original in range(natom):
        sort = sort_index_r[original]
        atoms_number_js[sort] = atoms_number_j[original]

    #   print atoms_index_js

    return sort_index, sort_index_r, atoms, atoms_index, atoms_number_j
