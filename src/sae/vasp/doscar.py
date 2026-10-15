# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import numpy as np


class ReadVaspDoscar(object):

    def __init__(self, name="DOSCAR"):
        from sae.common.text import TextFiles

        self.datlines, self.num = TextFiles().read_dataline(name)
        self.natom = int(self.datlines[0].split()[0])
        self.title = re.sub(" *$", "", str(self.datlines[4]))
        self.emax = float(self.datlines[5].split()[0])
        self.emin = float(self.datlines[5].split()[1])
        self.nedos = int(self.datlines[5].split()[2])
        self.efermi = float(self.datlines[5].split()[3])
        if len(self.datlines[7].split()) >= 4:
            self.nspin = 2
        else:
            self.nspin = 1
        self.ispin = self.nspin
        if len(self.datlines[6 + self.nedos + 1].split()) >= 10:
            self.lorbit = 11
        else:
            self.lorbit = 10
        lm_num = 0
        for atom0 in range(self.natom):
            _lm_num = len(
                self.datlines[6 + self.nedos * (atom0 + 1) + 1 + atom0].split()
            )
            if lm_num < _lm_num:
                lm_num = _lm_num
        if lm_num == 5:
            self.lmax = 1
            _spin = 1
        elif lm_num == 10:
            self.lmax = 2
            _spin = 1
        elif lm_num == 17:
            self.lmax = 3
            _spin = 1
        elif lm_num == 9:
            self.lmax = 1
            _spin = 2
        elif lm_num == 19:
            self.lmax = 2
            _spin = 2
        elif lm_num == 33:
            self.lmax = 3
            _spin = 2
        if not _spin == self.nspin:
            sys.exit("STOP: inconsistency  spin")
        lm_max = 0
        for l in range(self.lmax + 1):
            lm_max += (2 * l + 1) * self.nspin
        self.eng = np.zeros(self.nedos)
        self.tdos_all = np.zeros((self.nedos, self.nspin))
        self.inttdos_all = np.zeros((self.nedos, self.nspin))
        self.pdos_all = np.zeros((self.nedos, lm_max, self.natom, self.nspin))
        self.ldos_all = np.zeros((self.nedos, self.lmax + 1, self.natom, self.nspin))
        for i in range(self.nedos):
            self.eng[i] = float(self.datlines[6 + i].split()[0])
            dos_line = self.datlines[6 + i].split()
            if self.nspin >= 2:
                self.tdos_all[i, 0] = float(dos_line[1])
                self.tdos_all[i, 1] = float(dos_line[2])
                self.inttdos_all[i, 0] = float(dos_line[3])
                self.inttdos_all[i, 1] = float(dos_line[4])
            else:
                self.tdos_all[i, 0] = float(dos_line[1])
                self.inttdos_all[i, 0] = float(dos_line[2])
            for atom0 in range(self.natom):
                tmp = self.datlines[
                    6 + self.nedos * (atom0 + 1) + 1 + i + atom0
                ].split()
                if self.lorbit >= 11:
                    f = 1
                    if self.lmax >= 0:
                        for lm in range(0, 1):
                            for ispin in range(self.nspin):
                                self.pdos_all[i, lm, atom0, ispin] = float(tmp[f])
                                self.ldos_all[i, 0, atom0, ispin] = self.ldos_all[
                                    i, 0, atom0, ispin
                                ] + float(tmp[f])
                                f += 1
                    if self.lmax >= 1:
                        for lm in range(1, 4):
                            for ispin in range(self.nspin):
                                self.pdos_all[i, lm, atom0, ispin] = float(tmp[f])
                                self.ldos_all[i, 1, atom0, ispin] = self.ldos_all[
                                    i, 1, atom0, ispin
                                ] + float(tmp[f])
                                f += 1
                    if self.lmax >= 2:
                        for lm in range(4, 9):
                            for ispin in range(self.nspin):
                                self.pdos_all[i, lm, atom0, ispin] = float(tmp[f])
                                self.ldos_all[i, 2, atom0, ispin] = self.ldos_all[
                                    i, 2, atom0, ispin
                                ] + float(tmp[f])
                                f += 1
                    if self.lmax >= 3:
                        for lm in range(9, 16):
                            for ispin in range(self.nspin):
                                self.pdos_all[i, lm, atom0, ispin] = float(tmp[f])
                                self.ldos_all[i, 3, atom0, ispin] = self.ldos_all[
                                    i, 3, atom0, ispin
                                ] + float(tmp[f])
                                f += 1
                else:
                    f = 1
                    for lm in range(self.lmax + 1):
                        for ispin in range(self.nspin):
                            self.pdos_all[i, lm, atom0, ispin] = float(tmp[f])
                            f += 1
                    self.ldos_all = self.pdos_all
            self.tdos = self.tdos_all[:, 0]
            self.inttdos = self.inttdos_all[:, 0]

    def get_vbm(self, spin=0):
        METAL = True
        EPS = 1e-05
        for i in range(self.nedos):
            if abs(self.eng[i] - self.efermi) <= 0.2:
                if self.tdos_all[i, spin] < EPS:
                    METAL = False
                    self.e_vbm = float(self.eng[i - 1])
                    break
        if not METAL:
            pass
        else:
            self.e_vbm = 0.0
        return self.e_vbm

    def get_lmax(self):
        return self.lmax

    def get_ispin(self):
        return self.nspin

    def get_natom(self):
        return self.natom

    def get_title(self):
        return self.title

    def get_system(self):
        return self.title

    def get_emax(self):
        return self.emax

    def get_emin(self):
        return self.emin

    def get_nedos(self):
        return self.nedos

    def get_efermi(self):
        return self.efermi

    def get_lorbit(self):
        return self.lorbit

    def get_eng(self):
        return self.eng

    def get_ldos_all(self):
        return self.ldos_all

    def get_pdos_all(self):
        return self.pdos_all

    def get_tdos(self, spin=0):
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
        self.tdos = self.tdos_all[:, spin]
        return self.tdos

    def get_inttdos(self, spin=0):
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
        self.inttdos = self.inttdos_all[:, spin]
        return self.inttdos

    def get_pdos(self, lm=0, atom=0, spin=0):
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
        self.pdos = self.pdos_all[:, lm, atom, spin]
        return self.pdos

    def get_ldos(self, l=0, atom=0, spin=0):
        if isinstance(l, str):
            if l == "s":
                l = 0
            if l == "p":
                l = 1
            if l == "d":
                l = 2
            if l == "f":
                l = 3
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
        self.ldos = self.ldos_all[:, l, atom, spin]
        return self.ldos

    def get_tdos_spd(self, l=0, spin=0):
        if isinstance(l, str):
            if l.upper() == "S":
                l = 0
            if l.upper() == "P":
                l = 1
            if l.upper() == "D":
                l = 2
            if l.upper() == "F":
                l = 3
        tdos_spd = np.zeros((self.nedos, self.lmax + 1, self.nspin))
        for atom0 in range(self.natom):
            if self.lorbit >= 11:
                if self.lmax >= 0:
                    for lm in range(0, 1):
                        for ispin in range(self.nspin):
                            tdos_spd[:, 0, ispin] = (
                                tdos_spd[:, 0, ispin]
                                + self.pdos_all[:, lm, atom0, ispin]
                            )
                if self.lmax >= 1:
                    for lm in range(1, 4):
                        for ispin in range(self.nspin):
                            tdos_spd[:, 1, ispin] = (
                                tdos_spd[:, 1, ispin]
                                + self.pdos_all[:, lm, atom0, ispin]
                            )
                if self.lmax >= 2:
                    for lm in range(4, 9):
                        for ispin in range(self.nspin):
                            tdos_spd[:, 2, ispin] = (
                                tdos_spd[:, 2, ispin]
                                + self.pdos_all[:, lm, atom0, ispin]
                            )
                if self.lmax >= 3:
                    for lm in range(9, 16):
                        for ispin in range(self.nspin):
                            tdos_spd[:, 3, ispin] = (
                                tdos_spd[:, 3, ispin]
                                + self.pdos_all[:, lm, atom0, ispin]
                            )
            else:
                for l in range(self.lmax + 1):
                    for ispin in range(self.nspin):
                        tdos_spd[:, l, ispin] = (
                            tdos_spd[:, l, ispin] + self.pdos_all[:, l, atom0, ispin]
                        )
        self.tdos_spd = tdos_spd[:, l, spin]
        return self.tdos_spd

    def get_ldos_ion(self, l=0, ion=0, spin=0):
        from sae.vasp.outcar import ReadVaspOutcar

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
        oname = "OUTCAR"
        outcar = ReadVaspOutcar(oname)
        NATOM = outcar.get_natom()
        NION = outcar.get_nion()
        ATOMS_J = outcar.get_atoms_j()
        ldos_ion = np.zeros((self.nedos, self.lmax + 1, NION, self.nspin))
        for atom in range(NATOM):
            ion1 = ATOMS_J[atom]
            if self.lorbit >= 11:
                if self.lmax >= 0:
                    for lm in range(0, 1):
                        for ispin in range(self.nspin):
                            ldos_ion[:, 0, ion1, ispin] = (
                                ldos_ion[:, 0, ion1, ispin]
                                + self.pdos_all[:, lm, atom, ispin]
                            )
                if self.lmax >= 1:
                    for lm in range(1, 4):
                        for ispin in range(self.nspin):
                            ldos_ion[:, 1, ion1, ispin] = (
                                ldos_ion[:, 1, ion1, ispin]
                                + self.pdos_all[:, lm, atom, ispin]
                            )
                if self.lmax >= 2:
                    for lm in range(4, 9):
                        for ispin in range(self.nspin):
                            ldos_ion[:, 2, ion1, ispin] = (
                                ldos_ion[:, 2, ion1, ispin]
                                + self.pdos_all[:, lm, atom, ispin]
                            )
                if self.lmax >= 3:
                    for lm in range(9, 16):
                        for ispin in range(self.nspin):
                            ldos_ion[:, 3, ion1, ispin] = (
                                ldos_ion[:, 3, ion1, ispin]
                                + self.pdos_all[:, lm, atom, ispin]
                            )
            else:
                for l in range(self.lmax + 1):
                    for ispin in range(self.nspin):
                        ldos_ion[:, l, ion1, ispin] = (
                            ldos_ion[:, l, ion1, ispin]
                            + self.pdos_all[:, l, atom, ispin]
                        )
        self.ldos_ion = ldos_ion[:, l, ion, spin]
        return self.ldos_ion

    def get_ldos_ion_all(self):
        from sae.vasp.outcar import ReadVaspOutcar

        oname = "OUTCAR"
        outcar = ReadVaspOutcar(oname)
        NATOM = outcar.get_natom()
        NION = outcar.get_nion()
        ATOMS_J = outcar.get_atoms_j()
        ldos_ion = np.zeros((self.nedos, self.lmax + 1, NION, self.nspin))
        for atom in range(NATOM):
            ion1 = ATOMS_J[atom]
            for i in range(self.nedos):
                if self.lorbit >= 11:
                    if self.lmax >= 0:
                        for lm in range(0, 1):
                            for ispin in range(self.nspin):
                                ldos_ion[:, 0, ion1, ispin] = (
                                    ldos_ion[:, 0, ion1, ispin]
                                    + self.pdos_all[:, lm, atom, ispin]
                                )
                    if self.lmax >= 1:
                        for lm in range(1, 4):
                            for ispin in range(self.nspin):
                                ldos_ion[:, 1, ion1, ispin] = (
                                    ldos_ion[:, 1, ion1, ispin]
                                    + self.pdos_all[:, lm, atom, ispin]
                                )
                    if self.lmax >= 2:
                        for lm in range(4, 9):
                            for ispin in range(self.nspin):
                                ldos_ion[:, 2, ion1, ispin] = (
                                    ldos_ion[i, 2, ion1, ispin]
                                    + self.pdos_all[:, lm, atom, ispin]
                                )
                    if self.lmax >= 3:
                        for lm in range(9, 16):
                            for ispin in range(self.nspin):
                                ldos_ion[:, 3, ion1, ispin] = (
                                    ldos_ion[i, 3, ion1, ispin]
                                    + self.pdos_all[:, lm, atom, ispin]
                                )
                else:
                    for l in range(self.lmax + 1):
                        for ispin in range(self.nspin):
                            ldos_ion[:, l, ion1, ispin] = (
                                ldos_ion[:, l, ion1, ispin]
                                + self.pdos_all[:, lm, atom, ispin]
                            )
        self.ldos_ion_all = ldos_ion
        return self.ldos_ion_all
