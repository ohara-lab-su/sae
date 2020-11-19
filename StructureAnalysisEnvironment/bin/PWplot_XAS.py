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

    name = 'xanes.dat'

    parser = optparse.OptionParser()
    parser.add_option( '-i','--input', dest='INPUT',)
    parser.add_option( '--emax', dest='EMAX')
    parser.add_option( '--emin', dest='EMIN')
    parser.add_option( '--ymax', dest='YMAX')
    options,args = parser.parse_args()

    if options.INPUT: name=options.INPUT
    if options.EMAX: options.EMAX = float(options.EMAX)
    if options.EMIN: options.EMIN = float(options.EMIN)
    if options.YMAX: options.YMAX = float(options.YMAX)
    if len(args) > 0: name=args[0]

    return name,options.EMAX,options.EMIN,options.YMAX

################################################################################
if __name__ == '__main__':

    name,OPT_EMAX,OPT_EMIN,OPT_YMAX = options()

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

    E_edge = 0.0

#   ###########################################################################
#   times = 1.0
#   conv = SAE.ReadFdmConv('Au',suffix='_conv.txt')
#   plt.plot(conv.eng+E_edge,conv.xas*times,color='red',linewidth=1,label='FDM Green R3')

#   ###########################################################################
#   nor = SAE.ReadAthenaNor('Q14B_Au001_Aufoil.txt.nor')
#   plt.plot(nor.eng,nor.nor,color='blue',linewidth=1,label='exp.')

    ###########################################################################
    timesP = 1.0
    pw = SAE.io.ReadPwXanes('xanes.dat')
    plt.plot(pw.eng+E_edge,pw.xas*timesP,linewidth=1,label='PWSCF fch')
    plt.axvline(x=0,color='black',linewidth=1)

    plt.xlabel("Energy above Fermi [eV]")
#   plt.xlabel("Photon Energy [eV]")
    plt.ylabel("Absorption [arb. unit]")

    leg = plt.legend(fontsize=12,loc='lower right')
    leg.get_frame().set_alpha(0.5)

    plt.ylim( ymin=0 )

    if OPT_EMAX: plt.xlim( xmax=float(OPT_EMAX) )
    if OPT_EMIN: plt.xlim( xmin=float(OPT_EMIN) )
    if OPT_YMAX: plt.ylim( ymax=float(OPT_YMAX) )

#   plt.xlim( xmax=12100 )
#   plt.xlim( xmin=11900 )

#   plt.xlim( xmax=200 )
#   plt.xlim( xmin=-10 )

    plt.savefig("XAS.eps")
    plt.savefig("XAS.pdf")
    plt.savefig("XAS.png")

    plt.show()

#   plt.close('all')

#   print "NAME",name


