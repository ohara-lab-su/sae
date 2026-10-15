#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.geometry.coordinates import CoordinateTransforms
from sae.vasp.poscar import ReadVaspPoscar

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import optparse
import sys
import os
import re


def options():
    poscarname = "POSCAR"
    xyzname = "POSCAR"
    suffix = ".xyz"
    parser = optparse.OptionParser(os.getcwd())
    parser = optparse.OptionParser()
    parser.add_option("-s", "--stdout", action="store_true")
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-o", "--output", dest="OUTPUT")
    options, args = parser.parse_args()
    xyzname = re.sub("\\.xyz$", "", xyzname)
    xyzname = xyzname + suffix
    if options.INPUT:
        poscarname = options.INPUT
    if options.OUTPUT:
        xyzname = re.sub("\\.xyz$", "", options.OUTPUT)
        xyzname = xyzname + suffix
    if len(args) > 0:
        poscarname = args[0]
    if poscarname == xyzname:
        sys.exit("STOP: INPUT_NAME = OUTPUT_NAME :" + poscarname)
    return [poscarname, xyzname, suffix, options.stdout]


if __name__ == "__main__":
    poscarname, xyzname, suffix, OPT_STD = options()
    poscar = ReadVaspPoscar(poscarname)
    vasp = poscar.get_vasp_version()
    if vasp < 5:
        sys.exit("STOP: This script requires VASP5 style POSCAR")
    title = poscar.get_title()
    t = poscar.get_t()
    scale = poscar.get_scale()
    atoms = poscar.get_atoms()
    atoms_index = poscar.get_atoms_index()
    atoms_index_j = poscar.get_atoms_index_j()
    natom = poscar.get_natom()
    nion = poscar.get_nion()
    selective = poscar.get_selective()
    direct = poscar.get_direct()
    position = poscar.get_position()
    fix = poscar.get_fix()
    ion = poscar.get_ion()
    ion_local = poscar.get_ion_local()
    if direct:
        scale, t, natom, direct, position = CoordinateTransforms().conv_direct2carABS(
            scale, t, natom, direct, position
        )
    else:
        scale, t, natom, direct, position = CoordinateTransforms().conv_car2carABS(
            scale, t, natom, direct, position
        )
    if OPT_STD:
        out = sys.stdout
    else:
        try:
            out = open(xyzname, "w")
        except:
            out.close()
            sys.exit("STOP: " + xyzname + " can't open")
    print(natom, file=out)
    print("", file=out)
    for i in range(natom):
        atom = re.sub("_.*", "", atoms_index_j[i])
        atoms_index_j[i] = atom
        print(
            "%2s %12.8f %12.8f %12.8f "
            % (atoms_index_j[i], position[i][0], position[i][1], position[i][2]),
            file=out,
        )
    if not OPT_STD:
        out.close()
