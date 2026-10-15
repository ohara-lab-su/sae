# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.openmx.dos_methods import ReadMxDosMethod
import sys
import os
import re
import glob
import optparse
import numpy as np

try:
    ReadMxDosMethod = ReadMxDosMethod
except ImportError:
    ReadMxDosMethod = ReadMxDosMethod


class ReadMxPdos(ReadMxDosMethod):

    def __init__(self, name, suffix):
        from sae.common.text import TextFiles

        self.name = name
        self.suffix = suffix
        NSPIN = self.get_ispin()
        NATOM = self.get_natom()
        dosname = name + suffix
        pdos_list = glob.glob(dosname + ".atom*")
        if len(pdos_list) < 1:
            sys.exit("STOP: " + dosname + ".atom* file not found")
        NEDOS = sum((1 for line in open(pdos_list[0])))
        self.NATOM = NATOM
        self.NSPIN = NSPIN
        self.num = NEDOS
        ls = []
        for i in range(len(pdos_list)):
            pdos_name = pdos_list[i]
            subtract_name0 = dosname + ".atom"
            subtract_name1 = "\\..*"
            dst = re.sub(subtract_name0, "", pdos_name)
            dst = int(re.sub(subtract_name1, "", dst))
            ls.append(dst)
        atom_list = sorted(set(ls), key=ls.index)
        if atom_list < 1:
            sys.exit("STOP: Contradiction Number of atoms")
        self.ados = np.zeros((NEDOS, NATOM, NSPIN))
        self.intados = np.zeros((NEDOS, NATOM, NSPIN))
        for atom in atom_list:
            data, nline = TextFiles().read_dataline(dosname + ".atom" + str(atom))
            if nline != NEDOS:
                sys.exit("STOP: Contradiction Number of Data Line")
            for ispin in range(NSPIN):
                for j in range(nline):
                    self.ados[i, atom - 1, ispin] = float(data[i].split()[1 + ispin])
                    self.intados[i, atom - 1, ispin] = float(data[i].split()[2 + ispin])
        l_max = 4
        self.tdos_spd = np.zeros((NEDOS, l_max, NSPIN))
        self.inttdos_spd = np.zeros((NEDOS, l_max, NSPIN))
        l_max = 4
        self.ldos = np.zeros((NEDOS, l_max, NATOM, NSPIN))
        self.intldos = np.zeros((NEDOS, l_max, NATOM, NSPIN))
        lm_max = 1 + 3 + 5 + 7
        self.pdos = np.zeros((NEDOS, lm_max, NATOM, NSPIN))
        self.intpdos = np.zeros((NEDOS, lm_max, NATOM, NSPIN))
        self.eng = np.zeros((NEDOS, NATOM))
        for atom in atom_list:
            base = dosname + ".atom" + str(atom)
            orbit = "s"
            orbit_list = glob.glob(base + "." + orbit + "*")
            if len(orbit_list) > 0:
                for i in range(len(orbit_list)):
                    data, nline = TextFiles().read_dataline(orbit_list[i])
                    if nline != NEDOS:
                        sys.exit("STOP: Contradiction Number of Data Line")
                    for ispin in range(NSPIN):
                        for j in range(nline):
                            self.eng[j] = float(data[j].split()[0])
                            self.pdos[j, 0, atom - 1, ispin] = abs(
                                float(data[j].split()[1 + ispin])
                            )
                            self.intpdos[j, 0, atom - 1, ispin] = float(
                                data[j].split()[2 + ispin]
                            )
                            self.ldos[j, 0, atom - 1, ispin] = self.ldos[
                                j, 0, atom - 1, ispin
                            ] + abs(float(data[j].split()[1 + ispin]))
                            self.intpdos[j, 0, atom - 1, ispin] = self.intpdos[
                                j, 0, atom - 1, ispin
                            ] + float(data[j].split()[2 + ispin])
                            self.tdos_spd[j, 0, ispin] = self.tdos_spd[
                                j, 0, ispin
                            ] + abs(float(data[j].split()[1 + ispin]))
                            self.inttdos_spd[j, 0, ispin] = self.inttdos_spd[
                                j, 0, ispin
                            ] + float(data[j].split()[2 + ispin])
            orbit = "p"
            orbit_list = glob.glob(base + "." + orbit + "*")
            if len(orbit_list) > 0:
                for i in range(len(orbit_list)):
                    data, nline = TextFiles().read_dataline(orbit_list[i])
                    if nline != NEDOS:
                        sys.exit("STOP: Contradiction Number of Data Line")
                    for ispin in range(NSPIN):
                        for j in range(nline):
                            self.eng[j] = float(data[j].split()[0])
                            self.pdos[j, 1 + i, atom - 1, ispin] = abs(
                                float(data[j].split()[1 + ispin])
                            )
                            self.intpdos[j, 1 + i, atom - 1, ispin] = float(
                                data[j].split()[2 + ispin]
                            )
                            self.ldos[j, 1, atom - 1, ispin] = self.ldos[
                                j, 1, atom - 1, ispin
                            ] + abs(float(data[j].split()[1 + ispin]))
                            self.intldos[j, 1, atom - 1, ispin] = self.intldos[
                                j, 1, atom - 1, ispin
                            ] + float(data[j].split()[2 + ispin])
                            self.tdos_spd[j, 1, ispin] = self.tdos_spd[
                                j, 1, ispin
                            ] + abs(float(data[j].split()[1 + ispin]))
                            self.inttdos_spd[j, 1, ispin] = self.inttdos_spd[
                                j, 1, ispin
                            ] + float(data[j].split()[2 + ispin])
            orbit = "d"
            orbit_list = glob.glob(base + "." + orbit + "*")
            if len(orbit_list) > 0:
                for i in range(len(orbit_list)):
                    data, nline = TextFiles().read_dataline(orbit_list[i])
                    if nline != NEDOS:
                        sys.exit("STOP: Contradiction Number of Data Line")
                    for ispin in range(NSPIN):
                        for j in range(nline):
                            self.eng[i] = float(data[j].split()[0])
                            self.pdos[j, 4 + i, atom - 1, ispin] = abs(
                                float(data[j].split()[1 + ispin])
                            )
                            self.intpdos[j, 4 + i, atom - 1, ispin] = float(
                                data[j].split()[2 + ispin]
                            )
                            self.ldos[j, 2, atom - 1, ispin] = self.ldos[
                                j, 2, atom - 1, ispin
                            ] + abs(float(data[j].split()[1 + ispin]))
                            self.intldos[j, 2, atom - 1, ispin] = self.intldos[
                                j, 2, atom - 1, ispin
                            ] + float(data[j].split()[2 + ispin])
                            self.tdos_spd[j, 2, ispin] = self.tdos_spd[
                                j, 2, ispin
                            ] + abs(float(data[j].split()[1 + ispin]))
                            self.inttdos_spd[j, 2, ispin] = self.inttdos_spd[
                                j, 2, ispin
                            ] + float(data[j].split()[2 + ispin])
            orbit = "f"
            orbit_list = glob.glob(base + "." + orbit + "*")
            if len(orbit_list) > 0:
                for i in range(len(orbit_list)):
                    data, nline = TextFiles().read_dataline(orbit_list[i])
                    if nline != NEDOS:
                        sys.exit("STOP: Contradiction Number of Data Line")
                    for ispin in range(NSPIN):
                        for j in range(nline):
                            self.eng[i] = float(data[j].split()[0])
                            self.pdos[i, 9 + i, atom - 1, ispin] = abs(
                                float(data[j].split()[1 + ispin])
                            )
                            self.intpdos[i, 9 + i, atom - 1, ispin] = float(
                                data[j].split()[2 + ispin]
                            )
                            self.ldos[j, 3, atom - 1, ispin] = self.ldos[
                                j, 3, atom - 1, ispin
                            ] + abs(float(data[j].split()[1 + ispin]))
                            self.intldos[j, 3, atom - 1, ispin] = self.intldos[
                                j, 3, atom - 1, ispin
                            ] + float(data[j].split()[2 + ispin])
                            self.tdos_spd[j, 3, ispin] = self.tdos_spd[
                                j, 3, ispin
                            ] + abs(float(data[j].split()[1 + ispin]))
                            self.inttdos_spd[j, 3, ispin] = self.inttdos_spd[
                                j, 3, ispin
                            ] + float(data[j].split()[2 + ispin])
        self.pdos[:, 1, :, :] = self.pdos[:, 2, :, :]
        self.pdos[:, 2, :, :] = self.pdos[:, 3, :, :]
        self.pdos[:, 3, :, :] = self.pdos[:, 1, :, :]
        self.pdos[:, 4, :, :] = self.pdos[:, 6, :, :]
        self.pdos[:, 5, :, :] = self.pdos[:, 8, :, :]
        self.pdos[:, 6, :, :] = self.pdos[:, 4, :, :]
        self.pdos[:, 7, :, :] = self.pdos[:, 7, :, :]
        self.pdos[:, 8, :, :] = self.pdos[:, 5, :, :]
        self.intpdos[:, 1, :, :] = self.intpdos[:, 2, :, :]
        self.intpdos[:, 2, :, :] = self.intpdos[:, 3, :, :]
        self.intpdos[:, 3, :, :] = self.intpdos[:, 1, :, :]
        self.intpdos[:, 4, :, :] = self.intpdos[:, 6, :, :]
        self.intpdos[:, 5, :, :] = self.intpdos[:, 8, :, :]
        self.intpdos[:, 6, :, :] = self.intpdos[:, 4, :, :]
        self.intpdos[:, 7, :, :] = self.intpdos[:, 7, :, :]
        self.intpdos[:, 8, :, :] = self.intpdos[:, 5, :, :]

    def get_pdos(self, lm=0, atom=0, spin=0):
        self.pdos0 = self.pdos[:, lm, atom, spin]
        return self.pdos0

    def get_pdos_all(self):
        return self.pdos

    def get_ldos(self, l=0, atom=0, spin=0):
        self.ldos0 = self.ldos[:, l, atom, spin]
        return self.ldos0

    def get_ldos_all(self):
        return self.ldos

    def get_tdos_spd(self, l=0, spin=0):
        self.tdos_spd0 = self.tdos_spd[:, l, spin]
        return self.tdos_spd0

    def get_ldos_ion(self, l=0, ion=0, spin=0):
        NATOM = self.NATOM
        NSPIN = self.NSPIN
        NEDOS = self.num
        NION = self.get_nion()
        atoms_j = self.get_atoms_j()
        l_max = 4
        ldos_ion = np.zeros((NEDOS, l_max, NION, NSPIN))
        for spin in range(NSPIN):
            for atom in range(NATOM):
                ion1 = atoms_j[atom]
                for i in range(NEDOS):
                    for lm in range(0, 1):
                        ldos_ion[i, 0, ion1, spin] = (
                            ldos_ion[i, 0, ion, spin] + self.pdos[i, lm, atom, spin]
                        )
                    for lm in range(1, 4):
                        ldos_ion[i, 1, ion1, spin] = (
                            ldos_ion[i, 1, ion, spin] + self.pdos[i, lm, atom, spin]
                        )
                    for lm in range(4, 9):
                        ldos_ion[i, 2, ion1, spin] = (
                            ldos_ion[i, 2, ion, spin] + self.pdos[i, lm, atom, spin]
                        )
                    for lm in range(9, 16):
                        ldos_ion[i, 3, ion1, spin] = (
                            ldos_ion[i, 3, ion, spin] + self.pdos[i, lm, atom, spin]
                        )
        self.LDOS_ION = ldos_ion[:, l, ion, spin]
        return self.LDOS_ION

    def get_ldos_ion_all(self):
        pass

    def get_emax(self):
        from sae.openmx.tdos import ReadMxTdos

        suffix_tdos = ".DOS.Tetrahedron"
        if os.path.exists(self.name + suffix_tdos) or os.path.exists(
            self.name + suffix_tdos + ".gz"
        ):
            dos = ReadMxTdos(name, suffix_tdos)
            self.EMAX = dos.get_emax()
        return self.EMAX

    def get_emin(self):
        from sae.openmx.tdos import ReadMxTdos

        suffix_tdos = ".DOS.Tetrahedron"
        if os.path.exists(self.name + suffix_tdos) or os.path.exists(
            self.name + suffix_tdos + ".gz"
        ):
            dos = ReadMxTdos(name, suffix_tdos)
            self.EMIN = dos.get_emin()
        return self.EMIN

    def get_eng(self):
        from sae.openmx.tdos import ReadMxTdos

        suffix_tdos = ".DOS.Tetrahedron"
        if os.path.exists(self.name + suffix_tdos) or os.path.exists(
            self.name + suffix_tdos + ".gz"
        ):
            dos = ReadMxTdos(name, suffix_tdos)
            self.ENG = dos.get_eng()
        return self.ENG

    def get_tdos(self, spin=0):
        from sae.openmx.tdos import ReadMxTdos

        suffix_tdos = ".DOS.Tetrahedron"
        if os.path.exists(self.name + suffix_tdos) or os.path.exists(
            self.name + suffix_tdos + ".gz"
        ):
            dos = ReadMxTdos(name, suffix_tdos)
            self.TDOS = dos.get_tdos(spin)
        return self.TDOS

    def get_inttdos(self, spin=0):
        from sae.openmx.tdos import ReadMxTdos

        suffix_tdos = ".DOS.Tetrahedron"
        if os.path.exists(self.name + suffix_tdos) or os.path.exists(
            self.name + suffix_tdos + ".gz"
        ):
            dos = ReadMxTdos(name, suffix_tdos)
            self.INTTDOS = dos.get_inttdos(spin)
        return self.INTTDOS
