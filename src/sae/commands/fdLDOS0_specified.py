#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
#   print "NAME",name
from __future__ import print_function
from sae.fdmnes.sd import ReadFdmSd

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
# *_conv.txt plot program
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
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
import argparse
import matplotlib.pyplot as plt


#
################################################################################
#import sys
#import gzip
#import os
#import re
#import optparse
#import numpy as np
#import SpaceGroupEnvironment as SGE
################################################################################
#   parser = optparse.OptionParser()
#   options,args = parser.parse_args()
#   if len(args) > 0: name=args[0]
def options():
    name = "read_pdb.inp"
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="INPUT")
    parser.add_argument("--emax")
    parser.add_argument("--emin")
    parser.add_argument("--dmax")
    options = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    return (name, options.emax, options.emin, options.dmax)


################################################################################
###########################################################################
#   inp = SAE.io.ReadFdmInp(inpname)
#   filout = inp.get_filout()
#   ispin = inp.get_ispin()
#   txt = SAE.io.ReadFdmTxt(name0,'.txt')
#   bav = SAE.io.ReadFdmBav(name0)
###########################################################################
#   E_edge   = 24350.0
#   E_fermi  = -5.82491
###########################################################################
###########################################################################
#   sd = SAE.ReadFdmSd('Pd19/R5_fdm/allsite/Pd19',absorber=(1,2,3),weight=3.0)
#   dos = sd.get_ldos(l='p')
#   plt.plot(sd.eng,dos,linewidth=1,label='Pd19:absorber LDOS (p)')
###########################################################################
#   plt.xlabel("Energy above Fermi [eV]")
#   plt.ylabel("Absorption [arb. unit]")
#   plt.axvline(x=0,color='black',linewidth=1)
#   leg = plt.legend(fontsize=12,loc='lower right')
#   leg = plt.legend(loc='lower right')
if __name__ == "__main__":
    inpname, OPT_EMAX, OPT_EMIN, OPT_DMAX = options()
    if OPT_EMAX:
        OPT_EMAX = float(OPT_EMAX)
        print("Emax     =", OPT_EMAX)
    if OPT_EMIN:
        OPT_EMIN = float(OPT_EMIN)
        print("Emin     =", OPT_EMIN)
    if OPT_DMAX:
        OPT_DMAX = float(OPT_DMAX)
        print("Ymax(DOS)=", OPT_DMAX)
    suffix = "_sd0.txt"
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
    plt.axes([orgx, orgy, xsize, ysize])
    E_edge = 0.0
    E_fermi = 0.0
    EF0 = E_edge + E_fermi
    sd = ReadFdmSd(
        "Pd6/Pd6", inpname="Pd6/read_pdb.inp", absorber=(1, 2, 3, 4, 5), weight=6.0
    )
    dos = sd.get_ldos(l="p")
    plt.plot(sd.eng + E_edge, dos, linewidth=2, label="absorber LDOS (p)")
    plt.ylabel("LDOS [stat/eV]")
    plt.axvline(x=EF0, color="black", linewidth=1)
    plt.ticklabel_format(axis="x", useOffset=False)
    leg = plt.legend(loc="upper right")
    leg.get_frame().set_alpha(0.5)
    if OPT_EMAX:
        plt.xlim(xmax=float(OPT_EMAX))
    if OPT_EMIN:
        plt.xlim(xmin=float(OPT_EMIN))
    if OPT_DMAX:
        plt.ylim(ymax=float(OPT_DMAX))
    plt.savefig("LDOS.eps")
    plt.savefig("LDOS.pdf")
    plt.savefig("LDOS.png")
    plt.show()
    plt.close("all")
