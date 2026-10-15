#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.geometry.bonds import BondAnalysis
from sae.geometry.coordinates import CoordinateTransforms
from sae.rmcpot.cfg_fields import RmcConfigFields
from sae.rmcpot.conversion import RmcConversions
from sae.structure.elements import ElementTable

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
from copy import deepcopy
import numpy as np
import visual as vp

if __name__ == "__main__":
    cname = "igzo_coll"
    print("INPUT file name   :", cname)
    bond_FLAG = True
    atom1 = 1
    atom2 = 4
    distance = 2.4
    nloop, natom, nion = RmcConfigFields().read_cfg_coll_param(cname)
    t = np.zeros((3, 3), dtype=float)
    atoms = np.zeros(nion, dtype=int)
    ion_site = np.zeros(natom, dtype=int)
    position_loop = np.zeros((nloop, natom, 3))
    header, comment, scale, direct = RmcConfigFields().read_cfg_coll(
        cname, nloop, t, natom, nion, atoms, ion_site, position_loop
    )
    dummy = cname + ".atomlist"
    dummy_FLAG = False
    if os.path.exists(dummy):
        dummy_FLAG = True
        print("READ dummy list: " + dummy)
        try:
            tmp = open(dummy)
        except:
            sys.exit("STOP: " + dummy + " does'nt open")
        dummyfile = tmp.read()
        tmp.close
        dummylines = dummyfile.split("\n")
        atoms_index = dummylines[0].split()
        nion0 = len(atoms_index)
        if nion0 != nion:
            sys.exit("STOP: nion0 != nion (in dummy list)")
    f = vp.frame()
    O = [-3, -3, 0]
    RC = 0.03
    C = [255, 255, 2555]
    RATIO = 0.3
    t0 = deepcopy(t)
    scale0 = scale
    direct0 = direct
    for loop in range(nloop):
        t = deepcopy(t0)
        scale = scale0
        direct = direct0
        position = np.zeros((natom, 3))
        for i in range(natom):
            position[i, 0] = position_loop[loop, i, 0]
            position[i, 1] = position_loop[loop, i, 1]
            position[i, 2] = position_loop[loop, i, 2]
        scale, direct = RmcConversions().conv_cfg2vaspa(
            scale, t, natom, direct, position
        )
        if direct:
            ABS = False
            scale, direct = CoordinateTransforms().conv_direct2cara(
                ABS, scale, t, natom, direct, position
            )
        scale = CoordinateTransforms().conv_car2carABSa(
            scale, t, natom, direct, position
        )
        if bond_FLAG:
            bondnum = BondAnalysis().get_bond_info_param(
                atom1, atom2, distance, nion, atoms, position
            )
            bondr = np.zeros(bondnum)
            bond1 = np.zeros(bondnum, dtype=int)
            bond2 = np.zeros(bondnum, dtype=int)
            BondAnalysis().get_bond_info(
                atom1,
                atom2,
                distance,
                nion,
                atoms,
                atoms_index,
                position,
                bondr,
                bond1,
                bond2,
            )
        if loop == 0:
            crystal_make_unit(t, O, RC, C)
        for i in range(natom):
            xp = position[i, 0] + O[0]
            yp = position[i, 1] + O[1]
            zp = position[i, 2] + O[2]
            if dummy_FLAG:
                atom_type = atoms_index[int(ion_site[i])]
                radius = ElementTable().get_atomic_radius1(atom_type)
                R = radius * RATIO
                num = ElementTable().get_atomic_number1(atom_type)
            else:
                R = 0.3
                num = 6
            atom = vp.sphere(frame=f, pos=(xp, yp, zp), radius=R)
            atom.red = 0.5 * num * num
            atom.green = 0.1 * num
            atom.blue = 1 / num
        if bond_FLAG:
            BR = 0.08
            for num in range(bondnum):
                x1 = position[bond1[num], 0]
                y1 = position[bond1[num], 1]
                z1 = position[bond1[num], 2]
                x2 = position[bond2[num], 0]
                y2 = position[bond2[num], 1]
                z2 = position[bond2[num], 2]
                x12 = x2 - x1
                y12 = y2 - y1
                z12 = z2 - z1
                x0 = x1 + O[0]
                y0 = y1 + O[1]
                z0 = z1 + O[2]
                r1 = bondr[num]
                bond = vp.cylinder(
                    frame=f, pos=(x0, y0, z0), axis=(x12, y12, z12), radius=BR
                )
        vp.rate(5)
        for obj in f.objects:
            obj.visible = 0
