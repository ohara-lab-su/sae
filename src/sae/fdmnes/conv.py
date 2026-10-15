# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import optparse
import numpy as np


class ReadFdmConv(object):

    def __init__(self, cname, suffix="_conv.txt", weight=None):
        from sae.common.text import TextFiles

        if not os.path.exists(cname + suffix):
            cname = cname.replace(suffix, "")
        self.datlines, self.num = TextFiles().read_dataline(cname + suffix)
        self.name = cname
        self.suffix = suffix
        self.eng = np.zeros(self.num - 1)
        self.xas = np.zeros(self.num - 1)
        if weight is None:
            weight = 1.0
        for i in range(1, self.num):
            self.eng[i - 1] = float(self.datlines[i].split()[0])
            self.xas[i - 1] = float(self.datlines[i].split()[1]) / float(weight)

    def get_eng(self):
        return self.eng

    def get_xas(self):
        return self.xas

    def average_conv(self, name, absorber, weight=None):
        from sae.common.text import TextFiles

        if weight is None:
            n_site = float(len(absorber))
        else:
            print("weight : %s" % str(weight))
            n_site = float(weight)
        s_xas = np.zeros(self.num - 1)
        for site in absorber:
            convname = name + "_" + str(site) + self.suffix
            datlines, num = TextFiles().read_dataline(convname)
            print("sum : %s" % str(convname))
            for i in range(1, self.num):
                s_xas[i - 1] = float(datlines[i].split()[1]) + s_xas[i - 1]
        self.xas = s_xas / n_site
        return self.xas


class ConvOperations:

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
