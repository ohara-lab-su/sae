#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.common.paths import FileDiscovery
from sae.openmx.md import ReadMd
from sae.openmx.md_fields import MolecularDynamicsFields
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
        MD = options.INPUT
        if not os.path.exists(MD):
            MD = MD + "." + MD_suffix
    if not os.path.exists(MD):
        name0 = FileDiscovery().find_datfile(MD_suffix)
        if not name0 is None:
            name = name0
            MD = name + "." + MD_suffix
        else:
            sys.exit("STOP: " + MD + " not found.")
    if len(args) > 0:
        MD = args[0]
    print("INPUT :%s" % MD)
    print("OUTPUT:%s" % OUTPUT)
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
    position_max, position_min = MolecularDynamicsFields().get_max_md(
        nloop, natom, position_loop
    )
    max_range = abs(position_min) + position_max
    box_size = 10.0
    t = np.zeros((3, 3))
    t[0, 0] = 1.0 * box_size
    t[1, 1] = 1.0 * box_size
    t[2, 2] = 1.0 * box_size
    scale = 1.0
    position_loop = position_loop / box_size
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
