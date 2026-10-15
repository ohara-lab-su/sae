#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.vasp.doscar import ReadVaspDoscar
from sae.vasp.eigenval import ReadVaspEigenval
from sae.vasp.kpoints import ReadVaspKpoints
from sae.vasp.symdat import ReadVaspSymdat

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vplot_band.py
#
#  vplot_band.pl モドキ(習作)
#
#  オプション指定により vplot_band.pl, vplot_band_index.pl, vplot_band_both.pl
#  の機能を'ほぼ'全て兼ねる
#
#   リフレクションを使っているので python2/3 に注意
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.01.29
#  DOS と一緒に表示する
#   nonmag ( or spin=1 ) のみ対応
#   ゴリ押しで実装
#   ====> この時点でのバージョンを Vplot_band_multi_DOS.py として保存
#
# 2015.01.29
#  sym.dat ファイル( vplot_band.pl 相当 ) 読み込み+symmetry line 描画ルーチン
#   ====> この時点でのバージョンを Vplot_band_multi.py として保存
#
# 2015.01.28
#  zone の長さ判定(multiplotで表記)
#  Vplot_band_single.py の機能をほぼ再実装
#
# 問題点)
#   1) １つ目のzone の右側の ticks
#   2) zone の重なりの感じが微妙(結局常に線を二重に描いている)
#
# 2015.01.28 restart
#   multi-plot 方式での開発を停止して Vplot_band_single.py
#   (single plot 方式)でひと通り開発したので、もういちど
#   mutiplot 形式へ復帰(ゾーンの長さ変更機能を手にするために)
#
# 2015.01.28 stop
#  mutiplot 軽しいの開発を一旦停止
#
# 2015.01.27 startup
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
m_mmail__ = "kmngo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import optparse
import numpy as np
import matplotlib.pyplot as plt


#
################################################################################
#import gzip
#import re
#from copy import deepcopy
#import SpaceGroupEnvironment as SGE
################################################################################
# 必須ファイル(vasprun.xml に置き換え可能)
# オプション入力ファイル
###########################################
# INPUT files
###########################################
# FLAGS
###########################################
# Parameters
def options():
    # get Kと固有値
    eigenname = "EIGENVAL"
    # get 逆格子ベクトル(class ReadKpointsから読む)
    outcarname = "OUTCAR"
    # get 入力したゾーン情報
    kpointsname = "KPOINTS"
    # EF取得(もし無いときはOUTCARから読む)
    doscarname = "DOSCAR"
    # 対称軸の名前(ファイルの有無で動作変更)
    symdatname = "sym.dat"
    out1 = "band1.dat"
    out2 = "band2.dat"
    parser = optparse.OptionParser()
    parser.add_option("-e", "--eigenval", dest="EIGENVAL", default=eigenname)
    parser.add_option("-o", "--outcar", dest="OUTCAR", default=outcarname)
    parser.add_option("-k", "--kpoints", dest="KPOINTS", default=kpointsname)
    parser.add_option("-d", "--doscar", dest="DOSCAR", default=doscarname)
    parser.add_option("-s", "--symdat", dest="SYMDAT", default=symdatname)
    parser.add_option(
        "-a", "--absolute", action="store_true", default=False, dest="ABS_FLAG"
    )
    parser.add_option(
        "-1", "--up", action="store_true", default=False, dest="UP_SPIN_FLAG"
    )
    parser.add_option(
        "-2", "--down", action="store_true", default=False, dest="DOWN_SPIN_FLAG"
    )
    parser.add_option(
        "-i", "--index", action="store_true", default=False, dest="INDEX_FLAG"
    )
    # 禁断の line つなぎ
    parser.add_option(
        "-l", "--line", action="store_true", default=False, dest="LINE_FLAG"
    )
    # DOS と一緒に出力
    parser.add_option(
        "-w", "--withdos", action="store_true", default=False, dest="DOS_FLAG"
    )
    parser.add_option("--emin", dest="EMIN")
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--band", dest="BAND")
    options, args = parser.parse_args()
    if options.EIGENVAL:
        eigenname = options.EIGENVAL
    if options.OUTCAR:
        outcarname = options.OUTCAR
    if options.KPOINTS:
        kpointsname = options.KPOINTS
    if options.DOSCAR:
        doscarname = options.DOSCAR
    if options.SYMDAT:
        symdatname = options.SYMDAT
    return [
        eigenname,
        outcarname,
        kpointsname,
        doscarname,
        symdatname,
        out1,
        out2,
        options.ABS_FLAG,
        options.UP_SPIN_FLAG,
        options.DOWN_SPIN_FLAG,
        options.INDEX_FLAG,
        options.LINE_FLAG,
        options.DOS_FLAG,
        options.EMIN,
        options.EMAX,
        options.BAND,
    ]


