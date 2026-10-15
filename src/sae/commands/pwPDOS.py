#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
#   plt.close('all')
#   print "NAME",name
from __future__ import print_function
from sae.pwscf.out import ReadPwOut
from sae.pwscf.pdos import ReadPwPdos

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# TDOS plot
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
    prefix = "input"
    outname = None
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-p", "--prefix")
    parser.add_option("-o", "--outscf", dest="SCF")
    options, args = parser.parse_args()
    if options.INPUT:
        prefix = options.INPUT
    if options.prefix:
        prefix = options.prefix
    if options.SCF:
        outname = options.SCF
    return (prefix, outname)


################################################################################
#   leg = plt.legend(fontsize=12,loc='lower right')
#   plt.xlim( xmax=12100 )
#   plt.xlim( xmin=11900 )
#   plt.xlim( xmax=200 )
#   plt.xlim( xmin=-10 )
if __name__ == "__main__":
    prefix, outname = options()
    if outname is not None:
        out = ReadPwOut(outname)
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
    pw = ReadPwPdos(prefix)
    #       pw.pdos = pw.get_ldos(l=1, atom = 0, spin=0)
    #       plt.plot(pw.eng,pw.pdos,linewidth=1,label='p')
    #       pw.pdos = pw.get_ldos(l=1, atom = 0, spin=0)
    #       plt.plot(pw.eng-out.efermi,pw.pdos,linewidth=1,label='p')
    if outname is None:
        pw.pdos = pw.get_ldos(l=0, atom=0, spin=0)
        plt.plot(pw.eng, pw.pdos, linewidth=1, label="s")
        pw.pdos = pw.get_ldos(l=2, atom=0, spin=0)
        plt.plot(pw.eng, pw.pdos, linewidth=1, label="d")
    else:
        pw.pdos = pw.get_ldos(l=0, atom=0, spin=0)
        plt.plot(pw.eng - out.efermi, pw.pdos, linewidth=1, label="s")
        pw.pdos = pw.get_ldos(l=2, atom=0, spin=0)
        plt.plot(pw.eng - out.efermi, pw.pdos, linewidth=1, label="d")
    leg = plt.legend(fontsize=12, loc="upper right")
    leg.get_frame().set_alpha(0.5)
    plt.ylim(ymin=0)
    plt.savefig("TDOS.eps")
    plt.savefig("TDOS.pdf")
    plt.savefig("TDOS.png")
    plt.show()
