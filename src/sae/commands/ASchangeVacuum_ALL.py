#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import re
import os
import optparse
from ase.io import read, write
from ase.io.vasp import *
from ase.io.xyz import *
from ase.lattice.surface import *


def options():
    inpname = "POSCAR"
    outname = "POSCAR.vasp"
    vacuum = None
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-o", "--output", dest="OUTPUT")
    parser.add_option("-v", "--vacuum")
    options, args = parser.parse_args()
    if options.INPUT:
        inpname = options.INPUT
    if options.OUTPUT:
        outname = options.OUTPUT
    if options.vacuum:
        vacuum = float(options.vacuum)
    else:
        sys.exit("STOP: plase input vacuum size")
    if inpname == outname:
        sys.exit("STOP: (IN)" + inpname + ", (OUT)" + outputname)
    return [inpname, outname, vacuum]


if __name__ == "__main__":
    inpname, outname, vacuum = options()
    print("INPUT POSCAR file  = ", inpname)
    print("OUTPUT POSCAR file = ", outname)
    print("Vacuum SIZE        = ", str(vacuum))
    cell = read(inpname, format="vasp")
    if not vacuum is None:
        cell.center(vacuum=vacuum)
    cell.write(outname, format="vasp", direct=True, vasp5=True)
