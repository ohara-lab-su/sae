# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.openmx.dat_methods import ReadMxDatMethod
import sys
import os
import re
import numpy as np

try:
    ReadMxDatMethod = ReadMxDatMethod
except ImportError:
    ReadMxDatMethod = ReadMxDatMethod


class ReadMxDat(ReadMxDatMethod):

    def __init__(self, datname, suffix=".dat", sort=True, atoms_index=None):
        from sae.common.text import TextFiles
        from sae.structure.elements import ElementTable

        self.datlines, self.num = TextFiles().read_dataline(datname)
        BOHR = 0.529177
        comment_reg = re.compile("^#.*", re.IGNORECASE)
        reg_switch_off = re.compile("Off", re.IGNORECASE)
        reg_switch_on = re.compile("On", re.IGNORECASE)
        reg_title = re.compile(".*System\\.Name")
        reg_spin = re.compile(".*scf\\.SpinPolarization", re.IGNORECASE)
        reg_nion = re.compile(".*Species\\.Number")
        reg0_atoms_index = re.compile(".*\\<Definition\\.of\\.Atomic\\.Species")
        reg1_atoms_index = re.compile(".*Definition\\.of\\.Atomic\\.Species\\>")
        reg_natom = re.compile(".*Atoms\\.Number")
        reg_unit = re.compile(".*Atoms\\.SpeciesAndCoordinates\\.Unit")
        reg_unit0 = re.compile("AU", re.IGNORECASE)
        reg_unit1 = re.compile("Ang", re.IGNORECASE)
        reg_unit2 = re.compile("FRAC", re.IGNORECASE)
        reg0_atoms = re.compile(".*\\<Atoms\\.SpeciesAndCoordinates")
        reg1_atoms = re.compile(".*Atoms\\.SpeciesAndCoordinates\\>")
        reg_position1 = re.compile(".*\\<Atoms\\.SpeciesAndCoordinates")
        reg0_unit_vector = re.compile(".*Atoms\\.UnitVectors\\.Unit")
        reg2_unit_vector = re.compile(".*\\<Atoms\\.UnitVectors")
        reg3_unit_vector = re.compile(".*Atoms\\.UnitVectors\\>")
        reg_md0 = re.compile(".*\\<MD\\.Fixed\\.XYZ")
        reg_md1 = re.compile(".*MD\\.Fixed\\.XYZ\\>")
        self.ispin = 1
        self.scale = 1.0
        self.vasp_version = 5
        self.atoms_index = []
        self.t = np.zeros((3, 3))
        self.selective = False
        self.t_FLAG = False
        NION_FLAG = False
        NATOM_FLAG = False
        UNIT_FLAG = False
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg_title.match(self.datlines[i])):
                    src = self.datlines[i].split()[1]
                    self.system = re.sub(" *$", "", src)
                    self.title = self.system
                if not bool(comment_reg.match(self.datlines[i])):
                    if bool(reg_spin.match(self.datlines[i])):
                        if bool(reg_switch_off.match(self.datlines[i].split()[1])):
                            self.ispin = 1
                        elif bool(reg_switch_on.match(self.datlines[i].split()[1])):
                            self.ispin = 2
                        else:
                            sys.exit("STOP: unknown SpinPolarization switch")
                if bool(reg_nion.match(self.datlines[i])):
                    self.nion = int(self.datlines[i].split()[1])
                    if not NION_FLAG:
                        NION_FLAG = True
                        self.atoms = np.zeros(self.nion, dtype=int)
                if bool(reg0_atoms_index.match(self.datlines[i]) and NION_FLAG):
                    j = 1
                    while not bool(reg1_atoms_index.match(self.datlines[i + j])):
                        self.atoms_index.append(self.datlines[i + j].split()[0])
                        j += 1
                    if self.nion != j - 1:
                        sys.exit("STOP: Atomic.Species Tag Error")
                if bool(reg_natom.match(self.datlines[i])):
                    self.natom = int(self.datlines[i].split()[1])
                    if not NATOM_FLAG:
                        NATOM_FLAG = True
                        self.atoms_j = np.zeros(self.natom, dtype=int)
                        self.ion = np.zeros(self.natom)
                        self.position = np.zeros((self.natom, 3))
                        self.position_index = np.zeros(self.natom, dtype=int)
                        self.position_index_r = np.zeros(self.natom, dtype=int)
                        self.fix = np.zeros((self.natom, 3), dtype="S")
                if bool(reg_unit.match(self.datlines[i])):
                    if bool(reg_unit0.match(self.datlines[i].split()[1])):
                        self.direct = False
                        self.UNIT = BOHR
                    elif bool(reg_unit1.match(self.datlines[i].split()[1])):
                        self.direct = False
                        self.UNIT = 1.0
                    elif bool(reg_unit2.match(self.datlines[i].split()[1])):
                        self.direct = True
                        self.UNIT = 1.0
                    else:
                        sys.exit("STOP: Unknown Atoms.SpeciesAndCoordinates.Unit")
                    UNIT_FLAG = True
                if (
                    bool(reg0_atoms.match(self.datlines[i]))
                    and NION_FLAG
                    and NATOM_FLAG
                    and UNIT_FLAG
                ):
                    for j in range(self.natom):
                        for k in range(self.nion):
                            if (
                                self.datlines[i + j + 1].split()[1]
                                == self.atoms_index[k]
                            ):
                                self.atoms[k] += 1
                    if not bool(reg1_atoms.match(self.datlines[i + j + 1 + 1])):
                        sys.exit(
                            "STOP: Atomic.Number and Atoms.SpeciesAndCoordinates Tag Error"
                        )
                    ATOMS_FLAG = True
                if bool(reg_position1.match(self.datlines[i])) and ATOMS_FLAG:
                    l = 0
                    for k in range(self.nion):
                        for j in range(1, self.natom + 1):
                            if self.atoms_index[k] == self.datlines[i + j].split()[1]:
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
                    UNIT_FLAG = False
                if bool(reg0_unit_vector.match(self.datlines[i])):
                    if bool(reg_unit0.match(self.datlines[i].split()[1])):
                        self.UNIT = BOHR
                    elif bool(reg_unit1.match(self.datlines[i].split()[1])):
                        self.UNIT = 1.0
                    else:
                        sys.exit("STOP: Unknown Atoms.UnitVectors.Unit")
                    UNIT_FLAG = True
                if bool(reg2_unit_vector.match(self.datlines[i])) and UNIT_FLAG:
                    self.t_FLAG = True
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
                    if not bool(reg3_unit_vector.match(self.datlines[i + 1 + 3])):
                        sys.exit("STOP: Atoms.UnitVectors Error")
                if bool(reg_md0.match(self.datlines[i])):
                    self.selective = True
                if self.selective:
                    if bool(reg_md0.match(self.datlines[i])):
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
                        if self.natom != j - 1:
                            sys.exit(
                                "STOP: Atomic.Number and Atoms.SpeciesAndCoordinates Tag Error"
                            )
        j = 0
        for ion in range(self.nion):
            for atom in range(self.atoms[ion]):
                self.atoms_j[j] = int(ion)
                j += 1
        tmp = -1
        for i in range(self.nion):
            for k in range(self.atoms[i]):
                tmp += 1
                self.ion[tmp] = int(i)
        self.ion_local = np.zeros(self.natom, dtype=int)
        tmp = -1
        for j in range(self.nion):
            local = -1
            for k in range(int(self.atoms[j])):
                tmp += 1
                local += 1
                self.ion_local[tmp] = int(local)
        self.atoms_index_j = []
        for j in range(self.natom):
            self.atoms_index_j.append(self.atoms_index[self.atoms_j[j]])
        self.atoms_number = np.zeros(self.nion, dtype=int)
        for i in range(self.nion):
            self.atoms_number[i] = ElementTable().get_atomic_number1(
                str(self.atoms_index[i])
            )
        self.atoms_number_j = []
        for k in range(self.nion):
            for l in range(int(self.atoms[k])):
                num0 = ElementTable().get_atomic_number1(str(self.atoms_index[k]))
                self.atoms_number_j.append(num0)

    def get_title(self):
        return self.title

    def get_system(self):
        return self.system

    def get_scale(self):
        return self.scale

    def get_t(self):
        return self.t

    def get_vasp_version(self):
        return self.vasp_version

    def get_atoms(self):
        return self.atoms

    def get_atoms_j(self):
        return self.atoms_j

    def get_atoms_index(self):
        return self.atoms_index

    def get_atoms_number(self):
        return self.atoms_number

    def get_atoms_index_j(self):
        return self.atoms_index_j

    def get_atoms_number_j(self):
        return self.atoms_number_j

    def get_nion(self):
        return self.nion

    def get_natom(self):
        return self.natom

    def get_ion(self):
        return self.ion

    def get_ion_local(self):
        return self.ion_local

    def get_selective(self):
        return self.selective

    def get_direct(self):
        return self.direct

    def get_position(self):
        return self.position

    def get_fix(self):
        return self.fix

    def get_ispin(self):
        return self.ispin
