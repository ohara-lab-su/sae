#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.geometry.coordinates import CoordinateTransforms
from sae.structure.extract import StructureExtraction
from sae.vasp.poscar_fields import PoscarFields
from sae.vasp.poscar_writer import PoscarWriter

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import optparse
import numpy as np


def options():
    cname = "POSCAR"
    POSCAR = "POSCAR"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT", default=POSCAR)
    parser.add_option("-o", "--output", dest="OUTPUT", default=cname)
    options, args = parser.parse_args()
    if options.INPUT:
        POSCAR = options.INPUT
    if options.OUTPUT:
        cname = options.OUTPUT
    if len(args) > 0:
        cname = args[0]
    if not os.path.exists(POSCAR):
        if os.path.exists(POSCAR + ".vasp"):
            POSCAR = "POSCAR.vasp"
        else:
            sys.exit(POSCAR + " file not found")
    print("INPUT file name    : %s" % str(POSCAR))
    print("OUTPUT file name   : %s" % str(cname + ".vasp"))
    print("")
    return [POSCAR, cname]


if __name__ == "__main__":
    POSCAR, cname = options()
    nion, natom, VASP = PoscarFields().read_poscar_param(POSCAR)
    t = np.zeros((3, 3))
    atoms = []
    atoms_index = []
    ion = np.zeros(natom)
    ion_local = np.zeros(natom)
    position = np.zeros((natom, 3))
    fix = np.zeros((natom, 3), dtype="S")
    title, scale, selective, direct = PoscarFields().read_poscar(
        POSCAR, VASP, t, atoms, atoms_index, ion, ion_local, position, fix
    )
    direct0 = direct
    c0 = np.zeros(3)
    c1 = np.zeros(3)
    c1[2] = 0.90732
    c0[2] = 0.59268
    scale, direct, ex_natom = StructureExtraction().extract_struct_param(
        scale, t, natom, direct, position, c0, c1
    )
    ex_atoms = []
    ex_atoms_index = []
    ex_position = np.zeros((ex_natom, 3))
    ex_fix = np.zeros((ex_natom, 3), dtype="S")
    ex_j = np.zeros(ex_natom)
    ex_nion = StructureExtraction().extract_struct1(
        scale,
        t,
        natom,
        direct,
        position,
        fix,
        c0,
        c1,
        atoms,
        atoms_index,
        ion,
        ion_local,
        ex_j,
        ex_natom,
        ex_atoms,
        ex_atoms_index,
        ex_position,
        ex_fix,
    )
    if direct0:
        scale, direct = CoordinateTransforms().conv_car2directa(
            scale, t, ex_natom, direct, ex_position
        )
    try:
        out = open("LIST.ext", "w")
    except:
        sys.exit("LIST.ext not open")
    if direct:
        mode = "Direct"
    else:
        mode = "Cartesian"
    print("# ", file=out)
    print("# " + mode + " Mode", file=out)
    print("# num,   positon(x,y,z),                          atomtype, atom", file=out)
    for i in range(ex_natom):
        print(
            "%3i    %13.9f %13.9f %13.9f %3i %2s"
            % (
                ex_j[i],
                ex_position[i, 0],
                ex_position[i, 1],
                ex_position[i, 2],
                ion[ex_j[i]] + 1,
                atoms_index[int(ion[ex_j[i]])],
            ),
            file=out,
        )
    out.close
    STD = False
    PoscarWriter().print_poscar(
        cname,
        STD,
        title,
        scale,
        ex_natom,
        ex_nion,
        selective,
        direct,
        VASP,
        t,
        ex_atoms,
        ex_atoms_index,
        ex_position,
        ex_fix,
    )
