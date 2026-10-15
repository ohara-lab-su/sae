# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import optparse
import numpy as np


class ReadPwOut(object):

    def __init__(self, cname):
        from sae.common.text import TextFiles

        self.datlines, self.num = TextFiles().read_dataline(cname)
        natom_reg = re.compile(".*number of atoms/cell.*")
        nion_reg = re.compile(".*number of atomic types.*")
        nbands_reg = re.compile(".*number of Kohn-Sham states=.*")
        nsw_reg = re.compile(".*nstep.*")
        efermi_reg = re.compile(".*the Fermi energy is.*")
        nrho_reg = re.compile(".*negative rho.*")
        ion_loop_reg = re.compile(".*ATOMIC_POSITIONS.*")
        toten_ion_reg = re.compile(".*!.*total energy.*")
        scale_reg = re.compile(".*lattice parameter.*")
        bravais_reg = re.compile(".*bravais-lattice.*")
        save_reg = re.compile(".*save")
        self.nsw = 0
        self.n_ion_loop = 0
        self.atoms_index = []
        self.toten_ion = []
        self.efermi = "None"
        for line in self.datlines:
            if bool(bravais_reg.match(line)):
                ibrva = int(line.split()[3])
                if ibrva != 0:
                    sys.exit("STOP: ibrva != 0 ")
            if bool(scale_reg.match(line)):
                scale0 = float(line.split()[4])
                if line.split()[5] == "a.u.":
                    self.scale = scale0 * 0.529177249
                else:
                    self.scale = scale0
            if bool(natom_reg.match(line)):
                self.natom = int(line.split()[4])
            if bool(nion_reg.match(line)):
                self.nion = int(line.split()[5])
            if bool(nbands_reg.match(line)):
                self.nbands = int(line.split()[4])
            if bool(nsw_reg.match(line)):
                self.nsw = int(line.split()[2])
            if bool(nrho_reg.match(line)):
                if float(line.split()[5]) == 0.0:
                    self.ispin = 1
                else:
                    self.ispin = 2
            if bool(ion_loop_reg.match(line)):
                self.n_ion_loop += 1
            if bool(efermi_reg.match(line)):
                self.efermi = float(line.split()[4])
            if bool(toten_ion_reg.match(line)):
                self.toten_ion.append(float(line.split()[4]))
            if bool(save_reg.match(line)):
                tmp = re.sub(".*Writing output data file ", "", line)
                self.title = str(re.sub("\\.save", "", tmp))
        np.array(self.toten_ion)

    def get_atoms_index(self):
        species_v_reg = re.compile(".*atomic species.*valence")
        for i in range(self.num):
            if bool(species_v_reg.match(self.datlines[i])):
                for j in range(self.nion):
                    atom_name = self.datlines[i + j + 1].split()[0]
                    self.atoms_index.append(atom_name)
        return self.atoms_index

    def get_atoms(self):
        self.get_atoms_index()
        self.atoms = np.zeros(self.nion, dtype=int)
        atoms_reg = re.compile(".*site n.*")
        for i in range(self.num):
            line = self.datlines[i]
            if bool(atoms_reg.match(line)):
                for j in range(self.natom):
                    tmp = re.sub(" tau.*", "", self.datlines[i + j + 1])
                    tmp = re.sub("^ *\\d+ *", "", tmp)
                    tmp = re.sub(" *", "", tmp)
                    for k in range(self.nion):
                        if self.atoms_index[k] == tmp:
                            self.atoms[k] += 1
        return self.atoms

    def get_types(self):
        self.get_atoms()
        self.get_atoms_index()
        TYPES = [self.atoms, self.atoms_index]
        return [TYPES]

    def get_atoms_j(self):
        self.get_atoms()
        self.atoms_j = np.zeros(self.natom, dtype=int)
        j = 0
        for ion in range(self.nion):
            for atom in range(self.atoms[ion]):
                self.atoms_j[j] = int(ion)
                j += 1
        return self.atoms_j

    def get_atoms_index_j(self):
        position_reg = re.compile(".*ATOMIC_POSITIONS.*", re.IGNORECASE)
        self.atoms_index_j = []
        for i in range(self.num):
            if bool(position_reg.match(self.datlines[i])):
                for j in range(self.natom):
                    atom_name = self.datlines[i + j + 1].split()[0]
                    self.atoms_index_j.append(atom_name)
                break
        return self.atoms_index_j

    def get_t(self):
        self.t = np.zeros((3, 3))
        crystal_axes_reg = re.compile(".*crystal axes.*")
        for i in range(self.num):
            line = self.datlines[i]
            if bool(crystal_axes_reg.match(line)):
                t1_x = self.datlines[i + 1].split()[3]
                t1_y = self.datlines[i + 1].split()[4]
                t1_z = self.datlines[i + 1].split()[5]
                t2_x = self.datlines[i + 2].split()[3]
                t2_y = self.datlines[i + 2].split()[4]
                t2_z = self.datlines[i + 2].split()[5]
                t3_x = self.datlines[i + 3].split()[3]
                t3_y = self.datlines[i + 3].split()[4]
                t3_z = self.datlines[i + 3].split()[5]
                self.t[0, 0] = t1_x
                self.t[1, 0] = t1_y
                self.t[2, 0] = t1_z
                self.t[0, 1] = t2_x
                self.t[1, 1] = t2_y
                self.t[2, 1] = t2_z
                self.t[0, 2] = t3_x
                self.t[1, 2] = t3_y
                self.t[2, 2] = t3_z
        return self.t

    def get_t_initial(self):
        self.get_t()
        return self.t

    def get_position(self):
        ion_loop_reg = re.compile(".*ATOMIC_POSITIONS.*")
        self.position = np.zeros((self.natom, 3))
        for i in range(self.num):
            line = self.datlines[i]
            if bool(ion_loop_reg.match(line)):
                for j in range(self.natom):
                    self.position[j, 0] = self.datlines[i + j + 1].split()[1]
                    self.position[j, 1] = self.datlines[i + j + 1].split()[2]
                    self.position[j, 2] = self.datlines[i + j + 1].split()[3]
        return self.position

    def get_position_initial(self):
        self.get_position()
        return self.position

    def get_position_loop(self):
        ion_loop_reg = re.compile(".*ATOMIC_POSITIONS.*")
        self.position_loop = np.zeros((self.n_ion_loop, self.natom, 3))
        ion_loop = 0
        for i in range(self.num):
            line = self.datlines[i]
            if bool(ion_loop_reg.match(line)):
                for j in range(self.natom):
                    self.position_loop[ion_loop, j, 0] = self.datlines[
                        i + j + 1
                    ].split()[1]
                    self.position_loop[ion_loop, j, 1] = self.datlines[
                        i + j + 1
                    ].split()[2]
                    self.position_loop[ion_loop, j, 2] = self.datlines[
                        i + j + 1
                    ].split()[3]
                ion_loop += 1
        return self.position_loop

    def get_force_loop(self):
        self.force_loop = np.zeros((self.n_ion_loop, self.natom, 3))
        force_reg = re.compile(".*Forces acting on atoms.*")
        ion_loop = 0
        for i in range(self.num):
            if bool(force_reg.match(self.datlines[i])):
                for j in range(self.natom):
                    self.force_loop[ion_loop, j, 0] = self.datlines[i + j + 2].split()[
                        6
                    ]
                    self.force_loop[ion_loop, j, 1] = self.datlines[i + j + 2].split()[
                        7
                    ]
                    self.force_loop[ion_loop, j, 2] = self.datlines[i + j + 2].split()[
                        8
                    ]
                ion_loop += 1
        return self.force_loop

    def get_title(self):
        return self.title

    def get_natom(self):
        return self.natom

    def get_nion(self):
        return self.nion

    def get_nbands(self):
        return self.nbands

    def get_scale(self):
        return self.scale

    def get_nsw(self):
        return self.nsw

    def get_efermi(self):
        return self.efermi

    def get_ispin(self):
        return self.ispin

    def get_n_ion_loop(self):
        return self.n_ion_loop

    def get_toten_ion(self):
        return self.toten_ion

    def get_energy_loop(self):
        return self.toten_ion
