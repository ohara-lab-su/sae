#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
#   print "NAME",name
from __future__ import print_function
from sae.athena.nor import ReadAthenaNor
from sae.fdmnes.conv import ReadFdmConv
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
#import sys
#import gzip
#import re
#import numpy as np
#import SpaceGroupEnvironment as SGE
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
#   E_edge = 0.0
#   times = 35
#   times = 1.0
###########################################################################
###########################################################################
#   plt.plot(nor.eng - nor.e0 ,nor.nor,color='blue',linewidth=1,label='exp.')
#   timesP = 1.0
#   ###########################################################################
#   pw = SAE.ReadPwXanes('xanes.dat')
#   plt.plot(pw.eng+E_edge,pw.xas*timesP,color='green',linewidth=1,label='PWSCF fch')
#   plt.xlabel("Energy above Fermi [eV]")
#   plt.axvline(x=0,color='black',linewidth=1)
#   plt.xlim( xmax=200 )
#   plt.xlim( xmin=-10 )
#   plt.savefig("XAS.eps")
#   plt.savefig("XAS.png")
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
