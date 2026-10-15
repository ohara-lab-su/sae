#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.vasp.poscar import ReadVaspPoscar

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
    inpname = "POSCAR"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-o", "--output", dest="OUTPUT")
    options, args = parser.parse_args()
    if options.INPUT:
        inpname = options.INPUT
    if not os.path.exists(inpname):
        if os.path.exists(inpname + ".vasp"):
            POSCAR = "POSCAR.vasp"
        else:
            sys.exit(inpname + " file not found")
    if len(args) < 3:
        sys.exit("Error: args < 3")
    else:
        super_x = args[0]
        super_y = args[1]
        super_z = args[2]
        print("Super Cell         : [", super_x, ",", super_y, ",", super_z, "]")
    outname = (
        inpname + "_super_" + str(super_x) + "x" + str(super_y) + "x" + str(super_z)
    )
    if options.OUTPUT:
        outname = options.OUTPUT
    print("INPUT file name    :", inpname)
    print("OUTPUT file name   :", outname + ".vasp")
    return (inpname, outname, super_x, super_y, super_z)


if __name__ == "__main__":
    inpname, outname, super_x, super_y, super_z = options()
    poscar = ReadVaspPoscar(inpname)
    poscar.conv_supercell(times=(super_x, super_y, super_z))
    poscar.print_poscar(outname, STD=True)
    poscar.print_poscar(outname, STD=False)
