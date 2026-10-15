#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
# atom END
################################################
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
# Wplo_LDOSm.py
#
#   Wplot_LDOS.py の multi window 版(軌道成分ごとに別の box で描画する)
#   (vplot_LDOS に一番近い描画形式)
#
#   指定した原子番号 or 元素記号(サイトごとの記号) で記述
#
#   引数形式で記述とした時に複数の番号を記述した時のその和を記述する
#
#   -a が 原子番号記述のオプションとなっているのに注意
#   (Wplot_LDOS.py だと 原子サイトごとの total の表示オプションスイッチ)
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.04.22
#  暫定版(実用版)を一応リリース
#
# 2015.04.21
#  simple versoin
#  non-spin 版としてやり直し
#
# 2015.03.27
#  startup
#   --> 途中で放し、未完のまま放置
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
import matplotlib.cm as cm


#
################################################################################
#import gzip
#import numpy as np
#import re
#from copy import deepcopy
#import SpaceGroupEnvironment as SGE
#import matplotlib.mlab as mlab
################################################################################
def options():
    name = re.sub(".*/", "", os.getcwd())
    atom = 1
    parser = optparse.OptionParser(os.getcwd())
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-a", "--atom")
    parser.add_option("-u", "--up", action="store_true", default=False)
    parser.add_option("-d", "--down", action="store_true", default=False)
    parser.add_option("-e", "--ev", action="store_true", default=False)
    parser.add_option("-f", "--fermi", action="store_true", default=False)
    parser.add_option("-n", "--nw", action="store_true", default=False)
    parser.add_option("--all", dest="ALL", action="store_true", default=False)
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
    if options.atom:
        atom = options.atom
    if options.ALL:
        options.nw = True
    if len(args) > 0:
        atom = int(args[0])
    return [
        name,
        atom,
        unit,
        options.fermi,
        options.nw,
        options.ALL,
        options.up,
        options.down,
        options.EMAX,
        options.EMIN,
        options.YMAX,
    ]


################################################################################
############################################
# set input file
############################################
# プロットする軌道のリスト
############################################
# オプションの確認
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
############################################
############################################
# X軸
################################################
if __name__ == "__main__":
    (
        case,
        atom,
        unit,
        FERMI,
        NO_WINDOW_FLAG,
        ALL_FLAG,
        OPT_UP,
        OPT_DN,
        OPT_EMAX,
        OPT_EMIN,
        OPT_YMAX,
    ) = options()
    orbit_list = ["total-DOS", "s", "p", "d"]
    if OPT_EMAX:
        print("Emax=", OPT_EMAX)
    if OPT_EMIN:
        print("Emin=", OPT_EMIN)
    if OPT_YMAX:
        print("Ymax=", OPT_YMAX)
    if OPT_UP:
        print("SPIN-UP")
    if OPT_DN:
        print("SPIN-DOWN")
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
    print("UNIT:", unit)
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
    if FLAG_SPIN:
        if OPT_UP:
            dos = ReadWienDos(up_lists)
        elif OPT_DN:
            dos = ReadWienDos(dn_lists)
        else:
            sys.exit("STOP: You need spin(up/dn) option")
    else:
        dos = ReadWienDos(lists)
    nion = dos.get_nion()
    nedos = dos.get_nedos()
    efermi = dos.get_efermi()
    eng = dos.get_eng()
    title = case
    e = []
    for i in range(nedos):
        if FERMI:
            e.append(eng[i] - efermi)
        else:
            e.append(eng[i])
    print("IONS: ", ions_index)
    if ALL_FLAG:
        a1 = 1
        a2 = len(ions_index) + 1
    else:
        a1 = int(atom)
        a2 = int(atom) + 1
    ############################################
    # setting figure
    ############################################
    # multi-plot
    # END multi-plot
    ############################################
    for atom in range(a1, a2):
        # ラベル等のフォントサイズ
        plt.rcParams["font.size"] = 18
        # レジェンドのフォントサイズ
        plt.rcParams["legend.fontsize"] = 10
        # 軸の太さを設定。目盛りは変わらない
        plt.rcParams["axes.linewidth"] = 1.5
        # for portrait
        plt.figure(figsize=(7.0, 9.89))
        orgx = 0.15
        orgy = 0.08
        off = 0.034
        xsize = 0.75
        ysize = 0.74 / len(orbit_list)
        atom_name = ions_index[int(atom) - 1]
        print("ATOM: ", atom_name)
        j = 0
        for orbit in orbit_list:
            print("ORBIT: ", orbit)
            ############################################
            # EF0
            ############################################
            # Y軸の調整
            ############################################
            # Label 処理
            if dos.chk_raw_dos(atom=atom, orbit=orbit):
                plt.axes([orgx, orgy, xsize, ysize])
                ldos = dos.get_raw_dos(atom=atom, orbit=orbit)
                c = cm.prism(j * 20 / 4)
                plt.plot(e, ldos, color=c, linewidth=2, label=orbit)
                orgy = orgy + ysize + off
                if FERMI:
                    plt.axvline(x=0, color="black", linewidth=1)
                else:
                    plt.axvline(x=efermi, color="black", linewidth=1)
                plt.ylim(ymin=0)
                if OPT_EMAX:
                    plt.xlim(xmax=int(OPT_EMAX))
                if OPT_EMIN:
                    plt.xlim(xmin=int(OPT_EMIN))
                if OPT_YMAX:
                    plt.ylim(ymax=int(OPT_YMAX))
                # 凡例Box
                leg = plt.legend(fontsize=12)
                # Alphaチャンネル(半透明化)
                leg.get_frame().set_alpha(0.5)
                if j != 0:
                    plt.xticks([])
                    plt.ylabel("")
                if j == 0:
                    yl = plt.ylabel("DOS/" + unit, fontsize=20)
                    if FERMI:
                        plt.xlabel("$E -  E_{\\mathrm{F}}$ [" + unit + "]", fontsize=20)
                    else:
                        plt.xlabel("$E$ [" + unit + "]", fontsize=20)
                j += 1
        if FLAG_SPIN:
            if OPT_UP:
                plt.title(title + "  spin-up (" + str(atom_name) + ") ", fontsize=18)
            if OPT_DN:
                plt.title(title + "  spin-down (" + str(atom_name) + ") ", fontsize=18)
        else:
            plt.title(title + "  (" + str(atom_name) + ") ", fontsize=18)
        plt.savefig("LDOS" + str(atom) + ".eps")
        plt.savefig("LDOS" + str(atom) + ".pdf")
        plt.savefig("LDOS" + str(atom) + ".png")
        if not NO_WINDOW_FLAG:
            plt.show()
        plt.close("all")
