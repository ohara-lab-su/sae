#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.vasp.doscar import ReadVaspDoscar
from sae.vasp.outcar import ReadVaspOutcar

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vplot_ADOS_portrait.py
#
#   原子の種類ごとに画面分割を[自動]にして
#   種類ごとにオービタルを足しあわせ LDOS + TODOS 出力
#
#   注意) portrait モードが重要なのではなくて、自動分割がミソ
#
#   おそらく原子種の種類としては多くても４種類くらい(IGZOでも)
#   なので portrait で 4 分割+spin(合計8分割)はそれなりに現実的
#   それ以上小さくなると見難いので,自動で分割するのは非現実的かも
#
#   注意) ION 毎の情報が必要なので、OUTCAR の読み込みは必須となる
#         読み込めなかったら止まる。gzip 自動対応
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.01.15 startup
#      landscape モードを追加
#
# 2015.01.15 startup
#      Vplot_ADOS.py の再設計(複数画面化)
#      非SPIN版,完成
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
#import matplotlib.mlab as mlab
################################################################################
def options():
    dname = "DOSCAR"
    oname = "OUTCAR"
    parser = optparse.OptionParser()
    parser.add_option("-d", "--doscar", dest="DOSCAR", default=dname)
    parser.add_option("-o", "--outcar", dest="OUTCAR", default=oname)
    parser.add_option("-n", "--nw", action="store_true", default=False, dest="NOWINDOW")
    parser.add_option(
        "-l", "--landscape", action="store_true", default=False, dest="LANDSCAPE"
    )
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--emin", dest="EMIN")
    parser.add_option("--ymax", dest="YMAX")
    options, args = parser.parse_args()
    if options.DOSCAR:
        dname = options.DOSCAR
    if options.OUTCAR:
        oname = options.OUTCAR
    return [
        dname,
        oname,
        options.NOWINDOW,
        options.LANDSCAPE,
        options.EMAX,
        options.EMIN,
        options.YMAX,
    ]


