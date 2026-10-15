#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.fdmnes.structure_writer import FdmnesStructureWriter
from sae.structure.extract import StructureExtraction

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


if __name__ == "__main__":
    name = options()
    atoms = read(name, format="pdb")
    if StructureExtraction().chk_pdb_cryst1(name):
        MOL = False
    else:
        MOL = True
    FdmnesStructureWriter().print_fdmnes0(atoms=atoms, MOL=MOL)
    FdmnesStructureWriter().print_fdmnes0(name=name, atoms=atoms, STD=False, MOL=MOL)
