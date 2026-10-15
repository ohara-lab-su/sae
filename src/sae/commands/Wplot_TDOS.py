#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.common.paths import FileDiscovery
from sae.wien2k.dos import ReadWienDos
from sae.wien2k.output0 import ReadWienOutput0

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Wplot_TDOS.py
#
# MXplot_TDOS.py (2015.03.26ベース)
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
# 2015.03.27
#  unit の表示
#
# 2015.03.27
#  total-DOS がないときの処理と原子毎のtotal の処理
#
# 2015.03.26
#  get_ldos_ion() にて読んでいる case.output0 は並列計算すると
#  output0000 になるので注意、修正した
#
# 2015.03.26
#  startup
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
import os
import re
import optparse
import matplotlib.pyplot as plt


#
################################################################################
#import gzip
#import numpy as np
#from copy import deepcopy
#import SpaceGroupEnvironment as SGE
#import matplotlib.cm as cm
#import matplotlib.ticker as tic
#import matplotlib.mlab as mlab
################################################################################
def options():
    name = re.sub(".*/", "", os.getcwd())
    unit = "ev"
    parser = optparse.OptionParser(os.getcwd())
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-e", "--ev", action="store_true", default=False)
    parser.add_option("-f", "--fermi", action="store_true", default=False)
    parser.add_option("-n", "--nw", action="store_true", default=False)
    parser.add_option("-p", "--portrait", action="store_true", default=False)
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--emin", dest="EMIN")
    parser.add_option("--ymax", dest="YMAX")
    options, args = parser.parse_args()
    if options.ev:
        unit = "ev"
    else:
        unit = "None"
    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]
    return [
        name,
        unit,
        options.fermi,
        options.nw,
        options.portrait,
        options.EMAX,
        options.EMIN,
        options.YMAX,
    ]


################################################################################
############################################
# set input file
############################################
# case.dos ファイルを抽出
############################################
# check SPIN
############################################
# SPIN 有りの時に list のスピン毎の作り直し
############################################
# unit の書き直し
############################################################################
# matplotlib
#   plt.rcParams['font.family'] = 'Times New Roman'
#   plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)
############################################################################
##########################################################################
#   leg = plt.legend(fontsize=12)   # 凡例Box
#   leg.get_frame().set_alpha(0.5)  # Alphaチャンネル(半透明化)
#   plt.xlim([-10,10])
#   plt.ylim([0,200])
if __name__ == "__main__":
    case, unit, FERMI, NO_WINDOW_FLAG, PORTRAIT_FLAG, OPT_EMAX, OPT_EMIN, OPT_YMAX = (
        options()
    )
    if OPT_EMAX:
        print("Emax=", OPT_EMAX)
    if OPT_EMIN:
        print("Emin=", OPT_EMIN)
    if OPT_YMAX:
        print("Ymax=", OPT_YMAX)
    lists = FileDiscovery().find_suffix3(case + ".dos", unit)
    if not lists:
        sys.exit("STOP: " + case + ".dos* file not found")
    print("READ FILE    :", end="")
    for i in lists:
        print(i, end="")
    print("")
    if os.path.exists(case + ".output0"):
        output0_file = case + ".output0"
    elif os.path.exists(case + ".output0.gz"):
        output0_file = case + ".output0.gz"
    elif os.path.exists(case + ".output0000"):
        output0_file = case + ".output0000"
    elif os.path.exists(case + ".output0000.gz"):
        output0_file = case + ".output0000.gz"
    else:
        sys.exit("STOP: output0 file not found")
    output0 = ReadWienOutput0(output0_file)
    nspin = output0.get_ispin()
    ions_index = output0.get_ions_index()
    FLAG_SPIN = False
    if nspin >= 2:
        FLAG_SPIN = True
    if FLAG_SPIN:
        up = []
        dn = []
        for i in lists:
            up.append(re.sub("up", "", re.sub("dn", "", i)) + "up")
            dn.append(re.sub("up", "", re.sub("dn", "", i)) + "dn")
        up_lists = list(set(up))
        dn_lists = list(set(dn))
    if unit == "ev":
        unit = "eV"
        FERMI = True
    else:
        unit = "Ry"
    # ラベル等のフォントサイズ
    plt.rcParams["font.size"] = 20
    # レジェンドのフォントサイズ
    plt.rcParams["legend.fontsize"] = 18
    # 軸の太さを設定。目盛りは変わらない
    plt.rcParams["axes.linewidth"] = 1.5
    #       plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)
    #       plt.figure(figsize=(8.27, 11.69)) # for portrait
    if PORTRAIT_FLAG:
        # for portrait
        plt.figure(figsize=(7.0, 9.89))
    ############################
    # makes instance
    #plot_ions = dos.get_plot_ions()
    ########################################################
    ########################################################
    #s = dos.get_raw_dos(atom=ion,orbit='s')
    #p = dos.get_raw_dos(atom=ion,orbit='s')
    #d = dos.get_raw_dos(atom=ion,orbit='d')
    ########################################################
    # Y軸の調整
    # EF0
    ## for BCC-Fe
    #plt.xlim([-10,10])
    #plt.ylim([0,2.5])
    # EF0
    for spin in range(nspin):
        if FLAG_SPIN and spin == 0:
            lists = up_lists
        if FLAG_SPIN and spin == 1:
            lists = dn_lists
        dos = ReadWienDos(lists)
        nion = dos.get_nion()
        nedos = dos.get_nedos()
        efermi = dos.get_efermi()
        emax = dos.get_emax()
        emin = dos.get_emin()
        eng = dos.get_eng()
        title = case
        if nspin == 1:
            # 一段組の原点(x,y), 幅(x,y) nonmag
            plt.axes([0.13, 0.13, 0.8, 0.8])
            plt.title(title)
        if nspin == 2:
            if spin == 0:
                # 二段組の上側(y幅半分) up-spin
                plt.axes([0.13, 0.53, 0.8, 0.4])
            if spin == 1:
                # 二段組の下段( down-spin )
                plt.axes([0.13, 0.13, 0.8, 0.4])
        if dos.chk_raw_dos(atom=0, orbit="total-DOS"):
            tdos = dos.get_raw_dos(atom=0, orbit="total-DOS")
        else:
            sys.exit("STOP: don't found total-DOS section in case.dos*")
        e = []
        for i in range(nedos):
            if FERMI:
                e.append(eng[i] - efermi)
            else:
                e.append(eng[i])
        plt.fill_between(e, tdos, color="#cccccc", linewidth=2, label="total")
        plt.ylim(ymin=0)
        if FERMI:
            plt.axvline(x=0, color="black", linewidth=1)
        else:
            plt.axvline(x=efermi, color="black", linewidth=1)
        if spin == 0:
            yl = plt.ylabel("DOS/" + unit, fontsize=20)
        if OPT_EMAX:
            plt.xlim(xmax=int(OPT_EMAX))
        if OPT_EMIN:
            plt.xlim(xmin=int(OPT_EMIN))
        if OPT_YMAX:
            plt.ylim(ymax=int(OPT_YMAX))
        if nspin == 2:
            if spin == 0:
                plt.xticks([])
            # y 軸反転
            if spin == 1:
                xmin, xmax, ymin, ymax = plt.axis()
                plt.ylim([ymax, 0.0])
        if FERMI:
            plt.axvline(x=0, color="black", linewidth=1)
        else:
            plt.axvline(x=efermi, color="black", linewidth=1)
    if FERMI:
        plt.xlabel("$E -  E_{\\mathrm{F}}$ [" + unit + "]", fontsize=20)
    else:
        plt.xlabel("$E$ [" + unit + "]", fontsize=20)
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
