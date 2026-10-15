#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.geometry.coordinates import CoordinateTransforms
from sae.structure.elements import ElementTable
from sae.vasp.outcar_fields import OutcarFields
from sae.vasp.poscar_fields import PoscarFields

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import wx
import sys
import numpy as np
import visual as vp


def options():
    cname = "POSCAR"
    OUTCAR = "OUTCAR"
    POSCAR = "POSCAR"
    print("INPUT POSCAR file  :", POSCAR)
    print("INPUT OUTCAR file  :", OUTCAR)
    print("OUTPUT file name   :", cname + ".vasp")
    return [POSCAR, OUTCAR, cname]


if __name__ == "__main__":
    app = wx.App(True, None)
    frame0 = wx.Frame(None, -1, "Plot_Crystal")
    frame0.Show()
    cname = "POSCAR"
    POSCAR = "POSCAR"
    OUTCAR = "OUTCAR"
    print("INPUT POSCAR file  :", POSCAR)
    print("INPUT OUTCAR file  :", OUTCAR)
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
    nloop = OutcarFields().read_outcar_param(OUTCAR, natom)
    position_loop = np.zeros((nloop, natom, 3))
    force_loop = np.zeros((nloop, natom, 3))
    OutcarFields().read_outcar_position(OUTCAR, natom, nloop, position_loop, force_loop)
    if VASP < 5:
        sys.exit("STOP: VASP version < 5 ")
    f = vp.frame()
    O = [-3, -3, 0]
    R = 0.05
    C = [255, 255, 2555]
    RATIO = 0.3
    direct0 = direct
    conv = True
    for l in range(nloop):
        if conv:
            position0 = np.zeros((natom, 3))
        for i in range(natom):
            if conv:
                direct = direct0
                position0[i, 0] = position_loop[l, i, 0]
                position0[i, 1] = position_loop[l, i, 1]
                position0[i, 2] = position_loop[l, i, 2]
                ABS = False
                scale, direct = CoordinateTransforms().conv_direct2cara(
                    ABS, scale, t, natom, direct, position0
                )
                position_loop[l, i, 0] = position0[i, 0]
                position_loop[l, i, 1] = position0[i, 1]
                position_loop[l, i, 2] = position0[i, 2]
            xp = position_loop[l, i, 0] + O[0]
            yp = position_loop[l, i, 1] + O[1]
            zp = position_loop[l, i, 2] + O[2]
            atom_type = str(atoms_index[int(ion[i])])
            radius = ElementTable().get_atomic_radius1(atom_type)
            R = radius * RATIO
            num = ElementTable().get_atomic_number1(atom_type)
            atom = vp.sphere(frame=f, pos=(xp, yp, zp), radius=R)
            atom.red = 0.5 * num * num
            atom.green = 0.1 * num
            atom.blue = 1 / num
        vp.rate(10)
        for obj in f.objects:
            obj.visible = 0
