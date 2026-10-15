# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import optparse
import numpy as np
import pandas as pd


class ReadFdmSd2020(object):

    def __init__(
        self,
        sdname,
        suffix="_sd0.txt",
        inpname=None,
        bavname=None,
        absorber=None,
        weight=None,
    ):
        """
        :param sdname:  材料名(ex: Cu)
        :param suffix:  default '_sd0.txt'
        :param inpname: FDMNES input ファイルからいくつかの情報を読み込む
        :param bavname:
        :param absorber: absorber=[] :matrix
        :param weight:
        """
        from sae.fdmnes.fdmfile import ReadFdmFdmfile
        from sae.fdmnes.inp import ReadFdmInp

        print("===== sd2020 =====")
        if bavname is None:
            bavname = sdname
        if inpname is None:
            if os.path.exists("fdmfile.txt"):
                fdmfiletxt = ReadFdmFdmfile()
                inpname = fdmfiletxt.get_filout()
            else:
                inpname = "read_pdb.inp"
        print("sd name  = %s" % sdname)
        print("inp name = %s" % inpname)
        inpfile = inpname
        inpdir = os.path.dirname(sdname)
        if inpdir:
            inpname = inpdir + "/" + inpfile
        else:
            inpname = inpfile
        print("")
        print("******************************")
        inp = ReadFdmInp(inpname)
        if absorber is None:
            print("")
            print("---- ReadFdmSd ----")
            print("sdname + suffix = %s" % sdname + suffix)
            print("bavname_bav.txt = %s" % bavname + "_bav.txt")
            print("inpname         = %s" % inpname)
            print("-------------------")
            print("--- ReadFdmSd ------")
            df = self.__read_sd_file(sdname + suffix)
            if weight is not None:
                print(" weight = %s" % str(weight))
                df = df / float(weight)
        else:
            print("--- ReadFdmSd ------")
            print("--- average mode ---")
            if weight is None:
                n_site = float(len(absorber))
            else:
                print("    weight = %s" % str(weight))
                n_site = float(weight)
            sdname = bavname + "_" + str(absorber[0]) + suffix
            print("sum : %s" % str(sdname))
            df = self.__read_sd_file(sdname)
            dfsum = df.copy
            for i in range(1, len(absorber)):
                sdname = bavname + "_" + str(absorber[i]) + suffix
                print("sum : %s" % str(sdname))
                df = self.__read_sd_file(sdname)
                dfsum += df
            df = dfsum / n_site
        self.__num = len(df.values)
        print("START GET LDOS/DOS")
        _num_split = len(df.columns.values)
        if _num_split == 5:
            self.__lmax = 0
        elif _num_split == 10:
            self.__lmax = 1
        elif _num_split == 17:
            self.__lmax = 2
        else:
            print("*********** ERROR ***********, unknown header type")
            sys.exit(-1)
        print("lmax (sd) = %s" % self.__lmax)
        self.__ispin = int(inp.get_ispin())
        self.__mmax = int(2 * self.__lmax + 1)
        tmmax = 0
        for l in range(self.__lmax + 1):
            tmmax += (2 * l + 1) * self.__ispin
        total_orbit = tmmax
        total_row = _num_split
        print("lmax %s" % str(self.__lmax))
        print("ispin %s" % str(self.__ispin))
        print("mmax %s" % str(self.__mmax))
        print("total_row %s" % str(total_row))
        print("-----------")
        print("")
        print("index num = %d" % self.__num)
        self.__eng = np.zeros(self.__num)
        self.ylm = np.zeros((self.__num, self.__lmax + 1, self.__mmax, self.__ispin))
        self.ldos_all = np.zeros((self.__num, self.__lmax + 1, self.__ispin))
        self.tdos_all = np.zeros((self.__num, self.__ispin))
        self.intldos_all = np.zeros((self.__num, self.__lmax + 1, self.__ispin))
        self.inttdos_all = np.zeros((self.__num, self.__ispin))
        self.intylm = np.zeros((self.__num, self.__lmax + 1, self.__mmax, self.__ispin))
        self.ylm[:, 0, 0, 0] = df["s"].values
        self.ldos_all[:, 0, 0] = df["s"].values
        self.intldos_all[:, 0, 0] = df["Int(s)"].values
        if self.__lmax >= 1:
            self.ylm[:, 1, -1, 0] = df["py"].values
            self.ylm[:, 1, 0, 0] = df["pz"].values
            self.ylm[:, 1, 1, 0] = df["px"].values
            self.ldos_all[:, 1, 0] = df["p"].values
            self.intldos_all[:, 1, 0] = df["Int(p)"].values
        if self.__lmax >= 2:
            self.ylm[:, 2, -2, 0] = df["dxy"].values
            self.ylm[:, 2, -1, 0] = df["dyz"].values
            self.ylm[:, 2, 0, 0] = df["dz2"].values
            self.ylm[:, 2, 1, 0] = df["dxz"].values
            self.ylm[:, 2, 2, 0] = df["dx2-y2"].values
            self.ldos_all[:, 2, 0] = df["d"].values
            self.intldos_all[:, 2, 0] = df["Int(d)"].values
        self.inttdos_all[:, 0] = df["Int(total)"].values
        self.__eng = df["Energy"].values
        self.sd = df
        self.__emax = max(self.__eng)
        self.__emin = min(self.__eng)
        self.__ymax = 0.0

    def __read_sd_file(self, name):
        """
        :param name:  sdname + suffix
        :return: dataFrame
        """
        df = pd.read_table(name, header=0, sep="\\s+", skipinitialspace=True)
        self.__header = df.columns.values
        print(self.__header)
        print(df.index.values)
        return df

    def get_pdos(self, l=0, m=0, lm=None, spin=0):
        """
        2016/2020 互換 I/F
        pdos = np.zeros((self.nedos, self.lmax, self.mmax, self.nspin))

        :param l:
        :param m:
        :param lm: px, py などのキャラクター入力(lとmを個別に入力しなくて良い)
        :param spin:
        :return:
        """
        if lm != None and isinstance(lm, str):
            orbit_name = lm
            lml = lm.lower()
            if lml == "s":
                orbit_name = "s"
                l = 0
                m = 0
            if lml == "py" or lml == "p_y":
                orbit_name = "p_y"
                l = 1
                m = -1
            if lml == "pz" or lml == "p_z":
                orbit_name = "p_z"
                l = 1
                m = 0
            if lml == "px" or lml == "p_x":
                orbit_name = "p_x"
                l = 1
                m = 1
            if (
                lml == "dxy"
                or lml == "d_xy"
                or lml == "xy"
                or (lml == "yx")
                or (lml == "dyx")
                or (lml == "d_yx")
            ):
                orbit_name = "d_xy"
                l = 2
                m = -2
            if (
                lml == "dyz"
                or lml == "d_yz"
                or lml == "yz"
                or (lml == "zy")
                or (lml == "dzy")
                or (lml == "d_zy")
            ):
                orbit_name = "d_yz"
                l = 2
                m = -1
            if (
                lml == "dz2"
                or lml == "d_z^2"
                or lml == "d_z2"
                or (lml == "dz^2")
                or (lml == "z2")
                or (lml == "z^2")
                or (lml == "d_3z2")
                or (lml == "d3z^2")
                or (lml == "3z2")
                or (lml == "3z^2")
                or (lml == "r2")
                or (lml == "r^2")
                or (lml == "dr^2")
                or (lml == "d_r^2")
                or (lml == "d_r2")
                or (lml == "3z2-r2")
                or (lml == "3z^2-r^2")
                or (lml == "d_3z2-r2")
                or (lml == "d_3z^2-r^2")
            ):
                orbit_name = "d_z^2"
                l = 2
                m = 0
            if (
                lml == "dxz"
                or lml == "d_xz"
                or lml == "xz"
                or (lml == "dzx")
                or (lml == "zx")
                or (lml == "d_zx")
            ):
                orbit_name = "d_xz"
                l = 2
                m = 1
            if (
                lml == "x^2-y^2"
                or lml == "d_x^2-y^2"
                or lml == "d_x2-y2"
                or (lml == "x2-y2")
                or (lml == "dx2")
                or (lml == "x2")
                or (lml == "x^2")
                or (lml == "dx^2")
                or (lml == "dy2")
                or (lml == "y2")
                or (lml == "y^2")
                or (lml == "dy^2")
            ):
                orbit_name = "d_x^2-y^2"
                l = 2
                m = 2
        self.pdos = self.ylm[:, l, m, spin]
        self.__ymax = max(self.pdos)
        return self.pdos

    def get_ldos(self, l=0, spin=0):
        """
        2016/2020 互換 I/F
        LDOS(NEDOS,L,SPIN)

        :param l:
        :param spin:
        :return:
        """
        if isinstance(l, str):
            if l == "s" and self.__lmax >= 0:
                l = 0
            if l == "p" and self.__lmax >= 1:
                l = 1
            if l == "d" and self.__lmax >= 2:
                l = 2
            if l == "f" and self.__lmax >= 3:
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
        self.ldos = self.ldos_all[:, l, spin]
        return self.ldos

    def get_intldos(self, l=0, spin=0):
        """
        2016/2020 互換 I/F
        INTLDOS(NEDOS,L,SPIN)

        :param l:
        :param spin:
        :return:
        """
        if isinstance(l, str):
            if l == "s" and self.__lmax >= 0:
                l = 0
            if l == "p" and self.__lmax >= 1:
                l = 1
            if l == "d" and self.__lmax >= 2:
                l = 2
            if l == "f" and self.__lmax >= 3:
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
        self.intldos = self.intldos_all[:, l, spin]
        return self.intldos

    def get_tdos(self, spin=0):
        """TODS(NEDOS,SPIN)"""
        return self.tdos_all[:, spin]

    def get_inttdos(self, spin=0):
        """INTDOS(NEDOS,SPIN)"""
        return self.inttdos_all[:, spin]

    def get_eng(self):
        return self.__eng

    @property
    def eng(self):
        return self.__eng

    def get_emin(self):
        return self.__emin

    @property
    def emin(self):
        return self.__emin

    def get_emax(self):
        return self.__emax

    @property
    def emax(self):
        return self.__emax

    def get_ymax(self):
        return self.__ymax

    @property
    def ymax(self):
        return self.__ymax

    def get_header(self):
        return self.__header

    @property
    def header(self):
        return self.__header

    def get_num(self):
        """読み込んだ sd ファイルの行数"""
        return self.__num

    @property
    def num(self):
        return self.__num

    def get_sd(self):
        """読み込んだ sd ファイル丸ごと(平均化したら、平均化した値)"""
        return self.sd

    def get_lmax(self):
        """読み込んだ sd ファイルに基づいて lmax を抽出"""
        return self.__lmax

    @property
    def lmax(self):
        return self.__lmax

    def get_mmax(self):
        return self.__mmax

    @property
    def mmax(self):
        return self.__mmax

    def get_ispin(self):
        return self.__ispin

    @property
    def ispin(self):
        return self.__ispin
