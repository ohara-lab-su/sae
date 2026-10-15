#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.openmx.md_fields import MolecularDynamicsFields

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import numpy as np

if __name__ == "__main__":
    cname = "C60_position.xyz"
    nloop, natom = MolecularDynamicsFields().read_md_param(cname)
    position_loop = np.zeros((nloop, natom, 3))
    print("NLOOP :", nloop)
    print("NATOM :", natom)
    atoms_index_j = np.zeros(natom, dtype="S2")
    position_loop = np.zeros((nloop, natom, 3))
    MolecularDynamicsFields().read_md(cname, nloop, natom, atoms_index_j, position_loop)
    for l in range(nloop):
        print("------- LOOP " + str(l) + " ------")
        for j in range(natom):
            print(
                " %3s %14.10f %14.10f %14.10f "
                % (
                    atoms_index_j[j],
                    position_loop[l, j, 0],
                    position_loop[l, j, 1],
                    position_loop[l, j, 2],
                )
            )
