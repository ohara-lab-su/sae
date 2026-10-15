# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import numpy as np


class StructureExtraction:

    def chk_pdb_cryst1(self, filename):
        try:
            pdbfile = open(filename)
        except:
            pdbfile.close()
            sys.exit("STOP(chk_cryst1):" + filename + "file can'nt open")
        cryst1 = False
        for line in pdbfile.readlines():
            if line.startswith("CRYST1"):
                cryst1 = True
        pdbfile.close()
        return cryst1

    def extract_struct0(
        self,
        scale,
        t,
        natom,
        direct,
        position,
        c0,
        c1,
        atoms,
        atoms_index,
        ion,
        ion_local,
        ex_j,
        ex_natom,
        ex_atoms,
        ex_atoms_index,
        ex_position,
    ):
        from sae.geometry.coordinates import CoordinateTransforms

        t1_x = t[0, 0]
        t1_y = t[1, 0]
        t1_z = t[2, 0]
        t2_x = t[0, 1]
        t2_y = t[1, 1]
        t2_z = t[2, 1]
        t3_x = t[0, 2]
        t3_y = t[1, 2]
        t3_z = t[2, 2]
        c0_new = np.zeros(3)
        c0_new[0] = (t1_x * c0[0] + t2_x * c0[1] + t3_x * c0[2]) * scale
        c0_new[1] = (t1_y * c0[0] + t2_y * c0[1] + t3_y * c0[2]) * scale
        c0_new[2] = (t1_z * c0[0] + t2_z * c0[1] + t3_z * c0[2]) * scale
        c1_new = np.zeros(3)
        c1_new[0] = (t1_x * c1[0] + t2_x * c1[1] + t3_x * c1[2]) * scale
        c1_new[1] = (t1_y * c1[0] + t2_y * c1[1] + t3_y * c1[2]) * scale
        c1_new[2] = (t1_z * c1[0] + t2_z * c1[1] + t3_z * c1[2]) * scale
        if direct:
            ABS = False
            scale, direct = CoordinateTransforms().conv_direct2cara(
                ABS, scale, t, natom, direct, position
            )
        CoordinateTransforms().conv_car2carABSa(scale, t, natom, direct, position)
        j = 0
        for i in range(natom):
            if c0_new[2] <= position[i, 2] <= c1_new[2]:
                ex_position[j, 0] = position[i, 0]
                ex_position[j, 1] = position[i, 1]
                ex_position[j, 2] = position[i, 2]
                ex_j[j] = i
                j += 1
        ex_natom = j
        nion = 0
        tmp = "ZZ"
        local_atom_index = 0
        for i in range(ex_natom):
            atom0 = int(atoms[int(ion[ex_j[i]])])
            atom_index0 = str(atoms_index[int(ion[ex_j[i]])])
            local_atom_index += 1
            if tmp != atom_index0:
                nion += 1
                if tmp != "ZZ":
                    ex_atoms.append(str(local_atom_index))
                    ex_atoms_index.append(str(tmp))
                local_atom_index = 0
            tmp = atom_index0
        ex_nion = nion
        ex_atoms.append(str(local_atom_index))
        ex_atoms_index.append(str(tmp))
        return ex_nion

    def extract_struct1(
        self,
        scale,
        t,
        natom,
        direct,
        position,
        fix,
        c0,
        c1,
        atoms,
        atoms_index,
        ion,
        ion_local,
        ex_j,
        ex_natom,
        ex_atoms,
        ex_atoms_index,
        ex_position,
        ex_fix,
    ):
        from sae.geometry.coordinates import CoordinateTransforms

        t1_x = t[0, 0]
        t1_y = t[1, 0]
        t1_z = t[2, 0]
        t2_x = t[0, 1]
        t2_y = t[1, 1]
        t2_z = t[2, 1]
        t3_x = t[0, 2]
        t3_y = t[1, 2]
        t3_z = t[2, 2]
        c0_new = np.zeros(3)
        c0_new[0] = (t1_x * c0[0] + t2_x * c0[1] + t3_x * c0[2]) * scale
        c0_new[1] = (t1_y * c0[0] + t2_y * c0[1] + t3_y * c0[2]) * scale
        c0_new[2] = (t1_z * c0[0] + t2_z * c0[1] + t3_z * c0[2]) * scale
        c1_new = np.zeros(3)
        c1_new[0] = (t1_x * c1[0] + t2_x * c1[1] + t3_x * c1[2]) * scale
        c1_new[1] = (t1_y * c1[0] + t2_y * c1[1] + t3_y * c1[2]) * scale
        c1_new[2] = (t1_z * c1[0] + t2_z * c1[1] + t3_z * c1[2]) * scale
        if direct:
            ABS = False
            scale, direct = CoordinateTransforms().conv_direct2cara(
                ABS, scale, t, natom, direct, position
            )
        CoordinateTransforms().conv_car2carABSa(scale, t, natom, direct, position)
        j = 0
        for i in range(natom):
            if c0_new[2] <= position[i, 2] <= c1_new[2]:
                ex_position[j, 0] = position[i, 0]
                ex_position[j, 1] = position[i, 1]
                ex_position[j, 2] = position[i, 2]
                ex_fix[j, 0] = fix[i, 0]
                ex_fix[j, 1] = fix[i, 1]
                ex_fix[j, 2] = fix[i, 2]
                ex_j[j] = i
                j += 1
        ex_natom = j
        nion = 0
        tmp = "ZZ"
        local_atom_index = 0
        for i in range(ex_natom):
            atom0 = int(atoms[int(ion[ex_j[i]])])
            atom_index0 = str(atoms_index[int(ion[ex_j[i]])])
            local_atom_index += 1
            if tmp != atom_index0:
                nion += 1
                if tmp != "ZZ":
                    ex_atoms.append(str(local_atom_index))
                    ex_atoms_index.append(str(tmp))
                local_atom_index = 0
            tmp = atom_index0
        ex_nion = nion
        ex_atoms.append(str(local_atom_index))
        ex_atoms_index.append(str(tmp))
        return ex_nion

    def extract_struct_param(self, scale, t, natom, direct, position, c0, c1):
        from sae.geometry.coordinates import CoordinateTransforms

        t1_x = t[0, 0]
        t1_y = t[1, 0]
        t1_z = t[2, 0]
        t2_x = t[0, 1]
        t2_y = t[1, 1]
        t2_z = t[2, 1]
        t3_x = t[0, 2]
        t3_y = t[1, 2]
        t3_z = t[2, 2]
        c0_new = np.zeros(3)
        c0_new[0] = (t1_x * c0[0] + t2_x * c0[1] + t3_x * c0[2]) * scale
        c0_new[1] = (t1_y * c0[0] + t2_y * c0[1] + t3_y * c0[2]) * scale
        c0_new[2] = (t1_z * c0[0] + t2_z * c0[1] + t3_z * c0[2]) * scale
        c1_new = np.zeros(3)
        c1_new[0] = (t1_x * c1[0] + t2_x * c1[1] + t3_x * c1[2]) * scale
        c1_new[1] = (t1_y * c1[0] + t2_y * c1[1] + t3_y * c1[2]) * scale
        c1_new[2] = (t1_z * c1[0] + t2_z * c1[1] + t3_z * c1[2]) * scale
        if direct:
            ABS = False
            scale, direct = CoordinateTransforms().conv_direct2cara(
                ABS, scale, t, natom, direct, position
            )
        CoordinateTransforms().conv_car2carABS(scale, t, natom, direct, position)
        j = 0
        for i in range(natom):
            if position[i, 2] >= c0_new[2] and position[i, 2] <= c1_new[2]:
                j += 1
        extract_natom = j
        return [scale, direct, extract_natom]
