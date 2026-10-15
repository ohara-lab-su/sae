#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.common.text import TextFiles
from sae.geometry.coordinates import CoordinateTransforms
from sae.rmcpot.cfg_writer import RmcConfigWriter
from sae.rmcpot.conversion import RmcConversions
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
import numpy as np


def options():
    cname = "igzo"
    POSCAR = "POSCAR"
    lname = "lattice.list"
    if not os.path.exists(POSCAR):
        sys.exit("STOP: " + POSCAR + " file not found")
    if not os.path.exists(cname + ".dat"):
        sys.exit("STOP: " + cname + ".dat file not found")
    if not os.path.exists(lname):
        sys.exit("STOP: " + lname + " file not found")
    print("INPUT file name :", POSCAR)
    print("OUTPUT file name:", cname + ".cfg")
    return [POSCAR, cname, lname]


if __name__ == "__main__":
    POSCAR, cname, lname = options()
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
    nlist = TextFiles().read_list_param(lname)
    list_lattice = np.zeros(nlist, dtype=float)
    nlist = TextFiles().read_list1(lname, list_lattice)
    scale = CoordinateTransforms().conv_scale21a(scale, t)
    lattice_org = t[0, 0]
    cell_org = t[0, 0] / 2
    density = np.zeros(nlist, dtype=float)
    cell = np.zeros(nlist, dtype=float)
    print("")
    print("NATOM             = ", natom)
    print("ORIGINA LATTICE a = ", lattice_org)
    print("")
    for i in range(nlist):
        print("====================")
        density[i] = natom / (lattice_org * list_lattice[i]) ** 3
        cell[i] = lattice_org * list_lattice[i] / 2
        print("  LATTICE RATE    = ", list_lattice[i])
        print("  LATTICE         = ", lattice_org * list_lattice[i])
        print("  CELL            = ", cell[i])
        print("  DENSITY         = ", density[i])
        if not direct:
            scale, direct = CoordinateTransforms().conv_car2directa(
                scale, t, natom, direct, position
            )
        scale, direct = RmcConversions().conv_vasp2cfg(
            scale, t, natom, direct, position
        )
        t[0, 0] = cell[i]
        t[1, 1] = cell[i]
        t[2, 2] = cell[i]
        outname = cname + "_" + str(list_lattice[i])
        print("  OUTPUT DAT      = ", outname + ".dat")
        STD = False
        RmcConversions().change_density(STD, cname, outname, density[i])
        print("  OUTPUT CFG-FILE = ", outname + ".cfg")
        STD = False
        RmcConfigWriter().print_rmcpot_cfg(
            outname, STD, title, t, natom, nion, atoms, position
        )
        print("  OUTPUT POSCAR   = ", outname + ".vasp")
        direct = True
        scale = 1.0
        scale, direct = RmcConversions().conv_cfg2vaspa(
            scale, t, natom, direct, position
        )
        dummy = "In Ga Zn O"
        PV5FLAG = True
        STD = False
        PoscarWriter().print_poscar4(
            outname,
            STD,
            title,
            scale,
            natom,
            nion,
            direct,
            PV5FLAG,
            t,
            atoms,
            dummy,
            position,
        )
        print("")
