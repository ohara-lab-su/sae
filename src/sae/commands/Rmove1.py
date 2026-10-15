#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.common.text import TextFiles
from sae.geometry.coordinates import CoordinateTransforms
from sae.geometry.positions import PositionOperations
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
import optparse
import numpy as np


def options():
    cname = "igzo"
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
        POSCAR = args[0]
    if not os.path.exists(POSCAR):
        sys.exit(POSCAR + " file not found")
    if POSCAR:
        print("INPUT file name :", POSCAR)
    if cname:
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
    z_list = [0.0, 0.1]
    name = "LIST"
    nlist_top = TextFiles().read_list_param(name + "_top.ext")
    nlist_bottom = TextFiles().read_list_param(name + "_bottom.ext")
    list_atoms_top = np.zeros(nlist_top)
    list_atoms_bottom = np.zeros(nlist_bottom)
    nlist_top = TextFiles().read_list1(name + "_top.ext", list_atoms_top)
    nlist_bottom = TextFiles().read_list1(name + "_bottom.ext", list_atoms_bottom)
    nlist = nlist_top + nlist_bottom
    n_z_list = len(z_list)
    for i in range(n_z_list):
        z_new = z_list[i]
        print("z_new: ", z_new)
        list_atoms = np.zeros((nlist, 4))
        for i in range(nlist_top):
            list_atoms[i, 0] = int(list_atoms_top[i])
            list_atoms[i, 1] = 0.0
            list_atoms[i, 2] = 0.0
            list_atoms[i, 3] = -1.0 * z_new
        znew = open(name + "_top_z" + str(z_new) + ".list", "w")
        for i in range(nlist_top):
            print(
                "%3s %14.11f %14.11f %14.11f"
                % (
                    int(list_atoms[i, 0]),
                    list_atoms[i, 1],
                    list_atoms[i, 2],
                    list_atoms[i, 3],
                ),
                file=znew,
            )
        znew.close()
        for i in range(nlist_bottom):
            list_atoms[i + nlist_top, 0] = int(list_atoms_bottom[i])
            list_atoms[i + nlist_top, 1] = 0.0
            list_atoms[i + nlist_top, 2] = 0.0
            list_atoms[i + nlist_top, 3] = 1.0 * z_new
        znew = open(name + "_bottom_z" + str(z_new) + ".list", "w")
        for i in range(nlist_bottom):
            print(
                "%3s %14.11f %14.11f %14.11f"
                % (
                    int(list_atoms[i + nlist_top, 0]),
                    list_atoms[i + nlist_top, 1],
                    list_atoms[i + nlist_top, 2],
                    list_atoms[i + nlist_top, 3],
                ),
                file=znew,
            )
        znew.close()
        if direct:
            ABS = False
            scale, direct = CoordinateTransforms().conv_direct2cara(
                ABS, scale, t, natom, direct, position
            )
        scale = CoordinateTransforms().conv_scale21a(scale, t)
        PositionOperations().move_atoms1(scale, t, direct, position, nlist, list_atoms)
        if not direct:
            scale, direct = CoordinateTransforms().conv_car2directa(
                scale, t, natom, direct, position
            )
        scale, direct = RmcConversions().conv_vasp2cfg(
            scale, t, natom, direct, position
        )
        outname = str(cname) + "_z" + str(z_new)
        STD = False
        RmcConfigWriter().print_rmcpot_cfg(
            outname, STD, title, t, natom, nion, atoms, position
        )
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
