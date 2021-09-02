#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# PDB to FDMNES crystal 情報
#
#  using ASE version
#
################################################################################
#
# 2015.08.20
#  関数分離(ごく一部だけASE分離)
#
# 2015.05.18 startup
#
################################################################################
from __future__ import print_function
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

import os
import sys
import optparse
# import numpy as np

from ase.io import read
import StructureAnalysisEnvironment as SAE

################################################################################
def options():
    name = 'POSCAR.pdb'

    parser = optparse.OptionParser()
    parser.add_option( '-i','--ipput',dest='INPUT')
    options,args = parser.parse_args()

    if options.INPUT: name = options.INPUT
    if len(args) > 0: name = str(args[0])

    if not os.path.exists(name):
        sys.exit("STOP: "+name+" file not found")

    return name

################################################################################
if __name__ == '__main__':

    name = options()

    atoms = read(name,format='pdb')

#   print "atoms.cell"
#   print atoms.cell
#   print atoms.cellpar
#   print ""
#   print "atoms.positions"
#   print atoms.positions
#   print ""
#   print "atoms.gt_scaled_positions"
#   print atoms.get_scaled_positions()

    if SAEnv.chk_pdb_cryst1(name):
        MOL=False
    else:
        MOL=True

    SAEnv.print_fdmnes0(atoms=atoms,MOL=MOL)
    SAEnv.print_fdmnes0(name=name,atoms=atoms,STD=False,MOL=MOL)

