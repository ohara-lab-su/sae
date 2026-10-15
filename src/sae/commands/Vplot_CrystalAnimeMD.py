#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.openmx.md_fields import MolecularDynamicsFields
from sae.structure.elements import ElementTable

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014,2015, Kengo NAKADA"
__license__ = "MIT"
import wx
import numpy as np
import visual as vp
import optparse


def options():
    XYZ = "C60_position.xyz"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT", default=XYZ)
    options, args = parser.parse_args()
    if options.INPUT:
        XYZ = options.INPUT
    if len(args) > 0:
        XYZ = args[0]
    return XYZ


if __name__ == "__main__":
    app = wx.App(True, None)
    frame0 = wx.Frame(None, -1, "Plot_Crystal")
    frame0.Show()
    cname = options()
    print("INPUT file name   :", cname)
    nloop, natom = MolecularDynamicsFields().read_md_param(cname)
    position_loop = np.zeros((nloop, natom, 3))
    print("NLOOP :", nloop)
    print("NATOM :", natom)
    atoms_index_j = np.zeros(natom, dtype="S2")
    position_loop = np.zeros((nloop, natom, 3))
    MolecularDynamicsFields().read_md(cname, nloop, atoms_index_j, position_loop)
    f = vp.frame()
    O = [-3, -3, 0]
    R = 0.05
    C = [255, 255, 2555]
    RATIO = 0.3
    for loop in range(nloop):
        for ion in range(natom):
            xp = position_loop[loop, ion, 0] + O[0]
            yp = position_loop[loop, ion, 1] + O[1]
            zp = position_loop[loop, ion, 2] + O[2]
            atom_type = str(atoms_index_j[ion])
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
