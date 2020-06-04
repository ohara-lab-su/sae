#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vplot_ADOS.py
#
#   原子の種類ごとのオービタル足しあわせ LDOS + TODOS 出力
#
#   1) gnuplot の代わりに matplotlib を用いる
#   2) Vldos.py などは用いない
#   3) 内部的には直接 ReadDoscar クラス(ReadDoscar.py)を用いる
#      そもそも ReadDoscar クラスは matplotlib からの利用を念頭に構造化している
#
#   注意) ION 毎の情報が必要なので、OUTCAR の読み込みは必須となる
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.10.29
#    キャプション移動オプション
#    LMAX 判定による f軌道オプション
#
# 2015.01.29
#    Y軸(DOS軸) の下限の設定のバグを修正
#
# 2015.01.14
#      SPIN対応,option XMAX,XMIN,YMAX 対応
#
# 2015.01.14
#      元素名判別＆ラベルの自動出力
#
# 2015.01.13
#      とりあえず完成
#      色設定の自動化
#      むしろ、ReadDoscar, ReadOutcar を中心に修正・改良
#
# 2015.01.11 (sun) startup
#      原子種ごとのs成分,p成分,d成分をsumしたものを TDOS と一緒にプロット
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
__version__    = "0.0.4"
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
import matplotlib.cm as cm
#import matplotlib.mlab as mlab

################################################################################
def options():

    dname = 'DOSCAR'
    oname = 'OUTCAR'

    parser = optparse.OptionParser()
    parser.add_option('-d','--doscar', dest='DOSCAR', default=dname,)
    parser.add_option('-o', '--outcar', dest='OUTCAR', default=oname,)
    parser.add_option('--emax', dest='EMAX',)
    parser.add_option('--emin', dest='EMIN',)
    parser.add_option('--ymax', dest='YMAX',)
    # title
    parser.add_option('--title',)
    # up-spin のみプロット
    parser.add_option('--up', action='store_true', default=False)
    # dn-spin のみプロット
    parser.add_option('--dn', '--down', dest='dn', action='store_true', default=False)
    # total を描かないスイッチ(default はFalse で、total を描く
    parser.add_option('--total', action='store_true', default=False)
    # efermi を 0 ではなく efermi 近傍のDOSからVBMを探してそこをEF0 とする
    parser.add_option('--vbm', action='store_true')
    # efermi を 0 ではなく shift した値を使う
    parser.add_option('--shift')
    # legend の right と left の切り替え
    parser.add_option('--left', action='store_true')
    # EF0 のラインを消す
    parser.add_option('--noef', action='store_true')
    parser.add_option('-n', '--nw', action='store_true', default=False, dest='NOWINDOW',)
    options,  args = parser.parse_args()

    if options.DOSCAR: dname=options.DOSCAR
    if options.OUTCAR: oname=options.OUTCAR

    return [dname, oname,
            options.EMAX, options.EMIN, options.YMAX,
            options.title,
            options.up, options.dn,
            options.total, options.vbm, options.shift,
            options.left, options.noef, options.NOWINDOW]

################################################################################
if __name__ == '__main__':

    # set input file
    dname, oname,\
            OPT_EMAX, OPT_EMIN, OPT_YMAX, \
            OPT_TITLE,\
            FLAG_UP, FLAG_DN, \
            FLAG_TOT, FLAG_VBM, OPT_SHIFT, \
            FLAG_LEFT, FLAG_NOEF, FLAG_NW = options()

    if OPT_EMAX: print("Emax= %s" % str(OPT_EMAX))
    if OPT_EMIN: print("Emin= %s" % str(OPT_EMIN))
    if OPT_YMAX: print("Ymax= %s" % str(OPT_YMAX))

    # set output device
    out = sys.stdout

    # makes instance ( Read DOSCAR )
    print("READ %s" % str(dname))
    dos = SAE.ReadVaspDoscar(dname)
    print("END READ")

    NSPIN = dos.get_ispin()
    LORBIT = dos.get_lorbit()
    NATOM = dos.get_natom()
    EMAX = dos.get_emax()
    EMIN = dos.get_emin()
    NEDOS = dos.get_nedos()
    EFERMI = dos.get_efermi()
    ENG = dos.get_eng()
    LMAX = dos.lmax

    if not OPT_TITLE:
        TITLE =  dos.get_title()
    else:
        TITLE = OPT_TITLE

    if FLAG_VBM:
        EFERMI0 = dos.efermi
        print("SEARCH VBM MODE")
        print("  ORIGINAL EF =", end="")
        print(EFERMI0)
        EFERMI = dos.get_vbm()
        print("          VBM = %s" % str(EFERMI))

    if OPT_SHIFT:
        print("EF_SHIFT MODE")
        print("     NEW EF =")
        EFERMI = float(OPT_SHIFT)

    # makes instance ( Read OUTCAR )
    print("READ %s" % str(oname))
    outcar = SAE.ReadVaspOutcar(oname)
    print("END READ")

    NION = outcar.get_nion()
    atoms = outcar.get_atoms_index()

    ############################################################################
    # matplotlib

