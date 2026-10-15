#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.structure.document import Read

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import optparse


def options():
    POSCAR = "POSCAR"
    cname = "POSCAR"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-o", "--output", dest="OUTPUT")
    options, args = parser.parse_args()
    if options.INPUT:
        POSCAR = options.INPUT
    if options.OUTPUT:
        cname = options.OUTPUT
    if len(args) > 0:
        cname = args[0]
        POSCAR = args[0]
    if not os.path.exists(POSCAR):
        sys.exit(POSCAR + " file not found")
    if POSCAR:
        print("INPUT file name : %s" % str(POSCAR))
    if cname:
        print("OUTPUT file name: %s" % str(cname + ".cfg"))
    return [POSCAR, cname]


if __name__ == "__main__":
    POSCAR, cname = options()
    cell = Read(filename=POSCAR, code="VASP")
    cell.write(outname=cname, code="RMC_POT")
