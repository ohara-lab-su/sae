#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
#   print "NAME",name
from __future__ import print_function
from sae.fdmnes.conv import ReadFdmConv

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

    name = "POSCAR"
    suffix = "_conv.txt"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    if not os.path.exists(name):
        name0 = FileDiscovery().find_datfile1("_conv.txt")
        name0 = name0.replace(suffix, "")
        if name0 is None:
            name0 = name
    name = name0
    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]
    return (name, suffix)


################################################################################
#   leg = plt.legend(fontsize=12,loc='lower right')
#   plt.xlim( xmax=12100 )
#   plt.xlim( xmin=11900 )
#   plt.xlim( xmax=200 )
#   plt.xlim( xmin=-10 )
#   plt.savefig("XAS.eps")
#   plt.savefig("XAS.png")
if __name__ == "__main__":
    name, suffix = options()
    conv = ReadFdmConv(name, suffix)
    eng = conv.eng
    xas = conv.xas
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
    plt.plot(eng, xas, linewidth=2, label="XAS")
    plt.xlabel("Energy above Fermi [eV]")
    plt.ylabel("Absorption [arb. unit]")
    plt.axvline(x=0, color="black", linewidth=1)
    leg = plt.legend(loc="lower right")
    leg.get_frame().set_alpha(0.5)
    plt.savefig("XAS.pdf")
    plt.show()
    plt.close("all")
