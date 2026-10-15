# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import numpy as np


class ReadWienDos(object):

    def __init__(self, lists):
        from sae.common.text import TextFiles

        self.nfiles = len(lists)
        self.norbital = 0
        self.head_file = []
        self.head = []
        self.dos = []
        self.dos_list_atom = []
        self.dos_list_orbit = []
        for data in range(self.nfiles):
            name = lists[data]
            datlines, num = TextFiles().read_dataline(name)
            self.head_file.append(datlines[0])
            self.head_file.append(datlines[1])
            self.head_file.append(datlines[2])
            if data == 0:
                efermi0 = "^#EF="
                efermi1 = " *NDOS.*$"
                self.efermi = re.sub(efermi0, "", datlines[1])
                self.efermi = float(re.sub(efermi1, "", self.efermi))
                word0 = ".*NENRG="
                word1 = " *Gau.*$"
                self.nedos = re.sub(word0, "", datlines[1])
                self.nedos = int(re.sub(word1, "", self.nedos))
                word0 = ".*NDOS="
                word1 = " *NENRG.*$"
                ndos = re.sub(word0, "", datlines[1])
                ndos = int(re.sub(word1, "", ndos))
                self.dos_list_atom.append("ENERGY")
                self.dos_list_orbit.append("ENERGY")
                tmp = []
                for idos in range(self.nedos):
                    tmp.append(float(datlines[idos + 3].split()[0]))
                self.dos.append(tmp)
            label = datlines[2].split()
            del label[0:2]
            lorbit = 0
            for l in label:
                if not l == "total-DOS":
                    atom = int(re.sub(":.*", "", l))
                    orbit = str(re.sub("\\d:", "", l))
                    self.dos_list_atom.append(atom)
                    self.dos_list_orbit.append(orbit)
                elif l == "total-DOS":
                    atom = 0
                    orbit = "total-DOS"
                    self.dos_list_atom.append(atom)
                    self.dos_list_orbit.append(orbit)
                tmp = []
                for idos in range(self.nedos):
                    tmp.append(float(datlines[idos + 3].split()[lorbit + 1]))
                self.dos.append(tmp)
                lorbit += 1
            self.head.append(self.head_file)
            self.norbital += len(label)
        np.array(self.dos, dtype=float)

    def get_head(self):
        return self.head

    def get_efermi(self):
        return self.efermi

    def get_nedos(self):
        return self.nedos

    def get_nfiles(self):
        return self.nfiles

    def get_norbital(self):
        return self.norbital

    def get_eng(self):
        self.eng = self.dos[0]
        self.eng = np.array(self.eng)
        return self.eng

    def get_emax(self):
        self.emax = max(self.dos[0])
        return self.emax

    def get_emin(self):
        self.emin = min(self.dos[0])
        return self.emin

    def get_nion(self):
        work_list = list(self.dos_list_atom)
        for i in range(work_list.count("ENERGY")):
            work_list.remove("ENERGY")
        for i in range(work_list.count(0)):
            work_list.remove(0)
        plot_atoms = list(set(work_list))
        self.nion = len(plot_atoms)
        return self.nion

    def get_plot_ions(self):
        work_list = list(self.dos_list_atom)
        for i in range(work_list.count("ENERGY")):
            work_list.remove("ENERGY")
        for i in range(work_list.count(0)):
            work_list.remove(0)
        self.plot_ions = list(set(work_list))
        return self.plot_ions

    def get_plot_ions_index(self, case):
        from sae.wien2k.output0 import ReadWienOutput0

        if os.path.exists(case + ".output0"):
            output0_file = case + ".output0"
        elif os.path.exists(case + ".output0.gz"):
            output0_file = case + ".output0.gz"
        elif os.path.exists(case + ".output0000"):
            output0_file = case + ".output0000"
        elif os.path.exists(case + ".output0000.gz"):
            output0_file = case + ".output0000.gz"
        else:
            sys.exit("STOP: output0 file not found")
        output0 = ReadWienOutput0(output0_file)
        atoms_index = output0.get_atoms_index()
        plot_ions = self.get_plot_ions()
        self.plot_ions_index = []
        for atom in plot_ions:
            self.plot_ions_index.append(atoms_index[atom - 1])
        return self.plot_ions_index

    def get_plot_atoms_index(self, case):
        self.plot_atoms_index = self.get_plot_ions_index(case)
        return self.plot_atoms_index

    def get_raw_dos(self, atom=1, orbit="total", times=1.0):
        max_atom = len(self.dos_list_atom)
        max_orbit = len(self.dos_list_orbit)
        if not max_atom == max_orbit:
            sys.exit("STOP: not max_orbit == max_atom")
        if orbit == "total-DOS":
            atom = 0
        for i in range(max_atom):
            if str(self.dos_list_atom[i]) == str(atom):
                if str(self.dos_list_orbit[i]) == str(orbit):
                    self.dos_raw = np.array(self.dos[i])
                    break
        return self.dos_raw

    def get_ldos_ion(self, case="case", atom=1, orbit="total"):
        from sae.wien2k.output0 import ReadWienOutput0

        if os.path.exists(case + ".output0"):
            output0_file = case + ".output0"
        elif os.path.exists(case + ".output0.gz"):
            output0_file = case + ".output0.gz"
        elif os.path.exists(case + ".output0000"):
            output0_file = case + ".output0000"
        elif os.path.exists(case + ".output0000.gz"):
            output0_file = case + ".output0000.gz"
        else:
            sys.exit("STOP: output0 file not found")
        output0 = ReadWienOutput0(output0_file)
        atoms = output0.get_atoms()
        times = float(atoms[atom - 1])
        self.ldos_ion = self.get_raw_dos(atom=atom, orbit=orbit) * times
        return self.ldos_ion

    def chk_raw_dos(self, atom="1", orbit="total"):
        max_atom = len(self.dos_list_atom)
        max_orbit = len(self.dos_list_orbit)
        if not max_atom == max_orbit:
            sys.exit("STOP: not max_orbit == max_atom")
        if orbit == "total-DOS":
            atom = 0
        FLAG = False
        for i in range(max_atom):
            if str(self.dos_list_atom[i]) == str(atom):
                if str(self.dos_list_orbit[i]) == str(orbit):
                    FLAG = True
        return FLAG
