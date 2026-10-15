# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import numpy as np


class BondAnalysis:

    def get_bond_info_param(self, atom1, atom2, distance, nion, atoms, position):
        from sae.structure.elements import ElementTable

        start1, end1 = ElementTable().get_atom_start(atom1, nion, atoms)
        if atom1 != atom2:
            start2, end2 = ElementTable().get_atom_start(atom2, nion, atoms)
        atom1_0 = atom1 - 1
        num = 0
        if atom1 != atom2:
            for i in range(start1, end1 + 1, 1):
                x1 = position[i, 0]
                y1 = position[i, 1]
                z1 = position[i, 2]
                for j in range(start2, end2 + 1, 1):
                    if j != i:
                        x2 = position[j, 0]
                        y2 = position[j, 1]
                        z2 = position[j, 2]
                        r0 = np.fabs(
                            (x2 - x1) * (x2 - x1)
                            + (y2 - y1) * (y2 - y1)
                            + (z2 - z1) * (z2 - z1)
                        )
                        r1 = np.sqrt(r0)
                        if r1 < distance:
                            num += 1
        else:
            for i in range(start1, end1 + 1, 1):
                x1 = position[i, 0]
                y1 = position[i, 1]
                z1 = position[i, 2]
                for j in range(i, end1 + 1, 1):
                    if j != i:
                        x2 = position[j, 0]
                        y2 = position[j, 1]
                        z2 = position[j, 2]
                        r0 = np.fabs(
                            (x2 - x1) * (x2 - x1)
                            + (y2 - y1) * (y2 - y1)
                            + (z2 - z1) * (z2 - z1)
                        )
                        r1 = np.sqrt(r0)
                        if r1 < distance:
                            num += 1
        return num

    def get_bond_info(
        self,
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
    ):
        from sae.structure.elements import ElementTable

        start1, end1 = ElementTable().get_atom_start(atom1, nion, atoms)
        if atom1 != atom2:
            start2, end2 = ElementTable().get_atom_start(atom2, nion, atoms)
        atom1_0 = atom1 - 1
        num = 0
        if atom1 != atom2:
            for i in range(start1, end1 + 1, 1):
                x1 = position[i, 0]
                y1 = position[i, 1]
                z1 = position[i, 2]
                for j in range(start2, end2 + 1, 1):
                    if j != i:
                        x2 = position[j, 0]
                        y2 = position[j, 1]
                        z2 = position[j, 2]
                        r0 = np.fabs(
                            (x2 - x1) * (x2 - x1)
                            + (y2 - y1) * (y2 - y1)
                            + (z2 - z1) * (z2 - z1)
                        )
                        r1 = np.sqrt(r0)
                        if r1 < distance:
                            bondr[num] = r1
                            bond1[num] = i
                            bond2[num] = j
                            num += 1
        else:
            for i in range(start1, end1 + 1, 1):
                x1 = position[i, 0]
                y1 = position[i, 1]
                z1 = position[i, 2]
                for j in range(i, end1 + 1, 1):
                    if j != i:
                        x2 = position[j, 0]
                        y2 = position[j, 1]
                        z2 = position[j, 2]
                        r0 = np.fabs(
                            (x2 - x1) * (x2 - x1)
                            + (y2 - y1) * (y2 - y1)
                            + (z2 - z1) * (z2 - z1)
                        )
                        r1 = np.sqrt(r0)
                        if r1 < distance:
                            bondr[num] = r1
                            bond1[num] = i
                            bond2[num] = j
                            num += 1
