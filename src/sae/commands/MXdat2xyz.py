#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.geometry.coordinates import CoordinateTransforms
from sae.openmx.dat import ReadMxDat

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import re
import optparse


def options():
    from sae.common.paths import FileDiscovery

    name = "openmx"
    suffix = ".dat"
    mxname = name + suffix
    xyzname = "openmx.xyz"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-o", "--output", dest="OUTPUT")
    parser.add_option("-s", "--std", action="store_true", default=False, dest="STDOUT")
    options, args = parser.parse_args()
    if not os.path.exists(name + ".dat") or not os.path.exists(name + ".dat"):
        try:
            name0 = FileDiscovery().find_datfile("dat")
            if not name0 == None:
                name = name0
                mxname = name + suffix
                xyzname = mxname + ".xyz"
        except:
            pass
    if options.INPUT:
        mxname = options.INPUT
        xyzname = mxname + ".xyz"
    if options.OUTPUT:
        xyzname = options.OUTPUT
        xyzname = re.sub("\\.xyz", "", xyzname)
    if xyzname == mxname:
        sys.exit("STOP: input-filename = output-filename")
    return [mxname, xyzname, options.STDOUT]


if __name__ == "__main__":
    mxname, xyzname, OPT_STDOUT = options()
    if not OPT_STDOUT:
        print("STDOUT             =", OPT_STDOUT)
        print("INPUT OpenMX File  =", mxname)
        print("OUTPUT XYZ file    =", xyzname)
        try:
            outputfile = open(xyzname, "w")
        except:
            outputfile.close()
            sys.exit("STOP: " + xyzname + " does'nt open")
    dat = ReadMxDat(mxname)
    title = dat.get_title()
    nion = dat.get_nion()
    natom = dat.get_natom()
    atoms = dat.get_atoms()
    atoms_j = dat.get_atoms_j()
    atoms_index = dat.get_atoms_index()
    atoms_index_j = dat.get_atoms_index_j()
    scale = dat.get_scale()
    t = dat.get_t()
    selective = dat.get_selective()
    direct = dat.get_direct()
    position = dat.get_position()
    fix = dat.get_fix()
    position_max = dat.get_position_max()
    position_min = dat.get_position_min()
    left_natom = dat.get_left_natom()
    left_atoms_index_j = dat.get_left_atoms_index_j()
    left_position = dat.get_left_position()
    right_natom = dat.get_right_natom()
    right_atoms_index_j = dat.get_right_atoms_index_j()
    right_position = dat.get_right_position()
    if dat.FLAG_t:
        if direct:
            (
                scale,
                t,
                natom,
                direct,
                position,
            ) = CoordinateTransforms().conv_direct2carABS(
                scale, t, natom, direct, position
            )
        else:
            scale, t, natom, direct, position = CoordinateTransforms().conv_car2carABS(
                scale, t, natom, direct, position
            )
    print(outputfile, natom)
    print(outputfile, "")
    for i in range(natom):
        print(
            outputfile,
            " %s %13.9f %13.9f %13.9f"
            % (atoms_index_j[i], position[i, 0], position[i, 1], position[i, 2]),
        )
    if not OPT_STDOUT:
        outputfile.close()
    if dat.FLAG_left:
        left_xyz_name = re.sub("\\.xyz", "", xyzname)
        left_xyz_outname = left_xyz_name + ".left.xyz"
        try:
            out_left_xyz = open(left_xyz_outname, "w")
        except:
            out_left_xyz.close()
            sys.exit("STOP: " + left_xyz_outname + " does'nt open")
        print("OUTPUT left xyz    =", left_xyz_outname)
        print(left_natom, file=out_left_xyz)
        print("", file=out_left_xyz)
        for j in range(left_natom):
            print(
                " %s %13.9f %13.9f %13.9f"
                % (
                    left_atoms_index_j[j],
                    left_position[j, 0],
                    left_position[j, 1],
                    left_position[j, 2],
                ),
                file=out_left_xyz,
            )
        out_left_xyz.close()
    if dat.FLAG_right:
        right_xyz_name = re.sub("\\.xyz", "", xyzname)
        right_xyz_outname = left_xyz_name + ".right.xyz"
        try:
            out_right_xyz = open(right_xyz_outname, "w")
        except:
            out_right_xyz.close()
            sys.exit("STOP: " + right_xyz_outname + " does'nt open")
        print("OUTPUT right xyz   =", right_xyz_outname)
        print(right_natom, file=out_right_xyz)
        print("", file=out_right_xyz)
        for j in range(right_natom):
            print(
                " %s %13.9f %13.9f %13.9f"
                % (
                    right_atoms_index_j[j],
                    right_position[j, 0],
                    right_position[j, 1],
                    right_position[j, 2],
                ),
                file=out_right_xyz,
            )
        out_right_xyz.close()
