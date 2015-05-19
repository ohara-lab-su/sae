#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vplot_VEI.py
#   拙作 VEI スクリプト(free energy 項目を引っ張るだけ)
#   をその場で一発で可視化するためのスクリプト
#   gnuplot いらず
#
#   VEI は読まずに Vplot_VEI.py 中で同等のことをする
#
# 2015.01.06 1st
#
################################################################################
__author__     = "Kengo NAKADA"                                                           
__maintainer__ = "Kengo NAKADA"                                                           
__credits__    = ["Kengo NAKADA"]                                                         
__email__      = "kengo.nakada@gmail.com"                                                 
__copyright__  = "Copyright 2014, Kengo NAKADA"                                           
__license__    = "MIT"                                                                    
#                                                                                         
__status__     = "alpha"                                                                  
__version__    = "0.0.1"                                                                  
################################################################################

import sys
import os
import gzip
import re
#import optparse

#import numpy as np

#from pylab import *
import matplotlib.pyplot as plt
#import matplotlib.mlab as mlab

#import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE  

################################################################################
def options():

    OUTCAR      = "OUTCAR"

    return OUTCAR


################################################################################
if __name__ == '__main__':

    # Default & OptionParser
    OUTCAR = options()

    # ファイルの存在有無と圧縮の有無の確認
    if os.path.exists(OUTCAR):
        GZIP=False
    elif os.path.exists(OUTCAR+".gz"):
        GZIP=True
    else:
        sys.exit("STOP: "+OUTCAR+" or "+OUTCAR+".gz file not found")

    # ファイル読み込み
    try:
        if GZIP:
            tmp = gzip.open(OUTCAR+".gz")
        else:
            tmp = open(OUTCAR)
        datfile = tmp.read()
        datlines = datfile.split('\n')
    except:
        tmp.close()
        sys.exit("STOP: "+OUTCAR+" does'nt open")
    finally:
        tmp.close()

    ndat = int(len(datlines)) - 1

    # ION loop の帰結 ( with entropy ) energy は 5番目 <-- VEE 互換
#   energy_reg = re.compile(".*free  energy",re.IGNORECASE)
#   num = 5 - 1

    # ION loop の帰結 ( without entropy ) energy は 4番目
#   energy_reg = re.compile(".*energy  without entropy=",re.IGNORECASE)
#   num = 4 - 1

    # SCF & ION loop ( with entropy ) energy は 5番目
#   energy_reg = re.compile(".*free energy",re.IGNORECASE)
#   num = 5 - 1

    # SCF & ION loop ( with entropy ) energy は 5番目
    energy_reg = re.compile(".*energy without entropy",re.IGNORECASE )
    num = 5 - 1

    # free energy の吸い出し
    total_loop = 0
    y = []
    x = []
    for i in range(ndat):
        if bool(energy_reg.match(datlines[i])):
            tmp = datlines[i].split()
            y.append(tmp[num])     # Y: free energy
            x.append(total_loop) # X: total_loop ( scf & ion loop)
            total_loop += 1

 
    ############################################################################
    # matplotlib

    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size']         = 20  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize']   = 18  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']    = 1.5 # 軸の太さを設定。目盛りは変わらない

#   plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)

    plt.axes([ 0.130,0.130, 0.80,0.80 ])   # 原点(x,y), 幅(x,y)

    plt.plot(x,y, color="red", linewidth=2, label='Total Energy')
    plt.ylabel("Total Energy [eV]", fontsize=20 )
#   plt.xlabel("Total Loop ( ION Loop) [n]", fontsize=20 )
    plt.xlabel("Total Loop ( Total SCF(&ION) loop ) [n]", fontsize=20 )
 
    plt.savefig("convergeIONSCF.eps")
    plt.savefig("convergeIONSCF.pdf")
    plt.savefig("convergeIONSCF.png") 

    plt.show()

    plt.close('all')

################################################################################
