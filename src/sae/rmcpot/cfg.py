# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.structure.base import Method
import traceback
import sys
import os
import numpy as np

try:
    Method = Method
except ImportError:
    Method = Method


class ReadRmcpotCfg(Method):
    """
    for RMC version 3 format
    """

    def __init__(self, cname="POSCAR.cfg", suffix=".cfg", sort=False, atoms_index=None):
        from sae.common.text import TextFiles
        from sae.rmcpot.conversion import RmcConversions
        from sae.structure.elements import ElementTable

        self.datlines, self.num = TextFiles().read_dataline(cname)
        print("cfg name = %s" % cname)
        print("atoms_index = %s" % atoms_index)
        try:
            self.header = str(self.datlines[0])
            self.comment = str(self.datlines[1])
            self.title = self.comment
            self.system = self.title
            self.moves = self.datlines[4]
            self.saved = self.datlines[5]
            self.natom = int(self.datlines[7].split()[0].strip("."))
            self.nion = int(self.datlines[8].split()[0].strip("."))
            self.nmoles = self.datlines[9].split()[0]
            self.angles = self.datlines[10].split()[0]
        except Exception as e:
            print("\n*** Error ***, %s" % e)
            print(traceback.format_exc())
            sys.exit(-1)
        else:
            print("")
            print("natom = %s" % self.natom)
            print("nion = %s" % self.nion)
            print("nmoles = %s" % self.nmoles)
            print("angles = %s" % self.angles)
            print("")
        self.vasp_version = 5
        self.direct = True
        self.selective = False
        self.scale = 1.0
        t1_x = float(self.datlines[14].split()[0])
        t1_y = float(self.datlines[14].split()[1])
        t1_z = float(self.datlines[14].split()[2])
        t2_x = float(self.datlines[15].split()[0])
        t2_y = float(self.datlines[15].split()[1])
        t2_z = float(self.datlines[15].split()[2])
        t3_x = float(self.datlines[16].split()[0])
        t3_y = float(self.datlines[16].split()[1])
        t3_z = float(self.datlines[16].split()[2])
        self.t = np.zeros((3, 3))
        self.t[0, 0] = float(t1_x)
        self.t[1, 0] = float(t1_y)
        self.t[2, 0] = float(t1_z)
        self.t[0, 1] = float(t2_x)
        self.t[1, 1] = float(t2_y)
        self.t[2, 1] = float(t2_z)
        self.t[0, 2] = float(t3_x)
        self.t[1, 2] = float(t3_y)
        self.t[2, 2] = float(t3_z)
        print("t1_x = %s" % self.t[0, 0])
        print("t1_y = %s" % self.t[1, 0])
        print("t1_z = %s" % self.t[2, 0])
        print("")
        print("t2_x = %s" % self.t[0, 1])
        print("t2_y = %s" % self.t[1, 1])
        print("t2_z = %s" % self.t[2, 1])
        print("")
        print("t3_x = %s" % self.t[0, 2])
        print("t3_y = %s" % self.t[1, 2])
        print("t3_z = %s" % self.t[2, 2])
        print("")
        lines = 17
        self.atoms = np.zeros(self.nion, dtype=int)
        for i in range(self.nion):
            lines += 1
            self.atoms[i] = int(self.datlines[lines].split()[0])
            print(self.atoms[i])
            lines += 1
            tmp = self.datlines[lines]
            lines += 1
            tmp = self.datlines[lines]
            lines += 1
            tmp = self.datlines[lines]
        if atoms_index is None:
            atoms_index = ["N", "O", "Ca", "K"]
        print("nion = %s" % self.nion)
        print("dummy atoms_index = %s" % atoms_index)
        index = 0
        self.atoms_j = np.zeros(self.natom, dtype=int)
        for j in range(self.nion):
            for k in range(self.atoms[j]):
                self.atoms_j[index] = j
                index += 1
        print("END of atoms index (1)")
        if atoms_index:
            self.atoms_index = [""] * self.nion
            if self.nion == len(atoms_index):
                for i in range(self.nion):
                    self.atoms_index[i] = atoms_index[i]
            self.atoms_index_j = []
            for k in range(self.nion):
                for l in range(int(self.atoms[k])):
                    self.atoms_index_j.append(str(self.atoms_index[k]))
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
            self.ion = np.zeros(self.natom, dtype=int)
            self.ion_local = np.zeros(self.natom, dtype=int)
            tmp = -1
            for j in range(self.nion):
                local = -1
                for k in range(int(self.atoms[j])):
                    tmp += 1
                    local += 1
                    self.ion[tmp] = int(j)
                    self.ion_local[tmp] = int(local)
        else:
            self.vasp_version = 4
            self.atoms_index = []
            self.atoms_index_j = []
            self.atoms_number = []
            self.atoms_number_j = []
            self.ion = []
            self.ion_local = []
        print("END of atoms index (2)")
        self.position = np.zeros((self.natom, 3))
        for i in range(self.natom):
            lines += 1
            self.position[i, 0] = float(self.datlines[lines].split()[0])
            self.position[i, 1] = float(self.datlines[lines].split()[1])
            self.position[i, 2] = float(self.datlines[lines].split()[2])
        self.fix = ["T"] * self.natom
        self.scale, self.direct = RmcConversions().conv_cfg2vaspa(
            self.scale, self.t, self.natom, self.direct, self.position
        )

    def get_comment(self):
        return self.comment

    def conv_cfg2vasp(self):
        from sae.rmcpot.conversion import RmcConversions

        self.scale, self.direct = RmcConversions().conv_cfg2vaspa(
            self.scale, self.t, self.natom, self.direct, self.position
        )
        return (self.scale, self.direct)
