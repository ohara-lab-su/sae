# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import optparse
import numpy as np


class ReadFdmSd2016(object):

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
        :param inpname:
        :param bavname:
        :param absorber: absorber=[] :matrix (複数の吸収端の同時読み込みに対応する)
        :param weight:
        """
        from sae.fdmnes.fdmfile import ReadFdmFdmfile
        from sae.fdmnes.inp import ReadFdmInp
        from sae.common.text import TextFiles

        print("===== sd2016 =====")
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
        if absorber is None:
            print("")
            print("---- ReadFdmSd ----")
            print("sdname + suffix = %s" % sdname + suffix)
            print("bavname_bav.txt = %s" % bavname + "_bav.txt")
            print("inpname         = %s" % inpname)
            print("-------------------")
            self.datlines, self.__num = TextFiles().read_dataline(sdname + suffix)
            self.__header = self.datlines[0]
            if weight is not None:
                print("--- ReadFdmSd ------")
                print("--- weight mode ----")
                print(" weight = %s" % str(weight))
                sdname0 = sdname + suffix
                row, num = TextFiles().read_row(sdname0, column=1)
                print(" num = %s" % num)
                print(" row = %s" % row)
                numdata = np.zeros((num, row))
                for j in range(1, num):
                    for r in range(1, row):
                        numdata[j, r] = float(self.datlines[j].split()[r]) / float(
                            weight
                        )
                for i in range(1, num):
                    numdata[i, 0] = float(self.datlines[i].split()[0])
                listdata = list(numdata)
                self.datlines = []
                self.datlines.append("")
                for i in range(1, num):
                    self.datlines.append(
                        "".join(str(listdata[i]))
                        .replace("\n", "")
                        .replace("[", "")
                        .replace("]", "")
                    )
                self.datlines[0] = self.__header
        else:
            print("--- ReadFdmSd ------")
            print("--- average mode ---")
            sdname0 = bavname + "_" + str(absorber[0]) + suffix
            row, num = TextFiles().read_row(sdname0, column=1)
            if weight is None:
                n_site = float(len(absorber))
            else:
                print("    weight = %s" % str(weight))
                n_site = float(weight)
            dsum = np.zeros((num, row))
            dtmp = np.zeros((num, row))
            numdata = np.zeros((num, row))
            for i in range(len(absorber)):
                sdname = bavname + "_" + str(absorber[i]) + suffix
                print("sum : %s" % str(sdname))
                datatmp, num0 = TextFiles().read_dataline(sdname)
                if i == 0:
                    self.__header = datatmp[0]
                for j in range(1, num):
                    for r in range(1, row):
                        dtmp[j, r] = datatmp[j].split()[r]
                dsum = dtmp + dsum
            numdata = dsum / n_site
            for i in range(1, num):
                numdata[i, 0] = datatmp[i].split()[0]
            listdata = list(numdata)
            self.datlines = []
            self.datlines.append("")
            for i in range(1, num):
                self.datlines.append(
                    "".join(str(listdata[i]))
                    .replace("\n", "")
                    .replace("[", "")
                    .replace("]", "")
                )
            self.datlines[0] = self.__header
            self.__num = num
        print("START GET LDOS/DOS")
        self.sd = self.datlines
        inp = ReadFdmInp(inpname)
        nl = len(self.__header.split())
        tmp = self.__header.split()[nl - 1]
        tmp = re.sub(".*\\(", "", tmp)
        try:
            self.__lmax = int(re.sub("\\).*", "", tmp))
        except:
            self.__lmax = int(re.sub(",.*\\).*", "", tmp))
        print("lmax       = %s" % self.__lmax)
        self.__ispin = int(inp.get_ispin())
        self.__mmax = int(2 * self.__lmax + 1)
        tmmax = 0
        for l in range(self.__lmax + 1):
            tmmax += (2 * l + 1) * self.__ispin
        total_orbit = tmmax
        total_row = 1 + self.__ispin + total_orbit * 2 + (l + 1) * 2 * self.__ispin
        if absorber is None:
            if len(self.datlines[0].split()) != total_row:
                print("lmax %s" % str(self.__lmax))
                print("ispin %s" % str(self.__ispin))
                print("mmax %s" % str(self.__mmax))
                print("total_row %s" % str(total_row))
                print("-----------")
                print(
                    "%s = %s"
                    % (str(len(self.datlines[0].split())), str(self.datlines[0]))
                )
                sys.exit("STOP: unknown type " + sdname + suffix)
        self.ylm = np.zeros(
            (self.__num - 1, self.__lmax + 1, self.__mmax, self.__ispin)
        )
        self.intylm = np.zeros(
            (self.__num - 1, self.__lmax + 1, self.__mmax, self.__ispin)
        )
        self.ldos_all = np.zeros((self.__num - 1, self.__lmax + 1, self.__ispin))
        self.tdos_all = np.zeros((self.__num - 1, self.__ispin))
        self.intldos_all = np.zeros((self.__num - 1, self.__lmax + 1, self.__ispin))
        self.inttdos_all = np.zeros((self.__num - 1, self.__ispin))
        self.eng = np.zeros(self.__num - 1)
        for i in range(1, self.__num):
            row = 0
            self.eng[i - 1] = float(self.datlines[i].split()[row])
            row += 1
            for s in range(self.__ispin):
                self.inttdos_all[i - 1, s] = float(self.datlines[i].split()[row])
                row += 1
            for ll in range(self.__lmax + 1):
                m0 = 0
                for m in range(-ll, ll + 1):
                    for s in range(self.__ispin):
                        self.ylm[i - 1, ll, m0, s] = float(
                            self.datlines[i].split()[row]
                        )
                        row += 1
                        self.intylm[i - 1, ll, m0, s] = float(
                            self.datlines[i].split()[row]
                        )
                        row += 1
                    m0 += 1
                for s in range(self.__ispin):
                    self.ldos_all[i - 1, ll, s] = float(self.datlines[i].split()[row])
                    self.tdos_all[i - 1, s] = (
                        float(self.datlines[i].split()[row]) + self.tdos_all[i - 1, s]
                    )
                    row += 1
                    self.intldos_all[i - 1, ll, s] = float(
                        self.datlines[i].split()[row]
                    )
                    self.inttdos_all[i - 1, s] = (
                        float(self.datlines[i].split()[row])
                        + self.inttdos_all[i - 1, s]
                    )
                    row += 1
        self.__emax = max(self.eng)
        self.__emin = min(self.eng)
        self.__ymax = 0.0

    def get_pdos(self, l=0, m=0, lm=None, spin=0):
        """
        pdos = np.zeros((self.nedos, self.lmax, self.mmax, self.nspin))

        :param l:
        :param m:
        :param lm:
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
        self.ymax = max(self.pdos)
        return self.pdos

    def get_ldos(self, l=0, spin=0):
        """LDOS(NEDOS,L,SPIN)"""
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
        """INTLDOS(NEDOS,L,SPIN)"""
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
        return self.eng

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
        return self.sd

    def get_lmax(self):
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
