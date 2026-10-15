#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.fdmnes.conv import ReadFdmConv
from sae.fdmnes.txt import ReadFdmTxt

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import os
import optparse
import matplotlib.pyplot as plt

if __name__ == "__main__":
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
    txt = ReadFdmTxt("R3.0/Au", suffix=".txt")
    conv = ReadFdmConv("R3.0/Au", suffix="_conv.txt")
    plt.plot(conv.eng - txt.E_Fermi, conv.xas, linewidth=2, label="XAS")
    plt.ticklabel_format(axis="x", useOffset=False)
    plt.xlabel("Energy above Fermi [eV]")
    plt.ylabel("Absorption [arb. unit]")
    leg = plt.legend(fontsize=12, loc="lower right")
    leg.get_frame().set_alpha(0.5)
    plt.savefig("XAS.pdf")
    plt.show()
    plt.close("all")
