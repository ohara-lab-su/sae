# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import gzip
import numpy as np


class ReadVaspEigenval(object):

    def __init__(self, name):
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
            sys.exit("STOP: " + name + " or " + name + ".gz does'nt open")
        finally:
            tmp.close()
        self.datlines = datfile.split("\n")

    def get_natom(self):
        tmp = self.datlines[0].split()
        self.N_ATOM = int(tmp[0])
        return self.N_ATOM

    def get_title(self):
        src = str(self.datlines[4])
        self.SYSTEM = re.sub(" *$", "", src)
        return self.SYSTEM

    def get_nkpts(self):
        tmp = self.datlines[5].split()
        self.NKPTS = int(tmp[1])
        return self.NKPTS

    def get_nbands(self):
        tmp = self.datlines[5].split()
        self.NBANDS = int(tmp[2])
        return self.NBANDS

    def get_ispin(self):
        ispin_flag = len(self.datlines[8].split())
        if ispin_flag >= 3:
            self.NSPIN = 2
        else:
            self.NSPIN = 1
        return self.NSPIN

    def get_eigenval(self):
        NSPIN = self.get_ispin()
        NBANDS = self.get_nbands()
        NKPTS = self.get_nkpts()
        i = 6
        self.eigenval = np.zeros((NBANDS, NKPTS, NSPIN))
        for k in range(NKPTS):
            i += 1
            i += 1
            for j in range(NBANDS):
                tmp = self.datlines[i].split()
                ispin = 0
                self.eigenval[j, k, ispin] = float(tmp[1])
                if NSPIN >= 2:
                    ispin += 1
                    self.eigenval[j, k, ispin] = float(tmp[2])
                i += 1
        return self.eigenval

    def get_eigenval_kxyz(self):
        NBANDS = self.get_nbands()
        NKPTS = self.get_nkpts()
        i = 6
        self.eigenval_kxyzw = np.zeros((NKPTS, 4))
        for k in range(NKPTS):
            i += 1
            tmp = self.datlines[i].split()
            kx = float(tmp[0])
            ky = float(tmp[1])
            kz = float(tmp[2])
            w = float(tmp[3])
            self.eigenval_kxyzw[k, 0] = kx
            self.eigenval_kxyzw[k, 1] = ky
            self.eigenval_kxyzw[k, 2] = kz
            self.eigenval_kxyzw[k, 3] = w
            i += 1
            for j in range(NBANDS):
                i += 1
        return self.eigenval_kxyzw

    def get_max_eigenval(self):
        NSPIN = self.get_ispin()
        NBANDS = self.get_nbands()
        NKPTS = self.get_nkpts()
        eigenval = self.get_eigenval()
        all_eigen_list = np.zeros(NSPIN * NBANDS * NKPTS)
        i = 0
        for ispin in range(NSPIN):
            for j in range(NBANDS):
                for k in range(NKPTS):
                    all_eigen_list[i] = eigenval[j, k, ispin]
                    i += 1
        eigen_max = max(all_eigen_list)
        eigen_min = min(all_eigen_list)
        return [eigen_min, eigen_max]
