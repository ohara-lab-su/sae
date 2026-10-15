#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
##########################################################################
from __future__ import print_function
from sae.lobster.cohpcar import ReadLobCohp
from sae.lobster.doscar import ReadLobDos

#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vplot_COHP_yoko.py
#
#  1) 指定したCOHP描画のペア原子が一つの時は LDOS 追加表示モード
#  2) 指定したCOHP描画のペア原子が二つ以上の時は LDOS モードは OFF
#      かわりに COHP をペアごとに分割表示モードに
#
#      par は 1 番から (0番はAverage)
#
##########################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.09.01
#  par ごとの出力モード追加
#
# 2015.06.05
#  startup
#
##########################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import argparse
import matplotlib.pyplot as plt
import matplotlib.cm as cm


#
##########################################################################
#import sys
#import os
#import gzip
#import optparse
#import numpy as np
#import re
#from copy import deepcopy
#import SpaceGroupEnvironment as SGE
#import matplotlib.ticker as tic
#import matplotlib.mlab as mlab
##########################################################################
#   parser = optparse.OptionParser()
#   parser.add_option('-n', '--nw', action='store_true', default=False,)
#  par は 1 番から (0番はAverage)
#   options,  args = parser.parse_args()
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--nw", action="store_true", default=False)
    parser.add_argument("--emax", dest="EMAX")
    parser.add_argument("--emin", dest="EMIN")
    parser.add_argument("--dosmax", "--dmax", dest="DMAX")
    parser.add_argument("--cohpmax", "--ymax", dest="YMAX")
    parser.add_argument("--cohpmin", "--ymin", dest="YMIN")
    parser.add_argument("-u", "--up", action="store_true", default=False)
    parser.add_argument("-d", "--dn", action="store_true", default=False)
    parser.add_argument("--spin", action="store_true", default=False)
    parser.add_argument("--sp", action="store_true", default=False)
    parser.add_argument("--spd", action="store_true", default=True)
    parser.add_argument("--left", action="store_true", default=False)
    parser.add_argument("-p", "--pair", nargs="*")
    options = parser.parse_args()
    return [
        options.nw,
        options.DMAX,
        options.EMAX,
        options.EMIN,
        options.YMAX,
        options.YMIN,
        options.up,
        options.dn,
        options.spin,
        options.sp,
        options.spd,
        options.left,
        options.pair,
    ]


