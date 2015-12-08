#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vplot_LDOS.py
#
#   拙作シェルスクリプト版 vplo_LDOS* モドキ(小文字 vplot 系)
#   python(matplot) 版なのでもう少し一般化されているので Vplot (大文字)版へ
#
#   1) gnuplot の代わりに matplotlib を用いる
#   2) Vldos.py などは用いない
#   3) 内部的には直接 ReadDoscar クラス(ReadDoscar.py)を用いる
#      そもそも ReadDoscar クラスは matplotlib からの利用を念頭に構造化している
#
#   4) 引数処理(局所状態密度の原子選択や、対称性による軌道選択)などは
#      別プログラムで、それぞれ対応になるので、ほぼ vplot_LDOS* シリーズと
#      同じファイル構成になる。
#
################################################################################
#
# 2015.10.28
#    plot する site(atom) の指定をオプションありでも出来るようにした
#    ただし、一つのサイトのみ
#
# 2015.09.11
#    plot の仕方を少し変更
#
# 2015.01.29
#    Y軸(DOS軸) の下限の設定のバグを修正
#
# 2015.01.14
#    SPIN 対応版,option EMAX,EMIN,YMAX 対応
#
# 2015.01.14
#    OUTCAR が存在すれば atom (番号) から原子種情報を引っ張って
#    元素名として記述する
#    色設定の自動化
#
# 2015.01.13
#    引数処理&デフォルト動作を変更
#    1) デフォルト 1 番目の原子の局所状態密度のみプロット(vplot_LDOSシリーズ互換)
#    2) 引数にスペース区切りで連続した数字を与える(数字=原子種番号)
#       そのままその原子種の局所状態密度をプロット
#    注意)
#       引数に数字以外は想定してない
#
# 2015.01.11 (sun) startup
#    基本機能はほぼ完成,まったりと作成
#    非スピン版
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.5"
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
import matplotlib.cm as cm
#import matplotlib.mlab as mlab

################################################################################
def options():

    dname = 'DOSCAR'
    oname = 'OUTCAR'

    parser = optparse.OptionParser()
    parser.add_option('-d','--doscar', dest='DOSCAR', default=dname,)
    parser.add_option('-o', '--outcar', dest='OUTCAR', default=oname,)
    # atom は 1番から(内部的には0番からなので内部的に変換する)
    parser.add_option('-a', '--atom',)
    parser.add_option('--emax', dest='EMAX',)
    parser.add_option('--emin', dest='EMIN',)
    parser.add_option('--ymax', dest='YMAX',)
    # title
    parser.add_option('--title',)
    # total のプロットを 'off' にするスイッチ
    parser.add_option('--total', action='store_true', default=False)
    # efermi を 0 ではなく efermi 近傍のDOSからVBMを探してそこをEF0 とする
    parser.add_option('--vbm', action='store_true', default=False)
    # efermi を 0 ではなく shift した値を使う
    parser.add_option('--shift')
    # legend の right と left の切り替え
    parser.add_option('--left', action='store_true', default=False)
    # EF0 のラインを消す
    parser.add_option('--noef', action='store_true', default=False)
    # pdf,png,eps出力をonにする( default では pdf のみ)
    parser.add_option('--pdf',)
    parser.add_option('-n', '--nw', action='store_true', default=False,)
    options,  args = parser.parse_args()

    if options.DOSCAR: dname=options.DOSCAR
    if options.OUTCAR: oname=options.OUTCAR
    if options.atom: options.atom = int(options.atom)

    plot_atoms=[]
    if len(args) > 0:
        for i in range(0,len(args)):
            plot_atoms.append(int(args[i]))
    else:
        plot_atoms = [1]


    return [dname, oname,
            options.EMAX, options.EMIN, options.YMAX,
            options.title,
            options.atom, plot_atoms,
            options.total,
            options.vbm, options.shift,
            options.left, options.noef, options.pdf, options.nw]

################################################################################
if __name__ == '__main__':

    # set input file
    dname,oname,\
            OPT_EMAX,OPT_EMIN,OPT_YMAX,\
            OPT_TITLE,\
            plot_atom,\
            plot_atoms,\
            FLAG_TOT, \
            FLAG_VBM, OPT_SHIFT, \
            FLAG_LEFT, FLAG_NOEF, FLAG_PDF, FLAG_NW = options()

    if OPT_EMAX: print "Emax=",OPT_EMAX
    if OPT_EMIN: print "Emin=",OPT_EMIN
    if OPT_YMAX: print "Ymax=",OPT_YMAX

    # ION の種類ではなくて原子種の通し番号で入力
    if len(plot_atoms) > 1:
        print "Plot Atoms:"
        for i in plot_atoms:
            print i,
        print ""
    elif plot_atom:
        plot_atoms[0] = plot_atom

    print plot_atoms

    # set output device
    out = sys.stdout

    # makes instance ( Read DOSCAR )
    dos = SAE.ReadVaspDoscar(dname)

    NSPIN = dos.ispin
    LORBIT = dos.lorbit
    NATOM = dos.natom
    EMAX = dos.emax
    EMIN = dos.emin
    NEDOS = dos.nedos
    EFERMI = dos.efermi
    LMAX = dos.lmax

    ENG = dos.eng

    if not OPT_TITLE:
        TITLE =  dos.title
    else:
        TITLE = str(OPT_TITLE)

    if FLAG_VBM:
        EFERMI0 = dos.efermi
        print "SEARCH VBM MODE"
        print "  ORIGINAL EF =",
        print EFERMI0
        EFERMI = dos.get_vbm()
        print "          VBM =", EFERMI

    if OPT_SHIFT:
        print "EF_SHIFT MODE"
        print "     NEW EF ="
        EFERMI = float(OPT_SHIFT)

    # makes instance ( Read OUTCAR )
    if os.path.exists(oname) or os.path.exists(oname+'.gz'):
        FLAG_OUTCAR=True
        outcar = SAE.ReadVaspOutcar(oname)
        NION = outcar.get_nion()
        atoms = outcar.get_atoms_index()
        atoms_j = outcar.get_atoms_j()
