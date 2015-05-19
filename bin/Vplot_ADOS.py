#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vplot_ADOS.py
#
#   原子の種類ごとのオービタル足しあわせ LDOS + TODOS 出力
#
#   1) gnuplot の代わりに matplotlib を用いる
#   2) Vldos.py などは用いない
#   3) 内部的には直接 ReadDoscar クラス(ReadDoscar.py)を用いる
#      そもそも ReadDoscar クラスは matplotlib からの利用を念頭に構造化している
#
#   注意) ION 毎の情報が必要なので、OUTCAR の読み込みは必須となる
#
################################################################################
#
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
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015, Kengo NAKADA"
__license__    = "MIT"
#                                                                                         
__status__     = "alpha"
__version__    = "0.0.4"
################################################################################

import sys
#import os
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
    parser.add_option(  '-d','--doscar',
                        dest='DOSCAR',
                        default=dname,
    )
    parser.add_option( '-o', '--outcar',
                      dest='OUTCAR',
                      default=oname,
    )
    parser.add_option( '-n', '--nw',
                      action='store_true',
                      default=False,
                      dest='NOWINDOW',
    )
    parser.add_option(  '--emax',
                      dest='EMAX',
    )
    parser.add_option(  '--emin',
                      dest='EMIN',
    )
    parser.add_option(  '--ymax',
                      dest='YMAX',
    )
    options,  args = parser.parse_args()
                                                                                
    if options.DOSCAR:
        dname=options.DOSCAR

    if options.OUTCAR:
        oname=options.OUTCAR

    return [dname,oname,\
            options.NOWINDOW,options.EMAX,options.EMIN,options.YMAX]

################################################################################
if __name__ == '__main__':

    # set input file
    dname,oname,NO_WINDOW_FLAG,\
            OPT_EMAX,OPT_EMIN,OPT_YMAX= options()

    if OPT_EMAX:                                                                
                print "Emax=",OPT_EMAX                                                  
    if OPT_EMIN:                                                                
                print "Emin=",OPT_EMIN                                                  
    if OPT_YMAX:                                                                
                print "Ymax=",OPT_YMAX  

    # set output device
    out = sys.stdout

    # makes instance ( Read DOSCAR )
    dos = SAE.ReadDoscar(dname)

    NSPIN = dos.get_ispin()
    LORBIT = dos.get_lorbit()
    NATOM = dos.get_natom()
    TITLE =  dos.get_title()
    EMAX = dos.get_emax()
    EMIN = dos.get_emin()
    NEDOS = dos.get_nedos()
    EFERMI = dos.get_efermi()

    # makes instance ( Read OUTCAR )
    outcar = SAE.ReadOutcar(oname)
    NION = outcar.get_nion()
    atoms = outcar.get_atoms_index()

    ENG = dos.get_eng()

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

        INTTDOS = dos.get_inttdos(spin)
        TDOS = dos.get_tdos(spin)
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
            ADOS = dos.get_ldos_ion(0,ion,spin)
            plt.plot(ENG-EFERMI,ADOS, linestyle=":", color=c, linewidth=2, label=atom+'-s')
            j += 1
    
            c = cm.prism(float(j)/(3*NION))
            ADOS = dos.get_ldos_ion(1,ion,spin)
            plt.plot(ENG-EFERMI,ADOS, linestyle="-", color=c, linewidth=2, label=atom+'-p')
            j += 1
     
            c = cm.prism(float(j)/(3*NION))
            ADOS = dos.get_ldos_ion(2,ion,spin)
            plt.plot(ENG-EFERMI,ADOS, linestyle="--", color=c, linewidth=2, label=atom+'-d')
            j += 1

            # Y軸の調整                                                             
            plt.ylim( ymin=0 ) 

        if spin == 0:
            yl = plt.ylabel("DOS/eV", fontsize=20 )

        if OPT_EMAX:                                                            
            plt.xlim( xmax=int(OPT_EMAX) )                                      
        if OPT_EMIN:                                                            
            plt.xlim( xmin=int(OPT_EMIN) )                                      
        if OPT_YMAX:                                                            
            plt.ylim( ymax=int(OPT_YMAX) ) 

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
