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
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.1.1"
################################################################################
#
#from ase.io.xyz import *

from ase.io.wien2k import *  ## using cellconst
from ase import Atoms

#import os
#import sys
#import optparse
import numpy as np

#import StructureAnalysisEnvironment as SAEnv


################################################################################
## 独自実装版
##
def conv_cell2conventional(atoms):
    return

################################################################################
## ASE 利用 & atoms はASEの構造
##
def conv_cell2conventional0(atoms):

    cell = atoms.get_cell()  # from ASE
    metT = np.dot(cell, np.transpose(cell))
    cell2 = cellconst(metT)  # from ASE module

    a = cell2[0]
    b = cell2[1]
    c = cell2[2]
    alpha = cell2[3]
    beta = cell2[4]
    gamma = cell2[5]

    natom = len(atoms.get_positions())

    return a,b,c,alpha,beta,gamma,natom

