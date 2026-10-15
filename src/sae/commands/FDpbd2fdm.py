#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.fdmnes.structure_writer import FdmnesStructureWriter
from sae.structure.extract import StructureExtraction

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
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import os
import sys
import optparse
from ase.io import read


#
################################################################################
# import numpy as np
################################################################################
def options():
    name = "POSCAR.pdb"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--ipput", dest="INPUT")
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = str(args[0])
    if not os.path.exists(name):
        sys.exit("STOP: " + name + " file not found")
    return name


################################################################################
#   print "atoms.cell"
#   print atoms.cell
#   print atoms.cellpar
#   print ""
#   print "atoms.positions"
#   print atoms.positions
#   print ""
#   print "atoms.gt_scaled_positions"
#   print atoms.get_scaled_positions()
if __name__ == "__main__":
    name = options()
    atoms = read(name, format="pdb")
    if StructureExtraction().chk_pdb_cryst1(name):
        MOL = False
    else:
        MOL = True
    FdmnesStructureWriter().print_fdmnes0(atoms=atoms, MOL=MOL)
    FdmnesStructureWriter().print_fdmnes0(name=name, atoms=atoms, STD=False, MOL=MOL)
