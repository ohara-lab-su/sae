#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.common.paths import FileDiscovery
from sae.openmx.md_fields import MolecularDynamicsFields

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import optparse
import os
import numpy as np

if __name__ == "__main__":
    name = "openmx"
    suffix = "md"
    MD = name + "." + suffix
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    if not os.path.exists(MD):
        name0 = FileDiscovery().find_datfile("md")
        if not name0 is None:
            name = name0
            MD = name + "." + suffix
    if options.INPUT:
        MD = options.INPUT
    if len(args) > 0:
        MD = args[0]
    nloop, natom = MolecularDynamicsFields().read_md_param(MD)
    atoms_index_j = np.zeros(natom, dtype="S2")
    position_loop = np.zeros((nloop, natom, 3))
    force_loop = np.zeros((nloop, natom, 3))
    print("NLOOP :", nloop)
    print("NATOM :", natom)
    natom, nlist = MolecularDynamicsFields().read_md2(
        MD, nloop, atoms_index_j, position_loop, force_loop
    )
    print(nlist)
    if nlist >= 7:
        for l in range(nloop):
            print("------- LOOP " + str(l) + " ------")
            for j in range(natom):
                print(
                    " %3s %12.8f %12.8f %12.8f  %12.8f %12.8f %12.8f"
                    % (
                        atoms_index_j[j],
                        position_loop[l, j, 0],
                        position_loop[l, j, 1],
                        position_loop[l, j, 2],
                        force_loop[l, j, 0],
                        force_loop[l, j, 1],
                        force_loop[l, j, 2],
                    )
                )
    else:
        for l in range(nloop):
            print("------- LOOP " + str(l) + " ------")
            for j in range(natom):
                print(
                    " %3s %12.8f %12.8f %12.8f "
                    % (
                        atoms_index_j[j],
                        position_loop[l, j, 0],
                        position_loop[l, j, 1],
                        position_loop[l, j, 2],
                    )
                )
