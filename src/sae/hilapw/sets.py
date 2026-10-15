# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import optparse
import numpy as np


class ReadHiSets(object):

    def __init__(self, cname="sets.in"):
        from sae.common.text import TextFiles

        self.datlines, self.num = TextFiles().read_dataline(cname)
        self.title = str(self.datlines[0])
        self.nspin = int(self.datlines[2])
        self.sgn = str(self.datlines[4])
        self.lattices = np.zeros(6)
        self.lattices[0] = self.datlines[5].split()[0]
        self.lattices[1] = self.datlines[5].split()[1]
        self.lattices[2] = self.datlines[5].split()[2]
        self.lattices[3] = self.datlines[6].split()[0]
        self.lattices[4] = self.datlines[6].split()[1]
        self.lattices[5] = self.datlines[6].split()[2]
        self.nion = int(self.datlines[8])
        self.position = []
        self.atoms_index = np.zeros(self.nion, dtype="S2")
        self.atoms = np.zeros(self.nion, dtype=int)
        self.kpoints = np.zeros(3, dtype=int)
        self.natom = 0
        off = 9
        for i in range(self.nion):
            line = self.datlines[off].split()
            self.atoms_index[i] = str(line[0])
            self.atoms[i] = int(self.datlines[off].split()[1])
            for j in range(int(line[1])):
                x = float(self.datlines[off + 1].split()[0])
                y = float(self.datlines[off + 1].split()[1])
                z = float(self.datlines[off + 1].split()[2])
                self.position.append([x, y, z])
                self.natom += 1
                off += 1
            off += 1
        self.kinfo = int(self.datlines[off + 1])
        self.kpoints[0] = int(self.datlines[off + 2].split()[0])
        self.kpoints[1] = int(self.datlines[off + 2].split()[1])
        self.kpoints[2] = int(self.datlines[off + 2].split()[2])

    def get_title(self):
        return self.title

    def get_position(self):
        return self.position
