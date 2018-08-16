#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# XAS.py  (Wplot_XAS.py ベース)
#
#  小回りがきくようにシンプル化(使用には書き換えが前提)
#
################################################################################
#
# 2015.03.30
#  startup
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

import os
import re
import optparse

import StructureAnalysisEnvironment as SAE
import matplotlib.pyplot as plt

################################################################################
def options():

    name = re.sub('.*/','',os.getcwd())

    parser = optparse.OptionParser(os.getcwd())

    parser.add_option( '-i', '--input', dest='INPUT',)
    parser.add_option( '--emax', dest='EMAX',)
    parser.add_option( '--emin', dest='EMIN',)
    parser.add_option( '--ymax', dest='YMAX',)
    options,  args = parser.parse_args()

    if options.INPUT:
        name = options.INPUT

    return [name,\
            options.EMAX,options.EMIN,options.YMAX]

################################################################################
if __name__ == '__main__':

    ############################################
    # set input file
    case,OPT_EMAX,OPT_EMIN,OPT_YMAX = options()

    if OPT_EMAX:
                print "Emax=",OPT_EMAX
                OPT_EMAX=float(OPT_EMAX)
    if OPT_EMIN:
                print "Emin=",OPT_EMIN
                OPT_EMIN=float(OPT_EMIN)
    if OPT_YMAX:
                print "Ymax=",OPT_YMAX
                OPT_YMAX=float(OPT_YMAX)

    ############################################################################
    # matplotlib

    plt.rcParams['font.family']     = 'Times New Roman'
    plt.rcParams['font.size']       = 16  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize'] = 14  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']  = 1.5 # 軸の太さを設定。目盛りは変わらない

    plt.figure(figsize=(7.00, 9.89))  # for portrait

    ############################################################################

    orgx = 0.150
   #orgx = 0.130
    orgy = 0.080
   #orgy = 0.100
    off = 0.015
    xsize = 0.75
    ysize = 0.83/3.5
    ysize0 = 0.83/4

    ############################################################################
    # XAS ( *.xspec and *.txspec )
   #orgy = orgy + ysize + off + off + off
    plt.axes([ orgx,orgy, xsize, ysize ]) # 原点位置を自動調整

    # broad (XAS)
    xspec1 = SAE.ReadWienXspec(case='111')
    eng = xspec1.get_eng()
    eng_emin = xspec1.get_emin()
    eng_emax = xspec1.get_emax()
    xas1 = xspec1.get_xas()*0.85
    plt.plot(eng,xas1, linestyle=':', color='black', linewidth=2, label='222')

    # broad (XAS hole)
    xspec2 = SAE.ReadWienXspec(case='222fch')
    xas2 = xspec2.get_xas()*0.85
    eng2 = xspec2.get_eng()
    plt.plot(eng2,xas2, linestyle='-', color='red', linewidth=1, label='222 with hole')

    plt.yticks([])
   #plt.xlabel("")
    plt.xlabel("Energy above Fermi [ev]")
    plt.ylabel("Absorption [arb. unit]")
    plt.axvline(x=0,color='black',linewidth=1)

    if OPT_EMAX:
        emax = OPT_EMAX
    else:
        emax = eng_emax

    if OPT_EMIN:
        emin = OPT_EMIN
    else:
        emin = eng_emin

    plt.xlim([emin,emax])
    plt.ylim( ymin=0 )

#   leg = plt.legend(fontsize=12,loc='upper left')
    leg = plt.legend(fontsize=12,loc='lower center')
#   leg.get_frame().set_alpha(0.5)

    ############################################################################
    if OPT_YMAX:
        plt.ylim( ymax=float(OPT_YMAX) )
    else:
        ymax = xspec1.get_ymax_xas()
        print "YMAX = ",ymax
        plt.ylim( ymax=ymax )


    plt.savefig("XAS.eps")
    plt.savefig("XAS.pdf")
    plt.savefig("XAS.png")
    plt.show()

    plt.close('all')

################################################################################
