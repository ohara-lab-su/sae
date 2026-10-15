# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os


class SetsFields:

    def read_sets(
        self, cname, lattices, nion, sg_atoms, sg_atoms_index, sg_position, kpoints
    ):
        if not os.path.exists(cname):
            sys.exit("STOP: " + cname + " file not found")
        try:
            tmp = open(cname)
        except:
            tmp.close()
            sys.exit("STOP: " + cname + " does'nt open")
        setsfile = tmp.read()
        tmp.close()
        setslines = setsfile.split("\n")
        title = setslines[0]
        nspin = setslines[2]
        sgn = setslines[4]
        lattice_a = setslines[5].split()[0]
        lattice_b = setslines[5].split()[1]
        lattice_c = setslines[5].split()[2]
        alpha = setslines[6].split()[0]
        beta = setslines[6].split()[1]
        gamma = setslines[6].split()[2]
        lattices[0] = lattice_a
        lattices[1] = lattice_b
        lattices[2] = lattice_c
        lattices[3] = alpha
        lattices[4] = beta
        lattices[5] = gamma
        nion = int(setslines[8])
        sg_natom = 0
        index = 8
        for i in range(nion):
            index += 1
            tmp = setslines[index].split()
            sg_atoms_index.extend(tmp[0])
            sg_atoms[i] = int(tmp[1])
            for j in range(int(tmp[1])):
                index += 1
                tmp = setslines[index].split()
                sg_position[sg_natom, 0] = float(tmp[0])
                sg_position[sg_natom, 1] = float(tmp[1])
                sg_position[sg_natom, 2] = float(tmp[2])
                sg_natom += 1
        kinfo = int(setslines[index + 2])
        tmp = setslines[index + 3].split()
        kpoints[0] = int(tmp[0])
        kpoints[1] = int(tmp[1])
        kpoints[2] = int(tmp[2])
        return [title, nspin, kinfo]

    def read_sets_param(self, cname="sets.in"):
        if not os.path.exists(cname):
            sys.exit("STOP: " + cname + " file not found")
        try:
            tmp = open(cname)
        except:
            tmp.close()
            sys.exit("STOP: " + cname + " does'nt open")
        setsfile = tmp.read()
        tmp.close()
        setslines = setsfile.split("\n")
        sgn_index = str(setslines[4])
        nion = int(setslines[8])
        sg_natom = 0
        sg_atoms = []
        sg_atoms_index = []
        index = 8
        for i in range(nion):
            index += 1
            tmp = setslines[index].split()
            sg_atoms_index.extend(tmp[0])
            sg_atoms.extend(tmp[1])
            sg_natom = sg_natom + int(tmp[1])
            for j in range(int(tmp[1])):
                index += 1
        return (sgn_index, nion, sg_natom, sg_atoms)