#   plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size']         = 20  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize']   = 18  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']    = 1.5 # 軸の太さを設定。目盛りは変わらない

#   plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)

    orgx = 0.150
    orgy = 0.143
#   off = 0.015
    off = 0.0
    xsize = 0.75
    ysize0 = 0.75

    ############################################################################
    if NSPIN >=2:
        print("SPIN MODE")
        spin_index=['up','dn']
        if FLAG_UP:
            spin_list=[0]
            out_suffix='_up'
            ysize = ysize0
            FLAG_BOTH_SPIN = False
        elif FLAG_DN:
            spin_list=[1]
            out_suffix='_dn'
            ysize = ysize0
            FLAG_BOTH_SPIN = False
        else:
            spin_list=[1,0]  # down, up と'積む'
            out_suffix=''
            ysize = ysize0/2.
            FLAG_BOTH_SPIN = True
    else:
        print("NONMAGNETIC MODE")
        spin_list=[0]
        out_suffix=''
        ysize = ysize0
        FLAG_BOTH_SPIN = False

    ############################################################################
#   for spin in range(NSPIN):
    FLAG_YTICKS = False
    for spin in spin_list:

        plt.axes([orgx, orgy, xsize, ysize])

        if not FLAG_TOT:
            INTTDOS = dos.get_inttdos(spin)
            TDOS = dos.get_tdos(spin)
    #       plt.plot(ENG-EFERMI,TDOS, color="black", linewidth=2, label='total')
            plt.fill_between(ENG-EFERMI,TDOS, color='#cccccc', linewidth=2, label='total')

        j=0
        for ion in range(NION):

            atom = str(atoms[ion])
            if NSPIN ==1:
                print("ion = %d %s" % (ion+1, str(atom)))
            else:
               #print "ion (spin) : ",ion+1,"("+spin_index[spin]+")",atom
                print("ion (spin) : %d (%s) %s" % (ion+1, str(spin_index[spin]), str(atom)))

            # autumn, bone, cool, copper, flag, gray, hot, hsv,
            # jet, pink, prism, spring, summer, winter, spectral

            c = cm.prism(float(j)/(3*NION))
            ADOS = dos.get_ldos_ion(0,ion,spin)
            plt.plot(ENG - EFERMI,ADOS, linestyle=":", color=c, linewidth=2, label=atom+'-s')
            j += 1

            c = cm.prism(float(j)/(3*NION))
            ADOS = dos.get_ldos_ion(1,ion,spin)
            plt.plot(ENG - EFERMI,ADOS, linestyle="-", color=c, linewidth=2, label=atom+'-p')
            j += 1

            if LMAX >= 2:
                c = cm.prism(float(j)/(3*NION))
                ADOS = dos.get_ldos_ion(2,ion,spin)
                plt.plot(ENG - EFERMI,ADOS, linestyle="--", color=c, linewidth=2, label=atom+'-d')
                j += 1

            if LMAX >= 3:
                c = cm.prism(float(j)/(3*NION))
                ADOS = dos.get_ldos_ion(3,ion,spin)
                plt.plot(ENG - EFERMI,ADOS, linestyle="-.", color=c, linewidth=2, label=atom+'-f')
                j += 1

            # Y軸の調整
            plt.ylim( ymin=0 )

        # 最初のプロット(一番下に積んだブロック)における ylabel and xlabel 処理
        if not FLAG_YTICKS:
            yl = plt.ylabel("DOS/eV", fontsize=20 )
            xl = plt.xlabel("$E -  E_{\mathrm{F}}$ [eV]", fontsize=20 )
            FLAG_YTICKS = True

        if OPT_EMAX: plt.xlim( xmax=float(OPT_EMAX) )
        if OPT_EMIN: plt.xlim( xmin=float(OPT_EMIN) )
        if OPT_YMAX: plt.ylim( ymax=float(OPT_YMAX) )

        # 両スピン描画の時はdown-spin を反転表示させる
        if FLAG_BOTH_SPIN:
            if spin == 0:
                plt.xticks([])
            if spin == 1:
                # y 軸反転
                xmin,xmax,ymin,ymax = plt.axis()
                plt.ylim([ymax,0])

        # EF0
        if not FLAG_NOEF:
            plt.axvline(x=0,color="black",linewidth=1)

        # 次のスピンの時の原点位置修正
        orgy = orgy + off + ysize

    ############################################################################

    if FLAG_UP:
        plt.title(TITLE+' (up-spin)')
    elif FLAG_DN:
        plt.title(TITLE+' (dn-spin)')
    else:
        plt.title(TITLE)

    if FLAG_LEFT:
        leg = plt.legend(fontsize=12, loc='upper left')   # 凡例Box
    else:
        leg = plt.legend(fontsize=12)   # 凡例Box

    leg.get_frame().set_alpha(0.5)  # Alphaチャンネル(半透明化)

#   plt.xlim([-10,10])
#   plt.ylim([0,200])

#   plt.savefig("ADOS"+out_suffix+".eps")
    plt.savefig("ADOS"+out_suffix+".pdf")
#   plt.savefig("ADOS"+out_suffix+".png")

    if not FLAG_NW:
        plt.show()

    plt.close('all')

################################################################################
