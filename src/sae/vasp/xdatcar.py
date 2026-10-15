# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import gzip
import re
import numpy as np


class ReadVaspXdat(object):

    def __init__(self, name):
        self.num_reg = re.compile("^[+-]?(\\d*\\.\\d+|\\d+\\.?\\d*)([eE][+-]?\\d+|)\\Z")
        self.selective_reg = re.compile("^S.*", re.IGNORECASE)
        self.direct_reg = re.compile("^D.*", re.IGNORECASE)
        self.car_reg = re.compile("^C.*", re.IGNORECASE)
        if os.path.exists(name):
            GZIP = False
        elif os.path.exists(name + ".gz"):
            GZIP = True
        else:
            sys.exit("STOP: " + name + " or " + name + ".gz file not found")
        try:
            if GZIP:
                tmp = gzip.open(name + ".gz")
            else:
                tmp = open(name)
            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: " + name + " does'nt open")
        finally:
            tmp.close()
        self.datlines = datfile.split("\n")
        i = 5
        atoms = self.datlines[i].split()
        if atoms[0].isdigit():
            self.vasp_version = 4
        else:
            self.vasp_version = 5
            atoms_index = list(atoms)
            i += 1
            atoms = self.datlines[i].split()
        self.nion = int(len(atoms))
        self.natom = 0
        for j in range(self.nion):
            sum = int(atoms[j])
            self.natom = self.natom + sum

    def get_nion(self):
        return self.nion

    def get_natom(self):
        return self.natom

    def get_vasp_version(self):
        return self.vasp_version

    def get_title(self):
        src = str(self.datlines[0])
        title = re.sub(" *$", "", src)
        return title

    def get_scale(self):
        scale = float(self.datlines[1])
        return scale

    def get_nloop(self):
        vasp_version = self.get_vasp_version()
        natom = self.get_natom()
        if vasp_version == 5:
            base = len(self.datlines) - 2 - 3 - 2
        else:
            base = len(self.datlines) - 2 - 3 - 1
        self.nloop = base / (natom + 1)
        return self.nloop

    def get_t(self):
        v = self.datlines[2].split()
        t1_x = float(v[0])
        t1_y = float(v[1])
        t1_z = float(v[2])
        v = self.datlines[3].split()
        t2_x = float(v[0])
        t2_y = float(v[1])
        t2_z = float(v[2])
        v = self.datlines[4].split()
        t3_x = float(v[0])
        t3_y = float(v[1])
        t3_z = float(v[2])
        self.t = np.zeros((3, 3))
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

    def get_atoms(self):
        vasp_version = self.get_vasp_version()
        i = 5
        self.atoms = []
        self.atoms_index = []
        if vasp_version == 4:
            self.atoms.extend(self.datlines[i].split())
        elif vasp_version == 5:
            self.atoms_index.extend(self.datlines[i].split())
            i += 1
            self.atoms.extend(self.datlines[i].split())
        else:
            sys.exit("Error: unknown VASP format")
        return self.atoms

    def get_atoms_index(self):
        vasp_version = self.get_vasp_version()
        i = 5
        self.atoms = []
        self.atoms_index = []
        if vasp_version == 4:
            self.atoms.extend(self.datlines[i].split())
        elif vasp_version == 5:
            self.atoms_index.extend(self.datlines[i].split())
            i += 1
            self.atoms.extend(self.datlines[i].split())
        else:
            sys.exit("Error: unknown VASP format")
        return self.atoms_index

    def get_direct(self):
        vasp_version = self.get_vasp_version()
        i = 6
        if vasp_version == 5:
            i += 1
        tmp = self.datlines[i].split()
        if bool(self.num_reg.match(tmp[0])):
            print("%s" % str(tmp[0]))
            sys.exit("STOP: Format Error")
        else:
            if bool(self.selective_reg.match(tmp[0])):
                i += 1
                tmp = self.datlines[i].split()
                self.selective = True
            else:
                self.selective = False
            if bool(self.num_reg.match(tmp[0])):
                print("%s" % str(tmp[0]))
                sys.exit("STOP: Format Error")
            if bool(self.direct_reg.match(tmp[0])):
                self.direct = True
            elif bool(self.car_reg.match(tmp[0])):
                self.direct = False
        return self.direct

    def get_xyz(self, loop=0):
        i = 6
        vasp_version = self.get_vasp_version()
        natom = self.get_natom()
        if vasp_version == 5:
            i = i + 2
            tmp = self.datlines[i + loop * (natom + 1) - 1].split()
            num = int(tmp[2])
            if num != loop + 1:
                sys.exit("STOP: loop number error")
        else:
            i = i + 1
        xyz = np.zeros((natom, 3))
        for j in range(natom):
            tmp = self.datlines[i + loop * (natom + 1) + j].split()
            xyz[j, 0] = float(tmp[0])
            xyz[j, 1] = float(tmp[1])
            xyz[j, 2] = float(tmp[1])
        return xyz
