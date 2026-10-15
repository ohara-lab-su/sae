# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import numpy as np


class ReadWienOutput0(object):

    def __init__(self, name):
        from sae.common.text import TextFiles

        self.datlines, self.num = TextFiles().read_dataline(name)
        ion_txt = "^:NATO"
        ion_reg = re.compile(ion_txt)
        not_equiv_txt = ".*NOT EQUIV ATOM"
        not_equiv_reg = re.compile(not_equiv_txt)
        equiv_txt = " +EQUIV ATOM"
        equiv_reg = re.compile(equiv_txt)
        spin_txt = ".*IZED CALCULATION"
        spin_reg = re.compile(spin_txt)
        self.atoms_index = []
        i = 0
        j = 0
        while i < self.num:
            if bool(ion_reg.match(self.datlines[i])):
                self.nion = int(self.datlines[i].split()[2])
                self.natom = int(self.datlines[i].split()[5])
                self.atoms = np.zeros(self.nion, dtype=int)
            if bool(not_equiv_reg.match(self.datlines[i])):
                atom = self.datlines[i].split()[3]
                self.atoms_index.append(atom)
                while not bool(not_equiv_reg.match(self.datlines[i + 1])):
                    if bool(equiv_reg.match(self.datlines[i])):
                        self.atoms[j] = int(self.datlines[i].split()[2])
                    if bool(spin_reg.match(self.datlines[i])):
                        break
                    i += 1
                j += 1
            if bool(spin_reg.match(self.datlines[i])):
                spin_word = self.datlines[i].split()[0]
                if spin_word == "SPINPOLARIZED":
                    self.nspin = 2
                elif spin_word == "NON-SPINPOLARIZED":
                    self.nspin = 1
                else:
                    sys.exit("STOP: UNKNOWN SPIN MODE")
            i += 1

    def get_ions_index(self):
        return self.atoms_index

    def get_atoms_index(self):
        return self.atoms_index

    def get_atoms(self):
        return self.atoms

    def get_ispin(self):
        return self.nspin

    def get_nion(self):
        return self.nion

    def get_natom(self):
        return self.natom
