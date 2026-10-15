#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
#   print "NAME",name
from __future__ import print_function
from sae.athena.nor import ReadAthenaNor
from sae.fdmnes.conv import ReadFdmConv
from sae.fdmnes.sd import ReadFdmSd
from sae.fdmnes.txt import ReadFdmTxt

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
# *_conv.txt plot program
#
# Athena のデーターと一緒に比較する
#
################################################################################
#
# 2015.06.30
#  == None --> is None
#
# 2015.05.21 startup
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import os
import optparse
import matplotlib.pyplot as plt


#
################################################################################
# import sys
# import gzip
# import re
# import numpy as np
# import SpaceGroupEnvironment as SGE
################################################################################
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


################################################################################
#   name = options()
#######################################################
#   conv = SAE.io.ReadFdmConv('Au_conv_Fermi.txt')
#######################################################
###########################################################################
#   plt.xlabel("Energy above Fermi [eV]")
###########################################################################
#   plt.yticks([])
###########################################################################
if __name__ == "__main__":
    plt.rcParams["font.family"] = "Times New Roman"
    # ラベル等のフォントサイズ
    plt.rcParams["font.size"] = 16
    # レジェンドのフォントサイズ
    plt.rcParams["legend.fontsize"] = 14
    # 軸の太さを設定。目盛りは変わらない
    plt.rcParams["axes.linewidth"] = 1.5
    # for portrait
    plt.figure(figsize=(7.0, 9.89))
    orgx = 0.17
    orgy = 0.08
    off = 0.01
    xsize = 0.75
    ysize = 0.83 / 2.0
    e0 = 4.5
    exp_off = 0.015
    plt.axes([orgx, orgy, xsize, ysize])
    conv = ReadFdmConv("Cu", suffix="_conv.txt")
    txt = ReadFdmTxt("Cu", suffix=".txt")
    plt.plot(
        conv.eng + txt.E_edge + e0,
        conv.xas,
        color="black",
        linewidth=3,
        label="XAS with Broad",
    )
    plt.plot(
        conv.eng + txt.E_edge + e0,
        txt.xas,
        color="green",
        linewidth=1,
        label="XAS raw data",
    )
    nor = ReadAthenaNor("Cu_K_Cu_foil_Si311_50ms_140625.txt.nor")
    plt.plot(
        nor.eng,
        nor.nor / 39.0 + exp_off,
        color="blue",
        linewidth=3,
        label="exp. BL14B2",
    )
    plt.axvline(x=txt.E_edge + txt.E_fermi + e0, color="black", linewidth=1)
    plt.yticks([])
    plt.xlim(xmax=9015)
    plt.xlim(xmin=8968)
    plt.ylim(ymin=0)
    plt.xlabel("Photon Energy [eV]")
    plt.ylabel("Absorption [arb. unit]")
    leg = plt.legend(fontsize=12, loc="lower right")
    leg.get_frame().set_alpha(0.5)
    orgy = orgy + ysize + off
    plt.axes([orgx, orgy, xsize, ysize])
    sd = ReadFdmSd("Cu", suffix="_sd0.txt")
    ldos = sd.get_ldos(l="p")
    plt.plot(
        conv.eng + txt.E_edge + e0, ldos, color="red", linewidth=2, label="LDOS Cu-p"
    )
    plt.axvline(x=txt.E_edge + txt.E_fermi + e0, color="black", linewidth=1)
    plt.xticks([])
    plt.xlim(xmax=9015)
    plt.xlim(xmin=8968)
    plt.ylim(ymin=0)
    plt.ylabel("LDOS [/eV]")
    leg = plt.legend(fontsize=12, loc="lower right")
    leg.get_frame().set_alpha(0.5)
    plt.savefig("XAS.pdf")
    plt.show()
    plt.close("all")