################################################################################
# set input file
# set output device
# makes instance ( Read DOSCAR )
# makes instance ( Read OUTCAR )
############################################################################
# matplotlib
############################################################################
############################################################################
#   plt.xlim([-10,10])
#   plt.ylim([0,200])
if __name__ == "__main__":
    dname, oname, NO_WINDOW_FLAG, LANDSCAPE_FLAG, OPT_EMAX, OPT_EMIN, OPT_YMAX = (
        options()
    )
    TDOS_FLAG = True
    if OPT_EMAX:
        print("Emax= %s" % str(OPT_EMAX))
    if OPT_EMIN:
        print("Emin= %s" % str(OPT_EMIN))
    if OPT_YMAX:
        print("Ymax= %s" % str(OPT_YMAX))
    out = sys.stdout
    dos = ReadVaspDoscar(dname)
    NSPIN = dos.get_ispin()
    LORBIT = dos.get_lorbit()
    NATOM = dos.get_natom()
    TITLE = dos.get_title()
    EMAX = dos.get_emax()
    EMIN = dos.get_emin()
    NEDOS = dos.get_nedos()
    EFERMI = dos.get_efermi()
    outcar = ReadVaspOutcar(oname)
    NION = outcar.get_nion()
    atoms = outcar.get_atoms_index()
    ENG = dos.get_eng()
    plt.rcParams["font.family"] = "Times New Roman"
    # ラベル等のフォントサイズ
    plt.rcParams["font.size"] = 16
    # レジェンドのフォントサイズ
    plt.rcParams["legend.fontsize"] = 14
    # 軸の太さを設定。目盛りは変わらない
    plt.rcParams["axes.linewidth"] = 1.5
    #       plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)
    #       plt.figure(figsize=(8.27, 11.69)) # for portrait
    if not LANDSCAPE_FLAG:
        # for portrait
        plt.figure(figsize=(7.0, 9.89))
    orgx = 0.13
    orgy = 0.08
    off = 0.015
    size = 0.83 / NION / NSPIN
    # spin を逆から回す(先に描いものが下側に描画されるので)
    for ion in range(NION):
        ########################################################################
        # 原点位置を自動調整
        ########################################################################
        # DOSのY軸(DOS軸)原点をセットする(稀に必須)
        # down spin の時に反転させる
        # title,label,xticks
        # 一番上
        # 一番下以外
        # 一番下
        # EF0
        # 凡例BOX
        for spin in range(NSPIN - 1, -1, -1):
            #print "ion(spin) = ",ion+1,"("+str(spin+1)+")",atoms[ion]
            if NSPIN == 1:
                print("ion = %d %s" % (ion + 1, str(atoms[ion])))
            else:
                print(
                    "ion(spin) = %d (%s) %s" % (ion + 1, str(spin + 1), str(atoms[ion]))
                )
            atom = str(atoms[ion])
            plt.axes([orgx, orgy, 0.8, size])
            if NSPIN == 1:
                orgy = orgy + size + off
            if NSPIN == 2:
                if spin == 0:
                    orgy = orgy + size + off
                if spin == 1:
                    orgy = orgy + size
            if TDOS_FLAG:
                TDOS = dos.get_tdos(spin)
                plt.fill_between(
                    ENG - EFERMI, TDOS, color="#cccccc", linewidth=2, label="total"
                )
            c = "red"
            ADOS = dos.get_ldos_ion(0, ion, spin)
            plt.plot(
                ENG - EFERMI,
                ADOS,
                linestyle=":",
                color=c,
                linewidth=2,
                label=atom + "-s",
            )
            c = "green"
            ADOS = dos.get_ldos_ion(1, ion, spin)
            plt.plot(
                ENG - EFERMI,
                ADOS,
                linestyle="-",
                color=c,
                linewidth=2,
                label=atom + "-p",
            )
            c = "blue"
            ADOS = dos.get_ldos_ion(2, ion, spin)
            plt.plot(
                ENG - EFERMI,
                ADOS,
                linestyle="--",
                color=c,
                linewidth=2,
                label=atom + "-d",
            )
            if NSPIN == 1:
                xmin, xmax, ymin, ymax = plt.axis()
                plt.ylim([0, ymax])
            if NSPIN == 2:
                xmin, xmax, ymin, ymax = plt.axis()
                if spin == 0:
                    plt.ylim([0, ymax])
                if spin == 1:
                    plt.ylim([ymax, 0])
            if OPT_EMAX:
                plt.xlim(xmax=int(OPT_EMAX))
            if OPT_EMIN:
                plt.xlim(xmin=int(OPT_EMIN))
            if OPT_YMAX:
                plt.ylim(ymax=int(OPT_YMAX))
            if ion == NION - 1 and spin == 0:
                plt.title(TITLE, fontsize=16)
            if ion != 0:
                plt.xticks([])
            if NSPIN == 1:
                if ion == 0:
                    xl = plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=16)
                    yl = plt.ylabel("DOS/eV", fontsize=16)
            if NSPIN == 2:
                if ion == 0 and spin == 0:
                    plt.xticks([])
                if ion == 0 and spin == 1:
                    xl = plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=16)
                    yl = plt.ylabel("DOS/eV", fontsize=16)
            plt.axvline(x=0, color="black", linewidth=1)
            if spin == 0:
                # 凡例Box
                leg = plt.legend(fontsize=12)
                # Alphaチャンネル(半透明化)
                leg.get_frame().set_alpha(0.5)
    #       plt.savefig("ADOS_portrait.eps",orientation = 'portrait',papertype = 'a4')
    if LANDSCAPE_FLAG:
        plt.savefig("ADOS.eps")
        plt.savefig("ADOS.pdf")
        plt.savefig("ADOS.png")
    else:
        plt.savefig("ADOS_portrait.eps", orientation="portrait")
        plt.savefig("ADOS_portrait.pdf", orientation="portrait")
        plt.savefig("ADOS_portrait.png", orientation="portrait")
    if not NO_WINDOW_FLAG:
        plt.show()
    plt.close("all")
