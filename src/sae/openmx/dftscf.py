# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.openmx.out import ReadMxOut
import sys
import os
import re
import optparse
import numpy as np

try:
    ReadMxOut = ReadMxOut
except ImportError:
    ReadMxOut = ReadMxOut


class ReadMxDftscf(ReadMxOut):

    def __init__(self, cname):
        from sae.common.text import TextFiles

        self.datlines, self.num = TextFiles().read_dataline(cname)

    def get_n_ion_loop(self):
        md_text = ".*Total energy.*at MD ="
        md_reg = re.compile(md_text)
        self.n_ion_loop = 0
        for i in range(self.num):
            if bool(md_reg.match(self.datlines[i])):
                tmp = int(re.sub(md_text, "", self.datlines[i]))
                if self.n_ion_loop < tmp:
                    self.n_ion_loop = tmp
        return self.n_ion_loop

    def get_uele(self):
        md_start_txt = ".*SCF.*at MD="
        md_start_reg = re.compile(md_start_txt)
        scf_txt = ".*SCF=.*Uele="
        scf_reg = re.compile(scf_txt)
        n_ion_loop = self.get_n_ion_loop()
        max_n_scf = self.get_max_n_scf()
        self.uele = np.zeros((n_ion_loop + 1, max_n_scf))
        self.uele_index = np.zeros(n_ion_loop + 1, dtype=int)
        if not n_ion_loop == 0:
            i = 0
            md = 0
            while 1:
                if bool(md_start_reg.match(self.datlines[i])):
                    while not bool(scf_reg.match(self.datlines[i])):
                        i += 1
                    scf = 0
                    while bool(scf_reg.match(self.datlines[i])):
                        uele0 = float(re.sub(scf_reg, "", self.datlines[i]))
                        self.uele[md, scf] = uele0
                        self.uele_index[md] = scf
                        scf += 1
                        i += 1
                    self.uele_index[md] = scf
                    md += 1
                i += 1
                if md == n_ion_loop:
                    while 1:
                        if bool(md_start_reg.match(self.datlines[i])):
                            while not bool(scf_reg.match(self.datlines[i])):
                                i += 1
                            scf = 0
                            while bool(scf_reg.match(self.datlines[i])):
                                uele0 = float(re.sub(scf_reg, "", self.datlines[i]))
                                self.uele[md, scf] = uele0
                                self.uele_index[md] = scf
                                scf += 1
                                i += 1
                            self.uele_index[md] = scf
                            break
                        i += 1
                    break
        else:
            i = 0
            uele0 = []
            while 1:
                if bool(md_start_reg.match(self.datlines[i])):
                    while not bool(scf_reg.match(self.datlines[i])):
                        i += 1
                    while bool(scf_reg.match(self.datlines[i])):
                        uele0.append(float(re.sub(scf_reg, "", self.datlines[i])))
                        i += 1
                    break
                i += 1
            for j in range(len(uele0)):
                self.uele[0, j] = uele0[j]
            self.uele_index[0] = len(uele0)
        return (self.uele, self.uele_index)
