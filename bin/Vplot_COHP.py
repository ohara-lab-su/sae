#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vplot_COHP.py
#
################################################################################
#
# 2015.06.05
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
__version__    = "0.0.5"
################################################################################

import sys
#import os
#import gzip
import optparse
#import numpy as np

#import re
#from copy import deepcopy

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

import matplotlib.pyplot as plt
#import matplotlib.cm as cm
#import matplotlib.ticker as tic
#import matplotlib.mlab as mlab

################################################################################
def options():

    parser = optparse.OptionParser()
    parser.add_option( '-n', '--nw',
                      action='store_true',
                      default=False,
                      dest='NOWINDOW',
    )

    parser.add_option( '-p', '--portrait',
                      action='store_true',
                      default=False,
                      dest='PORTRAIT',
    )
    parser.add_option(  '--emax', dest='EMAX',)
    parser.add_option(  '--emin', dest='EMIN',)
    parser.add_option(  '--cohpmax', '--ymax',dest='YMAX',)
    parser.add_option(  '--cohpmin', '--ymin',dest='YMIN',)
    options,  args = parser.parse_args()

    return [options.NOWINDOW,options.PORTRAIT,\
            options.EMAX,options.EMIN,options.YMAX,options.YMIN]

################################################################################
if __name__ == '__main__':

    # set options file
    NO_WINDOW_FLAG,PORTRAIT_FLAG,\
            OPT_EMAX,OPT_EMIN,OPT_YMAX,OPT_YMIN = options()

    if OPT_EMAX:
                print "Emax=",OPT_EMAX
    if OPT_EMIN:
                print "Emin=",OPT_EMIN
    if OPT_YMAX:
                print "Ymax=",OPT_YMAX
    if OPT_YMIN:
                print "Ymax=",OPT_YMIN

    cohp = SAE.ReadLobCohp()
    dos = SAE.ReadLobDos()

    ############################################################################
    # matplotlib

#   plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size']         = 16  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize']   = 18  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']    = 1.5 # 軸の太さを設定。目盛りは変わらない

#   plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)
    if PORTRAIT_FLAG:
#       plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)
#       plt.figure(figsize=(8.27, 11.69)) # for portrait
        plt.figure(figsize=(7.00, 9.89))  # for portrait

    ############################################################################
    spin = 0

    dos_y = dos.get_tdos(spin)
    dos_x = dos.get_eng()
    cohp_y = cohp.get_ave(spin)
    cohp_x = cohp.get_eng()

    ## DOS
    plt.subplot(121)
    plt.plot(dos_y,dos_x, color="black", linewidth=2, label='TDOS')
#   plt.plot(dos_y,dos_x )
#   plt.fill_between(dos_y,dos_x, 0,facecolor='#cccccc', linewidth=2, label='TDOS')
    plt.axhline(y=0,color="black",linewidth=1)

    plt.xlim( xmin=0 )
    if OPT_EMAX:
        plt.ylim( ymax=int(OPT_EMAX) )
    if OPT_EMIN:
        plt.ylim( ymin=int(OPT_EMIN) )

    plt.xlabel("DOS/eV", fontsize=17 )
    plt.ylabel("$E -  E_{\mathrm{F}}$ [eV]", fontsize=17 )

    ## COHP
    plt.subplot(122)
    plt.plot(-1.*cohp_y,cohp_x, color="black", linewidth=2, label='TDOS')
   #plt.fill_between(-1.*cohp_y,cohp_x, color='#cccccc', linewidth=2, label='TDOS')
    plt.axhline(y=0,color="black",linewidth=1)
    plt.axvline(x=0,color="black",linewidth=1)

    plt.yticks([])

    if OPT_EMAX:
        plt.ylim( ymax=int(OPT_EMAX) )
    if OPT_EMIN:
        plt.ylim( ymin=int(OPT_EMIN) )
    if OPT_YMAX:
        plt.xlim( xmax=int(OPT_YMAX) )
    if OPT_YMIN:
        plt.xlim( xmin=int(OPT_YMIN) )

    plt.xlabel("-pCOHP", fontsize=17 )

    # Y軸の調整
#   plt.ylim( ymin=0 )


#   if spin == 0:

    ##########################################################################

#   plt.xlabel("$E -  E_{\mathrm{F}}$ [eV]", fontsize=20 )

#   leg = plt.legend(fontsize=12)   # 凡例Box
#   leg.get_frame().set_alpha(0.5)  # Alphaチャンネル(半透明化)

    xmin,xmax,ymin,ymax = plt.axis()


#   plt.xlim([-10,10])
#   plt.ylim([0,200])

    if PORTRAIT_FLAG:
        plt.savefig("TDOS.eps",orientation = 'portrait')
        plt.savefig("TDOS.pdf",orientation = 'portrait')
        plt.savefig("TDOS.png",orientation = 'portrait')
    else:
        plt.savefig("COHP.eps")
        plt.savefig("COHP.pdf")
        plt.savefig("COHP.png")

    if not NO_WINDOW_FLAG:
        plt.show()

    plt.close('all')

################################################################################
