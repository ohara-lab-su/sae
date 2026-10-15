#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
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
    cname = "POSCAR"
    POSCAR = "POSCAR"
    if not os.path.exists(POSCAR):
        sys.exit("STOP: " + POSCAR + " file not found")
    print("INPUT file name :", POSCAR)
    print("OUTPUT file name:", cname + ".cfg")
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
    scale = CoordinateTransforms().conv_scale21a(scale, t)
    lattice = t[0, 0]
    cell = t[0, 0] / 2
    density = natom / lattice**3
    print("")
    print("  NATOM           = ", natom)
    print("  LATTICE         = ", lattice)
    print("  CELL (RMC.cfg)  = ", cell)
    print("")
    print("  DENSITY         = ", density)
    print("")
    if not direct:
        scale, direct = CoordinateTransforms().conv_car2directa(
            scale, t, natom, direct, position
        )
    scale, direct = RmcConversions().conv_vasp2cfg(scale, t, natom, direct, position)
    t[0, 0] = cell
    t[1, 1] = cell
    t[2, 2] = cell
    outname = cname
    print("  OUTPUT CFG-FILE = ", outname + ".cfg")
    STD = False
    RmcConfigWriter().print_rmcpot_cfg(
        outname, STD, title, t, natom, nion, atoms, position
    )
    print("  OUTPUT POSCAR   = ", outname + ".vasp")
    direct = True
    scale = 1.0
    scale, direct = RmcConversions().conv_cfg2vaspa(scale, t, natom, direct, position)
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
