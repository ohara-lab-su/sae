#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.vasp.doscar import ReadVaspDoscar

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
#   3) 内部的には直接 ReadVaspDoscar クラス(ReadVaspDoscar.py)を用いる
#      そもそも ReadVaspDoscar クラスは matplotlib からの利用を念頭に
#      構造化している
#
#   4) 引数処理(局所状態密度の原子選択や、対称性による軌道選択)などは
#      別プログラムで、それぞれ対応になるので、ほぼ vplot_LDOS* シリーズと
#      同じファイル構成になる。
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.10.28
#   f軌道対応 & キャプション移動オプション
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
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import optparse
import matplotlib.pyplot as plt


#
################################################################################
#import os
#import gzip
#import numpy as np
#import re
#from copy import deepcopy
#import SpaceGroupEnvironment as SGE
#import matplotlib.cm as cm
#import matplotlib.ticker as tic
#import matplotlib.mlab as mlab
################################################################################
# 積分状態密度同時プロットオプション
# spd-all を 'off' するスイッチ
# f-all を 'on' にするスイッチ
# NSPIN=2 のときに、片方のスピンだけを表示するオプション
# efermi を 0 ではなく efermi 近傍のDOSからVBMを探してそこをEF0 とする
# efermi を 0 ではなく shift した値を使う
# legend の right と left の切り替え
# EF0 のラインを消す
#   if options.OPT_EMAX:
#       print options.OPT_EMAX
def options():
    dname = "DOSCAR"
    oname = "OUTCAR"
    parser = optparse.OptionParser()
    parser.add_option("-d", "--doscar", dest="DOSCAR")
    parser.add_option("-o", "--outcar", dest="OUTCAR")
    parser.add_option("-n", "--nw", action="store_true", default=False, dest="NOWINDOW")
    parser.add_option(
        "-p", "--portrait", action="store_true", default=False, dest="PORTRAIT"
    )
    parser.add_option("--inttdos", action="store_true", default=False)
    parser.add_option("--spd", action="store_true", default=False)
    parser.add_option("-f", action="store_true", default=False)
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--ymax", dest="YMAX")
    parser.add_option("--emin", dest="EMIN")
    parser.add_option("--up", action="store_true")
    parser.add_option("--dn", action="store_true")
    parser.add_option("--vbm", action="store_true", default=False)
    parser.add_option("--shift")
    parser.add_option("--left", action="store_true", default=False)
    parser.add_option("--noef", action="store_true", default=False)
    options, args = parser.parse_args()
    if options.DOSCAR:
        dname = options.DOSCAR
    if options.OUTCAR:
        oname = options.OUTCAR
    return [
        dname,
        oname,
        options.NOWINDOW,
        options.PORTRAIT,
        options.inttdos,
        options.spd,
        options.f,
        options.EMAX,
        options.EMIN,
        options.YMAX,
        options.up,
        options.dn,
        options.vbm,
        options.shift,
        options.left,
        options.noef,
    ]


