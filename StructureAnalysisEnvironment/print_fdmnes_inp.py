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
# 2015.05.18 startup
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

#from ase.io.wien2k import *  ## using cellconst
#from ase import Atoms

#import os
import sys
#import optparse
#import numpy as np

import StructureAnalysisEnvironment as SAEnv

################################################################################
## 独自実装版
##
def print_fdmnes_inp(outname='read_pdb.inp',atoms=None,MOL=False):
    return

################################################################################
## ASE 依存版 & atoms が ASE の構造を持つ
##
def print_fdmnes_inp0(outname='read_pdb.inp',atoms=None,MOL=False):

    try:
        out = open(outname,'w')
    except:
        out.close()
        sys.exit("STOP:"+outname+".fdmnes file can't open")

    # 基本並進系のセル情報をコンベンショナル系に変換(atomsはASEの構造)
    a,b,c,alpha,beta,gamma,nat = SAEnv.conv_cellparam0(atoms)
#   atoms = atoms2.copy()

    print >> out, "! FDMNES indata file"
    print >> out, ""
    print >> out, " Absorber"
    print >> out, "  1"
    print >> out, "! allsite"
    print >> out, ""
    print >> out, " Filout"
    print >> out, "  Cu"
    print >> out, ""
    print >> out, " Range                        ! Energy range of calculation (eV)"
    print >> out, "  -15. 0.2  0. 0.5 10. 1. 45. ! first energy, step, intermediary energy, step ..., last energy"
    print >> out, "! -15. 0.1 50. 1. 200.        !"
    print >> out, ""
    print >> out, "!Energpho"
    print >> out, ""
    print >> out, " Edge"
    print >> out, "  K"
    print >> out, "! L23"
    print >> out, ""
    print >> out, " Relativism"
    print >> out, ""
    print >> out, "!Magnetism"
    print >> out, ""
    print >> out, "!Quadrupole"
    print >> out, ""
    print >> out, "!TDDFT"
    print >> out, ""
    print >> out, " Green"
    print >> out, ""
    print >> out, "!No_Fermi"
    print >> out, "! SCF"
    print >> out, ""
    print >> out, " Radius                       ! Radius of the cluster where final state calculation is performed"
    print >> out, "   3.0                         ! For a good calculation, this radius must be increased up to 6 or 7 Angstroems"
    print >> out, ""
    print >> out, " Memory_save"
    print >> out, ""

    if MOL:
        print >> out, " molecule"
    else:
        print >> out, " Crystal"

    print >> out, "      %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f" % ( a,b,c,alpha,beta,gamma )
    for ii in range(nat):
        zzn = atoms.get_atomic_numbers()[ii]
       #pos = atoms.get_positions()[ii]
        pos = atoms.get_scaled_positions()[ii]
        sym = atoms.get_chemical_symbols()[ii]
        print >> out, "   %2d %8.4f %8.4f %8.4f    ! %s"  % ( zzn,pos[0],pos[1],pos[2],sym )

    print >> out, ""
    print >> out, " Density"
    print >> out, "  state_all"
    print >> out, ""
    print >> out, "!Adimp"
    print >> out, "! 0.20"
    print >> out, ""
    print >> out, " Convolution"
    print >> out, ""
    print >> out, "!Nonexc"
    print >> out, ""
    print >> out, " End"
    print >> out, ""

    out.close()

################################################################################
## ASE 依存版 & atoms が SAEnv の構造を持つ
##  ただし、conv_cellparam  内でまだASEを用いているので一部ASE依存版
##
##  self.atoms_number_j
##  self.atoms_index_j
##  self.position
##
##  セルパラメータゲット: conv_cellparam*(cell)
##
def print_fdmnes_inp1(outname='read_pdb.inp',cell=None,MOL=False):

    try:
        out = open(outname,'w')
    except:
        out.close()
        sys.exit("STOP:"+outname+".fdmnes file can't open")

    # 基本並進系のセル情報をコンベンショナル系に変換(cellはASEの構造)
    a,b,c,alpha,beta,gamma,nat = SAEnv.conv_cellparam1(cell)
#   atoms = atoms2.copy()

    print >> out, "! FDMNES indata file"
    print >> out, ""
    print >> out, " Absorber"
    print >> out, "  1"
    print >> out, "! allsite"
    print >> out, ""
    print >> out, " Filout"
    print >> out, "  Cu"
    print >> out, ""
    print >> out, " Range                        ! Energy range of calculation (eV)"
    print >> out, "  -15. 0.2  0. 0.5 10. 1. 45. ! first energy, step, intermediary energy, step ..., last energy"
    print >> out, "! -15. 0.1 50. 1. 200.        !"
    print >> out, ""
    print >> out, "!Energpho"
    print >> out, ""
    print >> out, " Edge"
    print >> out, "  K"
    print >> out, "! L23"
    print >> out, ""
    print >> out, " Relativism"
    print >> out, ""
    print >> out, "!Magnetism"
    print >> out, ""
    print >> out, "!Quadrupole"
    print >> out, ""
    print >> out, "!TDDFT"
    print >> out, ""
    print >> out, " Green"
    print >> out, ""
    print >> out, "!No_Fermi"
    print >> out, "! SCF"
    print >> out, ""
    print >> out, " Radius                       ! Radius of the cluster where final state calculation is performed"
    print >> out, "   3.0                         ! For a good calculation, this radius must be increased up to 6 or 7 Angstroems"
    print >> out, ""
    print >> out, " Memory_save"
    print >> out, ""

    if MOL:
        print >> out, " molecule"
    else:
        print >> out, " Crystal"

    print >> out, "      %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f" % ( a,b,c,alpha,beta,gamma )
    for ii in range(nat):
        zzn = cell.atoms_number_j[ii]
        pos = cell.position[ii,:]
        sym = cell.atoms_index_j[ii]
        print >> out, "   %2d %8.4f %8.4f %8.4f    ! %s"  % ( zzn,pos[0],pos[1],pos[2],sym )

    print >> out, ""
    print >> out, " Density"
    print >> out, "  state_all"
    print >> out, ""
    print >> out, "!Adimp"
    print >> out, "! 0.20"
    print >> out, ""
    print >> out, " Convolution"
    print >> out, ""
    print >> out, " End"
    print >> out, ""

    out.close()


