#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# 基本並進のセルをコンベンショナルセルに変換する
#  using ASE cellconst routine
#  (ASE の cell インスタンスを読む)
#
# (注意)
#  1) ASE のルーチン(cellconst) を使っている
#  2) ASE のmodule を呼び出している
#
################################################################################
#
# 2015.05.19 startup
#
################################################################################
from __future__ import print_function
try:
    from .copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.1.1"

################################################################################
#
# from ase.io.xyz import *

from ase.io.wien2k import *  ## using cellconst
from ase import Atoms

# import os
# import sys
# import optparse
import numpy as np


# import StructureAnalysisEnvironment as SAEnv


################################################################################
## 独自実装版
##
def conv_cellparam(atoms):
    return


################################################################################
## ASE 利用 & atoms はASEの構造
##
def conv_cellparam0(atoms):
    cell = atoms.get_cell()  # from ASE ( translation vector)
    metT = np.dot(cell, np.transpose(cell))
    cell2 = cellconst(metT)  # from ASE module

    a = cell2[0]
    b = cell2[1]
    c = cell2[2]
    alpha = cell2[3]
    beta = cell2[4]
    gamma = cell2[5]

    natom = len(atoms.get_positions())

    return a, b, c, alpha, beta, gamma, natom


################################################################################
## ASE 利用 & atoms(cell) は SAEnv の構造
##
def conv_cellparam1(cell):
    t = cell.t
    metT = np.dot(t, np.transpose(t))
    param = cellconst(metT)  # from ASE module

    a = param[0]
    b = param[1]
    c = param[2]
    alpha = param[3]
    beta = param[4]
    gamma = param[5]

    natom = cell.natom

    return a, b, c, alpha, beta, gamma, natom