##########################################################################
# set options file
##########################################################################
# matplotlib
#   plt.rcParams['font.family'] = 'Times New Roman'
##########################################################################
# plot する l軌道のリスト
# TOTAL DOS & PDOS
# COHP Average
# ペアプロットするかどうかの判断
# 分割サイズの変更
######################################################## COHP Average
################### COHP Average
################### COHP Pair
######################################################## TDOS
# TDOS のプロット
######################################################## COHP 分割プロット
# LDOS を描画しないとき(複数のペアを書いたとき),COHPの分割表示on
######################################################## LDOS
# ペア原子のLDOSをプロットする
##########################################################################
if __name__ == "__main__":
    (
        NO_WINDOW_FLAG,
        OPT_DMAX,
        OPT_EMAX,
        OPT_EMIN,
        OPT_YMAX,
        OPT_YMIN,
        OPT_UP,
        OPT_DN,
        OPT_SPIN,
        OPT_SP,
        OPT_SPD,
        OPT_LEFT,
        OPT_PAIR,
    ) = options()
    if OPT_DMAX:
        print("Dmax=", OPT_DMAX)
    if OPT_EMAX:
        print("Emax=", OPT_EMAX)
    if OPT_EMIN:
        print("Emin=", OPT_EMIN)
    if OPT_YMAX:
        print("Ymax=", OPT_YMAX)
    if OPT_YMIN:
        print("Ymax=", OPT_YMIN)
    # ラベル等のフォントサイズ
    plt.rcParams["font.size"] = 14
    # レジェンドのフォントサイズ
    plt.rcParams["legend.fontsize"] = 12
    # 軸の太さを設定。目盛りは変わらない
    plt.rcParams["axes.linewidth"] = 1.5
    # for portrait
    plt.figure(figsize=(7.0, 9.89))
    orgx = 0.13
    orgy = 0.075
    off = 0.015
    sizey_dos0 = 0.7
    sizey_cohp0 = 1.4
    sizex = 0.8
    if OPT_SPD:
        orbit_list = [0, 1, 2]
        orbit_index = ["s", "p", "d"]
        foot = "spd"
    if OPT_SP:
        foot = "sp"
        orbit_list = [0, 1]
        orbit_index = ["s", "p"]
    spin_list = [0]
    if OPT_UP:
        spin_list = [0]
    if OPT_DN:
        spin_list = [1]
    if OPT_UP and OPT_DN:
        spin_list = [0, 1]
    if OPT_SPIN:
        spin_list = [0, 1]
    print("--- READ DOSCAR.lobster")
    dos = ReadLobDos()
    print("    END")
    dos_x = dos.eng
    print("--- READ COHPCAR.lobster")
    cohp = ReadLobCohp()
    print("    END")
    cohp_x = cohp.eng
    OPT_LDOS = False
    sizey = sizey_dos0 / 2
    sizey_cohp = sizey_dos0 / 2
    npar = 0
    if OPT_PAIR:
        # 分割サイズの変更
        # 分割サイズの変更
        if len(OPT_PAIR) > 1:
            npar = len(OPT_PAIR)
            OPT_LDOS = False
            sizey_cohp0 = sizey_cohp0 * 0.8
            sizey = sizey_dos0 / (float(npar) + 2)
            sizey_cohp = sizey_cohp0 / (float(npar) + 2)
        else:
            npar = 1
            OPT_LDOS = True
            print("Plot Pairs = ", end="")
            print(cohp.bond_index[int(OPT_PAIR[0])])
            norbit = len(orbit_list)
            sizey = sizey_dos0 / (float(norbit) * 2 + 2)
            sizey_cohp = sizey_cohp0 / (float(norbit) * 2 + 2)
    print("ORBIT_LIST= ", orbit_list)
    print("SPIN_LIST = ", spin_list)
    plt.axes([orgx, orgy, sizex, sizey_cohp])
    for s in spin_list:
        if s == 0:
            spin_label = "up"
        if s == 1:
            spin_label = "down"
        label = "Average" + " (" + spin_label + ")"
        cohp_y = cohp.get_ave(spin=s)
        plt.fill_between(dos_x, -1.0 * cohp_y, facecolor="#cccccc", label=label)
        plt.plot(cohp_x, -1.0 * cohp_y, color="black", linewidth=1, label=label)
        plt.axvline(x=0, color="black", linewidth=1)
        plt.xlim(xmax=dos.emax - dos.efermi)
        plt.xlim(xmin=dos.emin - dos.efermi)
        if OPT_EMAX:
            plt.xlim(xmax=float(OPT_EMAX))
        if OPT_EMIN:
            plt.xlim(xmin=float(OPT_EMIN))
        if OPT_YMAX:
            plt.ylim(ymax=float(OPT_YMAX))
        if OPT_YMIN:
            plt.ylim(ymin=float(OPT_YMIN))
    if OPT_PAIR:
        ci = 0
        for i in OPT_PAIR:
            par_label = cohp.bond_index[int(i)]
            c = cm.prism(ci * 5)
            #label = par_label+'  ('+spin_label+')'
            for s in spin_list:
                if s == 0:
                    spin_label = "up"
                if s == 1:
                    spin_label = "down"
                label = "COHP" + ":" + par_label + " (" + spin_label + ")"
                cohp_pair = cohp.get_cohp(bond=int(i), spin=s)
                plt.plot(cohp_x, -1.0 * cohp_pair, color=c, linewidth=1, label=label)
                plt.axhline(y=0, color="black", linewidth=1)
                plt.axvline(x=0, color="black", linewidth=1)
                plt.xlim(xmax=dos.emax - dos.efermi)
                plt.xlim(xmin=dos.emin - dos.efermi)
                if OPT_EMAX:
                    plt.xlim(xmax=float(OPT_EMAX))
                if OPT_EMIN:
                    plt.xlim(xmin=float(OPT_EMIN))
                if OPT_YMAX:
                    plt.ylim(ymax=float(OPT_YMAX))
                if OPT_YMIN:
                    plt.ylim(ymin=float(OPT_YMIN))
            ci += 1
    plt.ylabel("-pCOHP", fontsize=14)
    plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=14)
    # 凡例Box
    leg = plt.legend(fontsize=9)
    if OPT_LEFT:
        leg = plt.legend(loc="lower left")
    # Alphaチャンネル(半透明化)
    leg.get_frame().set_alpha(0.5)
    orgy = orgy + sizey_cohp + off
    plt.axes([orgx, orgy, sizex, sizey])
    for s in spin_list:
        if s == 0:
            spin_label = "up"
        if s == 1:
            spin_label = "down"
        label = "total DOS" + " (" + spin_label + ")"
        dos_y = dos.get_tdos(spin=s)
        plt.fill_between(dos_x, dos_y, facecolor="#cccccc")
        plt.plot(dos_x, dos_y, linewidth=1, label=label)
        plt.axvline(x=0, color="black", linewidth=1)
        plt.ylim(ymin=0)
        plt.xlim(xmax=dos.emax - dos.efermi)
        plt.xlim(xmin=dos.emin - dos.efermi)
        if OPT_DMAX:
            plt.ylim(ymax=float(OPT_DMAX))
        if OPT_EMAX:
            plt.xlim(xmax=float(OPT_EMAX))
        if OPT_EMIN:
            plt.xlim(xmin=float(OPT_EMIN))
        plt.xticks([])
    plt.ylabel("DOS/eV", fontsize=14)
    # 凡例Box
    leg = plt.legend(fontsize=9)
    if OPT_LEFT:
        leg = plt.legend(loc="lower left")
    # Alphaチャンネル(半透明化)
    leg.get_frame().set_alpha(0.5)
    if not OPT_LDOS and npar > 1:
        ci = 0
        # autumn, bone, cool, copper, flag, gray, hot, hsv, jet, pink,
        # prism, spring, summer, winter, spectral
        for i in OPT_PAIR:
            orgy = orgy + sizey + off
            plt.axes([orgx, orgy, sizex, sizey])
            c = cm.prism(ci * 5)
            par_label = cohp.bond_index[int(i)]
            for s in spin_list:
                if s == 0:
                    spin_label = "up"
                if s == 1:
                    spin_label = "down"
                label = "COHP" + ":" + par_label + " (" + spin_label + ")"
                cohp_pair = cohp.get_cohp(bond=int(i), spin=s)
                plt.plot(cohp_x, -1.0 * cohp_pair, color=c, linewidth=1, label=label)
                plt.locator_params(axis="y", nbins=3)
                plt.axhline(y=0, color="black", linewidth=1)
                plt.axvline(x=0, color="black", linewidth=1)
                plt.xlim(xmax=dos.emax - dos.efermi)
                plt.xlim(xmin=dos.emin - dos.efermi)
                if OPT_EMAX:
                    plt.xlim(xmax=float(OPT_EMAX))
                if OPT_EMIN:
                    plt.xlim(xmin=float(OPT_EMIN))
                if OPT_YMAX:
                    plt.ylim(ymax=float(OPT_YMAX))
                if OPT_YMIN:
                    plt.ylim(ymin=float(OPT_YMIN))
                plt.xticks([])
            # 凡例Box
            leg = plt.legend(fontsize=9)
            if OPT_LEFT:
                leg = plt.legend(loc="lower left")
            # Alphaチャンネル(半透明化)
            leg.get_frame().set_alpha(0.5)
            ci += 1
        plt.ylabel("-pCOHP", fontsize=14)
    # ペア原子ごとのループ
    if OPT_LDOS and npar == 1:
        # ペア原子の情報を入手
        for par in range(len(cohp.bond_par[int(OPT_PAIR[0])])):
            c = cm.prism(par * 20)
            atom_j = cohp.bond_par[int(OPT_PAIR[0])][par]
            atom_index = cohp.bond_par_index[int(OPT_PAIR[0])][par]
            atom_label = atom_index + str(atom_j)
            orb = 0
            for l in orbit_list:
                orgy = orgy + sizey + off
                plt.axes([orgx, orgy, sizex, sizey])
                # ペア原子の元素名と通しの番号をゲット
                for s in spin_list:
                    if s == 0:
                        spin_label = "up"
                    if s == 1:
                        spin_label = "down"
                    atomj = int(atom_j) - 1
                    label = atom_label + "(" + orbit_index[orb] + ")" + "-" + spin_label
                    ldos_y = dos.get_ldos(l=l, atom=atomj, spin=s)
                    plt.plot(dos_x, ldos_y, color=c, linewidth=1, label=label)
                    plt.axvline(x=0, color="black", linewidth=1)
                    plt.locator_params(axis="y", nbins=3)
                plt.ylim(ymin=0)
                plt.xlim(xmax=dos.emax - dos.efermi)
                plt.xlim(xmin=dos.emin - dos.efermi)
                if OPT_DMAX:
                    plt.ylim(ymax=float(OPT_DMAX))
                if OPT_EMAX:
                    plt.xlim(xmax=float(OPT_EMAX))
                if OPT_EMIN:
                    plt.xlim(xmin=float(OPT_EMIN))
                plt.xticks([])
                orb += 1
                # 凡例Box
                leg = plt.legend(fontsize=9)
                if OPT_LEFT:
                    leg = plt.legend(loc="lower left")
                # Alphaチャンネル(半透明化)
                leg.get_frame().set_alpha(0.5)
    if OPT_PAIR:
        if len(OPT_PAIR) > 1:
            plt.savefig("COHP_pair" + "_" + foot + ".eps")
            plt.savefig("COHP_pair" + "_" + foot + ".pdf")
            plt.savefig("COHP_pair" + "_" + foot + ".png")
        else:
            plt.savefig("COHP_p" + str(OPT_PAIR[0]) + "_" + foot + ".eps")
            plt.savefig("COHP_p" + str(OPT_PAIR[0]) + "_" + foot + ".pdf")
            plt.savefig("COHP_p" + str(OPT_PAIR[0]) + "_" + foot + ".png")
    else:
        plt.savefig("COHP" + "_" + foot + ".eps")
        plt.savefig("COHP" + "_" + foot + ".pdf")
        plt.savefig("COHP" + "_" + foot + ".png")
    if not NO_WINDOW_FLAG:
        plt.show()
    plt.close("all")
