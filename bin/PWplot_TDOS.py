#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# PWplot_TDOS.py
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
    parser.add_option( '-i','--input', dest='INPUT',)
    parser.add_option( '-d','--outdos', dest='DOS',)
    parser.add_option( '-o','--outscf', dest='SCF',)
    parser.add_option( '-s','--scf', dest='SCF',)
    parser.add_option( '--emax', dest='EMAX')
    parser.add_option( '--ymax', dest='YMAX')
    parser.add_option( '--emin', dest='EMIN')
    options,args = parser.parse_args()

    if options.INPUT: dosname = options.INPUT
    if options.DOS: dosname = options.DOS
    if options.SCF: outname = options.SCF
    if options.EMAX: options.EMAX = float(options.EMAX)
    if options.EMIN: options.EMIN = float(options.EMIN)
    if options.YMAX: options.YMAX = float(options.YMAX)

    return dosname,outname,\
            options.EMAX,options.EMIN,options.YMAX

################################################################################
if __name__ == '__main__':

    dosname,outname,\
            OPT_EMAX,OPT_EMIN,OPT_YMAX = options()

    if outname is not None:
        out = SAE.ReadPwOut(outname)

    if OPT_EMAX: print "Emax=",OPT_EMAX
    if OPT_EMIN: print "Emin=",OPT_EMIN
    if OPT_YMAX: print "Ymax=",OPT_YMAX


    ############################################################################
    plt.rcParams['font.family']     = 'Times New Roman'
    plt.rcParams['font.size']       = 16  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize'] = 14  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']  = 1.5 # 軸の太さを設定。目盛りは変わらない

    plt.figure(figsize=(7.00, 9.89))  # for portrait
    ############################################################################

    pw = SAE.ReadPwTdos(dosname)

    for spin in range(pw.ispin):

        orgx = 0.130
        orgy = 0.130
        xsize = 0.80
        ysize = 0.70

        if pw.ispin > 1:
            ysize = ysize/3.  # half-size
            if spin == 0: orgy = orgy + ysize # up-spin
            if spin == 1: orgy = orgy         # down-spin
        else:
            ysize = ysize/2.

        plt.axes([orgx,orgy,xsize,ysize])

        pw.dos = pw.get_tdos(spin=spin)
        if outname is None:
            plt.plot(pw.eng,pw.dos,linewidth=1,label='total')
        else:
            plt.plot(pw.eng-out.efermi,pw.dos,linewidth=1,label='total')
            plt.axvline(x=0,color="black",linewidth=1)   # EF0

        plt.ylim( ymin=0 )

        if spin == 0: plt.ylabel("DOS/eV", fontsize=20)
        if OPT_EMAX: plt.xlim( xmax=float(OPT_EMAX) )
        if OPT_EMIN: plt.xlim( xmin=float(OPT_EMIN) )
        if OPT_YMAX: plt.ylim( ymax=float(OPT_YMAX) )

        if pw.ispin == 2:
            if spin == 0: plt.xticks([])
            if spin == 1:
                xmin,xmax,ymin,ymax = plt.axis()
                plt.ylim( [ymax,0] )

    if outname is None:
        plt.xlabel("Energy [eV]", fontsize=20)
    else:
        plt.xlabel("$E - E_{\mathrm{F}}$ [eV]", fontsize=20)

    leg = plt.legend(fontsize=12,loc='lower right')
#   leg = plt.legend(fontsize=12,loc='upper right')
    leg.get_frame().set_alpha(0.5)

    plt.savefig("TDOS.eps")
    plt.savefig("TDOS.pdf")
    plt.savefig("TDOS.png")

    plt.show()

    plt.close('all')

#   print "NAME",name


