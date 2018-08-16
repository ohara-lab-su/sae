#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# MXplot_LDOS.py
#
#   Vplot_LDOS.py (2015.02.25) ベースで作成
#   using ReadMxPdos
#
#   DosMain にて Tetrahedron , PDOS モードによる出力を仮定
#
################################################################################
#
# 2015.03.02
#  Gaussian スメアリングの時のオプション追加
#
# 2015.02.26
#  デフォルトファイル名 or 入力ファイル名が存在しない時には
#  カレントの *.out ファイルを検出して、もしカレントの *.out がひとつのときに
#  デフォルト名を変更する仕組みを導入
#
#  注意) *.out ファイルもしくは *.dat ファイルをキーにしているので
#        これらは必須となる
#        もととも、DOS系のクラスは実質的には *.out or *.dat  は必須
#
# 2015.02.25
#  MXplot_LDOS.py startup
#  Vplot_LDOS.py ベースで MXplot_LDOS.py を作成start
#
#
# ----------------------------- Vplot_LDOS.py (2015.02.25)
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
__version__    = "0.1.0"
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

    name = 'openmx' # input data name
    suffix_tdos = '.DOS.Tetrahedron'
    suffix_pdos = '.PDOS.Tetrahedron'
    suffix_tdos_g = '.DOS.Gaussian'
    suffix_pdos_g = '.PDOS.Gaussian'

    parser = optparse.OptionParser()
    parser.add_option( '-i', '--input', dest='INPUT', default=name,)
    parser.add_option( '-d', '--dat', dest='DATFILE',)
    parser.add_option( '-n', '--nw', action='store_true', default=False,)
    parser.add_option( '-g', '--gaussian', action='store_true', default=False,)
    parser.add_option(  '--emax', dest='EMAX',)
    parser.add_option(  '--emin', dest='EMIN',)
    parser.add_option(  '--ymax', dest='YMAX',)
    options,  args = parser.parse_args()

    plot_atoms=[]
    if len(args) > 0:
        for i in range(0,len(args)):
            plot_atoms.append(int(args[i]))
    else:
        plot_atoms = [1]

    if options.gaussian:
        print "GAUSSIAN MODE"
        suffix_tdos = suffix_tdos_g
        suffix_pdos = suffix_pdos_g

    # 'openmx' より最適なデフォルトファイル名の推定ルーチン
    if not os.path.exists(name+'.out') or not os.path.exists(name+'.out.gz'):
        try:
            options.INPUT = SAE.find_datfile('out')
        except:
            pass
    elif not os.path.exists(name+'.dat') or not os.path.exists(name+'.dat'):
        try:
            options.INPUT = SAE.find_datfile('dat')
        except:
            pass

    if not options.DATFILE:
        options.DATFILE = options.INPUT

    return [options.INPUT,options.DATFILE,suffix_tdos,suffix_pdos,\
            options.nw,\
            options.EMAX,options.EMIN,options.YMAX,plot_atoms]

################################################################################
if __name__ == '__main__':

    # set input file
    name,datname,suffix_tdos,suffix_pdos,NO_WINDOW_FLAG,\
            OPT_EMAX,OPT_EMIN,OPT_YMAX,\
            plot_atoms = options()

    if OPT_EMAX: print "Emax=",OPT_EMAX
    if OPT_EMIN: print "Emin=",OPT_EMIN
    if OPT_YMAX: print "Ymax=",OPT_YMAX

    # ION の種類ではなくて原子種の通し番号で入力
    if len(plot_atoms) > 1:
        print "Plot Atoms:"
        for i in plot_atoms:
            print i,
        print ""

    # set output device
    out = sys.stdout

    # makes instance ( Read PDOS.Tetrahedron )
    pdos = SAE.ReadMxPdos(name,suffix_pdos)

    NSPIN = pdos.get_ispin()
    NATOM = pdos.get_natom()
    TITLE =  pdos.get_title()
    EFERMI = 0.0


    # makes instance ( Read DOS.Tetrahedron )
    tdos = SAE.ReadMxTdos(name,suffix_tdos)
    EMAX = tdos.get_emax()
    EMIN = tdos.get_emin()
    NEDOS = tdos.get_nedos()
    ENG = tdos.get_eng()

    # makes instance ( Read *.out or *.dat )
    module_name = 'StructureAnalysisEnvironment'
    FLAG_DATFILE=False
    if os.path.exists(datname+'.out') or os.path.exists(datname+'.out'+'.gz'):
        class_name = 'ReadMxOut'
        datname = datname+'.out'
        FLAG_DATFILE=True
    elif os.path.exists(datname+'.dat') or os.path.exists(datname+'.dat'+'.gz'):
        class_name = 'ReadMxDat'
        datname = datname+'.dat'
        FLAG_DATFILE=True

    if FLAG_DATFILE:
        module = __import__(module_name,globals(),locals(),[class_name],-1)
        klass = getattr(module,class_name)

        dat = klass(datname)
        NION = dat.get_nion()
        atoms = dat.get_atoms_index()
        atoms_j = dat.get_atoms_j()
