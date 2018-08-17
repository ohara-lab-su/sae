#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# fch_XAS.py
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.04.21 : wplot_XAS.py ベース、特化版( non-spin ), K-edge
#              matplotlib の(numpyの) loadtxt() を用いて極限まで簡素化したバージョン
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
import sys
import os
#import gzip
import re
import optparse
import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

import pylab
import matplotlib.pyplot as plt
#import matplotlib.cm as cm
#import matplotlib.mlab as mlab

################################################################################
def options():

    parser = optparse.OptionParser(os.getcwd())
    parser.add_option( '--emax', dest='EMAX',)
    parser.add_option( '--emin', dest='EMIN',)
    parser.add_option( '--ymax', dest='YMAX',)
    options,  args = parser.parse_args()
    return [options.EMAX,options.EMIN,options.YMAX]

################################################################################
if __name__ == '__main__':

    # set input file
    case1 = '111/111'
    case2 = '222fch/222fch'

    OPT_EMAX,OPT_EMIN,OPT_YMAX = options()

    FLAG_SHOW=True
    dos_suffix = '.dos1ev'
    txspec_suffix = '.txspec'
    xspec_suffix = '.xspec'
    outname='fch_XAS'

    if OPT_EMAX:
                print("Emax=",OPT_EMAX)
    if OPT_EMIN:
                print("Emin=",OPT_EMIN)
    if OPT_YMAX:
                print("Ymax=",OPT_YMAX)

    ############################################
    # dos instance
    unit = 'ev'
    name1 = [ case1+dos_suffix ]
    name2 = [ case2+dos_suffix ]

    print('DOS(1) = ',name1[0])

    dos1 = SAE.ReadWienDos(name1)
    efermi1 = dos1.get_efermi()
    eng1 = dos1.get_eng()
    eng1_emin = dos1.get_emin()
    eng1_emax = dos1.get_emax()

    dos1_total = np.array(dos1.get_raw_dos(atom=0,orbit='total-DOS'))
    dos1_p = np.array(dos1.get_raw_dos(atom=1,orbit='p'))

    print('DOS(2) = ',name2[0])
    dos2 = SAE.ReadWienDos(name2)
    efermi2 = dos2.get_efermi()
    eng2 = dos2.get_eng()
    eng2_emin = dos2.get_emin()
    eng2_emax = dos2.get_emax()

    dos2_total = np.array(dos2.get_raw_dos(atom=0,orbit='total-DOS'))
    dos2_p = np.array(dos2.get_raw_dos(atom=1,orbit='p'))

    ############################################
    # txspec instance ( unbroad XAS )
    txspec = SAE.ReadWienTxspec(case=case2,suffix=txspec_suffix)
#   eng_unbroad = txspec.get_eng()
#   eng_unbroad_emin = txspec.get_emin()
#   eng_unbroad_emax = txspec.get_emax()
    unbroad = txspec.get_unbroad_xas()

    ############################################
    # xspec instance ( XAS )
    xspec = SAE.ReadWienXspec(case=case2,suffix=xspec_suffix)
    eng_xas = xspec.get_eng()
#   eng_xas_min = xspec.get_emin()
#   eng_xas_max = xspec.get_emax()
    xas = xspec.get_xas()


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
    off = 0.010
    xsize = 0.75

    ysize0 = 0.83

    ysize = ysize0/3.5
    ysize_dos = ysize0/4

    ####################################################################
    # 軸調整
    if OPT_EMAX:
        emax = float(OPT_EMAX)
    else:
        emax = eng2_emax

    if OPT_EMIN:
        emin = float(OPT_EMIN)
    else:
        emin = eng2_emin

    ####################################################################
    # DOS (*.dos1) TOTAL
    #
    plt.axes([ orgx,orgy, xsize, ysize_dos ]) # 原点位置を自動調整
    eng1 = eng1 - efermi1
    eng2 = eng2 - efermi2
    plt.plot(eng1,dos1_total*8.0, color='black', linestyle=':',linewidth=1, label='nch total-DOS')
    plt.plot(eng2,dos2_total, color='red', linestyle='-',linewidth=1, label='fch total-DOS')

    plt.ylabel("DOS [unit/"+unit+"]")
    plt.xlabel("Energy above Fermi ["+unit+"]")
    plt.axvline(x=0,color='black',linewidth=1)

    plt.xlim([emin,emax])
    plt.ylim( ymin=0 )

    leg = plt.legend(fontsize=12)
    leg.get_frame().set_alpha(0.5)

    ####################################################################
    # DOS (*.dos1) p-orbital
    #
    orgy = orgy + ysize_dos + off
    plt.axes([ orgx,orgy, xsize, ysize_dos ]) # 原点位置を自動調整
    eng1 = eng1 - efermi1
    eng2 = eng2 - efermi2
    plt.plot(eng1,dos1_p, color='black', linestyle=':',linewidth=1, label='nch-p')
    plt.plot(eng2,dos2_p, color='red', linestyle='-',linewidth=1, label='fch-p')

    plt.xticks([])
    plt.xlabel("")
    plt.ylabel("")
    plt.axvline(x=0,color='black',linewidth=1)

    plt.xlim([emin,emax])
    plt.ylim( ymin=0 )

    leg = plt.legend(fontsize=12)
    leg.get_frame().set_alpha(0.5)

    ############################################################################
    # XAS ( *.xspec and *.txspec )
    orgy = orgy + ysize + off + off + off + off
    plt.axes([ orgx,orgy, xsize, ysize ]) # 原点位置を自動調整

    # broad (XAS)
    plt.plot(eng_xas,xas, color='black', linewidth=2, label='XAS')
   #plt.fill_between(eng_xas,xas, color='#cccccc', linewidth=2, label='XAS')

    # unbroad (XAS)
    plt.plot(eng_xas,unbroad, linestyle='-', color='green', linewidth=0.8, label='unbroad')
    plt.yticks([])
   #plt.xlabel("")
    plt.xlabel("Energy above Fermi ["+unit+"]")
    plt.ylabel("Absorption [arb. unit]")
    plt.axvline(x=0,color='black',linewidth=1)

    plt.xlim([emin,emax])
    plt.ylim( ymin=0 )

    leg = plt.legend(fontsize=12)
    leg.get_frame().set_alpha(0.5)

    ############################################################################
    if OPT_YMAX:
        plt.ylim( ymax=float(OPT_YMAX) )
    else:
        ymax = xspec.get_ymax_xas()
        ymax0 = ymax/10.0
        ymax = ymax + ymax0*1.5
        plt.ylim( ymax=ymax )

    plt.savefig(outname+".eps")
    plt.savefig(outname+".pdf")
    plt.savefig(outname+".png")

    if FLAG_SHOW:
        plt.show()

    plt.close('all')


