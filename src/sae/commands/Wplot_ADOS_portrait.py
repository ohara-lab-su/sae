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
# Wplot_LDOS.py
#
# MXplot_ADOS_portrait.py (2015.03.26) ベースで作成
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
#   注意) ION 毎の情報が必要なので、OUTCAR の読み込み
#         (OpenMX だと *.out or *.dat ) は必須となる
#         読み込めなかったら止まる。gzip 自動対応
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
#  軌道成分の存在確認＆出力の有無の自動判別を追加
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
    parser.add_option("-l", "--landscape", action="store_true", default=False)
    parser.add_option("-a", "--atomtot", action="store_true", default=False)
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
    return [
        name,
        unit,
        options.fermi,
        options.nw,
        options.landscape,
        options.atomtot,
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
# unit の書き直し
############################################
# check SPIN
############################################
# SPIN 有りの時に list のスピン毎の作り直し
############################################################################
# matplotlib
############################################################################
# spin を逆から回す(先に描いものが下側に描画されるので)
############################################################################
#   plt.xlim([-10,10])
#   plt.ylim([0,200])
if __name__ == "__main__":
    (
        case,
        unit,
        FERMI,
        NO_WINDOW_FLAG,
        LANDSCAPE_FLAG,
        AT_FLAG,
        OPT_EMAX,
        OPT_EMIN,
        OPT_YMAX,
    ) = options()
    TDOS_FLAG = True
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
    if unit == "ev":
        unit = "eV"
        FERMI = True
    else:
        unit = "Ry"
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
    nion = output0.get_nion()
    atoms_index = output0.get_atoms_index()
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
    size = 0.83 / nion / nspin
    ############################
    # makes instance
    for spin in range(nspin - 1, -1, -1):
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
        plot_ions = dos.get_plot_ions()
        title = case
        ion_j = 0
        ####################################################
        # X 軸
        ####################################################
        # ラベル
        #atom = str(atoms_index[ion])
        ####################################################################
        # 原点位置を自動調整
        ####################################################################
        # Y軸
        ####################################################################
        # DOSのY軸(DOS軸)原点をセットする(稀に必須)
        # down spin の時に反転させる
        # title,label,xticks
        # 一番上
        # 一番下以外
        # 一番下
        # EF0
        # 凡例BOX
        for ion in plot_ions:
            e = []
            for i in range(nedos):
                if FERMI:
                    e.append(eng[i] - efermi)
                else:
                    e.append(eng[i])
            atom_index = atoms_index[ion - 1]
            if nspin == 1:
                print("ion = ", atom_index)
            else:
                print("ion(spin) = " + atom_index + "(" + str(spin + 1) + ")")
            atom = str(atom_index)
            plt.axes([orgx, orgy, 0.8, size])
            if nspin == 1:
                orgy = orgy + size + off
            if nspin == 2:
                if spin == 0:
                    orgy = orgy + size + off
                if spin == 1:
                    orgy = orgy + size
            if TDOS_FLAG and dos.chk_raw_dos(atom=0, orbit="total-DOS"):
                tdos = dos.get_raw_dos(atom=ion, orbit="total-DOS")
                plt.fill_between(e, tdos, color="#cccccc", linewidth=2, label="total")
            else:
                TDOS_FLAG = False
            if dos.chk_raw_dos(atom=ion, orbit="total") and AT_FLAG:
                t = dos.get_raw_dos(atom=ion, orbit="total")
                if TDOS_FLAG:
                    plt.plot(e, t, color="black", linewidth=2, label=atom + "-tot")
                else:
                    plt.fill_between(
                        e, t, color="#cccccc", linewidth=2, label=atom + "-tot"
                    )
            #s = dos.get_raw_dos(atom=ion,orbit='s')
            if dos.chk_raw_dos(atom=ion, orbit="s"):
                s = dos.get_ldos_ion(case=case, atom=ion, orbit="s")
                c = "red"
                plt.plot(e, s, linestyle=":", color=c, linewidth=2, label=atom + "-s")
            #p = dos.get_raw_dos(atom=ion,orbit='p')
            if dos.chk_raw_dos(atom=ion, orbit="p"):
                p = dos.get_ldos_ion(case=case, atom=ion, orbit="p")
                c = "green"
                plt.plot(e, p, linestyle="-", color=c, linewidth=2, label=atom + "-p")
            #d = dos.get_raw_dos(atom=ion,orbit='d')
            if dos.chk_raw_dos(atom=ion, orbit="d"):
                d = dos.get_ldos_ion(case=case, atom=ion, orbit="d")
                c = "blue"
                plt.plot(e, d, linestyle="-.", color=c, linewidth=2, label=atom + "-d")
            #f = dos.get_raw_dos(atom=ion,orbit='f')
            if dos.chk_raw_dos(atom=ion, orbit="f"):
                f = dos.get_ldos_ion(case=case, atom=ion, orbit="f")
                c = "yellow"
                plt.plot(e, f, linestyle="-.", color=c, linewidth=2, label=atom + "-f")
            if nspin == 1:
                xmin, xmax, ymin, ymax = plt.axis()
                plt.ylim([0, ymax])
            if nspin == 2:
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
            if ion_j == nion - 1 and spin == 0:
                plt.title(title, fontsize=16)
            if ion_j != 0:
                plt.xticks([])
            if nspin == 1:
                if ion_j == 0:
                    if FERMI:
                        xl = plt.xlabel(
                            "$E -  E_{\\mathrm{F}}$ [" + unit + "]", fontsize=16
                        )
                    else:
                        xl = plt.xlabel("$E$ [" + unit + "]", fontsize=16)
                    yl = plt.ylabel("DOS/" + unit, fontsize=16)
            if nspin == 2:
                if ion_j == 0 and spin == 0:
                    plt.xticks([])
                if ion_j == 0 and spin == 1:
                    if FERMI:
                        xl = plt.xlabel(
                            "$E -  E_{\\mathrm{F}}$ [" + unit + "]", fontsize=16
                        )
                    else:
                        xl = plt.xlabel("$E$ [" + unit + "]", fontsize=16)
                    yl = plt.ylabel("DOS/" + unit, fontsize=16)
            if FERMI:
                plt.axvline(x=0, color="black", linewidth=1)
            else:
                plt.axvline(x=efermi, color="black", linewidth=1)
            if spin == 0:
                # 凡例Box
                leg = plt.legend(fontsize=12)
                # Alphaチャンネル(半透明化)
                leg.get_frame().set_alpha(0.5)
            ion_j += 1
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
