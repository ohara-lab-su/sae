#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vplot_TDOS.py
#
#   拙作シェルスクリプト版 vplot_TDOS* モドキ(小文字 vplot 系)
#   python(matplot) 版なのでもう少し一般化されているので Vplot (大文字)版へ
#
#   1) gnuplot の代わりに matplotlib を用いる
#   2) Vldos.py などは用いない
#   3) 内部的には直接 ReadDoscar クラス(ReadDoscar.py)を用いる
#      そもそも ReadDoscar クラスは matplotlib からの利用を念頭に構造化している
#
#   4) 引数処理(局所状態密度の原子選択や、対称性による軌道選択)などは
#      別プログラムで、それぞれ対応になるので、ほぼ vplot_LDOS* シリーズと
#      同じファイル構成になる。
#
################################################################################
#
# 2015.01.29
#    Y軸(DOS軸) の下限の設定のバグを修正
#
# 2015.01.15
#    portrait モードを追加して、デフォルトを landscape にした
#    (PDOS と ADOS_portrait はデフォルトは portrait)
#    (TDOS はデフォルト landscape )
#
# 2015.01.14
#    SPIN 対応,option XMAX,XMIN,YMAX 対応
#
# 2015.01.13
#    とりあえず完成
#    ReadDoscar & ReadOutcar
#
# 2015.01.11 (sun) startup
#    LDOS10 以上を仮定
#      全原子のs成分,p成分,d成分をsumしたものを TDOS と一緒にプロット
#      非スピン版
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

import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE

import matplotlib.pyplot as plt
#import matplotlib.cm as cm
#import matplotlib.ticker as tic
#import matplotlib.mlab as mlab

################################################################################
def options():

    dname = 'DOSCAR'
    oname = 'OUTCAR'

    parser = optparse.OptionParser()
    parser.add_option('-d','--doscar', dest='DOSCAR',)
    parser.add_option('-o', '--outcar', dest='OUTCAR',)
    parser.add_option('-n', '--nw', action='store_true', default=False, dest='NOWINDOW',)
    parser.add_option('-p', '--portrait', action='store_true', default=False, dest='PORTRAIT',)
    # 積分状態密度同時プロットオプション
    parser.add_option('--inttdos', action='store_true', default=False)
    # spd-all を off するスイッチ
    parser.add_option('--spd', action='store_true', default=False)
    parser.add_option('--emax', dest='EMAX',)
    parser.add_option('--ymax', dest='YMAX',)
    parser.add_option('--emin', dest='EMIN',)
    options,  args = parser.parse_args()

    if options.DOSCAR: dname=options.DOSCAR
    if options.OUTCAR: oname=options.OUTCAR

#   if options.OPT_EMAX:
#       print options.OPT_EMAX

    return [dname,oname,
            options.NOWINDOW,options.PORTRAIT,
            options.inttdos, options.spd,
            options.EMAX,options.EMIN,options.YMAX]

################################################################################
if __name__ == '__main__':

    # set input file
    dname,oname,NO_WINDOW_FLAG,PORTRAIT_FLAG,\
            FLAG_INTTDOS, FLAG_SPD,\
            OPT_EMAX,OPT_EMIN,OPT_YMAX = options()

    if OPT_EMAX:
        OPT_EMAX=float(OPT_EMAX)
        print "Emax=",OPT_EMAX
    if OPT_EMIN:
        OPT_EMIN=float(OPT_EMIN)
        print "Emin=",OPT_EMIN
    if OPT_YMAX:
        OPT_YMAX=float(OPT_YMAX)
        print "Ymax=",OPT_YMAX

    if FLAG_INTTDOS:
        print "INTTDOS mode"

    # makes instance ( Read DOSCAR )
    dos = SAEnv.ReadVaspDoscar(dname)

#   if os.path.exists(oname) or os.path.exists(oname+'.gz'):
#       FLAG_outcar = True
#       outcar = SAEnv.ReadVaspOutcar(oname)

    # set output device
    out = sys.stdout

    NSPIN = dos.ispin
    LORBIT = dos.lorbit
    NATOM = dos.natom
    TITLE =  dos.title
    EMAX = dos.emax
    EMIN = dos.emin
    NEDOS = dos.nedos
    EFERMI = dos.efermi

    ENG = dos.eng

    ############################################################################
    # matplotlib

