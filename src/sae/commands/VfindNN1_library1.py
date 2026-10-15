#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.geometry.coordinates import CoordinateTransforms
from sae.geometry.supercell import SupercellOperations
from sae.vasp.poscar_fields import PoscarFields

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
    distance = "2.5"
    find = 1
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT", default=POSCAR)
    parser.add_option("-o", "--output", dest="OUTPUT", default=cname)
    parser.add_option("-a", "--atom", dest="NN", default=find)
    parser.add_option("-d", "--distance", dest="DISTANCE", default=distance)
    options, args = parser.parse_args()
    if options.INPUT:
        POSCAR = options.INPUT
    if options.OUTPUT:
        cname = options.OUTPUT
    if options.NN:
        find = int(options.NN)
    if options.DISTANCE:
        distance = float(options.DISTANCE)
    if len(args) > 0:
        distance = float(args[0])
    if not os.path.exists(POSCAR):
        if os.path.exists(POSCAR + ".vasp"):
            POSCAR = "POSCAR.vasp"
        else:
            sys.exit(POSCAR + " file not found")
    print("INPUT file name    : %s" % str(POSCAR))
    print("OUTPUT file name   : %s" % str(cname + "_nn_" + str(find) + ".out"))
    print("SEARCH DISTANCE    : %s" % str(distance))
    print("")
    return [POSCAR, cname, distance, find]


if __name__ == "__main__":
    POSCAR, cname, distance, find = options()
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
    if direct:
        ABS = True
        scale, direct = CoordinateTransforms().conv_direct2cara(
            ABS, scale, t, natom, direct, position
        )
    if direct:
        sys.exit("Error: current mode is Direct")
    super = int(3 * 3 * 3)
    sv = np.zeros((super, 3))
    sp = np.zeros((natom * super, 3))
    ion_sp = np.zeros(natom * super)
    ion_local_sp = np.zeros(natom * super)
    sp_j = np.zeros(natom * super)
    SupercellOperations().make_supercell_zb(
        t,
        natom,
        nion,
        atoms,
        ion,
        ion_local,
        position,
        sv,
        ion_sp,
        ion_local_sp,
        sp_j,
        sp,
    )
