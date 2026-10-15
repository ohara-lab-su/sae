#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.geometry.coordinates import CoordinateTransforms
from sae.vasp.outcar_fields import OutcarFields
from sae.vasp.poscar_fields import PoscarFields

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import optparse
import numpy as np


def options():
    OUTCAR = "OUTCAR"
    POSCAR = "POSCAR"
    parser = optparse.OptionParser()
    parser.add_option("-p", "--poscar", dest="INPUT", default=POSCAR)
    parser.add_option("-o", "--outcar", dest="OUTLOG", default=OUTCAR)
    options, args = parser.parse_args()
    if options.INPUT:
        POSCAR = options.INPUT
    if options.OUTLOG:
        OUTCAR = options.OUTLOG
    return [POSCAR, OUTCAR]


if __name__ == "__main__":
    POSCAR, OUTCAR = options()
    nion, natom, VASP = PoscarFields().read_poscar_param(POSCAR)
    t = np.zeros((3, 3))
    atoms = []
    atoms_index = []
    ion = np.zeros(natom)
    ion_site = np.zeros(natom)
    position = np.zeros((natom, 3))
    fix = np.zeros((natom, 3), dtype="S")
    title, scale, selective, direct = PoscarFields().read_poscar(
        POSCAR, VASP, t, atoms, atoms_index, ion, ion_site, position, fix
    )
    nloop = OutcarFields().read_outcar_param(OUTCAR, natom)
    position_loop = np.zeros((nloop, natom, 3))
    force_loop = np.zeros((nloop, natom, 3))
    OutcarFields().read_outcar_position(OUTCAR, natom, nloop, position_loop, force_loop)
    scale = CoordinateTransforms().conv_scale21a(scale, t)
    direct0 = direct
    conv = True
    for i in range(nloop):
        print(natom)
        print("   time=")
        if direct0 and conv:
            position0 = np.zeros((natom, 3))
        for j in range(natom):
            if direct0 and conv:
                direct = direct0
                position0[j, 0] = position_loop[i, j, 0]
                position0[j, 1] = position_loop[i, j, 1]
                position0[j, 2] = position_loop[i, j, 2]
                ABS = False
                scale, direct = CoordinateTransforms().conv_direct2cara(
                    ABS, scale, t, natom, direct, position0
                )
                position_loop[i, j, 0] = position0[j, 0]
                position_loop[i, j, 1] = position0[j, 1]
                position_loop[i, j, 2] = position0[j, 2]
            print(
                "     %2s  %10.7f %10.7f %10.7f  %17.9f %17.9f %17.9f"
                % (
                    str(atoms_index[int(ion[j])]),
                    position_loop[i, j, 0],
                    position_loop[i, j, 1],
                    position_loop[i, j, 2],
                    force_loop[i, j, 0],
                    force_loop[i, j, 1],
                    force_loop[i, j, 2],
                )
            )
