#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# LDOS_core.py
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.04.21 : Wplot_LDOS.py ベース
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
__version__    = "0.1.0"
################################################################################

#import sys
import os
#import re
#import gzip
import optparse
import numpy as np

#from copy import deepcopy
import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

import matplotlib.pyplot as plt
#import matplotlib.cm as cm
#import matplotlib.mlab as mlab

################################################################################
def options():

    parser = optparse.OptionParser(os.getcwd())
    parser.add_option( '-n', '--nw', action='store_true', default=False,)
    parser.add_option( '--emax', dest='EMAX',)
    parser.add_option( '--emin', dest='EMIN',)
    options,  args = parser.parse_args()

    return [options.nw,options.EMAX,options.EMIN]

################################################################################
if __name__ == '__main__':

    ############################################
    # set input file

    OPT_EMIN0 = '-5'
    OPT_EMAX0 = '30'

    case1 = '111/DOS/DOS'
    case2 = '222hole_inm/DOS/DOS'

    times = 1.0

    ymax_total = 38
    ymax_d = 2.5
    ymax_p = 0.20
    ymax_s = 0.17


    unit = 'ev'
    title = 'TEST'


    ############################################
    # options()
    NO_WINDOW_FLAG,OPT_EMAX,OPT_EMIN= options()

    if OPT_EMAX:
        print("Emax=",OPT_EMAX)
    else:
        OPT_EMAX = OPT_EMAX0

    if OPT_EMIN:
        print("Emin=",OPT_EMIN)
    else:
        OPT_EMIN = OPT_EMIN0

    ############################################
    # non-spin 専用
    nspin = 1
    ion = 1   # 1 から始める (0番はtotal-DOSの意味になる)
    FLAG_SPIN = False

    ########################################################
    orgx = 0.155
    orgy = 0.088
    xsize = 0.77
    ysize =0.75/4
    off = 0.030

#   plt.title(title)

    ############################################
    lists1 = SAE.find_suffix3(case1+'.dos',unit)
    print("READ FILE(1)  :", end="")
    for i in lists1:
        print(i, end="")
    print("")
    dos1 = SAE.io.ReadWienDos(lists1)
    eng1 = dos1.get_eng()

    ############################################
    lists2 = SAE.find_suffix3(case2+'.dos',unit)
    print("READ FILE(2)  :", end="")
    for i in lists2:
        print(i, end="")
    print("")
    dos2 = SAE.io.ReadWienDos(lists2)
    eng2 = dos2.get_eng()


    ############################################################################
    # matplotlib
   #plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size']         = 20  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize']   = 10  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']    = 1.5 # 軸の太さを設定。目盛りは変わらない
    plt.figure(figsize=(7.00,9.89)) # for portrait


    ############################################################################
    # total
    plt.axes([ orgx,orgy, xsize, ysize ])
    tdos1 = np.array(dos1.get_raw_dos(atom=ion,orbit='total-DOS'))
    tdos2 = np.array(dos2.get_raw_dos(atom=ion,orbit='total-DOS'))
    plt.plot(eng1,tdos1*times, color="black",linestyle=":", linewidth=2, label='nch-total')
    plt.plot(eng2,tdos2, color="red",linestyle="-", linewidth=1, label='fch-total')

    plt.axvline(x=0,color="black",linewidth=1)
    plt.ylim( ymin=0 )
    plt.xlabel("$E -  E_{\mathrm{F}}$ ["+unit+"]", fontsize=20 )

    leg = plt.legend(fontsize=12,loc='lower right')
    leg.get_frame().set_alpha(0.5)
    if OPT_EMAX:
        plt.xlim( xmax=int(OPT_EMAX) )
    if OPT_EMIN:
        plt.xlim( xmin=int(OPT_EMIN) )

   #plt.ylim( ymax=38 )
    plt.ylim( ymax=ymax_total )


    ############################################################################
    ## d
    orgy=orgy+ysize+off
    plt.axes([ orgx,orgy, xsize, ysize ])
    d1 = dos1.get_raw_dos(atom=ion,orbit='d')
    d2 = dos2.get_raw_dos(atom=ion,orbit='d')
    plt.plot(eng1,d1, color="black", linestyle=":", linewidth=2, label='nch-d')
    plt.plot(eng2,d2, color="blue", linestyle="-", linewidth=1, label='fch-d')

    plt.axvline(x=0,color="black",linewidth=1)
    plt.ylim( ymin=0 )
    plt.xticks([])

    leg = plt.legend(fontsize=12)   # 凡例Box
    leg.get_frame().set_alpha(0.5)  # Alphaチャンネル(半透明化)
    if OPT_EMAX:
        plt.xlim( xmax=int(OPT_EMAX) )
    if OPT_EMIN:
        plt.xlim( xmin=int(OPT_EMIN) )

   #plt.ylim( ymax=2.5 )
    plt.ylim( ymax=ymax_d )


    ############################################################################
    ## p
    orgy=orgy+ysize+off
    plt.axes([ orgx,orgy, xsize, ysize ])
    p1 = dos1.get_raw_dos(atom=ion,orbit='p')
    p2 = dos2.get_raw_dos(atom=ion,orbit='p')
    plt.plot(eng1,p1, color="black", linestyle=":", linewidth=2, label='nch-p')
    plt.plot(eng2,p2, color="green", linestyle="-", linewidth=1, label='fch-p')

    plt.axvline(x=0,color="black",linewidth=1)
    plt.ylim( ymin=0 )
    plt.xticks([])
    yl = plt.ylabel("DOS/"+unit, fontsize=20 )

    leg = plt.legend(fontsize=12)   # 凡例Box
    leg.get_frame().set_alpha(0.5)  # Alphaチャンネル(半透明化)
    if OPT_EMAX:
        plt.xlim( xmax=int(OPT_EMAX) )
    if OPT_EMIN:
        plt.xlim( xmin=int(OPT_EMIN) )

   #plt.ylim( ymax=0.20 )
    plt.ylim( ymax=ymax_p )


    ############################################################################
    ## S
    orgy=orgy+ysize+off
    plt.axes([ orgx,orgy, xsize, ysize ])
    s1 = dos1.get_raw_dos(atom=ion,orbit='s')
    s2 = dos2.get_raw_dos(atom=ion,orbit='s')
    plt.plot(eng1,s1, color="black", linestyle=":", linewidth=2, label='nch-s')
    plt.plot(eng2,s2, color="red", linestyle="-", linewidth=1, label='fch-s')

    plt.axvline(x=0,color="black",linewidth=1)
    plt.ylim( ymin=0 )
    plt.xticks([])

    leg = plt.legend(fontsize=12)   # 凡例Box
    leg.get_frame().set_alpha(0.5)  # Alphaチャンネル(半透明化)
    if OPT_EMAX:
        plt.xlim( xmax=int(OPT_EMAX) )
    if OPT_EMIN:
        plt.xlim( xmin=int(OPT_EMIN) )

   #plt.ylim( ymax=0.17 )
    plt.ylim( ymax=ymax_s )


#   plt.xlim([-10,10])
#   plt.ylim([0,200])

    plt.savefig("LDOS_core.eps")
    plt.savefig("LDOS_core.pdf")
    plt.savefig("LDOS_core.png")

    if not NO_WINDOW_FLAG:
        plt.show()

    plt.close('all')

#############################################################################
