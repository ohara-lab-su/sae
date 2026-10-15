#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
#   plt.close('all')
#   print "NAME",name
from __future__ import print_function
from sae.pwscf.xanes import ReadPwXanes

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# PWplot_XAS.py
#
################################################################################
#
# 2015.07.22 startup
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
import matplotlib.pyplot as plt


#
################################################################################
#import sys
#import gzip
#import os
#import re
#import numpy as np
#import SpaceGroupEnvironment as SGE
################################################################################
def options():
    name = "xanes.dat"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--emin", dest="EMIN")
    parser.add_option("--ymax", dest="YMAX")
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    if options.EMAX:
        options.EMAX = float(options.EMAX)
    if options.EMIN:
        options.EMIN = float(options.EMIN)
    if options.YMAX:
        options.YMAX = float(options.YMAX)
    if len(args) > 0:
        name = args[0]
    return (name, options.EMAX, options.EMIN, options.YMAX)


################################################################################
#   ###########################################################################
#   times = 1.0
#   conv = SAE.ReadFdmConv('Au',suffix='_conv.txt')
#   plt.plot(conv.eng+E_edge,conv.xas*times,color='red',linewidth=1,label='FDM Green R3')
#   ###########################################################################
#   nor = SAE.ReadAthenaNor('Q14B_Au001_Aufoil.txt.nor')
#   plt.plot(nor.eng,nor.nor,color='blue',linewidth=1,label='exp.')
###########################################################################
#   plt.xlabel("Photon Energy [eV]")
#   plt.xlim( xmax=12100 )
#   plt.xlim( xmin=11900 )
#   plt.xlim( xmax=200 )
#   plt.xlim( xmin=-10 )
if __name__ == "__main__":
    name, OPT_EMAX, OPT_EMIN, OPT_YMAX = options()
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
    timesP = 1.0
    pw = ReadPwXanes("xanes.dat")
    plt.plot(pw.eng + E_edge, pw.xas * timesP, linewidth=1, label="PWSCF fch")
    plt.axvline(x=0, color="black", linewidth=1)
    plt.xlabel("Energy above Fermi [eV]")
    plt.ylabel("Absorption [arb. unit]")
    leg = plt.legend(fontsize=12, loc="lower right")
    leg.get_frame().set_alpha(0.5)
    plt.ylim(ymin=0)
    if OPT_EMAX:
        plt.xlim(xmax=float(OPT_EMAX))
    if OPT_EMIN:
        plt.xlim(xmin=float(OPT_EMIN))
    if OPT_YMAX:
        plt.ylim(ymax=float(OPT_YMAX))
    plt.savefig("XAS.eps")
    plt.savefig("XAS.pdf")
    plt.savefig("XAS.png")
    plt.show()
