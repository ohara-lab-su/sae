# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import optparse
import numpy as np
import sys
import os


class MolecularDynamicsFields:

    def get_max_md(self, nloop, natom, position_loop):
        position_max_atom_xyz = np.zeros((natom, 3))
        position_min_atom_xyz = np.zeros((natom, 3))
        for xyz in range(0, 3):
            for j in range(natom):
                position_max_atom_xyz[j, xyz] = max(position_loop[:, j, xyz])
                position_min_atom_xyz[j, xyz] = min(position_loop[:, j, xyz])
        position_max_xyz = np.zeros(3)
        position_min_xyz = np.zeros(3)
        for xyz in range(0, 3):
            position_max_xyz[xyz] = max(position_max_atom_xyz[:, xyz])
            position_min_xyz[xyz] = min(position_min_atom_xyz[:, xyz])
        position_max = max(position_max_xyz[:])
        position_min = min(position_max_xyz[:])
        return [position_max, position_min]

    def read_md(self, cname, nloop, atoms_index_j, position_loop):
        if not os.path.exists(cname):
            sys.exit(cname + " file not found")
        try:
            tmp = open(cname)
        except:
            tmp.close()
            sys.exit("STOP: " + cname + " does'nt open")
        datfile = tmp.read()
        tmp.close()
        datlines = datfile.split("\n")
        natom = int(datlines[0])
        i = 0
        for l in range(nloop):
            i = i + 2
            for j in range(natom):
                tmp = datlines[i].split()
                atoms_index_j[j] = str(tmp[0])
                position_loop[l, j, 0] = float(tmp[1])
                position_loop[l, j, 1] = float(tmp[2])
                position_loop[l, j, 2] = float(tmp[3])
                i += 1
        return [natom]

    def read_md2(self, cname, nloop, atoms_index_j, position_loop, force_loop):
        if not os.path.exists(cname):
            sys.exit(cname + " file not found")
        try:
            tmp = open(cname)
        except:
            tmp.close()
            sys.exit("STOP: " + cname + " does'nt open")
        datfile = tmp.read()
        tmp.close()
        datlines = datfile.split("\n")
        natom = int(datlines[0])
        i = 0
        for l in range(nloop):
            i = i + 2
            for j in range(natom):
                tmp = datlines[i].split()
                nlist = len(tmp)
                atoms_index_j[j] = str(tmp[0])
                position_loop[l, j, 0] = float(tmp[1])
                position_loop[l, j, 1] = float(tmp[2])
                position_loop[l, j, 2] = float(tmp[3])
                if nlist >= 7:
                    force_loop[l, j, 0] = float(tmp[4])
                    force_loop[l, j, 1] = float(tmp[5])
                    force_loop[l, j, 2] = float(tmp[6])
                i += 1
        return [natom, nlist]

    def read_md3(self, cname, nloop, atoms_index_j, position_loop, force_loop):
        if not os.path.exists(cname):
            sys.exit(cname + " file not found")
        try:
            tmp = open(cname)
        except:
            tmp.close()
            sys.exit("STOP: " + cname + " does'nt open")
        datfile = tmp.read()
        tmp.close()
        datlines = datfile.split("\n")
        natom = int(datlines[0])
        i = 0
        energy_loop = np.zeros(nloop)
        atoms_index = []
        for l in range(nloop):
            tmp = datlines[i + 1].split()
            elist = len(tmp)
            if len(tmp) >= 5:
                energy_loop[l] = tmp[4]
            i = i + 2
            atoms_tmp = ""
            nion = 0
            for j in range(natom):
                tmp = datlines[i].split()
                atoms_index_j[j] = str(tmp[0])
                if atoms_index_j[j] != atoms_tmp:
                    nion += 1
                    atoms_tmp = atoms_index_j[j]
                    atoms_index.append(atoms_index_j[j])
                position_loop[l, j, 0] = float(tmp[1])
                position_loop[l, j, 1] = float(tmp[2])
                position_loop[l, j, 2] = float(tmp[3])
                nlist = len(tmp)
                if nlist >= 7:
                    force_loop[l, j, 0] = float(tmp[4])
                    force_loop[l, j, 1] = float(tmp[5])
                    force_loop[l, j, 2] = float(tmp[6])
                i += 1
        i = 0
        atoms = np.zeros(nion, dtype=int)
        for l in range(nloop):
            i = i + 2
            atoms_tmp = ""
            nion = 0
            local = 0
            for j in range(natom):
                tmp = datlines[i].split()
                atoms_index_j[j] = str(tmp[0])
                if atoms_index_j[j] != atoms_tmp:
                    local = 0
                    nion += 1
                    atoms_tmp = atoms_index_j[j]
                if atoms_index_j[j] == atoms_tmp:
                    local += 1
                    atoms[nion - 1] = local
                i += 1
        return [natom, nlist, elist, nion, atoms, atoms_index, energy_loop]

    def read_md_param(self, cname):
        if not os.path.exists(cname):
            sys.exit(cname + " file not found")
        try:
            tmp = open(cname)
        except:
            tmp.close()
            sys.exit("STOP: " + cname + " does'nt open")
        datfile = tmp.read()
        tmp.close()
        datlines = datfile.split("\n")
        total_line = len(datlines) - 1
        natom = int(datlines[0])
        j = 0
        step = natom + 2
        for i in range(0, total_line, step):
            j += 1
        nloop = j
        return [nloop, natom]