#   plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size']         = 16  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize']   = 15  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']    = 1.5 # 軸の太さを設定。目盛りは変わらない

#   plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)
    if PORTRAIT_FLAG:
#       plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)
#       plt.figure(figsize=(8.27, 11.69)) # for portrait
        plt.figure(figsize=(7.00, 9.89))  # for portrait

    ############################################################################

    orgx = 0.130
    orgy = 0.125
    sizex = 0.75
    sizey0 = 0.80

    for spin in range(NSPIN):

        if NSPIN == 1:
            sizey = sizey0
        if NSPIN == 2:
            sizey = sizey0/2.

        if NSPIN == 2 and spin == 0:
            # 二段組の上側(y幅半分) up-spin
            orgy = orgy + sizey
        if NSPIN == 2 and spin == 1:
            # 二段組の下段( down-spin )
            orgy = orgy - sizey

        plt.axes([orgx, orgy, sizex, sizey])

        if NSPIN == 1:
            plt.title(TITLE)

        INTTDOS = dos.get_inttdos(spin)
        TDOS = dos.get_tdos(spin)

        if not FLAG_SPD:
            plt.fill_between(ENG-EFERMI,TDOS, color='#cccccc', linewidth=2)
        else:
            plt.plot(ENG-EFERMI,TDOS, color="black", linewidth=2, label='total')
            plt.fill_between(ENG-EFERMI,TDOS, color='#cccccc', linewidth=2)

        if spin == 0:
            yl = plt.ylabel("DOS/eV", fontsize=20 )

        if FLAG_INTTDOS:
            ax = plt.twinx()
            ax.plot(ENG-EFERMI,INTTDOS, color="black", linewidth=2, label='INTTDOS')
            plt.ylabel("INTTDOS [n]", fontsize=20 )

        if not FLAG_SPD:
            TDOS = dos.get_tdos_spd(0,spin)
            plt.plot(ENG-EFERMI,TDOS, color='red', linewidth=2, label='ALL-s')

            TDOS = dos.get_tdos_spd(1,spin)
            plt.plot(ENG-EFERMI,TDOS, color="green", linewidth=2, label='ALL-p')

            TDOS = dos.get_tdos_spd(2,spin)
            plt.plot(ENG-EFERMI,TDOS, color="blue", linewidth=2, label='ALL-d')

        # Y軸の調整
        plt.ylim( ymin=0 )

        # EF0
        plt.axvline(x=0,color="black",linewidth=1)

       ## for BCC-Fe
       #plt.xlim([-10,10])
       #plt.ylim([0,2.5])

        if OPT_EMAX: plt.xlim( xmax=float(OPT_EMAX) )
        if OPT_EMIN: plt.xlim( xmin=float(OPT_EMIN) )
        if OPT_YMAX: plt.ylim( ymax=float(OPT_YMAX) )

        if NSPIN == 2:
            if spin == 0:
                plt.xticks([])
            if spin == 1:
                # y 軸反転
                xmin,xmax,ymin,ymax = plt.axis()
                plt.ylim([ymax,0.0])

        # EF0
        plt.axvline(x=0,color="black",linewidth=1)

  ##########################################################################

    plt.xlabel("$E -  E_{\mathrm{F}}$ [eV]", fontsize=20 )

    leg = plt.legend(fontsize=12)   # 凡例Box
    leg.get_frame().set_alpha(0.5)  # Alphaチャンネル(半透明化)

    xmin,xmax,ymin,ymax = plt.axis()


#   plt.xlim([-10,10])
#   plt.ylim([0,200])

    if PORTRAIT_FLAG:
        plt.savefig("TDOS.eps",orientation = 'portrait')
        plt.savefig("TDOS.pdf",orientation = 'portrait')
        plt.savefig("TDOS.png",orientation = 'portrait')
    else:
        plt.savefig("TDOS.eps")
        plt.savefig("TDOS.pdf")
        plt.savefig("TDOS.png")

    if not NO_WINDOW_FLAG:
        plt.show()

    plt.close('all')

################################################################################
