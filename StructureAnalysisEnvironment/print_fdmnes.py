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

from ase.io.wien2k import *  ## using cellconst
from ase import Atoms

#import os
import sys
#import optparse
#import numpy as np

import StructureAnalysisEnvironment as SAEnv

################################################################################
## 独自実装版
##
def print_fdmnes(name='POSCAR',atoms=None,STD=True,MOL=False):
    return

################################################################################
## ASE 依存版 & atoms は ASEの構造
##
def print_fdmnes0(name='POSCAR',atoms=None,STD=True,MOL=False):

    if STD:
        out = sys.stdout
    else:
        try:
            out = open(name+'.fdmnes','w')
        except:
            out.close()
            sys.exit("STOP:"+name+".fdmnes file can't open")

#   atoms = atoms2.copy()

    # 基本並進系のセル情報をコンベンショナル系に変換(atomsはASEの構造)
    a,b,c,alpha,beta,gamma,nat = SAEnv.conv_cell2conventional0(atoms)

    if MOL:
        print >> out, " molecule"
    else:
        print >> out, " Crystal"

    print >> out, "      %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f" % ( a,b,c,alpha,beta,gamma )
    for ii in range(nat):
        zza = atoms.get_atomic_numbers()[ii]
       #pos = atoms.get_positions()[ii]
        pos = atoms.get_scaled_positions()[ii]
        sym = atoms.get_chemical_symbols()[ii]
        print >> out, "   %2d %8.4f %8.4f %8.4f    ! %s"  % ( zza,pos[0],pos[1],pos[2],sym )

    if not STD:
        out.close()

################################################################################
## ASE 依存版 & atoms(cell) は SAEnv の構造
##
def print_fdmnes1(name='POSCAR',cell=None,STD=True,MOL=False):

    if STD:
        out = sys.stdout
    else:
        try:
            out = open(name+'.fdmnes','w')
        except:
            out.close()
            sys.exit("STOP:"+name+".fdmnes file can't open")

#   atoms = atoms2.copy()

    # 基本並進系のセル情報をコンベンショナル系に変換(atomsはASEの構造)
    a,b,c,alpha,beta,gamma,nat = SAEnv.conv_cell2conventional1(cell)

    if MOL:
        print >> out, " molecule"
    else:
        print >> out, " Crystal"

    print >> out, "      %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f" % ( a,b,c,alpha,beta,gamma )
    for ii in range(nat):
        zza = atoms.get_atomic_numbers()[ii]
        pos = cell.position[ii,:]
        sym = cell.atoms_index_j[ii]
        print >> out, "   %2d %8.4f %8.4f %8.4f    ! %s"  % ( zza,pos[0],pos[1],pos[2],sym )

    if not STD:
        out.close()

