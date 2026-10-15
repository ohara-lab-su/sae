#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.vasp.doscar import ReadVaspDoscar

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# vLDOSs.py
#
# Vplot_LDOSm.py (2015.04.22 ベース)
# 超 Simple 化 nonmag版
#
# Mac OS X 上で Vldos.py と名前の重複注意
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.06.15
#    startup
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import optparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


#
################################################################################
#import sys
#import os
#import gzip
#import re
#from copy import deepcopy
#import SpaceGroupEnvironment as SGE
#import matplotlib.mlab as mlab
################################################################################
def options():
    # 0版から始まる
    atom = 1
    parser = optparse.OptionParser()
    parser.add_option("-a", "--atom")
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--emin", dest="EMIN")
    options, args = parser.parse_args()
    if options.atom:
        atom = options.atom
    if len(args) > 0:
        atom = int(args[0])
    return [atom, options.EMAX, options.EMIN]


################################################################################
#####################################################
#
#####################################################
# set input file
#####################################################
# オプションの確認
#   orbit = 0 # s
#   orbit = 1 # p
#####################################################
#
#####################################################
#####################################################
#####################################################
#   leg = plt.legend(fontsize=12,bbox_to_anchor=(orgx,orgy+ysize*4),loc='lower left')
if __name__ == "__main__":
    # non-spin( nspin=1 ), spin( nspin=2 )
    nspin = 1
    # non-spin/up-spin( spin=0 ), dn-spin( spin=1 )
    spin = 0
    atom, OPT_EMAX, OPT_EMIN = options()
    # 原子種の番号を0番からスタートの変換する
    atom -= 1
    title = "ZrO2"
    output = "LDOS"
    # d
    orbit = 2
    plt.rcParams["font.size"] = 18
    plt.rcParams["legend.fontsize"] = 10
    plt.rcParams["axes.linewidth"] = 1.5
    # for portrait
    plt.figure(figsize=(7.0, 9.89))
    orgx = 0.15
    orgy = 0.082
    xsize = 0.75
    ysize = 0.55
    off = 0.02
    plt.axes([orgx, orgy, xsize, ysize])
    dos = ReadVaspDoscar("05_layer/relax/DOSCAR")
    eng = dos.get_eng() - dos.get_efermi()
    tdos = dos.get_tdos()
    ldos = dos.get_ldos(orbit, atom, spin)
    plt.plot(eng, tdos, linewidth=1, label="total 05-layer")
    dos = ReadVaspDoscar("06_layer/relax/DOSCAR")
    eng = dos.get_eng() - dos.get_efermi()
    tdos = dos.get_tdos()
    ldos = dos.get_ldos(orbit, atom, spin)
    plt.plot(eng, tdos, linewidth=1, label="total 06-layer")
    dos = ReadVaspDoscar("07_layer/relax/DOSCAR")
    eng = dos.get_eng() - dos.get_efermi()
    tdos = dos.get_tdos()
    ldos = dos.get_ldos(orbit, atom, spin)
    plt.plot(eng, tdos, linewidth=1, label="total 07-layer")
    plt.axvline(x=0, color="black", linewidth=1)
    xl = plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=20)
    yl = plt.ylabel("DOS/eV", fontsize=20)
    plt.ylim(ymin=0)
    leg = plt.legend(fontsize=8, loc="upper right")
    leg.get_frame().set_alpha(0.5)
    if OPT_EMAX:
        plt.xlim(xmax=float(OPT_EMAX))
    if OPT_EMIN:
        plt.xlim(xmin=float(OPT_EMIN))
    plt.title(title, fontsize=16)
    plt.savefig(output + str(atom + 1) + ".eps")
    plt.savefig(output + str(atom + 1) + ".pdf")
    plt.savefig(output + str(atom + 1) + ".png")
    plt.show()
    plt.close("all")
