#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
#   print "NAME",name
from __future__ import print_function
from sae.fdmnes.inp import ReadFdmInp
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
    name = "read_pdb.inp"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-a", "--atom")
    parser.add_option("-l")
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]
    return (name, options.atom, options.l)


################################################################################
###########################################################################
#   txt = SAE.io.ReadFdmTxt(name0,'.txt')
#   bav = SAE.io.ReadFdmBav(name0)
###########################################################################
#   plt.xlabel("Energy above Fermi [eV]")
#   plt.ylabel("Absorption [arb. unit]")
#   leg = plt.legend(fontsize=12,loc='lower right')
#   leg = plt.legend(loc='lower right')
#   plt.savefig("XAS.eps")
#   plt.savefig("XAS.pdf")
#   plt.savefig("XAS.png")
if __name__ == "__main__":
    inpname, atom, orbit = options()
    if not atom:
        atom = 1
    suffix_sd = "_sd" + str(atom) + ".txt"
    if not orbit:
        orbit = 1
    inp = ReadFdmInp(inpname)
    name0 = inp.get_filout()
    sd = ReadFdmSd(name0, suffix_sd)
    ispin = inp.get_ispin()
    dos = sd.get_ldos(l=orbit)
    eng = sd.get_eng()
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
    plt.plot(eng, dos, linewidth=2, label="DOS")
    plt.axvline(x=0, color="black", linewidth=1)
    leg = plt.legend(loc="upper right")
    leg.get_frame().set_alpha(0.5)
    plt.show()
    plt.close("all")
