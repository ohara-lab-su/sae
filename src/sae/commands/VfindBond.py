#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.geometry.bonds import BondAnalysis
from sae.geometry.coordinates import CoordinateTransforms
from sae.vasp.poscar_fields import PoscarFields

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import sys
import numpy as np


def options():
    POSCAR = "POSCAR"
    atom1 = 1
    atom2 = 4
    distance = 2.4
    return [POSCAR, atom1, atom2, distance]


if __name__ == "__main__":
    POSCAR, atom1, atom2, distance = options()
    nion, natom, VASP = PoscarFields().read_poscar_param(POSCAR)
    t = np.zeros((3, 3))
    atoms = []
    atoms_index = []
    ion = np.zeros(natom, dtype=int)
    ion_local = np.zeros(natom, dtype=int)
    position = np.zeros((natom, 3))
    fix = np.zeros((natom, 3), dtype="S")
    title, scale, selective, direct = PoscarFields().read_poscar(
        POSCAR, VASP, t, atoms, atoms_index, ion, ion_local, position, fix
    )
    if direct:
        ABS = False
        scale, direct = CoordinateTransforms().conv_direct2cara(
            ABS, scale, t, natom, direct, position
        )
    scale = CoordinateTransforms().conv_car2carABSa(scale, t, natom, direct, position)
    if direct:
        sys.exit("Error: current mode is Direct")
    if nion < atom1 or nion < atom2:
        sys.exit("Error: nion < atom1 or atom2")
    bondnum = BondAnalysis().get_bond_info_param(
        atom1, atom2, distance, nion, atoms, position
    )
    if bondnum != 0:
        print(bondnum)
    bondr = np.zeros(bondnum)
    bond1 = np.zeros(bondnum, dtype=int)
    bond2 = np.zeros(bondnum, dtype=int)
    BondAnalysis().get_bond_info(
        atom1, atom2, distance, nion, atoms, atoms_index, position, bondr, bond1, bond2
    )
    for num in range(bondnum):
        x1 = position[bond1[num], 0]
        y1 = position[bond1[num], 1]
        z1 = position[bond1[num], 2]
        x2 = position[bond2[num], 0]
        y2 = position[bond2[num], 1]
        z2 = position[bond2[num], 2]
        r1 = bondr[num]
        print(
            "%d %d (%s) - %s (%s)   %10.7f   %11.8f %11.8f %11.8f   %11.8f %11.8f %11.8f"
            % (
                num,
                bond1[num],
                str(atoms_index[ion[bond1[num]]]),
                bond2[num],
                str(atoms_index[ion[bond2[num]]]),
                r1,
                x1,
                y1,
                z1,
                x2,
                y2,
                z2,
            )
        )
