#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.geometry.coordinates import CoordinateTransforms
from sae.rmcpot.cfg_fields import RmcConfigFields

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import numpy as np
import visual as vp
import wx

if __name__ == "__main__":
    app = wx.App(True, None)
    frame0 = wx.Frame(None, -1, "Plot_Crystal")
    frame0.Show()
    cname = "igzo"
    print("INPUT file name   :", cname)
    natom, nion = RmcConfigFields().read_cfg_param(cname)
    t = np.zeros((3, 3))
    atoms = np.zeros(nion, dtype=int)
    atoms_j = np.zeros(natom, dtype=int)
    position = np.zeros((natom, 3))
    header, comment = RmcConfigFields().read_cfg(cname, t, atoms, atoms_j, position)
    t1_x = t[0, 0] * 2.0
    t1_y = t[1, 0] * 2.0
    t1_z = t[2, 0] * 2.0
    t2_x = t[0, 1] * 2.0
    t2_y = t[1, 1] * 2.0
    t2_z = t[2, 1] * 2.0
    t3_x = t[0, 2] * 2.0
    t3_y = t[1, 2] * 2.0
    t3_z = t[2, 2] * 2.0
    x_offset = 0.5
    y_offset = 0.5
    z_offset = 0.5
    for i in range(natom):
        position[i, 0] = position[i, 0] / 2.0 + x_offset
        position[i, 1] = position[i, 1] / 2.0 + y_offset
        position[i, 2] = position[i, 2] / 2.0 + z_offset
    ABS = False
    scale = 1.0
    direct = True
    CoordinateTransforms().conv_direct2cara(ABS, scale, t, natom, direct, position)
    f = vp.frame()
    O = [-3, -3, 0]
    R = 0.03
    C = [255, 255, 2555]
    crystal_make_unit(t, O, R, C)
    RATIO = 0.3
    for ion in range(natom):
        xp = position[ion, 0] + O[0]
        yp = position[ion, 1] + O[1]
        zp = position[ion, 2] + O[2]
        atom = vp.sphere(frame=f, pos=(xp, yp, zp), radius=0.2)
        factor = 5
        num = atoms_j[ion] + 1 + atoms_j[ion] + 1 + atoms_j[ion] + 1
        num = factor * num
        print(ion, num)
        atom.red = 0.05 * num
        atom.green = 0.01 * num * num
        atom.blue = 10 / num
