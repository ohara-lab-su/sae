#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# MXplot_ADOS.py
#      Vplot_ADOS.py (2015.02.25ベース)
#
#   原子の種類ごとのオービタル足しあわせ LDOS + TODOS 出力
#
#
################################################################################
#
# 2015.03.02
#  Gaussian スメアリングの時のモードを追加
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
#  startup
#  MXplot_ADOS.py
#
# -------------------------------- Vplot_ADOS.py (2015.02.25)
# 2015.01.29
#    Y軸(DOS軸) の下限の設定のバグを修正
#
# 2015.01.14
#      SPIN対応,option XMAX,XMIN,YMAX 対応
#
# 2015.01.14
#      元素名判別＆ラベルの自動出力
#
# 2015.01.13
#      とりあえず完成
#      色設定の自動化
#      むしろ、ReadDoscar, ReadOutcar を中心に修正・改良
#
# 2015.01.11 (sun) startup
#      原子種ごとのs成分,p成分,d成分をsumしたものを TDOS と一緒にプロット
#      非スピン版
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

    name = 'openmx'  # input data name
    suffix_tdos = '.DOS.Tetrahedron'
    suffix_pdos = '.PDOS.Tetrahedron'
    suffix_tdos_g = '.DOS.Gaussian'
    suffix_pdos_g = '.PDOS.Gaussian'

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT', default=name,)
    parser.add_option( '-d', '--dat', dest='DATFILE',)
    parser.add_option( '-n', '--nw', action='store_true', default=False,)
    parser.add_option( '-g', '--gaussian', action='store_true', default=False,)
    parser.add_option(  '--emax', dest='EMAX',)
    parser.add_option(  '--emin', dest='EMIN',)
    parser.add_option(  '--ymax', dest='YMAX',)
    options,  args = parser.parse_args()

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

    return [options.INPUT, options.DATFILE,\
            suffix_tdos, suffix_pdos,\
            options.nw,options.EMAX,options.EMIN,options.YMAX]

################################################################################
if __name__ == '__main__':

    # set input file
    name,datname,suffix_tdos,suffix_pdos,\
            NO_WINDOW_FLAG,\
            OPT_EMAX,OPT_EMIN,OPT_YMAX= options()

    if OPT_EMAX: print "Emax=",OPT_EMAX
    if OPT_EMIN: print "Emin=",OPT_EMIN
    if OPT_YMAX: print "Ymax=",OPT_YMAX

    # set output device
    out = sys.stdout

    # makes instance ( Read *.out or *.dat )
    module_name = 'StructureAnalysisEnvironment'
    FLAG_DATFILE=False
    if os.path.exists(datname+'.out') or os.path.exists(datname+'.out'+'.gz'):
        class_name = 'ReadMxOut'
        datname = datname+'.out'
    elif os.path.exists(datname+'.dat') or os.path.exists(datname+'.dat'+'.gz'):
        class_name = 'ReadMxDat'
        datname = datname+'.dat'
    else:
        sys.exit("STOP: "+datname+'.dat or .dat.gz file not found')

    module = __import__(module_name,globals(),locals(),[class_name],-1)
    klass = getattr(module,class_name)

    dat = klass(datname)
    NION = dat.get_nion()
    NSPIN = dat.get_ispin()
    NATOM = dat.get_natom()
    TITLE =  dat.get_title()
    EFERMI = 0.0
    atoms = dat.get_atoms_index()

    # makes instance ( Read DOS.Tetrahedron )
    tdos = SAE.ReadMxTdos(name,suffix_tdos)

    EMAX = tdos.get_emax()
    EMIN = tdos.get_emin()
    NEDOS = tdos.get_nedos()
    ENG = tdos.get_eng()

    # makes instance ( Read PDOS.Tetrahedron )
    pdos = SAE.ReadMxPdos(name,suffix_pdos)

    ############################################################################
    # matplotlib

#   plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size']         = 20  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize']   = 18  # レジェンドのフォントサイズ
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

        INTTDOS = tdos.get_inttdos(spin)
        TDOS = tdos.get_tdos(spin)
    #   plt.plot(ENG-EFERMI,TDOS, color="black", linewidth=2, label='total')
        plt.fill_between(ENG-EFERMI,TDOS, color='#cccccc', linewidth=2, label='total')

        j=0
        for ion in range(NION):

            if NSPIN ==1:
                print "ion = ",ion+1,atoms[ion]
            else:
                print "ion(spin) = ",ion+1,"("+str(spin+1)+")",atoms[ion]
            atom = str(atoms[ion])

            # autumn, bone, cool, copper, flag, gray, hot, hsv,
            # jet, pink, prism, spring, summer, winter, spectral

            c = cm.prism(float(j)/(3*NION))
            ADOS = pdos.get_ldos_ion(0,ion,spin)
            plt.plot(ENG-EFERMI,ADOS, linestyle=":", color=c, linewidth=2, label=atom+'-s')
            j += 1

            c = cm.prism(float(j)/(3*NION))
            ADOS = pdos.get_ldos_ion(1,ion,spin)
            plt.plot(ENG-EFERMI,ADOS, linestyle="-", color=c, linewidth=2, label=atom+'-p')
            j += 1

            c = cm.prism(float(j)/(3*NION))
            ADOS = pdos.get_ldos_ion(2,ion,spin)
            plt.plot(ENG-EFERMI,ADOS, linestyle="--", color=c, linewidth=2, label=atom+'-d')
            j += 1

            # Y軸の調整
            plt.ylim( ymin=0 )

        if spin == 0:
            yl = plt.ylabel("DOS/eV", fontsize=20 )

        if OPT_EMAX: plt.xlim( xmax=int(OPT_EMAX) )
        if OPT_EMIN: plt.xlim( xmin=int(OPT_EMIN) )
        if OPT_YMAX: plt.ylim( ymax=int(OPT_YMAX) )

        if NSPIN == 2 :
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

    plt.savefig("ADOS.eps")
    plt.savefig("ADOS.pdf")
    plt.savefig("ADOS.png")

    if not NO_WINDOW_FLAG:
        plt.show()

    plt.close('all')

################################################################################
