# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.structure.base import Method
import sys
import os
import re
import numpy as np

try:
    Method = Method
except ImportError:
    Method = Method


class ReadMxDatMethod(Method):

    def get_title(self):
        comment_reg = re.compile("^#.*", re.IGNORECASE)
        title_reg = re.compile(".*System\\.Name")
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(title_reg.match(self.datlines[i])):
                    src = self.datlines[i].split()[1]
                    self.SYSTEM = re.sub(" *$", "", src)
                    break
        return self.SYSTEM

    def get_ispin(self):
        comment_reg = re.compile("^#.*", re.IGNORECASE)
        reg_spin = re.compile(".*scf\\.SpinPolarization", re.IGNORECASE)
        reg_switch_off = re.compile("Off", re.IGNORECASE)
        reg_switch_on = re.compile("On", re.IGNORECASE)
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg_spin.match(self.datlines[i])):
                    if bool(reg_switch_off.match(self.datlines[i].split()[1])):
                        self.ispin = 1
                    elif bool(reg_switch_on.match(self.datlines[i].split()[1])):
                        self.ispin = 2
                    else:
                        sys.exit("STOP: unknown SpinPolarization switch")
        return self.ispin

    def get_natom(self):
        comment_reg = re.compile("^#.*", re.IGNORECASE)
        reg = re.compile(".*Atoms\\.Number")
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg.match(self.datlines[i])):
                    self.natom = int(self.datlines[i].split()[1])
                    break
        return self.natom

    def get_nion(self):
        comment_reg = re.compile("^#.*", re.IGNORECASE)
        reg = re.compile(".*Species\\.Number")
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg.match(self.datlines[i])):
                    self.NION = int(self.datlines[i].split()[1])
                    break
        return self.NION

    def get_atoms_index(self):
        nion = self.get_nion()
        comment_reg = re.compile("^#.*", re.IGNORECASE)
        reg0 = re.compile(".*\\<Definition\\.of\\.Atomic\\.Species")
        reg1 = re.compile(".*Definition\\.of\\.Atomic\\.Species\\>")
        self.atoms_index = []
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg0.match(self.datlines[i])):
                    j = 1
                    while not bool(reg1.match(self.datlines[i + j])):
                        self.atoms_index.append(self.datlines[i + j].split()[0])
                        j += 1
                    if nion != j - 1:
                        sys.exit("STOP: Atomic.Species Tag Error")
                    break
        return self.atoms_index

    def get_atoms(self):
        nion = self.get_nion()
        natom = self.get_natom()
        atoms_index = self.get_atoms_index()
        comment_reg = re.compile("^#.*", re.IGNORECASE)
        reg0 = re.compile(".*\\<Atoms\\.SpeciesAndCoordinates")
        reg1 = re.compile(".*Atoms\\.SpeciesAndCoordinates\\>")
        self.atoms = np.zeros(nion, dtype=int)
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg0.match(self.datlines[i])):
                    i += 1
                    for j in range(natom):
                        for k in range(nion):
                            if self.datlines[i + j].split()[1] == atoms_index[k]:
                                self.atoms[k] += 1
                    if not bool(reg1.match(self.datlines[i + j + 1])):
                        sys.exit(
                            "STOP: Atomic.Number and Atoms.SpeciesAndCoordinates Tag Error"
                        )
        return self.atoms

    def get_atoms_j(self):
        nion = self.get_nion()
        natom = self.get_natom()
        atoms = self.get_atoms()
        j = 0
        self.atoms_j = np.zeros(natom, dtype=int)
        for ion in range(nion):
            for atom in range(atoms[ion]):
                self.atoms_j[j] = int(ion)
                j += 1
        return self.atoms_j

    def get_ion(self):
        natom = self.get_natom()
        atoms = self.get_atoms()
        nion = self.get_nion()
        self.ion = np.zeros(natom)
        tmp = -1
        for i in range(nion):
            for k in range(atoms[i]):
                tmp += 1
                self.ion[tmp] = int(i)
        return self.ion

    def get_atoms_index_j(self):
        natom = self.get_natom()
        atoms_j = self.get_atoms_j()
        atoms_index = self.get_atoms_index()
        self.atoms_index_j = []
        for j in range(natom):
            self.atoms_index_j.append(atoms_index[atoms_j[j]])
        return self.atoms_index_j

    def get_left_natom(self):
        self.FLAG_left = False
        self.left_natom = 0
        comment_reg = re.compile("^#.*", re.IGNORECASE)
        reg = re.compile(".*LeftLeadAtoms\\.Number")
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg.match(self.datlines[i])):
                    self.FLAG_left = True
                    self.left_natom = int(self.datlines[i].split()[1])
                    break
        return self.left_natom

    def get_left_atoms_index_j(self):
        self.FLAG_left = False
        left_natom = self.get_left_natom()
        comment_reg = re.compile("^#.*", re.IGNORECASE)
        reg0 = re.compile(".*\\<LeftLeadAtoms\\.SpeciesAndCoordinates")
        self.left_atoms_index_j = []
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg0.match(self.datlines[i])):
                    self.FLAG_left = True
                    for j in range(left_natom):
                        self.left_atoms_index_j.append(
                            self.datlines[i + j + 1].split()[1]
                        )
                    break
        return self.left_atoms_index_j

    def get_left_position(self):
        self.FLAG_left = False
        left_natom = self.get_left_natom()
        comment_reg = re.compile("^#.*", re.IGNORECASE)
        reg0 = re.compile(".*\\<LeftLeadAtoms\\.SpeciesAndCoordinates")
        self.FLAG_left = False
        self.left_position = np.zeros((left_natom, 3))
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg0.match(self.datlines[i])):
                    self.FLAG_left = True
                    for j in range(left_natom):
                        self.left_position[j, 0] = (
                            float(self.datlines[i + j + 1].split()[2]) * self.UNIT
                        )
                        self.left_position[j, 1] = (
                            float(self.datlines[i + j + 1].split()[3]) * self.UNIT
                        )
                        self.left_position[j, 2] = (
                            float(self.datlines[i + j + 1].split()[4]) * self.UNIT
                        )
                    break
        return self.left_position

    def get_right_natom(self):
        self.FLAG_right = False
        self.right_natom = 0
        comment_reg = re.compile("^#.*", re.IGNORECASE)
        reg = re.compile(".*RightLeadAtoms\\.Number")
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg.match(self.datlines[i])):
                    self.FLAG_right = True
                    self.right_natom = int(self.datlines[i].split()[1])
                    break
        return self.right_natom

    def get_right_atoms_index_j(self):
        self.FLAG_right = False
        right_natom = self.get_right_natom()
        comment_reg = re.compile("^#.*", re.IGNORECASE)
        reg0 = re.compile(".*\\<RightLeadAtoms\\.SpeciesAndCoordinates")
        self.right_atoms_index_j = []
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg0.match(self.datlines[i])):
                    self.FLAG_right = True
                    for j in range(right_natom):
                        self.right_atoms_index_j.append(
                            self.datlines[i + j + 1].split()[1]
                        )
                    break
        return self.right_atoms_index_j

    def get_right_position(self):
        self.FLAG_right = False
        right_natom = self.get_right_natom()
        comment_reg = re.compile("^#.*", re.IGNORECASE)
        reg0 = re.compile(".*\\<RightLeadAtoms\\.SpeciesAndCoordinates")
        self.right_position = np.zeros((right_natom, 3))
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg0.match(self.datlines[i])):
                    self.FLAG_right = True
                    for j in range(right_natom):
                        self.right_position[j, 0] = (
                            float(self.datlines[i + j + 1].split()[2]) * self.UNIT
                        )
                        self.right_position[j, 1] = (
                            float(self.datlines[i + j + 1].split()[3]) * self.UNIT
                        )
                        self.right_position[j, 2] = (
                            float(self.datlines[i + j + 1].split()[4]) * self.UNIT
                        )
                    break
        return self.right_position

    def get_scale(self):
        return 1.0

    def get_t(self):
        BOHR = 0.529177
        comment_reg = re.compile("^#.*", re.IGNORECASE)
        reg_unit0 = re.compile("AU", re.IGNORECASE)
        reg_unit1 = re.compile("Ang", re.IGNORECASE)
        reg2 = re.compile(".*Atoms\\.UnitVectors\\.Unit")
        reg3 = re.compile(".*\\<Atoms\\.UnitVectors")
        reg4 = re.compile(".*Atoms\\.UnitVectors\\>")
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg2.match(self.datlines[i])):
                    if bool(reg_unit0.match(self.datlines[i].split()[1])):
                        self.UNIT = BOHR
                    elif bool(reg_unit1.match(self.datlines[i].split()[1])):
                        self.UNIT = 1.0
                    else:
                        sys.exit("STOP: Unknown Atoms.UnitVectors.Unit")
                    break
        self.t = np.zeros((3, 3))
        self.FLAG_t = False
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg3.match(self.datlines[i])):
                    self.FLAG_t = True
                    self.t[0, 0] = (
                        float(self.datlines[i + 1 + 0].split()[0]) * self.UNIT
                    )
                    self.t[1, 0] = (
                        float(self.datlines[i + 1 + 0].split()[1]) * self.UNIT
                    )
                    self.t[2, 0] = (
                        float(self.datlines[i + 1 + 0].split()[2]) * self.UNIT
                    )
                    self.t[0, 1] = (
                        float(self.datlines[i + 1 + 1].split()[0]) * self.UNIT
                    )
                    self.t[1, 1] = (
                        float(self.datlines[i + 1 + 1].split()[1]) * self.UNIT
                    )
                    self.t[2, 1] = (
                        float(self.datlines[i + 1 + 1].split()[2]) * self.UNIT
                    )
                    self.t[0, 2] = (
                        float(self.datlines[i + 1 + 2].split()[0]) * self.UNIT
                    )
                    self.t[1, 2] = (
                        float(self.datlines[i + 1 + 2].split()[1]) * self.UNIT
                    )
                    self.t[2, 2] = (
                        float(self.datlines[i + 1 + 2].split()[2]) * self.UNIT
                    )
                    if not bool(reg4.match(self.datlines[i + 1 + 3])):
                        sys.exit("STOP: Atoms.UnitVectors Error")
                    break
        return self.t

    def get_selective(self):
        comment_reg = re.compile("^#.*", re.IGNORECASE)
        reg_md0 = re.compile(".*\\<MD\\.Fixed\\.XYZ")
        self.selective = False
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg_md0.match(self.datlines[i])):
                    self.selective = True
                    break
        return self.selective

    def get_direct(self):
        comment_reg = re.compile("^#.*", re.IGNORECASE)
        reg_unit0 = re.compile("AU", re.IGNORECASE)
        reg_unit1 = re.compile("Ang", re.IGNORECASE)
        reg_unit2 = re.compile("FRAC", re.IGNORECASE)
        reg3 = re.compile(".*Atoms\\.SpeciesAndCoordinates\\.Unit")
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg3.match(self.datlines[i])):
                    if bool(reg_unit0.match(self.datlines[i].split()[1])):
                        direct = False
                    elif bool(reg_unit1.match(self.datlines[i].split()[1])):
                        direct = False
                    elif bool(reg_unit2.match(self.datlines[i].split()[1])):
                        direct = True
                    else:
                        sys.exit("STOP: Unknown Atoms.SpeciesAndCoordinates.Unit")
                    break
        return direct

    def get_position(self):
        BOHR = 0.529177
        comment_reg = re.compile("^#.*", re.IGNORECASE)
        reg_unit0 = re.compile("AU", re.IGNORECASE)
        reg_unit1 = re.compile("Ang", re.IGNORECASE)
        reg_unit2 = re.compile("FRAC", re.IGNORECASE)
        reg_position0 = re.compile(".*Atoms\\.SpeciesAndCoordinates\\.Unit")
        reg_position1 = re.compile(".*\\<Atoms\\.SpeciesAndCoordinates")
        natom = self.get_natom()
        nion = self.get_nion()
        atoms_index = self.get_atoms_index()
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg_position0.match(self.datlines[i])):
                    if bool(reg_unit0.match(self.datlines[i].split()[1])):
                        self.UNIT = BOHR
                    elif bool(reg_unit1.match(self.datlines[i].split()[1])):
                        self.UNIT = 1.0
                    elif bool(reg_unit2.match(self.datlines[i].split()[1])):
                        self.UNIT = 1.0
                    else:
                        sys.exit("STOP: Unknown Atoms.SpeciesAndCoordinates.Unit")
                    break
        self.position = np.zeros((natom, 3))
        self.position_index = np.zeros(natom, dtype=int)
        self.position_index_r = np.zeros(natom, dtype=int)
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg_position1.match(self.datlines[i])):
                    l = 0
                    for k in range(nion):
                        for j in range(1, natom + 1):
                            if atoms_index[k] == self.datlines[i + j].split()[1]:
                                self.position_index[l] = (
                                    int(self.datlines[i + j].split()[0]) - 1
                                )
                                self.position_index_r[j - 1] = l
                                self.position[l, 0] = (
                                    float(self.datlines[i + j].split()[2]) * self.UNIT
                                )
                                self.position[l, 1] = (
                                    float(self.datlines[i + j].split()[3]) * self.UNIT
                                )
                                self.position[l, 2] = (
                                    float(self.datlines[i + j].split()[4]) * self.UNIT
                                )
                                l += 1
                    break
        return self.position

    def get_fix(self):
        natom = self.get_natom()
        selective = self.get_selective()
        self.fix = np.zeros((natom, 3), dtype="S")
        if selective:
            comment_reg = re.compile("^#.*", re.IGNORECASE)
            reg_md0 = re.compile(".*\\<MD\\.Fixed\\.XYZ")
            reg_md1 = re.compile(".*MD\\.Fixed\\.XYZ\\>")
            self.selective = False
            for i in range(self.num):
                if not bool(comment_reg.match(self.datlines[i])):
                    if bool(reg_md0.match(self.datlines[i])):
                        self.selective = True
                        j = 1
                        while not bool(reg_md1.match(self.datlines[i + j])):
                            fix_x = int(self.datlines[i + j].split()[1])
                            fix_y = int(self.datlines[i + j].split()[2])
                            fix_z = int(self.datlines[i + j].split()[3])
                            if fix_x == 1:
                                fix_x = "F"
                            elif fix_x == 0:
                                fix_x = "T"
                            else:
                                sys.exit("STOP: unknown Fixed Parameter")
                            if fix_y == 1:
                                fix_y = "F"
                            elif fix_y == 0:
                                fix_y = "T"
                            else:
                                sys.exit("STOP: unknown Fixed Parameter")
                            if fix_z == 1:
                                fix_z = "F"
                            elif fix_z == 0:
                                fix_z = "T"
                            else:
                                sys.exit("STOP: unknown Fixed Parameter")
                            self.fix[self.position_index_r[j - 1], 0] = fix_x
                            self.fix[self.position_index_r[j - 1], 1] = fix_y
                            self.fix[self.position_index_r[j - 1], 2] = fix_z
                            j += 1
                        if natom != j - 1:
                            sys.exit(
                                "STOP: Atomic.Number and Atoms.SpeciesAndCoordinates Tag Error"
                            )
                        break
        return self.fix
