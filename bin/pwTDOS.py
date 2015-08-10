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

    dosname = 'input.dos'
    outname = None

    parser = optparse.OptionParser()
    parser.add_option(  '-d','--outdos', dest='DOS',)
    parser.add_option(  '-o','--outscf', dest='SCF',)
    options,args = parser.parse_args()

    if options.DOS: dosname=options.DOS
    if options.SCF: outname=options.SCF

    return dosname,outname

################################################################################
if __name__ == '__main__':

    dosname,outname = options()

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


    pw = SAE.ReadPwTdos(dosname)
    pw.dos_up = pw.get_tdos(spin=0)
    if outname is None:
        plt.plot(pw.eng,pw.dos_up,linewidth=1,label='PWSCF TDOS')
    else:
        plt.plot(pw.eng-out.efermi,pw.dos_up,linewidth=1,label='PWSCF TDOS')

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


