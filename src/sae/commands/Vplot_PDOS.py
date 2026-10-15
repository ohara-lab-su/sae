#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.vasp.doscar import ReadVaspDoscar
from sae.vasp.orbitals import VaspOrbitals
from sae.vasp.outcar import ReadVaspOutcar

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vplot_PDOS_sym.py ---> Vplot_PDOS.py (名前変更)
#
#   拙作シェルスクリプト版 vplo_PDOS* ほぼすべての
#   機能を有するまとめプログラム(オプションで制御)
#
#   atom は 1 番から(内部的には0番からなので内部的に変換する)
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.09.08
#  Pd_pv などの擬ポテンシャルが入るときに一部機能の確保に失敗(バグ発見)
#
# 2015.01.15
#   旧バージョンを Vplot_PDOS_OLD_20150115.py として BACKUP へ
#   現場ジョンを Vplot_PDOS_sym.py から Vplot_PDOS.py へ
#
# 2015.01.15
#   cubic モード, hexagonal モードを追加
#   対称性自動判別
#   sp軌道 or spd軌道 モード
#   --> コードの全面改修(作り直し),前のコードの面影がない
#   --> コードをブランチ
#
# 2015.01.15
#   デフォルト動作を portrait にして landscape モードとオプションで
#   切り替え可能にした。
#
# 2015.01.14
#   SPIN 対応
#
# 2015.01.14 startup
#    Vplot_PDOS.py から Vplod_PDOS.py がベース
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
#  atom は 1 番から(内部的には0番からなので内部的に変換する)
# title
# efermi を 0 ではなく efermi 近傍のDOSからVBMを探してそこをEF0 とする
# efermi を 0 ではなく shift した値を使う
# landscape モード切替
# legend の　right と left の切り替え
# EF0 のラインを消す
# pdf,png,eps出力をonにする( default では pdf のみ)
def options():
    dname = "DOSCAR"
    oname = "OUTCAR"
    parser = optparse.OptionParser()
    parser.add_option("-d", "--doscar", dest="DOSCAR")
    parser.add_option("-o", "--outcar", dest="OUTCAR")
    parser.add_option("--auto", action="store_true", default=False)
    parser.add_option("--hexagonal", action="store_true", default=False)
    parser.add_option("--cubic", action="store_true", default=False)
    parser.add_option("--sp", action="store_true", default=False)
    parser.add_option("--spd", action="store_true", default=False)
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--emin", dest="EMIN")
    parser.add_option("--ymax", dest="YMAX")
    parser.add_option("--atom", dest="ATOM")
    parser.add_option("--title")
    parser.add_option("--vbm", action="store_true", default=False)
    parser.add_option("--shift")
    parser.add_option("-l", "--landscape", action="store_true", default=False)
    parser.add_option("--left", action="store_true")
    parser.add_option("--noef", action="store_true")
    parser.add_option("--pdf")
    parser.add_option("-n", "--nw", action="store_true", default=False)
    options, args = parser.parse_args()
    if options.DOSCAR:
        dname = options.DOSCAR
    if options.OUTCAR:
        oname = options.OUTCAR
    return [
        dname,
        oname,
        options.auto,
        options.hexagonal,
        options.cubic,
        options.spd,
        options.sp,
        options.EMAX,
        options.EMIN,
        options.YMAX,
        options.ATOM,
        options.title,
        options.vbm,
        options.shift,
        options.landscape,
        options.left,
        options.noef,
        options.pdf,
        options.nw,
    ]


