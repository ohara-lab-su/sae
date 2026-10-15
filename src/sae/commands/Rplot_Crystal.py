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
import wx
import sys
import os
import numpy as np
import visual as vp
from crystal_make_unit import *

if __name__ == "__main__":
    app = wx.App(True, None)
    frame0 = wx.Frame(None, -1, "Plot_Crystal")
    frame0.Show()
    cname = "igzo"
    print("INPUT file name   :", cname)
    bond_FLAG = True
    atom1 = 1
    atom2 = 4
    distance = 2.4
    natom, nion = RmcConfigFields().read_cfg_param(cname)
    t = np.zeros((3, 3))
    atoms = np.zeros(nion, dtype=int)
    ion_site = np.zeros(natom, dtype=int)
    position = np.zeros((natom, 3))
    header, comment = RmcConfigFields().read_cfg(cname, t, atoms, ion_site, position)
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
    direct = True
    scale = 1.0
    scale, direct = RmcConversions().conv_cfg2vaspa(scale, t, natom, direct, position)
    if direct:
        ABS = False
        scale, direct = CoordinateTransforms().conv_direct2cara(
            ABS, scale, t, natom, direct, position
        )
    scale = CoordinateTransforms().conv_car2carABSa(scale, t, natom, direct, position)
    if bond_FLAG:
        bondnum = BondAnalysis().get_bond_info_param(
            atom1, atom2, distance, nion, atoms, position
        )
        print("NUMBER OF BOND     :", bondnum)
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
    f = vp.frame()
    O = [-3, -3, 0]
    RC = 0.03
    C = [255, 255, 2555]
    crystal_make_unit(t, O, RC, C)
    RATIO = 0.3
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
            print(
                num,
                bond1[num],
                "(" + str(ion_site[num]) + ") -",
                bond2[num],
                "(" + str(ion_site[num]) + ")",
                " %10.7f   %11.8f %11.8f %11.8f   %11.8f %11.8f %11.8f"
                % (r1, x1, y1, z1, x2, y2, z2),
            )
