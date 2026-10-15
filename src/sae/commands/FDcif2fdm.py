#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function

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


if __name__ == "__main__":
    name, MOL = options()
    atoms = read(name, format="cif")
    print("bug version")
