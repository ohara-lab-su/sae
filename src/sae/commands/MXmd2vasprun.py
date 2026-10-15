#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.common.paths import FileDiscovery
from sae.geometry.coordinates import CoordinateTransforms
from sae.openmx.md import ReadMd
from sae.vasp.vasprun_writer import VasprunWriter

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import optparse
import numpy as np

if __name__ == "__main__":
    OUTPUT = "vasprun.xml"
    name = "openmx"
    MD_suffix = "md"
    MD = name + "." + MD_suffix
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    if options.INPUT:
        MD0 = options.INPUT
        if not os.path.exists(MD0):
            MD = MD0 + "." + MD_suffix
            if os.path.exists(MD):
                name = MD0
            else:
                sys.exit("STOP: INPUT " + MD0 + " file not found.")
        else:
            name = MD0.replace("." + MD_suffix, "")
            MD = MD0
    if len(args) > 0:
        MD = args[0]
        name = MD.replace("." + MD_suffix, "")
    if not os.path.exists(MD):
        name0 = FileDiscovery().find_datfile(MD_suffix)
        if not name0 is None:
            name = name0
            MD = name + "." + MD_suffix
        else:
            sys.exit("STOP: " + MD + " not found.")
    print("INPUT :", MD)
    print("OUTPUT:", OUTPUT)
    title = MD
    md = ReadMd(MD)
    natom = md.get_natom()
    nion = md.get_nion()
    nloop = md.get_nloop()
    atoms_index_j = md.get_atoms_index_j()
    atoms_index = md.get_atoms_index()
    atoms = md.get_atoms()
    energy_loop = md.get_energy_loop()
    position_loop = md.get_position_loop()
    selective = md.get_selective()
    force_loop = md.get_force_loop()
    if os.path.exists(name + ".dat"):
        file_name = name + ".dat"
        class_name = "ReadMxDat"
    elif os.path.exists(name + ".out"):
        file_name = name + ".out"
        class_name = "ReadMxOut"
    else:
        sys.exit("STOP: " + name + ".out or " + name + ".dat file not fond")
    module_name = "sae._class_registry"
    try:
        module = __import__(module_name, globals(), locals(), [class_name], 0)
    except:
        module = __import__(module_name, fromlist=[class_name])
    klass = getattr(module, class_name)
    out = klass(file_name)
    t = out.get_t()
    scale = out.get_scale()
    direct = out.get_direct()
    if not direct:
        for loop in range(nloop):
            CoordinateTransforms().conv_car2directa(
                scale, t, natom, direct, position_loop[loop, :, :]
            )
    print("")
    print("TITLE = ", title)
    print("NLOOP = ", nloop)
    print("NATOM = ", natom)
    print("NION  = ", nion)
    print("SCALE = ", scale)
    print("ATOM")
    print("  ", end="")
    for atom in range(nion):
        print(atoms_index[atom], end="")
    print("")
    print("  ", end="")
    for atom in range(nion):
        print(atoms[atom], end="")
    print("")
    print("")
    print(t)
    VasprunWriter().print_vasprun0(
        OUTPUT,
        title,
        nloop,
        natom,
        nion,
        atoms,
        atoms_index,
        atoms_index_j,
        t,
        position_loop,
        force_loop,
        energy_loop,
    )
