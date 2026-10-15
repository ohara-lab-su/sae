#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.athena.nor import ReadAthenaNor
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


def options():
    from sae.common.paths import FileDiscovery

    name = "POSCAR_conv.txt"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    if not os.path.exists(name):
        name0 = FileDiscovery().find_datfile1("_conv.txt")
        if name0 is None:
            name0 = name
    name = name0
    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]
    return name


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
    conv = ReadFdmConv("Au", suffix="_conv.txt")
    txt = ReadFdmTxt("Au", suffix=".txt")
    plt.plot(
        conv.eng + txt.E_edge, conv.xas, color="red", linewidth=1, label="FDM Green R3"
    )
    nor = ReadAthenaNor("Q14B_Au001_Aufoil.txt.nor")
    plt.plot(nor.eng, nor.nor, color="blue", linewidth=1, label="exp.")
    plt.xlabel("Photon Energy [eV]")
    plt.ylabel("Absorption [arb. unit]")
    leg = plt.legend(fontsize=12, loc="lower right")
    leg.get_frame().set_alpha(0.5)
    plt.xlim(xmax=12100)
    plt.xlim(xmin=11900)
    plt.ylim(ymin=0)
    plt.savefig("XAS.pdf")
    plt.show()
    plt.close("all")
