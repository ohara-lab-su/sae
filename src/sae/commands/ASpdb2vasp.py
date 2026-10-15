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


def options():
    base = "case"
    in_suffix = ".pdb"
    out_suffix = ".vasp"
    name = base + in_suffix
    parser = optparse.OptionParser(os.getcwd())
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
        base = re.sub(in_suffix, "", name)
    if len(args) > 0:
        name = args[0]
        base = re.sub(in_suffix, "", name)
    if not os.path.exists(name):
        sys.exit("STOP: " + name + " file not found")
    return (name, base, in_suffix, out_suffix)


if __name__ == "__main__":
    pdbname, base, in_suffix, out_suffix = options()
    poscarname = pdbname + out_suffix
    structname = pdbname + ".struct"
    print("INPUT PDB file  = ", pdbname)
    print("OUTPUT POSCAR file = ", poscarname)
    atoms = read(pdbname, format="pdb")
    atoms.center()
    atoms.write(poscarname, format="vasp", vasp5=True, sort=True)
