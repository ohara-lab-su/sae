#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# MXplot_ADOS_portrait.py
#   Vplot_ADOS_portrait.py
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
# 2015.02.26
#  デフォルトファイル名 or 入力ファイル名が存在しない時には
#  カレントの *.out ファイルを検出して、もしカレントの *.out がひとつのときに
#  デフォルト名を変更する仕組みを導入
#
#  注意) *.out ファイルもしくは *.dat ファイルをキーにしているので
#        これらは必須となる
#        もととも、DOS系のクラスは実質的には *.out or *.dat  は必須
#
# 2015.02.26
#  [startup]
#  MXplot_ADOS_portrait.py
#
# ----------------------------------- Vplot_ADOS_portrait.py
# 2015.01.15 startup
#      landscape モードを追加
#
# 2015.01.15 startup
#      Vplot_ADOS.py の再設計(複数画面化)
#      非SPIN版,完成
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
__version__    = "0.0.1"
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
#import matplotlib.cm as cm
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
    parser.add_option( '-l', '--landscape',
                      action='store_true',
                      default=False,
                      dest='LANDSCAPE',
    )
    parser.add_option( '-g', '--gaussian',
                      action='store_true',
                      default=False,
    )
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
            options.nw,options.LANDSCAPE,\
            options.EMAX,options.EMIN,options.YMAX]

################################################################################
if __name__ == '__main__':

    # set input file
    name,datname,suffix_tdos,suffix_pdos,\
            NO_WINDOW_FLAG,LANDSCAPE_FLAG,\
            OPT_EMAX,OPT_EMIN,OPT_YMAX= options()

    TDOS_FLAG=True

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

    plt.rcParams['font.family']     = 'Times New Roman'
    plt.rcParams['font.size']       = 16  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize'] = 14  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']  = 1.5 # 軸の太さを設定。目盛りは変わらない

    if not LANDSCAPE_FLAG:
#       plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)
#       plt.figure(figsize=(8.27, 11.69)) # for portrait
        plt.figure(figsize=(7.00, 9.89))  # for portrait

    ############################################################################

    orgx = 0.130
    orgy = 0.080

    off = 0.015
    size = 0.83/NION/NSPIN

    for ion in range(NION):
        # spin を逆から回す(先に描いものが下側に描画されるので)
        for spin in range(NSPIN-1,-1,-1):

            if NSPIN == 1:
                print "ion = ",ion+1,atoms[ion]
            else:
                print "ion(spin) = ",ion+1,"("+str(spin+1)+")",atoms[ion]

            atom = str(atoms[ion])

            ########################################################################
            plt.axes([ orgx,orgy, 0.80, size ])

            # 原点位置を自動調整
            if NSPIN == 1:
                orgy=orgy+size+off
            if NSPIN == 2:
                if spin == 0:
                    orgy=orgy+size+off
                if spin == 1:
                    orgy=orgy+size

            if TDOS_FLAG:
                TDOS = tdos.get_tdos(spin)
                plt.fill_between(ENG-EFERMI,TDOS, color='#cccccc', linewidth=2, label='total')

            c = "red"
            ADOS = pdos.get_ldos_ion(0,ion,spin)
            plt.plot(ENG-EFERMI,ADOS, linestyle=":", color=c, linewidth=2, label=atom+'-s')

            c = "green"
            ADOS = pdos.get_ldos_ion(1,ion,spin)
            plt.plot(ENG-EFERMI,ADOS, linestyle="-", color=c, linewidth=2, label=atom+'-p')

            c = "blue"
            ADOS = pdos.get_ldos_ion(2,ion,spin)
            plt.plot(ENG-EFERMI,ADOS, linestyle="--", color=c, linewidth=2, label=atom+'-d')

            ########################################################################

            # DOSのY軸(DOS軸)原点をセットする(稀に必須)
            if NSPIN == 1:
                xmin,xmax,ymin,ymax = plt.axis()
                plt.ylim([0,ymax])

            # down spin の時に反転させる
            if NSPIN == 2:
                xmin,xmax,ymin,ymax = plt.axis()
                if spin == 0: plt.ylim([0,ymax])
                if spin == 1: plt.ylim([ymax,0])

            if OPT_EMAX: plt.xlim( xmax=int(OPT_EMAX) )
            if OPT_EMIN: plt.xlim( xmin=int(OPT_EMIN) )
            if OPT_YMAX: plt.ylim( ymax=int(OPT_YMAX) )

            # title,label,xticks
            # 一番上
            if ion == (NION-1) and spin == 0:
               plt.title(TITLE,fontsize=16)

            # 一番下以外
            if ion != 0:
                plt.xticks([])

            # 一番下
            if NSPIN == 1:
                if ion == 0:
                    xl = plt.xlabel("$E -  E_{\mathrm{F}}$ [eV]", fontsize=16 )
                    yl = plt.ylabel("DOS/eV", fontsize=16 )
            if NSPIN == 2:
                if ion == 0 and spin == 0:
                    plt.xticks([])
                if ion == 0 and spin == 1:
                    xl = plt.xlabel("$E -  E_{\mathrm{F}}$ [eV]", fontsize=16 )
                    yl = plt.ylabel("DOS/eV", fontsize=16 )

            # EF0
            plt.axvline(x=0,color="black",linewidth=1)

            # 凡例BOX
            if spin == 0:
                leg = plt.legend(fontsize=12)   # 凡例Box
                leg.get_frame().set_alpha(0.5)  # Alphaチャンネル(半透明化)

    ############################################################################

#   plt.xlim([-10,10])
#   plt.ylim([0,200])

    if LANDSCAPE_FLAG:
        plt.savefig("ADOS.eps")
        plt.savefig("ADOS.pdf")
        plt.savefig("ADOS.png")
    else:
#       plt.savefig("ADOS_portrait.eps",orientation = 'portrait',papertype = 'a4')
        plt.savefig("ADOS_portrait.eps",orientation = 'portrait')
        plt.savefig("ADOS_portrait.pdf",orientation = 'portrait')
        plt.savefig("ADOS_portrait.png",orientation = 'portrait')

    if not NO_WINDOW_FLAG:
        plt.show()

    plt.close('all')

################################################################################
