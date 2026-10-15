# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import gzip
import re
import optparse
import numpy as np


class ReadProcar(object):

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
        self.num = len(self.datlines)

    def get_ispin(self):
        band_reg = re.compile("^band")
        for i in range(self.num):
            if bool(band_reg.match(self.datlines[i])):
                if "occ." == self.datlines[i].split()[6]:
                    occ = float(self.datlines[i].split()[7])
                    if occ > 1.0:
                        self.ISPIN = 1
                    else:
                        self.ISPIN = 2
                break
        return self.ISPIN

    def get_nkpts(self):
        self.NKPTS = 0
        if "k-points:" == str(self.datlines[1].split()[2]):
            self.NKPTS = int(self.datlines[1].split()[3])
        return self.NKPTS

    def get_nbands(self):
        self.NBANDS = 0
        if "bands:" == str(self.datlines[1].split()[6]):
            self.NBANDS = int(self.datlines[1].split()[7])
        return self.NBANDS

    def get_natom(self):
        self.NKPTS = 0
        if "k-points:" == str(self.datlines[1].split()[2]):
            if "ions:" == str(self.datlines[1].split()[10]):
                self.NATOM = int(self.datlines[1].split()[11])
        return self.NATOM

    def get_lorbit(self):
        ion_reg = re.compile("^ion")
        for i in range(self.num):
            if bool(ion_reg.match(self.datlines[i])):
                if len(self.datlines[i].split()) > 10:
                    self.LORBIT = 11
                else:
                    self.LORBIT = 10
                break
        return self.LORBIT

    def get_pro_all(self):
        NSPIN = self.get_ispin()
        NKPTS = self.get_nkpts()
        NBANDS = self.get_nbands()
        NATOM = self.get_natom()
        LORBIT = self.get_lorbit()
        if LORBIT > 10:
            LMMAX = 9
        else:
            LMMAX = 3
        kp = np.zeros((NKPTS, 4))
        eig = np.zeros((NBANDS, NKPTS, NSPIN))
        occ = np.zeros((NBANDS, NKPTS, NSPIN))
        if NATOM > 1:
            pro = np.zeros((LMMAX + 1, NATOM + 1, NBANDS, NKPTS, NSPIN))
            pro_ratio = np.zeros((LMMAX + 1, NATOM + 1, NBANDS, NKPTS, NSPIN))
        else:
            pro = np.zeros((LMMAX + 1, NATOM, NBANDS, NKPTS, NSPIN))
            pro_ratio = np.zeros((LMMAX + 1, NATOM, NBANDS, NKPTS, NSPIN))
        j = 2
        for s in range(NSPIN):
            if s == 1:
                j += 1
            for k in range(NKPTS):
                j += 1
                kp[k, 0] = float(self.datlines[j][18:29])
                kp[k, 1] = float(self.datlines[j][29:40])
                kp[k, 2] = float(self.datlines[j][40:51])
                kp[k, 3] = float(self.datlines[j][64:75])
                j += 1
                for i in range(NBANDS):
                    j += 1
                    eig[i, k, s] = float(self.datlines[j].split()[4])
                    occ[i, k, s] = float(self.datlines[j].split()[7])
                    j += 2
                    for a in range(NATOM):
                        j += 1
                        if LORBIT > 10:
                            pro[0, a, i, k, s] = float(self.datlines[j].split()[1])
                            pro[1, a, i, k, s] = float(self.datlines[j].split()[2])
                            pro[2, a, i, k, s] = float(self.datlines[j].split()[3])
                            pro[3, a, i, k, s] = float(self.datlines[j].split()[4])
                            pro[4, a, i, k, s] = float(self.datlines[j].split()[5])
                            pro[5, a, i, k, s] = float(self.datlines[j].split()[6])
                            pro[6, a, i, k, s] = float(self.datlines[j].split()[7])
                            pro[7, a, i, k, s] = float(self.datlines[j].split()[8])
                            pro[8, a, i, k, s] = float(self.datlines[j].split()[9])
                            pro[9, a, i, k, s] = float(self.datlines[j].split()[10])
                        else:
                            pro[0, a, i, k, s] = float(self.datlines[j].split()[1])
                            pro[1, a, i, k, s] = float(self.datlines[j].split()[2])
                            pro[2, a, i, k, s] = float(self.datlines[j].split()[3])
                            pro[3, a, i, k, s] = float(self.datlines[j].split()[4])
                    if NATOM > 1:
                        j += 1
                        a += 1
                        if LORBIT > 10:
                            pro[0, a, i, k, s] = float(self.datlines[j].split()[1])
                            pro[1, a, i, k, s] = float(self.datlines[j].split()[2])
                            pro[2, a, i, k, s] = float(self.datlines[j].split()[3])
                            pro[3, a, i, k, s] = float(self.datlines[j].split()[4])
                            pro[4, a, i, k, s] = float(self.datlines[j].split()[5])
                            pro[5, a, i, k, s] = float(self.datlines[j].split()[6])
                            pro[6, a, i, k, s] = float(self.datlines[j].split()[7])
                            pro[7, a, i, k, s] = float(self.datlines[j].split()[8])
                            pro[8, a, i, k, s] = float(self.datlines[j].split()[9])
                            pro[9, a, i, k, s] = float(self.datlines[j].split()[10])
                        else:
                            pro[0, a, i, k, s] = float(self.datlines[j].split()[1])
                            pro[1, a, i, k, s] = float(self.datlines[j].split()[2])
                            pro[2, a, i, k, s] = float(self.datlines[j].split()[3])
                            pro[3, a, i, k, s] = float(self.datlines[j].split()[4])
                    j += 1
                j += 1
        return [kp, eig, occ, pro, pro_ratio]

    def get_pro_spd(self):
        NSPIN = self.get_ispin()
        NKPTS = self.get_nkpts()
        NBANDS = self.get_nbands()
        NATOM = self.get_natom()
        LORBIT = self.get_lorbit()
        LMMAX = 3
        kp = np.zeros((NKPTS, 4))
        eig = np.zeros((NBANDS, NKPTS, NSPIN))
        occ = np.zeros((NBANDS, NKPTS, NSPIN))
        if NATOM > 1:
            pro = np.zeros((LMMAX + 1, NATOM + 1, NBANDS, NKPTS, NSPIN))
            pro_ratio = np.zeros((LMMAX + 1, NATOM + 1, NBANDS, NKPTS, NSPIN))
        else:
            pro = np.zeros((LMMAX + 1, NATOM, NBANDS, NKPTS, NSPIN))
            pro_ratio = np.zeros((LMMAX + 1, NATOM, NBANDS, NKPTS, NSPIN))
        j = 2
        for s in range(NSPIN):
            if s == 1:
                j += 1
            for k in range(NKPTS):
                j += 1
                kp[k, 0] = float(self.datlines[j][18:29])
                kp[k, 1] = float(self.datlines[j][29:40])
                kp[k, 2] = float(self.datlines[j][40:51])
                kp[k, 3] = float(self.datlines[j][64:75])
                j += 1
                for i in range(NBANDS):
                    j += 1
                    eig[i, k, s] = float(self.datlines[j].split()[4])
                    occ[i, k, s] = float(self.datlines[j].split()[7])
                    j += 2
                    for a in range(NATOM):
                        j += 1
                        if LORBIT > 10:
                            pro[0, a, i, k, s] = float(self.datlines[j].split()[1])
                            pro[1, a, i, k, s] = (
                                float(self.datlines[j].split()[2])
                                + +float(self.datlines[j].split()[3])
                                + +float(self.datlines[j].split()[4])
                            )
                            pro[2, a, i, k, s] = (
                                float(self.datlines[j].split()[5])
                                + +float(self.datlines[j].split()[6])
                                + +float(self.datlines[j].split()[7])
                                + +float(self.datlines[j].split()[8])
                                + +float(self.datlines[j].split()[9])
                            )
                            pro[3, a, i, k, s] = float(self.datlines[j].split()[10])
                        else:
                            pro[0, a, i, k, s] = float(self.datlines[j].split()[1])
                            pro[1, a, i, k, s] = float(self.datlines[j].split()[2])
                            pro[2, a, i, k, s] = float(self.datlines[j].split()[3])
                            pro[3, a, i, k, s] = float(self.datlines[j].split()[4])
                    if NATOM > 1:
                        j += 1
                        a += 1
                        if LORBIT > 10:
                            pro[0, a, i, k, s] = float(self.datlines[j].split()[1])
                            pro[1, a, i, k, s] = (
                                float(self.datlines[j].split()[2])
                                + +float(self.datlines[j].split()[3])
                                + +float(self.datlines[j].split()[4])
                            )
                            pro[2, a, i, k, s] = (
                                float(self.datlines[j].split()[5])
                                + +float(self.datlines[j].split()[6])
                                + +float(self.datlines[j].split()[7])
                                + +float(self.datlines[j].split()[8])
                                + +float(self.datlines[j].split()[9])
                            )
                            pro[3, a, i, k, s] = float(self.datlines[j].split()[10])
                        else:
                            pro[0, a, i, k, s] = float(self.datlines[j].split()[1])
                            pro[1, a, i, k, s] = float(self.datlines[j].split()[2])
                            pro[2, a, i, k, s] = float(self.datlines[j].split()[3])
                            pro[3, a, i, k, s] = float(self.datlines[j].split()[4])
                    j += 1
                j += 1
        return [kp, eig, occ, pro, pro_ratio]

    def get_max_eigenval(self):
        NSPIN = self.get_ispin()
        NBANDS = self.get_nbands()
        NKPTS = self.get_nkpts()
        kp, eig, occ, pro, pro_ratio = self.get_pro_all()
        all_eigen_list = np.zeros(NSPIN * NBANDS * NKPTS)
        i = 0
        for ispin in range(NSPIN):
            for j in range(NBANDS):
                for k in range(NKPTS):
                    all_eigen_list[i] = eig[j, k, ispin]
                    i += 1
        eigen_max = max(all_eigen_list)
        eigen_min = min(all_eigen_list)
        return [eigen_min, eigen_max]
