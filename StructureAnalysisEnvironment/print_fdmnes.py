#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# VASP to FDMNES crystal 情報のルーチン
# FDMNES の構造書き出しルーチン
#
# using ASE version
#
# (注意)
#  1) ASE のmodule を呼び出している
#
################################################################################
#
# 2018.08.21
#  Python2/3 両対応
#
# 2015.05.18 startup
#
################################################################################
from __future__ import print_function

try:
    from copyright import *
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
import sys
# import optparse
# import numpy as np

import StructureAnalysisEnvironment as SAEnv


################################################################################
## 独自実装版
##
def print_fdmnes(outname='POSCAR', atoms=None, STD=True, MOL=False):
    return


################################################################################
## ASE 依存版 & atoms は ASEの構造
##
def print_fdmnes0(outname='POSCAR', atoms=None, STD=True, MOL=False):
    if STD:
        out = sys.stdout
    else:
        try:
            out = open(outname + '.fdmnes', 'w')
        except:
            out.close()
            sys.exit("STOP:" + outname + ".fdmnes file can't open")

    #   atoms = atoms2.copy()

    # 基本並進系のセル情報をコンベンショナル系に変換(atomsはASEの構造)
    a, b, c, alpha, beta, gamma, nat = SAEnv.conv_cellparam0(atoms)

    if MOL:
        print(" molecule", file=out)
    else:
        print(" Crystal", file=out)

    print("      %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f" % (a, b, c, alpha, beta, gamma), file=out)
    for ii in range(nat):
        zzn = atoms.get_atomic_numbers()[ii]
        # pos = atoms.get_positions()[ii]
        pos = atoms.get_scaled_positions()[ii]
        sym = atoms.get_chemical_symbols()[ii]
        print("   %2d %8.4f %8.4f %8.4f    ! %s" % (zzn, pos[0], pos[1], pos[2], sym), file=out)

    if not STD:
        out.close()


################################################################################
## ASE 依存版 & atoms(cell) は SAEnv の構造
##  ただし、conv_cellparam 内でまだASEを用いているので一部ASE依存
##
##  self.atoms_number_j
##  self.atoms_index_j
##  self.position
##
##  セルパラメータゲット: conv_cellparam*(cell)
##
def print_fdmnes1(outname='POSCAR', cell=None, STD=True, MOL=False):
    if STD:
        out = sys.stdout
    else:
        try:
            out = open(outname + '.fdmnes', 'w')
        except:
            out.close()
            sys.exit("STOP:" + outname + ".fdmnes file can't open")

    # 基本並進系のセル情報をコンベンショナル系に変換(atomsはASEの構造)
    a, b, c, alpha, beta, gamma, nat = SAEnv.conv_cellparam1(cell)

    if MOL:
        print(" molecule", file=out)
    else:
        print(" Crystal", file=out)

    print("      %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f" % (a, b, c, alpha, beta, gamma), file=out)
    for ii in range(nat):
        zzn = cell.atoms_number_j[ii]
        pos = cell.position[ii, :]
        sym = cell.atoms_index_j[ii]
        print("   %2d %8.4f %8.4f %8.4f    ! %s" % (zzn, pos[0], pos[1], pos[2], sym), file=out)

    if not STD:
        out.close()
