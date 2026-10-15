#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import os
import sys
import optparse
from ase.io.vasp import *


def options():
    name = "POSCAR"
    outname = "read_pdb.inp"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--ipput", dest="INPUT")
    parser.add_option("-o", "--outname")
    parser.add_option("-m", "--mol", action="store_true", default=False)
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    if options.outname:
        outname = options.outname
    if len(args) > 0:
        name = str(args[0])
    if options.mol:
        MOL = True
    else:
        MOL = False
    if not os.path.exists(name):
        if os.path.exists(name + ".vasp"):
            name = name + ".vasp"
        elif os.path.exists("CONTCAR"):
            name = "CONTCAR"
        else:
            sys.exit("STOP: " + name + " file not found")
    return (name, outname, MOL)


if __name__ == "__main__":
    name, outname, MOL = options()
    print("gug version")
