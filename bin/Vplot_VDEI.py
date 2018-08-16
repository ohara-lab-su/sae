#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vplot_VDEI.py
#  CONTCAR から ION ループごとの energy distance を求める
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
#
# 2015.01.06 1st
#
################################################################################
from __future__ import print_function
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

    OSZICAR      = "OSZICAR"

    return OSZICAR


################################################################################
if __name__ == '__main__':

    # Default & OptionParser
    OSZICAR = options()

    # ファイルの存在有無と圧縮の有無の確認
    if os.path.exists(OSZICAR):
        GZIP=False
    elif os.path.exists(OSZICAR+".gz"):
        GZIP=True
    else:
        sys.exit("STOP: "+OSZICAR+" or "+OSZICAR+".gz file not found")

    # ファイル読み込み
    try:
        if GZIP:
            tmp = gzip.open(OSZICAR+".gz")
        else:
            tmp = open(OSZICAR)
        datfile = tmp.read()
    except:
        tmp.close()
        sys.exit("STOP: "+OSZICAR+" does'nt open")
    finally:
        tmp.close()

    datlines = datfile.split('\n')
    ndat = int(len(datlines)) - 1

    # SCF & ION loop ( with entropy ) energy は 5番目
    energy_reg = re.compile(".*F=",re.IGNORECASE )

    # free energy の吸い出し
    total_loop = 0
    y = []
    x = []
    for i in range(ndat):
        if bool(energy_reg.match(datlines[i])):
            tmp = datlines[i].split()
            print tmp[7]
#           y.append(tmp[7])     # Y: free energy
#           x.append(total_loop) # X: total_loop ( scf & ion loop)
#           total_loop += 1

 
#     ############################################################################
#     # matplotlib
# 
#     plt.rcParams['font.family'] = 'Times New Roman'
#     plt.rcParams['font.size']         = 20  # ラベル等のフォントサイズ
#     plt.rcParams['legend.fontsize']   = 18  # レジェンドのフォントサイズ
#     plt.rcParams['axes.linewidth']    = 1.5 # 軸の太さを設定。目盛りは変わらない
# 
# #   plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)
# 
#     plt.axes([ 0.130,0.130, 0.80,0.80 ])   # 原点(x,y), 幅(x,y)
# 
#     plt.plot(x,y, color="red", linewidth=2, label='Total Energy')
#     plt.ylabel("Total Energy [eV]", fontsize=20 )
# #   plt.xlabel("Total Loop ( ION Loop) [n]", fontsize=20 )
#     plt.xlabel("Total Loop ( Total SCF(&ION) loop ) [n]", fontsize=20 )
#  
#     plt.savefig("convergeIONSCF.eps")
#     plt.savefig("convergeIONSCF.pdf")
#     plt.savefig("convergeIONSCF.png") 
# 
#     plt.show()
# 
#     plt.close('all')
# 
# ################################################################################