################################################################################
# set input file
# makes instance ( Read DOSCAR )
#   if os.path.exists(oname) or os.path.exists(oname+'.gz'):
#       FLAG_outcar = True
#       outcar = SAE.io.ReadVaspOutcar(oname)
# set output device
############################################################################
# matplotlib
#   plt.rcParams['font.family'] = 'Times New Roman'
#   plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)
############################################################################
#   for spin in range(NSPIN):
##########################################################################
#   plt.xlim([-10,10])
#   plt.ylim([0,200])
if __name__ == "__main__":
    (
        dname,
        oname,
        NO_WINDOW_FLAG,
        PORTRAIT_FLAG,
        FLAG_INTTDOS,
        FLAG_SPD,
        FLAG_F,
        OPT_EMAX,
        OPT_EMIN,
        OPT_YMAX,
        FLAG_UP,
        FLAG_DN,
        FLAG_VBM,
        OPT_SHIFT,
        FLAG_LEFT,
        FLAG_NOEF,
    ) = options()
    if OPT_EMAX:
        OPT_EMAX = float(OPT_EMAX)
        print("Emax= %s" % str(OPT_EMAX))
    if OPT_EMIN:
        OPT_EMIN = float(OPT_EMIN)
        print("Emin= %s" % str(OPT_EMIN))
    if OPT_YMAX:
        OPT_YMAX = float(OPT_YMAX)
        print("Ymax= %s" % str(OPT_YMAX))
    if FLAG_INTTDOS:
        print("INTTDOS mode")
    dos = ReadVaspDoscar(dname)
    out = sys.stdout
    NSPIN = dos.ispin
    LORBIT = dos.lorbit
    NATOM = dos.natom
    TITLE = dos.title
    EMAX = dos.emax
    EMIN = dos.emin
    NEDOS = dos.nedos
    EFERMI = dos.efermi
    LMAX = dos.lmax
    ENG = dos.eng
    if FLAG_VBM:
        print("EF SHIFT")
        EFERMI0 = dos.efermi
        EFERMI = dos.get_vbm()
        print(EFERMI0, EFERMI)
    if OPT_SHIFT:
        EFERMI = float(OPT_SHIFT)
    # ラベル等のフォントサイズ
    plt.rcParams["font.size"] = 16
    # レジェンドのフォントサイズ
    plt.rcParams["legend.fontsize"] = 15
    # 軸の太さを設定。目盛りは変わらない
    plt.rcParams["axes.linewidth"] = 1.5
    #       plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)
    #       plt.figure(figsize=(8.27, 11.69)) # for portrait
    if PORTRAIT_FLAG:
        # for portrait
        plt.figure(figsize=(7.0, 9.89))
    orgx = 0.13
    orgy = 0.125
    sizex = 0.75
    sizey0 = 0.8
    if NSPIN >= 2:
        spin_list = [0, 1]
        if FLAG_UP:
            spin_list = [0]
            NSPIN = 1
        if FLAG_DN:
            spin_list = [1]
            NSPIN = 1
    else:
        spin_list = [0]
    # Y軸の調整
    # EF0
    ## for BCC-Fe
    #plt.xlim([-10,10])
    #plt.ylim([0,2.5])
    # EF0
    for spin in spin_list:
        if NSPIN == 1:
            sizey = sizey0
        if NSPIN == 2:
            sizey = sizey0 / 2.0
        # 二段組の上側(y幅半分) up-spin
        if NSPIN == 2 and spin == 0:
            orgy = orgy + sizey
        # 二段組の下段( down-spin )
        if NSPIN == 2 and spin == 1:
            orgy = orgy - sizey
        plt.axes([orgx, orgy, sizex, sizey])
        if NSPIN == 1:
            plt.title(TITLE)
        INTTDOS = dos.get_inttdos(spin)
        TDOS = dos.get_tdos(spin)
        if not FLAG_SPD:
            plt.fill_between(ENG - EFERMI, TDOS, color="#cccccc", linewidth=2)
        else:
            plt.plot(ENG - EFERMI, TDOS, color="black", linewidth=2, label="total")
            plt.fill_between(ENG - EFERMI, TDOS, color="#cccccc", linewidth=2)
        if spin == 0:
            yl = plt.ylabel("DOS/eV", fontsize=20)
        if FLAG_INTTDOS:
            ax = plt.twinx()
            ax.plot(ENG - EFERMI, INTTDOS, color="black", linewidth=2, label="INTTDOS")
            plt.ylabel("INTTDOS [n]", fontsize=20)
        if not FLAG_SPD:
            TDOS = dos.get_tdos_spd(0, spin)
            plt.plot(ENG - EFERMI, TDOS, color="red", linewidth=2, label="ALL-s")
            TDOS = dos.get_tdos_spd(1, spin)
            plt.plot(ENG - EFERMI, TDOS, color="green", linewidth=2, label="ALL-p")
            TDOS = dos.get_tdos_spd(2, spin)
            plt.plot(ENG - EFERMI, TDOS, color="blue", linewidth=2, label="ALL-d")
            if FLAG_F or LMAX >= 3:
                TDOS = dos.get_tdos_spd(3, spin)
                plt.plot(ENG - EFERMI, TDOS, color="yellow", linewidth=2, label="ALL-f")
        plt.ylim(ymin=0)
        if not FLAG_NOEF:
            plt.axvline(x=0, color="black", linewidth=1)
        if OPT_EMAX:
            plt.xlim(xmax=float(OPT_EMAX))
        if OPT_EMIN:
            plt.xlim(xmin=float(OPT_EMIN))
        if OPT_YMAX:
            plt.ylim(ymax=float(OPT_YMAX))
        if NSPIN == 2:
            if spin == 0:
                plt.xticks([])
            # y 軸反転
            if spin == 1:
                xmin, xmax, ymin, ymax = plt.axis()
                plt.ylim([ymax, 0.0])
        if not FLAG_NOEF:
            plt.axvline(x=0, color="black", linewidth=1)
    plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=20)
    if FLAG_LEFT:
        leg = plt.legend(fontsize=12, loc="upper left")
    else:
        # 凡例Box
        leg = plt.legend(fontsize=12)
    # Alphaチャンネル(半透明化)
    leg.get_frame().set_alpha(0.5)
    xmin, xmax, ymin, ymax = plt.axis()
    if PORTRAIT_FLAG:
        plt.savefig("TDOS.eps", orientation="portrait")
        plt.savefig("TDOS.pdf", orientation="portrait")
        plt.savefig("TDOS.png", orientation="portrait")
    else:
        plt.savefig("TDOS.eps")
        plt.savefig("TDOS.pdf")
        plt.savefig("TDOS.png")
    if not NO_WINDOW_FLAG:
        plt.show()
    plt.close("all")
