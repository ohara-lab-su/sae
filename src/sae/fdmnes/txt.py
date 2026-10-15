# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import optparse
import numpy as np


class ReadFdmTxt(object):

    def __init__(self, cname, suffix=".txt", edge="K", weight=None):
        """
        注意) convolution した 横軸（エネルギー）は生データ(txt)と異なるので、
             生データXAS をプロットするときは、 生データ(eng) を横軸にすること
        :param cname:
        :param suffix:
        :param edge:
        :param weight:
        """
        from sae.common.text import TextFiles

        name = cname.replace(suffix, "")
        suffix0 = cname.replace(name, "")
        if suffix0 != suffix:
            suffix = ".txt"
            cname = name + suffix
        self.suffix = suffix
        self.__datlines, self.num = TextFiles().read_dataline(cname)
        self.__header = self.__datlines[0]
        self.__eng = np.zeros(self.num - 2)
        if weight is None:
            weight = 1.0
        else:
            print("ReadFdmTxt(weight=%s)" % str(weight))
        count = 0
        for i in self.__datlines[0].split():
            count += 1
            if i == "=":
                break
        self.__param = {}
        for i in range(count, len(self.__datlines[0].replace(",", " ").split())):
            key = str(self.__datlines[0].replace(",", " ").split()[i].strip())
            value = float(self.__datlines[0].replace(",", " ").split()[i - count])
            self.__param[key] = value
        try:
            self.__param["E_Fermi"]
        except:
            self.__param["E_Fermi"] = 0.0
        if isinstance(edge, str):
            if edge == "K":
                edge = 0
            if edge == "L2":
                edge = 0
            if edge == "L3":
                edge = 1
        if len(self.__datlines[1].split()) == 3:
            if bool(re.match(".*\\<xanes\\>_L", self.__datlines[1].split()[1])):
                self.__nspin = 1
            else:
                self.__nspin = 2
        elif len(self.__datlines[1].split()) >= 4:
            self.__nspin = 2
        else:
            self.__nspin = 1
        self.__xas_all = np.zeros((self.num - 2, self.__nspin))
        for i in range(2, self.num):
            self.__eng[i - 2] = float(self.__datlines[i].split()[0])
            for spin in range(self.__nspin):
                self.__xas_all[i - 2, spin] = (
                    float(self.__datlines[i].split()[1 + spin + edge]) / weight
                )
        self.__E_Fermi = self.__param["E_Fermi"]
        self.__E_edge = self.__param["E_edge"]
        self.__Z = self.__param["Z"]
        self.__ispin = self.__nspin
        self.__xas = self.__xas_all[:, 0]

    def get_eedge(self):
        return self.__E_edge

    @property
    def eedge(self):
        return self.__E_edge

    @property
    def e_edge(self):
        return self.__E_edge

    @property
    def E_edge(self):
        return self.__E_edge

    def get_efermi(self):
        return self.__E_Fermi

    @property
    def efermi(self):
        return self.__E_Fermi

    def get_e_fermi(self):
        return self.__E_Fermi

    @property
    def e_fermi(self):
        return self.__E_Fermi

    @property
    def E_Fermi(self):
        return self.__E_Fermi

    @property
    def E_fermi(self):
        return self.__E_Fermi

    def get_z(self):
        return self.__Z

    def get_eng(self):
        return self.__eng

    @property
    def eng(self):
        return self.__eng

    def get_xas_all(self):
        return self.__xas_all

    @property
    def xas_all(self):
        return self.__xas_all

    def get_xas(self, spin=0):
        return self.__xas_all[:, spin]

    @property
    def xas(self):
        return self.__xas

    def get_header(self):
        return self.__header

    @property
    def header(self):
        return self.__header

    def get_nspin(self):
        return self.__nspin

    @property
    def nspin(self):
        return self.__nspin

    def get_ispin(self):
        return self.__ispin

    @property
    def ispin(self):
        return self.__ispin

    def average(self, name, absorber, spin=0, weight=None):
        """
        allsite のときの複数の *.txt の平均を取る
        filout = Pd のとき allsite ならばとして結果を出力したとする
        Pd_1.txt
        Pd_2.txt
        Pd_3.txt
        このとき、average_txt(1,2,3) とすると Pd_1,Pd_2,Pd_3 の self.xas の
        平均を self.xas に返す

        non-spin

        :param name:
        :param absorber:
        :param spin:
        :param weight:
        :return:
        """
        from sae.common.text import TextFiles

        if weight is None:
            n_site = float(len(absorber))
        else:
            print("weight : %s" % str(weight))
            n_site = float(weight)
        s_xas = np.zeros((self.num - 2, self.__nspin))
        for site in absorber:
            txtname = name + "_" + str(site) + self.suffix
            datlines, num = TextFiles().read_dataline(txtname)
            print("sum : %s" % str(txtname))
            for i in range(2, self.num):
                s_xas[i - 2, spin] = (
                    float(datlines[i].split()[1 + spin - 1]) + s_xas[i - 2, spin]
                )
        self.__xas = s_xas / n_site
        return self.__xas


class TxtOperations:

    def plot_fdm_xas(self, eng, xas):
        import matplotlib.pyplot as plt

        plt.rcParams["font.family"] = "Times New Roman"
        plt.rcParams["font.size"] = 16
        plt.rcParams["legend.fontsize"] = 14
        plt.rcParams["axes.linewidth"] = 1.5
        plt.figure(figsize=(7.0, 9.89))
        orgx = 0.17
        orgy = 0.08
        off = 0.01
        xsize = 0.75
        ysize = 0.83 / 2.0
        plt.axes([orgx, orgy, xsize, ysize])
        plt.plot(eng, xas, linewidth=2, label="XAS")
        plt.xlabel("Energy above Fermi [eV]")
        plt.ylabel("Absorption [arb. unit]")
        plt.axvline(x=0, color="black", linewidth=1)
        leg = plt.legend(fontsize=12, loc="lower right")
        leg.get_frame().set_alpha(0.5)
        plt.savefig("XAS.eps")
        plt.savefig("XAS.pdf")
        plt.savefig("XAS.png")
        plt.show()
        plt.close("all")
