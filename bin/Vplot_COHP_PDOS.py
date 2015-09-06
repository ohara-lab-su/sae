#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vplot_PDOS.py ---> Vplot_PDOS.py (名前変更)
#
#   Vplot_PDOS.py とほぼ同等
#     DOSCAR の代わりに DOSCAR.lobster を読み込む
#
################################################################################
#
# 2015.09.07
#  自動モードを止めて手動モードのみに(hex,cubic選択)
#  軌道成分の指定部分を直接数字の指定は出来ない（計算ごとに異なる）
#  ため、実際に計算している成分から、たとえば、px のみの番号を取得する
#  などの仕様に変更した。
#  --> それにともなって Vplod_PDOS.py から少しだけ変更
#
# 2015.09.03
#  lobster 版へブランチ
#  ---> いきなり頓挫、lm 分解モードが lobster DOSCAR だと、原子種に依存する
#       そのため対称性分解モードがそのままでは移植できないことに気がつく。
#       ---> auto-mode を停止で対応(デフォルトは full-lm モード)
#
################################################################################
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
#import os
#import gzip
import optparse
#import numpy as np

#import re
#from copy import deepcopy

import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE

import matplotlib.pyplot as plt
import matplotlib.cm as cm
#import matplotlib.mlab as mlab

################################################################################
def options():

    dname = 'DOSCAR.lobster'

    parser = optparse.OptionParser()
    parser.add_option(  '-d','--doscar', dest='DOSCAR',)
    parser.add_option( '-n', '--nw', action='store_true', default=False,)
    parser.add_option( '-l', '--landscape', action='store_true', default=False,)
    parser.add_option( '--hexagonal',
                      action='store_true',
                      default=False,
                      dest='HEX',
    )
    parser.add_option( '--cubic',
                      action='store_true',
                      default=False,
                      dest='CUBIC',
    )
    parser.add_option( '--spd',
                      action='store_true',
                      default=False,
                      dest='SPD',
    )
    parser.add_option( '--sp',
                      action='store_true',
                      default=False,
                      dest='SP',
    )
    parser.add_option(  '--emax', dest='EMAX',)
    parser.add_option(  '--emin', dest='EMIN',)
    parser.add_option(  '--ymax', dest='YMAX',)
    parser.add_option(  '--atom', dest='ATOM',)
    options,  args = parser.parse_args()

    if options.DOSCAR: dname=options.DOSCAR

    return [dname,
            options.nw,options.landscape,
            options.HEX,options.CUBIC,options.SPD,options.SP,
            options.EMAX,options.EMIN,options.YMAX,options.ATOM]

################################################################################
if __name__ == '__main__':

    # set input file
    dname,\
            NO_WINDOW_FLAG,LANDSCAPE_FLAG,\
            HEX_FLAG,CUBIC_FLAG,SPD_FLAG,SP_FLAG,\
            OPT_EMAX,OPT_EMIN,OPT_YMAX,OPT_ATOM = options()

    if HEX_FLAG:
        print "Hexagonal MODE"
    elif CUBIC_FLAG:
        print "Cubic MODE"
    elif SPD_FLAG:
        print "SPD(lm=0,1,2,,,,9) MODE"
    elif SP_FLAG:
        print "Selective s-orbital and p-orbital MODE (disable d-orbital plot)"
    else:
        print "Default (lm=0,1,2,,,,9) MODE"

    if OPT_EMAX: print "Emax=",OPT_EMAX
    if OPT_EMIN: print "Emin=",OPT_EMIN
    if OPT_YMAX: print "Ymax=",OPT_YMAX
    if OPT_ATOM:
        print "ATOM=",OPT_ATOM
        atom=int(OPT_ATOM)-1
    else:
        atom=0

    # set output device
    out = sys.stdout

    # makes instance ( Read DOSCAR )
#   dos = SAEnv.ReadVaspDoscar(dname)
    dos = SAEnv.ReadLobDos(dname)

    NSPIN = dos.ispin
    LORBIT = dos.lorbit
    NATOM = dos.natom
#   TITLE =  dos.title
    TITLE =  'DOSCAR.lobster'
    EMAX = dos.emax
    EMIN = dos.emin
    NEDOS = dos.nedos

    if NATOM <  atom+1:
        sys.exit("STOP: NATOM="+str(NATOM))

    if LORBIT <= 10:
        sys.exit("STOP: LORIBT="+str(LORBIT))

    ENG = dos.eng

    ############################################################################
    # matplotlib

#   plt.rcParams['font.family']       = 'Times New Roman'
    plt.rcParams['font.size']         = 14  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize']   = 5   # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']    = 1.5 # 軸の太さを設定。目盛りは変わらない

#   plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)

    if not LANDSCAPE_FLAG:
#       plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)
#       plt.figure(figsize=(8.27, 11.69)) # for portrait
        plt.figure(figsize=(7.00, 9.89))  # for portrait

    ############################################################################
    # block のリスト

    # for s,p,d
#   list1_1=[0]         # 0:s
#   list1_2=[1,2,3]     # 1:p_y, 2:p_z, 3:p_x
#   list1_3=[4,5,6,7,8] # 4:d_xy, 5:d_yz, 6:d_3z2-r2, 7:d_xz, 8:d_x2-y2
    list1_1=['s']
    list1_2=['p_y','p_z','p_x']
    list1_3=['d_xy','d_yz','d_3z2-r2','d_xz','d_x2-y2']
    list1 = [list1_1,list1_2,list1_3]

    # for cubic
