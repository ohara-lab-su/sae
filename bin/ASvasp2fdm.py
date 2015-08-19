#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# VASP to FDMNES crystal 情報
#
# using ASE version
#
# (注意)
#  1) ASE のルーチン(cellconst) を使っている
#  2) ASE のmodule を呼び出している
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

from ase import Atoms
from ase.io import read,write
from ase.io.vasp import *
from ase.io.wien2k import *  ## using cellconst

import os
import sys
import optparse
#import numpy as np

import StructureAnalysisEnvironment as SAEnv

################################################################################
def options():
    name = 'POSCAR'

    parser = optparse.OptionParser()
    parser.add_option( '-i','--ipput',dest='INPUT')
    parser.add_option( '-m','--mol',action='store_true',default=False)
    options,args = parser.parse_args()

    if options.INPUT: name = options.INPUT
    if len(args) > 0: name = str(args[0])

    if options.mol:
        MOL=True
    else:
        MOL=False

    if not os.path.exists(name):
        if os.path.exists(name+'.vasp'):
            name = name+'.vasp'
        else:
            sys.exit("STOP: "+name+" file not found")

    return [name,MOL]

################################################################################
if __name__ == '__main__':


    name,MOL = options()
    atoms = read_vasp(name)
    #atoms.write('POSCAR.pdb',format='pdb')

    #print atoms.positions
    #print ""
    #print atoms.cell
    #print ""
    #print atoms.get_scaled_positions()

    SAEnv.print_fdmnes0(atoms=atoms,MOL=MOL)
    SAEnv.print_fdmnes0(name=name,atoms=atoms,STD=False,MOL=MOL)
    SAEnv.write_fdmnes_inp0(atoms=atoms,MOL=MOL)

