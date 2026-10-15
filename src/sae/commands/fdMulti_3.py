#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.fdmnes.conv import ReadFdmConv
from sae.fdmnes.sd import ReadFdmSd
from sae.fdmnes.txt import ReadFdmTxt

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
#  sd*.txt plot program
#  multiplot version
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.08.18 startup
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import argparse
import matplotlib.pyplot as plt


#
################################################################################
# import sys
# import gzip
# import os
# import re
# import optparse
# import numpy as np
# import SpaceGroupEnvironment as SGE
################################################################################
#   parser = optparse.OptionParser()
#   options,args = parser.parse_args()
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emax")
    parser.add_argument("--emin")
    options = parser.parse_args()
    return (options.emax, options.emin)


################################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
# multiplot 設定
###########################################################################
###########################################################################
### 共通項目
#EF = txt1.E_edge + txt1.E_fermi
#EF = txt1.E_fermi
#Edge = txt1.E_edge
###########################################################################
### box1 (下から積む)
###########################################################################
### box2
###########################################################################
### box3
###########################################################################
if __name__ == "__main__":
    OPT_EMAX, OPT_EMIN = options()
    if OPT_EMAX:
        OPT_EMAX = float(OPT_EMAX)
        print("Emax     =", OPT_EMAX)
    if OPT_EMIN:
        OPT_EMIN = float(OPT_EMIN)
        print("Emin     =", OPT_EMIN)
    plt.rcParams["font.family"] = "Times New Roman"
    # ラベル等のフォントサイズ
    plt.rcParams["font.size"] = 16
    # レジェンドのフォントサイズ
    plt.rcParams["legend.fontsize"] = 14
    # 軸の太さを設定。目盛りは変わらない
    plt.rcParams["axes.linewidth"] = 1.5
    # for portrait
    fig = plt.figure(figsize=(7.0, 9.89))
    orgx = 0.17
    orgy = 0.08
    off = 0.015
    xsize = 0.72
    ysize0 = 0.75
    ysize = ysize0 / 3.0
    sd1 = ReadFdmSd("Pd55_1", suffix="_sd0.txt", weight=1.0)
    sd2 = ReadFdmSd("Pd55_5", suffix="_sd0.txt", weight=1.0)
    sd3 = ReadFdmSd("FCC/Pd", suffix="_sd0.txt", weight=1.0)
    ldos1 = sd1.get_ldos(l="p")
    ldos2 = sd2.get_ldos(l="p")
    ldos3 = sd3.get_ldos(l="p")
    conv1 = ReadFdmConv("Pd55_1", suffix="_conv.txt", weight=24.0)
    conv2 = ReadFdmConv("Pd55_5", suffix="_conv.txt", weight=1.0)
    conv3 = ReadFdmConv("FCC/Pd", suffix="_conv.txt", weight=1.0)
    txt1 = ReadFdmTxt("Pd55_1", suffix=".txt", weight=24.0)
    txt2 = ReadFdmTxt("Pd55_5", suffix=".txt", weight=1.0)
    txt3 = ReadFdmTxt("FCC/Pd", suffix=".txt", weight=1.0)
    EF = 0.0
    Edge = -txt1.E_fermi
    plt.axes([orgx, orgy, xsize, ysize])
    plt.plot(sd1.eng + Edge, ldos1, color="red", linewidth=1, label="Pd55_1: Pd-p")
    plt.axvline(x=EF, color="black", linewidth=1)
    plt.ylim([0, 5])
    if OPT_EMAX:
        plt.xlim(xmax=float(OPT_EMAX))
    if OPT_EMIN:
        plt.xlim(xmin=float(OPT_EMIN))
    l1 = plt.legend(fontsize=12, loc="upper right")
    orgy = orgy + ysize + off
    plt.axes([orgx, orgy, xsize, ysize])
    plt.plot(sd2.eng + Edge, ldos2, color="blue", linewidth=1, label="Pd55_5: Pd-p")
    plt.axvline(x=EF, color="black", linewidth=1)
    plt.xticks([])
    plt.ylim([0, 5])
    if OPT_EMAX:
        plt.xlim(xmax=float(OPT_EMAX))
    if OPT_EMIN:
        plt.xlim(xmin=float(OPT_EMIN))
    l1 = plt.legend(fontsize=12, loc="upper right")
    plt.ylabel("Absorption [arb. unit]")
    Edge = -txt3.E_fermi
    orgy = orgy + ysize + off
    plt.axes([orgx, orgy, xsize, ysize])
    plt.plot(sd3.eng + Edge, ldos3, color="green", linewidth=1, label="Pd-foil: Pd-p")
    plt.axvline(x=EF, color="black", linewidth=1)
    plt.xticks([])
    plt.ylim([0, 5])
    if OPT_EMAX:
        plt.xlim(xmax=float(OPT_EMAX))
    if OPT_EMIN:
        plt.xlim(xmin=float(OPT_EMIN))
    l1 = plt.legend(fontsize=12, loc="upper right")
    plt.savefig("LDOSmulti.eps")
    plt.savefig("LDOSmulti.pdf")
    plt.savefig("LDOSmulti.png")
    plt.show()
    plt.close("all")