#   list2_1=[0]         # 0:s
#   list2_2=[1,2,3]     # 1:p_y, 2:p_z, 3:p_x
#   list2_3=[4,5,7]     # 4:d_xy, 5:d_yz, 7:d_zx    (t2g)
#   list2_4=[6,8]       # 6:d_3z2-r2, 8:d_x2-y2     (eg)
    list2_1=['s']
    list2_2=['p_y','p_z','p_x']
    list2_3=['d_xy','d_yz','d_zx']
    list2_4=['d_3z2-r2','d_x2-y2']
    list2 = [list2_1,list2_2,list2_3,list2_4]

    # for hexagonal (without s,p )
#   list3_1=[0,1,2,3]   # 0:s, 1:p_y, 2:p_z, 3:p_x
#   list3_2=[5,7]       # 5:d_yz, 7:d_xz
#   list3_3=[4,8]       # 4:d_yz, 8:d_x2-y2
#   list3_4=[6]         # 6:d_3z2-r2
    list3_1=['s','p_y','p_x']
    list3_2=['d_yz','d_xz']
    list3_3=['d_yz','d_x2-y2']
    list3_4=['d_3z2-r2']

    list3 = [list3_1,list3_2,list3_3,list3_4]

    # for hexagonal (s-orbital and p-orbital MODE)
#   list4_1=[0]         # 0:s
#   list4_2=[2]         # 2:p_z
#   list4_3=[1,3]       # 1:p_y, 3:p_x
    list4_1=['s']         # 0:s
    list4_2=['p_z']         # 2:p_z
    list4_3=['p_y','p_x']
    list4 = [list4_1,list4_2,list4_3]

    ############################################################################
    # block のリスト作成

    if SP_FLAG:
        block_list = list4
    elif HEX_FLAG:
        block_list = list3
    elif CUBIC_FLAG:
        block_list = list2
    elif SPD_FLAG:
        block_list = list1
    else:
        block_list = list1

    ########################################################################
    # 画面分割のブロック
    nblock = len(block_list)
    print "Number of nblock = ",nblock

    orgx = 0.130
    orgy = 0.080
    off = 0.015
    size = 0.83/nblock/NSPIN

    for blk in range(nblock-1,-1,-1):
        for spin in range(NSPIN-1,-1,-1):

            # ラベルの作成
            if blk == nblock-1:
                atom_label =str(atom)
                if spin == 1:
                    print "Atom =",atom+1

            # 描画軸の作成
            plt.axes([ orgx,orgy, 0.80, size ])

            # 次回の描画原点位置の調整
            if NSPIN == 1:
                orgy=orgy+size+off
            if NSPIN == 2:
                if spin == 0:
                    orgy = orgy+size+off
                if spin == 1:
                    orgy = orgy+size

            ####################################################################
            # グラフ描画ブロック
            lm_list = block_list[blk]
            ll = 0
            for lm in lm_list:

                c = cm.prism(float(ll+1)/9)
                PDOS = dos.get_pdos(lm=lm,atom=atom,spin=spin)
                plt.plot(ENG, PDOS, linestyle="-", color=c, linewidth=2, \
                        label=str(atom_label)+" "+str(lm))

                ll += 1

#           plt.xticks([])
#           if blk != (nblock-1):
#               plt.xticks([])

            ####################################################################
            # EF0
            plt.axvline(x=0,color="black",linewidth=1)

            ################################################################
            # DOSのY軸(DOS軸)原点をセットする(稀に必須)
            if NSPIN == 1:
                xmin,xmax,ymin,ymax = plt.axis()
                plt.ylim([0,ymax])

            ################################################################
            # down spin の時に反転させる
            if NSPIN == 2:
                xmin,xmax,ymin,ymax = plt.axis()
                if spin == 0:
                    plt.ylim([0,ymax])
                if spin == 1:
                    plt.ylim([ymax,0])

            ################################################################
            # title,label,xticks 処理
            # 一番上
            if blk == 0 and spin == 0:
                plt.title(TITLE,fontsize=16)

            # 一番下以外
            if blk != (nblock -1):
                plt.xticks([])

            # 一番下
            if NSPIN == 1:
                if blk == (nblock -1):
                    xl = plt.xlabel("$E -  E_{\mathrm{F}}$ [eV]", fontsize=16 )
                    yl = plt.ylabel("DOS/eV", fontsize=16)
            if NSPIN == 2:
                if blk == (nblock -1) and spin == 0:
                    plt.xticks([])
                if blk == (nblock -1) and spin == 1:
                    xl = plt.xlabel("$E -  E_{\mathrm{F}}$ [eV]", fontsize=16 )
                    yl = plt.ylabel("DOS/eV", fontsize=16)

            if OPT_EMAX: plt.xlim( xmax=int(OPT_EMAX) )
            if OPT_EMIN: plt.xlim( xmin=int(OPT_EMIN) )
            if OPT_YMAX: plt.ylim( ymax=int(OPT_YMAX) )

            if spin == 0:
                leg = plt.legend(fontsize=9)   # 凡例Box
                leg.get_frame().set_alpha(0.5)  # Alphaチャンネル(半透明化)


    ############################################################################


#   plt.xlim([-10,10])
#   plt.ylim([0,200])

    if LANDSCAPE_FLAG:
        plt.savefig("PDOS"+str(atom+1)+".eps")
        plt.savefig("PDOS"+str(atom+1)+".pdf")
        plt.savefig("PDOS"+str(atom+1)+".png")
    else:
        plt.savefig("PDOS"+str(atom+1)+".eps",orientation = 'portrait')
        plt.savefig("PDOS"+str(atom+1)+".pdf",orientation = 'portrait')
        plt.savefig("PDOS"+str(atom+1)+".png",orientation = 'portrait')

    if not NO_WINDOW_FLAG:
        plt.show()

    plt.close('all')

################################################################################