################################################################################
# set input file
# set output device
# makes instance ( Read DOSCAR )
# makes instance ( Read OUTCAR )
############################################################################
# matplotlib
#   plt.rcParams['font.family']       = 'Times New Roman'
#   plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)
############################################################################
# block のリスト
#
#  Ylm : 「real」 spherical harmonics
# l=1
#  m=-1: p_y
#  m= 0: p_z
#  m= 1: p_x
#
# l=2
#  m=-2: d_xy
#  m=-1: d_yz
#  m= 0: d_z2
#  m= 1: d_xz
#  m= 2: d_x2-y2
#
# for s,p,d
# for cubic
# for hexagonal (without s,p )
# for hexagonal (s-orbital and p-orbital MODE)
############################################################################
# block のリスト作成
########################################################################
# 画面分割のブロック
############################################################################
#   plt.xlim([-10,10])
#   plt.ylim([0,200])
if __name__ == "__main__":
    (
        dname,
        oname,
        AUTO_FLAG,
        HEX_FLAG,
        CUBIC_FLAG,
        SPD_FLAG,
        SP_FLAG,
        OPT_EMAX,
        OPT_EMIN,
        OPT_YMAX,
        OPT_ATOM,
        OPT_TITLE,
        FLAG_VBM,
        OPT_SHIFT,
        FLAG_LANDSCAPE,
        FLAG_LEFT,
        FLAG_NOEF,
        FLAG_PDF,
        FLAG_NW,
    ) = options()
    if HEX_FLAG:
        print("Hexagonal MODE")
    elif CUBIC_FLAG:
        print("Cubic MODE")
    elif SPD_FLAG:
        print("SPD(lm=0,1,2,,,,9) MODE")
    elif SP_FLAG:
        print("Selective s-orbital and p-orbital MODE (disable d-orbital plot)")
    elif AUTO_FLAG:
        print("Automatic Symmetry MODE")
    else:
        print("Default (lm=0,1,2,,,,9) MODE")
    if OPT_EMAX:
        print("Emax= %s" % str(OPT_EMAX))
    if OPT_EMIN:
        print("Emin= %s" % str(OPT_EMIN))
    if OPT_YMAX:
        print("Ymax= %s" % str(OPT_YMAX))
    if OPT_ATOM:
        print("ATOM= %s" % str(OPT_ATOM))
        atom = int(OPT_ATOM) - 1
    else:
        atom = 0
    out = sys.stdout
    dos = ReadVaspDoscar(dname)
    NSPIN = dos.get_ispin()
    LORBIT = dos.get_lorbit()
    NATOM = dos.get_natom()
    EMAX = dos.get_emax()
    EMIN = dos.get_emin()
    NEDOS = dos.get_nedos()
    EFERMI = dos.get_efermi()
    if not OPT_TITLE:
        TITLE = dos.get_title()
    else:
        TITLE = str(OPT_TITLE)
    if FLAG_VBM:
        print("EF SHIFT")
        EFERMI0 = dos.efermi
        EFERMI = dos.get_vbm()
        print(EFERMI0, EFERMI)
    if OPT_SHIFT:
        EFERMI = float(OPT_SHIFT)
    if NATOM < atom + 1:
        sys.exit("STOP: NATOM=" + str(NATOM))
    if LORBIT <= 10:
        sys.exit("STOP: LORIBT=" + str(LORBIT))
    if os.path.exists(oname) or os.path.exists(oname + ".gz"):
        FLAG_OUTCAR = True
        outcar = ReadVaspOutcar(oname)
        NION = outcar.get_nion()
        atoms = outcar.get_atoms_index()
        atoms_j = outcar.get_atoms_j()
        point_sym = outcar.get_point_symmetry()
    ENG = dos.get_eng()
    # ラベル等のフォントサイズ
    plt.rcParams["font.size"] = 14
    # レジェンドのフォントサイズ
    plt.rcParams["legend.fontsize"] = 5
    # 軸の太さを設定。目盛りは変わらない
    plt.rcParams["axes.linewidth"] = 1.5
    #       plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)
    #       plt.figure(figsize=(8.27, 11.69)) # for portrait
    if not FLAG_LANDSCAPE:
        # for portrait
        plt.figure(figsize=(7.0, 9.89))
    # 0:s
    list1_1 = [0]
    # 1:p_y, 2:p_z, 3:p_x
    list1_2 = [1, 2, 3]
    # 4:d_xy, 5:d_yz, 6:d_3z2-r2, 7:d_xz, 8:d_x2-y2
    list1_3 = [4, 5, 6, 7, 8]
    list1 = [list1_1, list1_2, list1_3]
    # 0:s
    list2_1 = [0]
    # 1:p_y, 2:p_z, 3:p_x
    list2_2 = [1, 2, 3]
    # 4:d_xy, 5:d_yz, 7:d_zx    (t2g)
    list2_3 = [4, 5, 7]
    # 6:d_3z2-r2, 8:d_x2-y2     (eg)
    list2_4 = [6, 8]
    list2 = [list2_1, list2_2, list2_3, list2_4]
    # 0:s, 1:p_y, 2:p_z, 3:p_x
    list3_1 = [0, 1, 2, 3]
    # 5:d_yz, 7:d_xz
    list3_2 = [5, 7]
    # 4:d_yz, 8:d_x2-y2
    list3_3 = [4, 8]
    # 6:d_3z2-r2
    list3_4 = [6]
    list3 = [list3_1, list3_2, list3_3, list3_4]
    # 0:s
    list4_1 = [0]
    # 2:p_z
    list4_2 = [2]
    # 1:p_y, 3:p_x
    list4_3 = [1, 3]
    list4 = [list4_1, list4_2, list4_3]
    if SP_FLAG:
        block_list = list4
    elif HEX_FLAG:
        block_list = list3
    elif CUBIC_FLAG:
        block_list = list2
    elif SPD_FLAG:
        block_list = list1
    elif AUTO_FLAG and FLAG_OUTCAR:
        point_sym = outcar.get_point_symmetry()
        print("Point Symmetry = %s" % str(point_sym))
        # O_h
        if point_sym[0:1] == "O":
            CUBIC_FLAG = True
            block_list = list2
            print("Cubic MODE")
        # D_3h
        elif point_sym[0:1] == "D":
            HEX_FLAG = True
            block_list = list3
            print("Hexagonal MODE")
        elif point_sym == "D_6h":
            HEX_FLAG = True
            block_list = list3
            print("Hexgonal MODE")
        else:
            block_list = list1
    else:
        block_list = list1
    nblock = len(block_list)
    print("Number of nblock = %s" % str(nblock))
    orgx = 0.13
    orgy = 0.08
    off = 0.015
    size = 0.83 / nblock / NSPIN
    for blk in range(nblock - 1, -1, -1):
        # ラベルの作成
        # 描画軸の作成
        # 次回の描画原点位置の調整
        ####################################################################
        # グラフ描画ブロック
        #           plt.xticks([])
        #           if blk != (nblock-1):
        #               plt.xticks([])
        ####################################################################
        # EF0
        ################################################################
        # DOSのY軸(DOS軸)原点をセットする(稀に必須)
        ################################################################
        # down spin の時に反転させる
        ################################################################
        # title,label,xticks 処理
        # 一番上
        # 一番下以外
        # 一番下
        for spin in range(NSPIN - 1, -1, -1):
            if blk == nblock - 1:
                if FLAG_OUTCAR:
                    atom_label = str(atoms[atoms_j[atom]]) + str(atom + 1)
                    if spin == 1:
                        print("Atom = %d %s" % (atom + 1, str(atom_label)))
                else:
                    atom_label = str(atom)
                    if spin == 1:
                        print("Atom = %d" % atom + 1)
            plt.axes([orgx, orgy, 0.8, size])
            if NSPIN == 1:
                orgy = orgy + size + off
            if NSPIN == 2:
                if spin == 0:
                    orgy = orgy + size + off
                if spin == 1:
                    orgy = orgy + size
            lm_list = block_list[blk]
            for lm in lm_list:
                orbit = VaspOrbitals().get_vasp_orbital_info(lm)
                c = cm.prism(float(lm + 1) / 9)
                PDOS = dos.get_pdos(lm=lm, atom=atom, spin=spin)
                plt.plot(
                    ENG - EFERMI,
                    PDOS,
                    linestyle="-",
                    color=c,
                    linewidth=2,
                    label=str(atom_label) + " " + str(orbit),
                )
            if not FLAG_NOEF:
                plt.axvline(x=0, color="black", linewidth=1)
            if NSPIN == 1:
                xmin, xmax, ymin, ymax = plt.axis()
                plt.ylim([0, ymax])
            if NSPIN == 2:
                xmin, xmax, ymin, ymax = plt.axis()
                if spin == 0:
                    plt.ylim([0, ymax])
                if spin == 1:
                    plt.ylim([ymax, 0])
            if blk == 0 and spin == 0:
                plt.title(TITLE, fontsize=16)
            if blk != nblock - 1:
                plt.xticks([])
            if NSPIN == 1:
                if blk == nblock - 1:
                    xl = plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=16)
                    yl = plt.ylabel("DOS/eV", fontsize=16)
            if NSPIN == 2:
                if blk == nblock - 1 and spin == 0:
                    plt.xticks([])
                if blk == nblock - 1 and spin == 1:
                    xl = plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=16)
                    yl = plt.ylabel("DOS/eV", fontsize=16)
            if OPT_EMAX:
                plt.xlim(xmax=float(OPT_EMAX))
            if OPT_EMIN:
                plt.xlim(xmin=float(OPT_EMIN))
            if OPT_YMAX:
                plt.ylim(ymax=float(OPT_YMAX))
            if spin == 0:
                # 凡例Box
                leg = plt.legend(fontsize=9)
                # Alphaチャンネル(半透明化)
                leg.get_frame().set_alpha(0.5)
    if FLAG_LANDSCAPE:
        plt.savefig("PDOS" + str(atom + 1) + ".pdf")
        if FLAG_PDF:
            plt.savefig("PDOS" + str(atom + 1) + ".eps")
            plt.savefig("PDOS" + str(atom + 1) + ".png")
    else:
        plt.savefig("PDOS" + str(atom + 1) + ".pdf", orientation="portrait")
        if FLAG_PDF:
            plt.savefig("PDOS" + str(atom + 1) + ".eps", orientation="portrait")
            plt.savefig("PDOS" + str(atom + 1) + ".png", orientation="portrait")
    if not FLAG_NW:
        plt.show()
    plt.close("all")
