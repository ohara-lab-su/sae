# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import numpy as np


class ReadLobCohp(object):

    def __init__(self, name="COHPCAR.lobster"):
        from sae.common.text import TextFiles

        self.datlines, self.num = TextFiles().read_dataline(name)
        self.nedos = int(self.datlines[1].split()[2])
        self.nbond = int(self.datlines[1].split()[0])
        self.nspin = int(self.datlines[1].split()[1])
        self.eng = np.zeros(self.nedos)
        self.cohp_all = np.zeros((self.nedos, self.nbond, self.nspin))
        self.icohp_all = np.zeros((self.nedos, self.nbond, self.nspin))
        self.bond_index = [""] * self.nbond
        self.bond_leng = np.zeros(self.nbond)
        self.bond_index[0] = "Average"
        leng0 = 0
        self.bond_max_index = 0
        for i in range(1, self.nbond):
            char0 = self.datlines[i + 2].split()[0]
            char1 = re.sub("^.*:", "", char0)
            self.bond_index[i] = re.sub("\\(.*", "", char1)
            length = float(re.sub("\\)", "", re.sub("^.*\\(", "", char0)).strip())
            if leng0 < length:
                leng0 = length
                self.bond_max_index = i
            self.bond_leng[i] = length
        self.bond_par_index = []
        self.bond_par = []
        for i in self.bond_index:
            li = i.split("->")
            par_index = []
            par = []
            for l in li:
                par_index.append(re.sub("\\d", "", l))
                par.append(re.sub("\\D", "", l))
            self.bond_par_index.append(par_index)
            self.bond_par.append(par)
        for i in range(self.nedos):
            line = i + 2 + self.nbond
            self.eng[i] = float(self.datlines[line].split()[0])
            for ispin in range(self.nspin):
                for bond in range(self.nbond):
                    row0 = 1 + 2 * bond + ispin * (2 * self.nbond)
                    row1 = 2 + 2 * bond + ispin * (2 * self.nbond)
                    self.cohp_all[i, bond, ispin] = float(
                        self.datlines[line].split()[row0]
                    )
                    self.icohp_all[i, bond, ispin] = float(
                        self.datlines[line].split()[row1]
                    )

    def get_nedos(self):
        return self.nedos

    def get_nspin(self):
        return self.nspin

    def get_nbond(self):
        return self.nbond

    def get_bond_index(self):
        return self.bond_index

    def get_bond_par(self):
        return self.bond_par

    def get_bond_par_index(self):
        return self.bond_par_index

    def get_bond_max_index(self):
        return self.bond_max_index

    def get_bond_leng(self):
        return self.bond_leng

    def get_eng(self):
        return self.eng

    def get_ave(self, spin=0):
        if isinstance(spin, str):
            if spin == "nonmag":
                spin = 0
            if spin == "non":
                spin = 0
            if spin == "up":
                spin = 0
            if spin == "dn":
                spin = 1
            if spin == "down":
                spin = 1
        self.ave = self.cohp_all[:, 0, spin]
        return self.ave

    def get_iave(self, spin=0):
        if isinstance(spin, str):
            if spin == "nonmag":
                spin = 0
            if spin == "non":
                spin = 0
            if spin == "up":
                spin = 0
            if spin == "dn":
                spin = 1
            if spin == "down":
                spin = 1
        self.ave = self.icohp_all[:, 0, spin]
        return self.ave

    def get_cohp(self, bond=0, spin=0):
        if isinstance(spin, str):
            if spin == "nonmag":
                spin = 0
            if spin == "non":
                spin = 0
            if spin == "up":
                spin = 0
            if spin == "dn":
                spin = 1
            if spin == "down":
                spin = 1
        self.cohp = self.cohp_all[:, bond, spin]
        return self.cohp

    def get_icohp(self, bond=0, spin=0):
        if isinstance(spin, str):
            if spin == "nonmag":
                spin = 0
            if spin == "non":
                spin = 0
            if spin == "up":
                spin = 0
            if spin == "dn":
                spin = 1
            if spin == "down":
                spin = 1
        self.icohp = self.icohp_all[:, bond, spin]
        return self.icohp
