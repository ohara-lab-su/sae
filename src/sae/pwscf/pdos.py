# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import glob
import re
import numpy as np


class ReadPwPdos(object):

    def __init__(self, prefix):
        from sae.common.text import TextFiles

        self.datlines, self.num = TextFiles().read_dataline(prefix + ".pdos.pdos_tot")
        nedos = self.num - 1
        if len(self.datlines[1].split()) > 3:
            ispin = 2
        else:
            ispin = 1
        pdos_list = glob.glob(prefix + ".pdos.pdos_atm#*")
        if len(pdos_list) < 1:
            sys.exit("STOP: " + prefix + ".pdos.pdos_atm#* file not found")
        pdos_list.sort()
        atom_ls = []
        for f in pdos_list:
            tmp = re.sub(prefix + ".pdos.pdos_atm#", "", f)
            atom = int(re.sub("\\(.*", "", tmp))
            atom_ls.append(atom)
        atom_list = []
        for x in atom_ls:
            if x not in atom_list:
                atom_list.append(x)
        natom = len(atom_list)
        atoms_index_j = []
        for atom in atom_list:
            pname = glob.glob(prefix + ".pdos.pdos_atm#" + str(atom) + "*")[0]
            tmp = re.sub(prefix + ".pdos.pdos_atm#" + str(atom) + "\\(", "", pname)
            tmp = re.sub("\\)_wfc#.*", "", tmp).strip()
            atoms_index_j.append(tmp)
        l_index_j = []
        for atom in atom_list:
            tmp = glob.glob(prefix + ".pdos.pdos_atm#" + str(atom) + "(*")
            list_tmp = []
            for g in tmp:
                tmp0 = re.sub(prefix + ".pdos.pdos_atm#", "", g)
                tmp0 = re.sub("\\d*\\(.*#\\d\\(", "", tmp0)
                tmp0 = re.sub("\\)", "", tmp0)
                list_tmp.append(tmp0)
            l_index_j.append(list_tmp)
        l_list = []
        for i in range(natom):
            list_tmp = []
            for j in range(len(l_index_j[i])):
                l = l_index_j[i][j]
                if l == "s":
                    lmax = 0
                if l == "p":
                    lmax = 1
                if l == "d":
                    lmax = 2
                if l == "f":
                    lmax = 3
                list_tmp.append(lmax)
            l_list.append(list_tmp)
        l_max = 4
        self.ldos_all = np.zeros((nedos, l_max, natom, ispin))
        lm_max = 7
        lm_list = [1, 3, 5, 7]
        self.pdos_all = np.zeros((nedos, l_max, lm_max, natom, ispin))
        self.eng = np.zeros(nedos)
        for atom in range(natom):
            for ll in range(len(l_index_j[atom])):
                l = int(l_list[atom][ll])
                l_index = l_index_j[atom][ll]
                pname = (
                    prefix
                    + ".pdos.pdos_atm#"
                    + str(atom + 1)
                    + "("
                    + atoms_index_j[atom]
                    + ")_wfc#"
                    + str(ll + 1)
                    + "("
                    + l_index
                    + ")"
                )
                print(pname)
                if not os.path.exists(pname):
                    sys.exit("STOP: " + pname + " not found")
                data, nline = TextFiles().read_dataline1(pname)
                if nline != nedos:
                    sys.exit("STOP: Contradiction Number of Data Line :" + pname)
                for spin in range(ispin):
                    for line in range(nline):
                        self.eng[line] = float(data[line].split()[0])
                        self.ldos_all[line, l, atom, spin] = float(
                            data[line].split()[1 + spin]
                        )
                        for lm in range(lm_list[l]):
                            row = (
                                1
                                + ispin
                                - 1
                                + ispin
                                + (lm * ispin - 1 * (ispin - 1))
                                + spin
                            )
                            self.pdos_all[line, l, lm, atom, spin] = float(
                                data[line].split()[row]
                            )
        self.nedos = nedos
        self.ispin = ispin
        self.natom = natom
        self.atoms_index_j = atoms_index_j
        self.l_index_j = l_index_j
        self.lm_list = lm_list

    def get_ldos(self, l=0, atom=0, spin=0):
        if isinstance(l, str):
            if l == "s":
                l = 0
                l_index = "s"
            if l == "p":
                l = 1
                l_index = "p"
            if l == "d":
                l = 2
                l_index = "d"
            if l == "d":
                l = 3
                l_index = "4"
        if isinstance(l, int):
            if l == 0:
                l_index = "s"
            if l == 1:
                l_index = "p"
            if l == 2:
                l_index = "d"
            if l == 3:
                l_index = "f"
        if isinstance(spin, str):
            if spin == "up":
                spin = 0
            if spin == "dn":
                spin = 1
            if spin == "down":
                spin = 1
        FLAG_CHK = False
        for chk in self.l_index_j[atom]:
            if chk == l_index:
                FLAG_CHK = True
        if not FLAG_CHK:
            sys.exit("STOP: " + l_index + "-orbit not calculated")
        if spin > self.ispin - 1:
            sys.exit("STOP: spin = " + str(spin) + " not calculated")
        self.ldos = self.ldos_all[:, l, atom, spin]
        return self.ldos

    def get_pdos(self, l=0, lm=0, atom=0, spin=0):
        if isinstance(l, str):
            if l == "s":
                l = 0
                l_index = "s"
            if l == "p":
                l = 1
                l_index = "p"
            if l == "d":
                l = 2
                l_index = "d"
            if l == "d":
                l = 3
                l_index = "4"
        if isinstance(l, int):
            if l == 0:
                l_index = "s"
            if l == 1:
                l_index = "p"
            if l == 2:
                l_index = "d"
            if l == 3:
                l_index = "f"
        if isinstance(spin, str):
            if spin == "up":
                spin = 0
            if spin == "dn":
                spin = 1
            if spin == "down":
                spin = 1
        FLAG_CHK = False
        for chk in self.l_index_j[atom]:
            if chk == l_index:
                FLAG_CHK = True
        if not FLAG_CHK:
            sys.exit("STOP: " + l_index + "-orbit not calculated")
        if lm > self.lm_list[l] - 1:
            sys.exit("STOP: " + l_index + "-orbit , lm=" + str(lm) + " not calculated")
        if spin > self.ispin - 1:
            sys.exit("STOP: spin = " + str(spin) + " not calculated")
        self.pdos = self.pdos_all[:, l, lm, atom, spin]
        return self.pdos

    def get_pdos_all(self):
        return self.pdos_all

    def get_ldos_all(self):
        return self.ldos_all

    def get_natom(self):
        return self.natom

    def get_atoms_index_j(self):
        return self.atoms_index_j

    def get_nedos(self):
        return self.nedos

    def get_ispin(self):
        return self.ispin