#       for atom in range(NATOM):
#           print atom,atoms_j[atom], atoms[atoms_j[atom]]
#       print ""

    ############################################################################
    # matplotlib

#   plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size']         = 18  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize']   = 10  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']    = 1.5 # 軸の太さを設定。目盛りは変わらない

#   plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)

    orgx = 0.130
    orgy = 0.130
    xsize = 0.80
    ysize0 = 0.80
    ysize = 0.80/NSPIN

    if NSPIN == 1:
        spin_list = [0]
    if NSPIN == 2:
        spin_list = [1,0]

    ############################################################################
    for spin in spin_list:

        plt.axes([orgx, orgy, xsize, ysize])

        # makes title & xlabel
        if NSPIN == 1:
            plt.title(TITLE)
            plt.xlabel("$E -  E_{\mathrm{F}}$ [eV]", fontsize=20 )
        if NSPIN == 2 and spin == 0: plt.title(TITLE)
        if NSPIN == 2 and spin == 1:
            plt.xlabel("$E -  E_{\mathrm{F}}$ [eV]", fontsize=20 )

        j=0
        for atom in plot_atoms:

            if len(plot_atoms) > 1:
                if atom == 0:
                    sys.exit("STOP:INPUT ERROR, atom= 0")
            atom -= 1

            # makes label
            if FLAG_OUTCAR:
                atom_label =str(atoms[atoms_j[atom]])+str(atom+1)
                if NSPIN == 1:
                    print "atom =",atom+1,atom_label
                else:
                    print "atom(spin) =",atom+1,"("+str(spin+1)+")",atom_label
            else:
                atom_label =str(atom)
                if NSPIN == 1:
                    print "atom =",atom+1
                else:
                    print "atom(spin) =",atom+1,"("+str(spin+1)+")"

            if not FLAG_TOT:
                INTTDOS = dos.get_inttdos(spin)
                TDOS = dos.get_tdos(spin)
#               plt.plot(ENG-EFERMI,TDOS, color="black", linewidth=2, label='total')
                plt.fill_between(ENG-EFERMI,TDOS, color='#cccccc', linewidth=2, label='total')

            # autumn, bone, cool, copper, flag, gray, hot, hsv,
            # jet, pink, prism, spring, summer, winter, spectral

            c = cm.prism(float(j)/(NATOM*(LMAX+1)))
            LDOS = dos.get_ldos(l='s',atom=atom,spin=spin)
           #plt.plot(ENG-EFERMI,LDOS, linestyle=":", color=c, linewidth=2, label=atom_label+'-s')
            plt.plot(ENG-EFERMI,LDOS, linestyle="-", color=c, linewidth=2, label=atom_label+'-s')
            j += 1

            if LMAX >= 1:
                c = cm.prism(float(j)/(NATOM*(LMAX+1)))
                LDOS = dos.get_ldos(l='p',atom=atom,spin=spin)
                plt.plot(ENG-EFERMI,LDOS, linestyle="-", color=c, linewidth=2, label=atom_label+'-p')
                j += 1

            if LMAX >= 2:
                c = cm.prism(float(j)/(NATOM*(LMAX+1)))
                LDOS = dos.get_ldos(l='d',atom=atom,spin=spin)
               #plt.plot(ENG-EFERMI,LDOS, linestyle="--", color=c, linewidth=2, label=atom_label+'-d')
                plt.plot(ENG-EFERMI,LDOS, linestyle="-", color=c, linewidth=2, label=atom_label+'-d')
                j += 1

            if LMAX >= 3:
                c = cm.prism(float(j)/(NATOM*(LMAX+1)))
                LDOS = dos.get_ldos(l='f',atom=atom,spin=spin)
               #plt.plot(ENG-EFERMI,LDOS, linestyle="-.", color=c, linewidth=2, label=atom_label+'-f')
                plt.plot(ENG-EFERMI,LDOS, linestyle="-", color=c, linewidth=2, label=atom_label+'-f')
                j += 1

            # Y軸の調整
            plt.ylim( ymin=0 )

        if spin == 0: yl = plt.ylabel("DOS/eV", fontsize=20 )

        if OPT_EMAX: plt.xlim( xmax=float(OPT_EMAX) )
        if OPT_EMIN: plt.xlim( xmin=float(OPT_EMIN) )
        if OPT_YMAX: plt.ylim( ymax=float(OPT_YMAX) )

        if NSPIN == 2 and spin == 0:
            plt.xticks([])
        if NSPIN == 2 and spin == 1:
            # y 軸反転
            xmin,xmax,ymin,ymax = plt.axis()
            plt.ylim([ymax,0])

        # EF0
        if not FLAG_NOEF:
            plt.axvline(x=0,color="black",linewidth=1)

        orgy = orgy + ysize


    ############################################################################

    leg = plt.legend(fontsize=12)   # 凡例Box
    if FLAG_LEFT:
        leg = plt.legend(loc='upper left')
    leg.get_frame().set_alpha(0.5)  # Alphaチャンネル(半透明化)

#   plt.xlim([-10,10])
#   plt.ylim([0,200])

    if plot_atom:
        tail = str(plot_atom)
    else:
        tial = ''

    plt.savefig("LDOS"+tial+".pdf")
    if FLAG_PDF:
        plt.savefig("LDOS"+tail+".eps")
        plt.savefig("LDOS"+tail+".png")

    if not FLAG_NW:
        plt.show()

    plt.close('all')

################################################################################
