#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.openmx.md_fields import MolecularDynamicsFields

#!/usr/bin/env python
# -*- coding: utf-8 -*-   
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2014.11.17
#    MD ファイル(x,y,z)読み込み
#    注意) LOOP 構造を持つ x,y,z 形式のみ対応
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import numpy as np

#                                                                                         
################################################################################
#import sys
#import os
#import re
#import SpaceGroupEnvironment as SGE 
#from numpy import *
#from LIB_vasp.read_md_param import *
#from LIB_vasp.read_md import *
################################################################################
###########################################
###########################################
# MD(xyz) ファイルの事前読み込み
# MD(xyz) ファイルの事前準備
# MD(xyz) ファイル読み込み
if __name__ == "__main__":
    cname = "C60_position.xyz"
    nloop, natom = MolecularDynamicsFields().read_md_param(cname)
    position_loop = np.zeros((nloop, natom, 3))
    print("NLOOP :", nloop)
    print("NATOM :", natom)
    # 通し番号(max=atom)で元素名(記号)を保存する
    atoms_index_j = np.zeros(natom, dtype="S2")
    # 原子のx,y,z 座標
    position_loop = np.zeros((nloop, natom, 3))
    MolecularDynamicsFields().read_md(cname, nloop, natom, atoms_index_j, position_loop)
    for l in range(nloop):
        print("------- LOOP " + str(l) + " ------")
        for j in range(natom):
            print(
                " %3s %14.10f %14.10f %14.10f "
                % (
                    atoms_index_j[j],
                    position_loop[l, j, 0],
                    position_loop[l, j, 1],
                    position_loop[l, j, 2],
                )
            )