#       for atom in range(NATOM):
#           print atom,atoms_j[atom], atoms[atoms_j[atom]]
#       print ""


    ############################################################################
    # matplotlib

#   plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size']         = 20  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize']   = 10  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']    = 1.5 # 軸の太さを設定。目盛りは変わらない

#   plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)


    ############################################################################
    for spin in range(NSPIN):

        if NSPIN == 1:
            plt.axes([ 0.130,0.130, 0.80,0.80 ])  # 一段組の原点(x,y), 幅(x,y)
            plt.title(TITLE)
        if NSPIN == 2:
            if spin == 0:
                plt.axes([ 0.130,0.530, 0.80,0.40 ])  # 二段組の上側(y幅半分) up-spin
                plt.title(TITLE)
            if spin == 1:
                plt.axes([ 0.130,0.130, 0.80,0.40 ])  # 二段組の下段( down-spin )

        j=0
        for atom in plot_atoms:

            if len(plot_atoms) > 1:
                if atom == 0:
                    sys.exit("STOP:INPUT ERROR, atom= 0")
            atom -= 1

            if FLAG_DATFILE:
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

            INTTDOS = tdos.get_inttdos(spin)
            TDOS = tdos.get_tdos(spin)
#           plt.plot(ENG-EFERMI,TDOS, color="black", linewidth=2, label='total')
            plt.fill_between(ENG-EFERMI,TDOS, color='#cccccc', linewidth=2, label='total')

            # autumn, bone, cool, copper, flag, gray, hot, hsv,
            # jet, pink, prism, spring, summer, winter, spectral

            c = cm.prism(float(j)/(NATOM*3))
            LDOS = pdos.get_ldos(0,atom,spin)
            plt.plot(ENG-EFERMI,LDOS, linestyle=":", color=c, linewidth=2, label=atom_label+'-s')
            j += 1

            c = cm.prism(float(j)/(NATOM*3))
            LDOS = pdos.get_ldos(1,atom,spin)
            plt.plot(ENG-EFERMI,LDOS, linestyle="-", color=c, linewidth=2, label=atom_label+'-p')
            j += 1

            c = cm.prism(float(j)/(NATOM*3))
            LDOS = pdos.get_ldos(2,atom,spin)
            plt.plot(ENG-EFERMI,LDOS, linestyle="--", color=c, linewidth=2, label=atom_label+'-d')
            j += 1

            # Y軸の調整
            plt.ylim( ymin=0 )

        if spin == 0:
            yl = plt.ylabel("DOS/eV", fontsize=20 )

        if OPT_EMAX: plt.xlim( xmax=int(OPT_EMAX) )
        if OPT_EMIN: plt.xlim( xmin=int(OPT_EMIN) )
        if OPT_YMAX: plt.ylim( ymax=int(OPT_YMAX) )

        if NSPIN == 2:
            if spin == 0:
                plt.xticks([])
            if spin == 1:
                # y 軸反転
                xmin,xmax,ymin,ymax = plt.axis()
                plt.ylim([ymax,0])

        # EF0
        plt.axvline(x=0,color="black",linewidth=1)

    ############################################################################

    plt.xlabel("$E -  E_{\mathrm{F}}$ [eV]", fontsize=20 )

    leg = plt.legend(fontsize=12)   # 凡例Box
    leg.get_frame().set_alpha(0.5)  # Alphaチャンネル(半透明化)

#   plt.xlim([-10,10])
#   plt.ylim([0,200])

    plt.savefig("LDOS.eps")
    plt.savefig("LDOS.pdf")
    plt.savefig("LDOS.png")

    if not NO_WINDOW_FLAG:
        plt.show()

    plt.close('all')

################################################################################
