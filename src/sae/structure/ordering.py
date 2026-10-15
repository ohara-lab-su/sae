# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import numpy as np
import collections


class AtomOrdering:

    def sort_atom_index_j(self, atoms_index_j):
        natom = len(atoms_index_j)
        counter = collections.Counter(atoms_index_j)
        nion = len(counter)
        atoms = np.zeros(nion, dtype=int)
        atoms_index = []
        i = 0
        for atom, cnt in counter.most_common():
            atoms_index.append(atom)
            atoms[i] = cnt
            i += 1
        sort_index = np.zeros(natom, dtype=int)
        sort_index_r = np.zeros(natom, dtype=int)
        for i in range(natom):
            index = 0
            for k in range(nion):
                for j in range(natom):
                    if atoms_index[k] == atoms_index_j[j]:
                        sort_index[index] = j
                        sort_index_r[j] = index
                        index += 1
        atoms_index_js = [""] * natom
        for original in range(natom):
            sort = sort_index_r[original]
            atoms_index_js[sort] = atoms_index_j[original]
        return (sort_index, sort_index_r, atoms, atoms_index, atoms_index_js)

    def sort_atom_number_j(self, atoms_number_j):
        from sae.structure.elements import ElementTable

        natom = len(atoms_number_j)
        counter = collections.Counter(atoms_number_j)
        nion = len(counter)
        atoms = np.zeros(nion, dtype=int)
        atoms_index = []
        atoms_number = np.zeros(nion, dtype=int)
        i = 0
        for number, cnt in counter.most_common():
            atoms_index.append(ElementTable().get_atomic_symbol0(int(number)))
            atoms_number[i] = int(number)
            atoms[i] = cnt
            i += 1
        sort_index = np.zeros(natom, dtype=int)
        sort_index_r = np.zeros(natom, dtype=int)
        for i in range(natom):
            index = 0
            for k in range(nion):
                for j in range(natom):
                    if atoms_number[k] == atoms_number_j[j]:
                        sort_index[index] = j
                        sort_index_r[j] = index
                        index += 1
        atoms_number_js = np.zeros(natom, dtype=float)
        for original in range(natom):
            sort = sort_index_r[original]
            atoms_number_js[sort] = atoms_number_j[original]
        return (sort_index, sort_index_r, atoms, atoms_index, atoms_number_j)

    def sort_fix(self, sort_index_r, fix):
        natom = len(fix)
        fix_s = np.zeros((natom, 3), dtype="S")
        for original in range(natom):
            sort = sort_index_r[original]
            fix_s[sort, :] = fix[original, :]
        return fix_s

    def sort_position(self, sort_index_r, position):
        natom = len(position)
        position_s = np.zeros((natom, 3))
        for original in range(natom):
            sort = sort_index_r[original]
            position_s[sort, :] = position[original, :]
        return position_s
