#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# VASP to FDMNES crystal 情報 関係の出力ルーチン
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

from sae.errors import legacy_error as _legacy_error

try:
    from .copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.1.1"

################################################################################
#
# from ase.io.xyz import *

# from ase.io.wien2k import *  ## using cellconst
# from ase import Atoms

# import os
import sys
# import optparse
import numpy as np

import StructureAnalysisEnvironment as SAEnv


################################################################################
## 独自実装版
##
def print_fdmnes_inp(outname='read_pdb.inp', atoms=None, MOL=False):
    return


################################################################################
## ASE 依存版 & atoms が ASE の構造を持つ
##
def print_fdmnes_inp0(outname='read_pdb.inp', atoms=None, MOL=False):
    try:
        out = open(outname, 'w')
    except:
        out.close()
        _legacy_error("STOP:" + outname + ".fdmnes file can't open")

    # 基本並進系のセル情報をコンベンショナル系に変換(atomsはASEの構造)
    a, b, c, alpha, beta, gamma, nat = SAEnv.conv_cellparam0(atoms)
    #   atoms = atoms2.copy()

    print("! FDMNES indata file", file=out)
    print("", file=out)
    print("!Nonexc", file=out)
    print("", file=out)
    print(" Absorber", file=out)
    print("  1", file=out)
    print("! allsite", file=out)
    print("", file=out)
    print(" Filout", file=out)
    print("  Cu", file=out)
    print("", file=out)
    print(" Range                        ! Energy range of calculation (eV)", file=out)
    print("  -15. 0.2  0. 0.5 10. 1. 45. ! first energy, step, intermediary energy, step ..., last energy", file=out)
    print("! -15. 0.1 50. 1. 200.        !", file=out)
    print("", file=out)
    print("!Energpho", file=out)
    print("", file=out)
    print(" Edge", file=out)
    print("  K", file=out)
    print("! L23", file=out)
    print("", file=out)
    print("!Quadrupole", file=out)
    print("", file=out)
    print(" Relativism", file=out)
    print("", file=out)
    print(" Convolution", file=out)
    print("", file=out)
    print("!No_Fermi", file=out)
    print("!Efermi", file=out)
    print("!  -6.0", file=out)
    print("!Estart", file=out)
    print("! -10.0", file=out)
    print("", file=out)
    print("!SCF", file=out)
    print("!R_self", file=out)
    print("! 5.0", file=out)
    print("!N_self", file=out)
    print("! 100", file=out)
    print("!P_self", file=out)
    print("! 0.05", file=out)
    print("!Delta_E_conv", file=out)
    print("! 0.01", file=out)
    print("", file=out)
    print("!Magnetism", file=out)
    print("!SCF_mag_free", file=out)
    print("", file=out)
    print("!Hubbard", file=out)
    print("! 0.0 6.3 0.0", file=out)
    print("", file=out)
    print("!TDDFT", file=out)
    print("", file=out)
    print("!Green", file=out)
    print("", file=out)
    print(" Radius                       ! Radius of the cluster where final state calculation is performed", file=out)
    print(
        "   5.0                         ! For a good calculation, this radius must be increased up to 6 or 7 Angstroems",
        file=out)
    print("", file=out)
    print(" Memory_save", file=out)
    print("", file=out)

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

    print("", file=out)
    print(" Density", file=out)
    print("  state_all", file=out)
    print("", file=out)
    print("!Adimp", file=out)
    print("! 0.20", file=out)
    print("", file=out)
    print(" End", file=out)
    print("", file=out)

    out.close()


################################################################################
## ASE 依存版 & atoms が SAE の構造を持つ
##  ただし、conv_cellparam  内でまだASEを用いているので一部ASE依存版
##
##  self.atoms_number_j
##  self.atoms_index_j
##  self.position
##
##  セルパラメータゲット: conv_cellparam*(cell)
##
def print_fdmnes_inp1(outname='read_pdb.inp', cell=None, MOL=False):
    try:
        out = open(outname, 'w')
    except:
        out.close()
        _legacy_error("STOP:" + outname + ".fdmnes file can't open")

    # 基本並進系のセル情報をコンベンショナル系に変換(cellはASEの構造)
    a, b, c, alpha, beta, gamma, nat = SAEnv.conv_cellparam1(cell)
    #   atoms = atoms2.copy()

    print("! FDMNES indata file", file=out)
    print("", file=out)
    print("!Nonexc", file=out)
    print("", file=out)
    print(" Absorber", file=out)
    print("  1", file=out)
    print("! allsite", file=out)
    print("", file=out)
    print(" Filout", file=out)
    print("  Cu", file=out)
    print("", file=out)
    print(" Range                        ! Energy range of calculation (eV)", file=out)
    print("  -15. 0.2  0. 0.5 10. 1. 45. ! first energy, step, intermediary energy, step ..., last energy", file=out)
    print("! -15. 0.1 50. 1. 200.        !", file=out)
    print("", file=out)
    print("!Energpho", file=out)
    print("", file=out)
    print(" Edge", file=out)
    print("  K", file=out)
    print("! L23", file=out)
    print("", file=out)
    print("!Quadrupole", file=out)
    print("", file=out)
    print(" Relativism", file=out)
    print("", file=out)
    print(" Convolution", file=out)
    print("", file=out)
    print("!No_Fermi", file=out)
    print("!Efermi", file=out)
    print("!  -6.0", file=out)
    print("!Estart", file=out)
    print("! -10.0", file=out)
    print("", file=out)
    print("!SCF", file=out)
    print("!R_self", file=out)
    print("! 5.0", file=out)
    print("!N_self", file=out)
    print("! 100", file=out)
    print("!P_self", file=out)
    print("! 0.05", file=out)
    print("!Delta_E_conv", file=out)
    print("! 0.01", file=out)
    print("", file=out)
    print("!Magnetism", file=out)
    print("!SCF_mag_free", file=out)
    print("", file=out)
    print("!Hubbard", file=out)
    print("! 0.0 6.3 0.0", file=out)
    print("", file=out)
    print("!TDDFT", file=out)
    print("", file=out)
    print("!Green", file=out)
    print("", file=out)
    print(" Radius                       ! Radius of the cluster where final state calculation is performed", file=out)
    print(
        "   5.0                         ! For a good calculation, this radius must be increased up to 6 or 7 Angstroems",
        file=out)
    print("", file=out)
    print(" Memory_save", file=out)
    print("", file=out)

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

    print("", file=out)
    print(" Density", file=out)
    print("  state_all", file=out)
    print("", file=out)
    print("!Adimp", file=out)
    print("! 0.20", file=out)
    print("", file=out)
    print(" End", file=out)
    print("", file=out)

    out.close()
