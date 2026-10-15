#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.openmx.tdos import ReadMxTdos

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# mxDOS.py
#
#  TOTAL DOS シンプル版
#
################################################################################
#
# 2015.06.11 startup
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import optparse
import matplotlib.pyplot as plt


#
################################################################################
# import gzip
# import numpy as np
# import re
# from copy import deepcopy
# import SpaceGroupEnvironment as SGE
# import matplotlib.cm as cm
# import matplotlib.ticker as tic
# import matplotlib.mlab as mlab
################################################################################
def options():
    parser = optparse.OptionParser()
    parser.add_option("-n", "--nw", action="store_true", default=False, dest="NOWINDOW")
    parser.add_option(
        "-p", "--portrait", action="store_true", default=False, dest="PORTRAIT"
    )
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--emin", dest="EMIN")
    parser.add_option("--ymax", dest="YMAX")
    options, args = parser.parse_args()
    return [
        options.NOWINDOW,
        options.PORTRAIT,
        options.EMAX,
        options.EMIN,
        options.YMAX,
    ]


################################################################################
# set input file
############################################################################
# matplotlib
#   plt.rcParams['font.family'] = 'Times New Roman'
############################################################################
# 222
# 444
# for BCC-Fe
##########################################################################
if __name__ == "__main__":
    NO_WINDOW_FLAG, PORTRAIT_FLAG, OPT_EMAX, OPT_EMIN, OPT_YMAX = options()
    if OPT_EMAX:
        print("Emax=", OPT_EMAX)
    if OPT_EMIN:
        print("Emin=", OPT_EMIN)
    if OPT_YMAX:
        print("Ymax=", OPT_YMAX)
    out = sys.stdout
    # ラベル等のフォントサイズ
    plt.rcParams["font.size"] = 20
    # レジェンドのフォントサイズ
    plt.rcParams["legend.fontsize"] = 18
    # 軸の太さを設定。目盛りは変わらない
    plt.rcParams["axes.linewidth"] = 1.5
    if PORTRAIT_FLAG:
        # for portrait
        plt.figure(figsize=(7.0, 9.89))
    # 一段組の原点(x,y), 幅(x,y) nonmag
    plt.axes([0.13, 0.13, 0.8, 0.8])
    dos = ReadMxTdos("222/POSCAR", ".DOS.Tetrahedron")
    tdos = dos.get_tdos(spin=0)
    eng = dos.get_eng()
    plt.plot(eng, tdos, linewidth=2, label="222 cluster")
    plt.ylim(ymin=0)
    dos = ReadMxTdos("444/POSCAR", ".DOS.Tetrahedron")
    tdos = dos.get_tdos(spin=0)
    eng = dos.get_eng()
    plt.plot(eng, tdos * (1.0 / 8.0), linewidth=2, label="444 cluster")
    plt.ylim(ymin=0)
    # EF0
    plt.axvline(x=0, color="black", linewidth=1)
    yl = plt.ylabel("DOS/eV", fontsize=20)
    xl = plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=20)
    plt.xlim([-10, 10])
    if OPT_EMAX:
        plt.xlim(xmax=int(OPT_EMAX))
    if OPT_EMIN:
        plt.xlim(xmin=int(OPT_EMIN))
    if OPT_YMAX:
        plt.ylim(ymax=int(OPT_YMAX))
    # 凡例Box
    leg = plt.legend(fontsize=12)
    # Alphaチャンネル(半透明化)
    leg.get_frame().set_alpha(0.5)
    if PORTRAIT_FLAG:
        plt.savefig("TDOS.eps", orientation="portrait")
        plt.savefig("TDOS.pdf", orientation="portrait")
        plt.savefig("TDOS.png", orientation="portrait")
    else:
        plt.savefig("TDOS.eps")
        plt.savefig("TDOS.pdf")
        plt.savefig("TDOS.png")
    if not NO_WINDOW_FLAG:
        plt.show()
    plt.close("all")
