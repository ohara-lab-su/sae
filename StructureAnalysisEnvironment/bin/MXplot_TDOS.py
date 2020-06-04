#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# MXplot_TDOS.py
#
#   拙作シェルスクリプト版 vplot_TDOS* モドキ(小文字 vplot 系)
#   をベースにした Vplot_TDOS.py をベースにして OpenMX に対応した
#
#   DosMain にて Tetrahedron , DOS モードにる出力を仮定
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.03.02
#  Gaussian スメアリングの時のモードを追加
#
# 2015.02.26
#  デフォルトファイル名 or 入力ファイル名が存在しない時には
#  カレントの *.out ファイルを検出して、もしカレントの *.out がひとつのときに
#  デフォルト名を変更する仕組みを導入
#
#  注意) *.out ファイルもしくは *.dat ファイルをキーにしているので
#        これらは必須となる
#        もととも、DOS系のクラスは実質的には *.out or *.dat  は必須
#
# 2015.02.25
#   MXplot_TDOS.py startup
#   Vplot_TDOS.py ベースで MXplot_TDOS.py を作成
#
# ----------------------------- Vplot_TDOS.py (2015.02.25)
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

import sys
import os
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

    name = 'openmx'  # input date name
    suffix = '.DOS.Tetrahedron'
    suffix_g = '.DOS.Gaussian'

    parser = optparse.OptionParser()
    parser.add_option( '-i', '--input', dest='INPUT', default=name,)
    parser.add_option( '-n', '--nw', action='store_true', default=False,)

    parser.add_option( '-p', '--portrait', action='store_true', default=False,)
    parser.add_option( '-g', '--gaussian', action='store_true', default=False,)
    parser.add_option(  '--emax', dest='EMAX',)
    parser.add_option(  '--ymax', dest='YMAX',)
    parser.add_option(  '--emin', dest='EMIN',)
    options,  args = parser.parse_args()

    if options.gaussian:
        print("GAUSSIAN MODE")
        suffix =suffix_g

    if options.INPUT:
        name=options.INPUT

    if len(args) > 0:
        name=args[0]

    # 'openmx' より最適なデフォルトファイル名の推定ルーチン
    if not os.path.exists(name+'.out') or not os.path.exists(name+'.out.gz'):
        try:
            name = SAE.find_datfile('out')
        except:
            pass
    elif not os.path.exists(name+'.dat') or not os.path.exists(name+'.dat'):
        try:
            name = SAE.find_datfile('dat')
        except:
            pass

    return [name,suffix,\
            options.nw,options.portrait,\
            options.EMAX,options.EMIN,options.YMAX]

################################################################################
if __name__ == '__main__':

    # set input file
    name,suffix,NO_WINDOW_FLAG,PORTRAIT_FLAG,\
            OPT_EMAX,OPT_EMIN,OPT_YMAX = options()

    if OPT_EMAX: print("Emax=",OPT_EMAX)
    if OPT_EMIN: print("Emin=",OPT_EMIN)
    if OPT_YMAX: print("Ymax=",OPT_YMAX)

    # makes instance ( Read DOS.Tetrahedron )
    dos = SAE.ReadMxTdos(name,suffix)

    # set output device
    out = sys.stdout

    NSPIN = dos.get_ispin()
    NATOM = dos.get_natom()
    TITLE =  dos.get_title()
    EMAX = dos.get_emax()
    EMIN = dos.get_emin()
    NEDOS = dos.get_nedos()
    EFERMI = 0.0

    ENG = dos.get_eng()

    ############################################################################
    # matplotlib

#   plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size']         = 20  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize']   = 18  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']    = 1.5 # 軸の太さを設定。目盛りは変わらない

#   plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)
    if PORTRAIT_FLAG:
#       plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)
#       plt.figure(figsize=(8.27, 11.69)) # for portrait
        plt.figure(figsize=(7.00, 9.89))  # for portrait

    ############################################################################
    for spin in range(NSPIN):

        if NSPIN == 1:
            plt.axes([ 0.130,0.130, 0.80,0.80 ]) # 一段組の原点(x,y), 幅(x,y) nonmag
            plt.title(TITLE)
        if NSPIN == 2:
            if spin == 0:
                plt.axes([ 0.130,0.530, 0.80, 0.4])  # 二段組の上側(y幅半分) up-spin
            if spin == 1:
                plt.axes([ 0.130,0.130, 0.80, 0.4])  # 二段組の下段( down-spin )

        INTTDOS = dos.get_inttdos(spin)
        TDOS = dos.get_tdos(spin)
    #   plt.plot(ENG-EFERMI,TDOS, color="black", linewidth=2, label='total')
        plt.fill_between(ENG-EFERMI,TDOS, color='#cccccc', linewidth=2, label='total')

#       TDOS = dos.get_tdos_spd(0,spin)
#       plt.plot(ENG-EFERMI,TDOS, color='red', linewidth=2, label='ALL-s')
#
#       TDOS = dos.get_tdos_spd(1,spin)
#       plt.plot(ENG-EFERMI,TDOS, color="green", linewidth=2, label='ALL-p')
#
#       TDOS = dos.get_tdos_spd(2,spin)
#       plt.plot(ENG-EFERMI,TDOS, color="blue", linewidth=2, label='ALL-d')

        # Y軸の調整
        plt.ylim( ymin=0 )

        # EF0
        plt.axvline(x=0,color="black",linewidth=1)

       ## for BCC-Fe
       #plt.xlim([-10,10])
       #plt.ylim([0,2.5])

        if spin == 0:
            yl = plt.ylabel("DOS/eV", fontsize=20 )

        if OPT_EMAX: plt.xlim( xmax=int(OPT_EMAX) )
        if OPT_EMIN: plt.xlim( xmin=int(OPT_EMIN) )
        if OPT_YMAX: plt.ylim( ymax=int(OPT_YMAX) )

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
        plt.savefig("TDOS.eps")
        plt.savefig("TDOS.pdf")
        plt.savefig("TDOS.png")

    if not NO_WINDOW_FLAG:
        plt.show()

    plt.close('all')

################################################################################
