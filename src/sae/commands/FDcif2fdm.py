#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function

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
# 2018.08.17
#  Python2/3 両対応
#
# 2015.05.18 startup
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
from ase import Atoms
from ase.io import read, write
from ase.io.vasp import *
from ase.io.wien2k import *
import os
import sys
import optparse


#
################################################################################
#
#from ase.io.xyz import *
## using cellconst
#import numpy as np
################################################################################
def options():
    name = "POSCAR.cif"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--ipput", dest="INPUT")
    parser.add_option("-m", "--mol", action="store_true", default=False)
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = str(args[0])
    if options.mol:
        MOL = True
    else:
        MOL = False
    if not os.path.exists(name):
        if os.path.exists(name + ".vasp"):
            name = name + ".vasp"
        else:
            sys.exit("STOP: " + name + " file not found")
    return [name, MOL]


################################################################################
#atoms.write('POSCAR.pdb',format='pdb')
#print atoms.positions
#print ""
#print atoms.cell
#print ""
#print atoms.get_scaled_positions()
# bug version につきコメントアウト
#
#    SAE.print_fdmnes0(atoms=atoms,MOL=MOL)
#    SAE.print_fdmnes0(name=name,atoms=atoms,STD=False,MOL=MOL)
#    SAE.write_fdmnes_inp0(atoms=atoms,MOL=MOL)
if __name__ == "__main__":
    name, MOL = options()
    atoms = read(name, format="cif")
    print("bug version")
