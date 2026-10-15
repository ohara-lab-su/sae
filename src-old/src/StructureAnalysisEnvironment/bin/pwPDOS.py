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
from __future__ import print_function
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"
################################################################################

#import sys
#import gzip
#import os
#import re
import optparse
#import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

import matplotlib.pyplot as plt


################################################################################
def options():

    prefix = 'input'
    outname = None

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT',)
    parser.add_option(  '-p','--prefix',)
    parser.add_option(  '-o','--outscf', dest='SCF',)
    options,args = parser.parse_args()

    if options.INPUT: prefix=options.INPUT
    if options.prefix: prefix=options.prefix
    if options.SCF: outname=options.SCF

    return prefix,outname

################################################################################
if __name__ == '__main__':

    prefix,outname = options()

    if outname is not None:
        out = SAE.ReadPwOut(outname)

    plt.rcParams['font.family']     = 'Times New Roman'
    plt.rcParams['font.size']       = 16  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize'] = 14  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']  = 1.5 # 軸の太さを設定。目盛りは変わらない

    plt.figure(figsize=(7.00, 9.89))  # for portrait

    orgx = 0.170
    orgy = 0.080
    off = 0.010
    xsize = 0.75
    ysize = 0.83/2.

    plt.axes([orgx,orgy,xsize,ysize])


    pw = SAE.io.ReadPwPdos(prefix)
    if outname is None:
        pw.pdos = pw.get_ldos(l=0, atom = 0, spin=0)
        plt.plot(pw.eng,pw.pdos,linewidth=1,label='s')
#       pw.pdos = pw.get_ldos(l=1, atom = 0, spin=0)
#       plt.plot(pw.eng,pw.pdos,linewidth=1,label='p')
        pw.pdos = pw.get_ldos(l=2, atom = 0, spin=0)
        plt.plot(pw.eng,pw.pdos,linewidth=1,label='d')
    else:
        pw.pdos = pw.get_ldos(l=0, atom = 0, spin=0)
        plt.plot(pw.eng-out.efermi,pw.pdos,linewidth=1,label='s')
#       pw.pdos = pw.get_ldos(l=1, atom = 0, spin=0)
#       plt.plot(pw.eng-out.efermi,pw.pdos,linewidth=1,label='p')
        pw.pdos = pw.get_ldos(l=2, atom = 0, spin=0)
        plt.plot(pw.eng-out.efermi,pw.pdos,linewidth=1,label='d')

#   leg = plt.legend(fontsize=12,loc='lower right')
    leg = plt.legend(fontsize=12,loc='upper right')
    leg.get_frame().set_alpha(0.5)

#   plt.xlim( xmax=12100 )
#   plt.xlim( xmin=11900 )

#   plt.xlim( xmax=200 )
#   plt.xlim( xmin=-10 )

    plt.ylim( ymin=0 )

    plt.savefig("TDOS.eps")
    plt.savefig("TDOS.pdf")
    plt.savefig("TDOS.png")

    plt.show()

#   plt.close('all')

#   print "NAME",name