################################################################################
# 基本インスタンス生成
# バンドの基本情報取得
# K点&バンドごとの固有値(本丸データ)
# K点のゾーン情報
# データーのチェック
############################################################################
# E-fermi は DOSCAR から取得する(DOSCARがない場合はOUTCARから)
# K点情報はバンドの計算のOUTCARが必須
# E-fermi情報は SCF 計算の DOSCAR(E-fermi が欲しい)
#
############################################################################
# sym.dat ファイルをゲットする(K点の自動処理をする前の暫定措置)
############################################################################
# KPOINTS print
############################################################################
# 最大の固有値と最小の固有値をゲット
# multi-plot する zone 共通のデフォルト ymin,ymax を作成する
############################################################################
# matplotlib
#   plt.rcParams['font.family']       = 'Times New Roman'
############################################################################
# DOS plot
############################################################################
#   plt.subplot(1,num_kpoints_line,1)
#   plt.subplot(1,num_kpoints_line,3)
#   for i in range(num_kpoints_line):
#       print vector[i]
#       plt.subplot(1,num_kpoints_line,i)
#   ax3 = fig.add_subplot(1,num_kpoints_line,3, sharey=ax1)
#   plt.subplots_adjust(wspace=0)
#   plt.subplots_adjust(hspace=0)
if __name__ == "__main__":
    (
        eigenname,
        outcarname,
        kpointsname,
        doscarname,
        symdatname,
        out1,
        out2,
        ABS_FLAG,
        UP_FLAG,
        DOWN_FLAG,
        INDEX_FLAG,
        LINE_FLAG,
        DOS_FLAG,
        OPT_EMIN,
        OPT_EMAX,
        OPT_BAND,
    ) = options()
    print("EIGENVAL   : %s" % str(eigenname))
    print("OUTCAR     : %s" % str(outcarname))
    print("KPOINTS    : %s" % str(kpointsname))
    print("DOSCAR     : %s" % str(doscarname))
    if OPT_EMIN:
        print("EMIN       : %s" % str(OPT_EMIN))
    if OPT_EMAX:
        print("EMAX       : %s" % str(OPT_EMAX))
    if UP_FLAG:
        print("UP_SPIN    : %s" % str(UP_FLAG))
    if DOWN_FLAG:
        print("DOWN_FLAG  : %s" % str(DOWN_FLAG))
    if OPT_BAND:
        print("BAND       : %s" % str(OPT_BAND))
    if DOS_FLAG:
        print("WRITE DOS  : %s" % str(DOS_FLAG))
    band = ReadVaspEigenval(eigenname)
    kpoints = ReadVaspKpoints(kpointsname)
    NATOM = band.get_natom()
    TITLE = band.get_title()
    NKPTS = band.get_nkpts()
    NBANDS = band.get_nbands()
    NSPIN = band.get_ispin()
    # eigenval(NBANDS,NKPTS,NSPIN)
    eigenval = band.get_eigenval()
    kpoints_array = kpoints.get_kpoints_array()
    num_kpoints_line = kpoints.get_num_kpoints_line()
    div_kpoints_line = kpoints.get_div_kpoints_line()
    # OUTCAR
    zone_ratio = kpoints.get_kpoints_vector_ratio(outcarname)
    flags = kpoints.get_kpoints_mode()
    if flags[0]:
        sys.exit("STOP: KPOINTS file format error")
    if not flags[1]:
        sys.exit("STOP: KPOINTS file format error")
    if num_kpoints_line != NKPTS / div_kpoints_line:
        print("STOP: KPONTS lines = %s" % str(num_kpoints_line))
        sys.exit("STOP: NKPTS inconsistence")
    # module の動的ロード
    # class の動的ロード
    if not DOS_FLAG:
        if os.path.exists(doscarname) or os.path.exists(doscarname + ".gz"):
            class_name = "ReadVaspDoscar"
            optname = doscarname
            print("EFERMI(DOS):", end="")
        else:
            class_name = "ReadVaspOutcar"
            optname = outcarname
            print("EFERMI(OUT):", end="")
        module_name = "sae._class_registry"
        # このリフレクションは python2 方式なので注意
        # for Python3
        try:
            module = __import__(module_name, globals(), locals(), [class_name], 0)
        except:
            module = __import__(module_name, fromlist=[class_name])
        klass = getattr(module, class_name)
        efermifile = klass(optname)
        efermi = efermifile.get_efermi()
        print(efermi)
    else:
        dos = ReadVaspDoscar(doscarname)
        efermi = dos.get_efermi()
        print("EFERMI(DOS):", end="")
        print(efermi)
    SYMDAT_FLAG = False
    if os.path.exists(symdatname) or os.path.exists(symdatname + ".gz"):
        print("SYM.DAT    : %s" % str(symdatname))
        sym = ReadVaspSymdat(symdatname)
        num_symlines = sym.get_num_symlines()
        symlines = sym.get_symlines()
        for i in range(num_symlines):
            print("  ", symlines[i])
        if num_kpoints_line != num_symlines - 1:
            print("STOP: KPONTS lines =", num_kpoints_line)
            sys.exit("STOP: sym.dat inconsistence")
        SYMDAT_FLAG = True
    print("KPOINTS")
    for i in range(len(kpoints_array)):
        print(
            " %10.7f %10.7f %10.7f "
            % (kpoints_array[i, 0], kpoints_array[i, 1], kpoints_array[i, 2])
        )
        if not i % 2 == 0:
            print("")
    for i in range(int(num_kpoints_line)):
        print(" line %d : %10.7f " % (i, zone_ratio[i]))
    eigen_min, eigen_max = band.get_max_eigenval()
    delta = (eigen_max - eigen_min) / 20
    if ABS_FLAG:
        eigen_max = eigen_max + delta
        eigen_min = eigen_min - delta
    else:
        eigen_max = eigen_max + delta - efermi
        eigen_min = eigen_min - delta - efermi
    # ラベル等のフォントサイズ
    plt.rcParams["font.size"] = 14
    # レジェンドのフォントサイズ
    plt.rcParams["legend.fontsize"] = 5
    # 軸の太さを設定。目盛りは変わらない
    plt.rcParams["axes.linewidth"] = 1.5
    orgx = 0.13
    orgy = 0.11
    sizey = 0.8
    sizex0 = 0.8
    sizex_dos = 0.2
    if DOS_FLAG:
        sizex0 = sizex0 - sizex_dos
    ymin0 = 0
    ymax0 = 0
    if NSPIN == 2:
        istart = 0
        iend = 2
        title = TITLE + " both-spin"
    if NSPIN == 1:
        istart = 0
        iend = 1
        title = TITLE + " nonmag"
    if UP_FLAG:
        istart = 0
        iend = 1
        title = TITLE + " majority-spin"
    if DOWN_FLAG:
        istart = 1
        iend = 2
        title = TITLE + " minority-spin"
    if OPT_BAND:
        title = title + "  band= " + str(OPT_BAND)
    # multi plot の原点と軸の修正
    # X 軸の作成(lines数)
    # X軸のticks (gnuplot形式のsym.dat を TeX 形式へ変更
    # Y軸のticks
    # バンドの重ね書きプロット
    ## ispin/band-loop ##
    # X幅の調整
    # Fermi-Level
    for i in range(int(num_kpoints_line)):
        sizex = zone_ratio[i] * sizex0
        plt.axes([orgx, orgy, sizex, sizey])
        orgx = orgx + sizex
        X = np.zeros(div_kpoints_line)
        # (0) 〜 (div_kpoints_line)
        for j in range(div_kpoints_line):
            X[j] = j
        if SYMDAT_FLAG:
            if i != num_kpoints_line - 1:
                if "{/Symbol G}" == symlines[i]:
                    # gnuplot 形式から TeX形式へ
                    symlines[i] = "\\Gamma"
                # TeX 出力形式へ
                sym = "$" + str(symlines[i]) + "$"
                plt.xticks([0], [sym])
            if i == num_kpoints_line - 1:
                if "{/Symbol G}" == symlines[i]:
                    # gnuplot 形式から TeX形式へ
                    symlines[i] = "\\Gamma"
                if "{/Symbol G}" == symlines[i + 1]:
                    # gnuplot 形式から TeX形式へ
                    symlines[i + 1] = "\\Gamma"
                # TeX 出力形式へ
                sym0 = "$" + str(symlines[i]) + "$"
                # TeX 出力形式へ
                sym1 = "$" + str(symlines[i + 1]) + "$"
                plt.xticks([0, div_kpoints_line - 1], (sym0, sym1))
        if i != 0:
            plt.yticks([])
        if i == 0:
            plt.title(title)
            plt.ylabel("$E - E_{\\mathrm{F}}$ [eV]", fontsize=16)
        for ispin in range(istart, iend):
            # Y 軸の作成,eigenval(NBANDS,NKPTS,NSPIN), NKPTS の分割プロット
            # 線の色の調整
            # Y幅の調整
            for iband in range(NBANDS):
                startx = i * div_kpoints_line
                endx = startx + div_kpoints_line - 1
                Y = np.zeros(div_kpoints_line)
                k = 0
                for j in range(startx, endx):
                    if ABS_FLAG:
                        Y[k] = eigenval[iband, j, ispin]
                    else:
                        Y[k] = eigenval[iband, j, ispin] - efermi
                    k += 1
                alpha = 1
                if ispin == 0:
                    c = "black"
                else:
                    c = "red"
                if OPT_BAND:
                    c = "black"
                    alpha = 0.2
                    if iband == int(OPT_BAND):
                        c = "red"
                        alpha = 1
                if INDEX_FLAG:
                    plt.plot(X, Y)
                elif not LINE_FLAG:
                    plt.plot(
                        X,
                        Y,
                        color=c,
                        linestyle="None",
                        marker="o",
                        markersize=2,
                        markeredgecolor=c,
                        markerfacecolor="None",
                        alpha=alpha,
                    )
                else:
                    plt.plot(X, Y, color=c)
                plt.ylim(ymin=eigen_min, ymax=eigen_max)
                if OPT_EMIN:
                    plt.ylim(ymin=float(OPT_EMIN))
                if OPT_EMAX:
                    plt.ylim(ymax=float(OPT_EMAX))
        plt.xlim(xmin=0, xmax=div_kpoints_line - 1)
        if ABS_FLAG:
            plt.axhline(y=efermi, color="blue")
        else:
            plt.axhline(y=0, color="blue")
    if DOS_FLAG:
        # スピンの有無と SPIN_FLAG による位置修正
        # 目盛の調整
        #      #    plt.xticks(range(1,4))
        #           plt.xticks([])
        # X軸の調整
        # Y幅の調整(DOS)
        # Fermi-Level
        for ispin in range(istart, iend):
            if NSPIN == 2:
                if UP_FLAG or DOWN_FLAG:
                    sizex_dos1 = sizex_dos
                else:
                    sizex_dos1 = sizex_dos / 2
            else:
                sizex_dos1 = sizex_dos
            plt.axes([orgx, orgy, sizex_dos1, sizey])
            if UP_FLAG or DOWN_FLAG:
                pass
            else:
                orgx = orgx + sizex_dos1
            ENG = dos.get_eng()
            TDOS = dos.get_tdos(ispin)
            c = "#cccccc"
            if UP_FLAG or DOWN_FLAG:
                plt.fill_between(TDOS, ENG - efermi, color=c, linewidth=2)
            else:
                if ispin == 0:
                    lc = "black"
                if ispin == 1:
                    lc = "red"
                plt.fill_between(TDOS, ENG - efermi, color=lc, facecolor=c, linewidth=2)
            plt.yticks([])
            plt.xlim(xmin=0)
            plt.ylim(ymin=eigen_min, ymax=eigen_max)
            if OPT_EMIN:
                plt.ylim(ymin=float(OPT_EMIN))
            if OPT_EMAX:
                plt.ylim(ymax=float(OPT_EMAX))
            if ABS_FLAG:
                plt.axhline(y=efermi, color="blue")
            else:
                plt.axhline(y=0, color="blue")
    plt.savefig("ek_band.eps")
    plt.savefig("ek_band.pdf")
    plt.savefig("ek_band.png")
    plt.show()
    plt.close("all")
