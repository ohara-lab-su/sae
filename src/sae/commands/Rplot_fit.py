#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.common.text import TextFiles

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Rplot_fit.py
#   matplotlib 習作用 Rplot_fit.sh 同等機能実装番
#
# 2014.12.15                                                                              
#  numpy のインポート方法を変更  
#
# 2014.11.19 1st
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import numpy as np
import matplotlib.pyplot as plt


#                                                                                         
################################################################################
#import sys
#import os
#import re
#import optparse
#from pylab import *
#import matplotlib.mlab as mlab
#from LIB_vasp.read_dat import *
#import SpaceGroupEnvironment as SGE  
################################################################################
def options():
    IN = "igzo"
    IN_FIT = IN + ".fit"
    IN_CALC = IN + ".calcdat"
    return [IN, IN_FIT, IN_CALC]


################################################################################
# Default & OptionParser
###################################################################
#   for i in range(sfit,nfit0):
#       print " %12.6e  %+18.12e  %+18.12e  %+18.12e  %+18.12e" \
#               % ( fitdat[i,0],    # Q
#                   fitdat[i,1],    # S(Q) RMC++
#                   fitdat[i,2],    # renormalized experimental S(Q)
#                   fitdat[i,3],    # original exp. S(Q)
#                   fitdat[i,4] )   # additive backgroupd      
#   for i in range(scalc,ncalc0):
#       print " %12.6e  %+18.12e  " \
#               % ( calcdat[i,0],    # Q
#                   calcdat[i,1] )   # S(Q)
###################################################################
# initial caldata
# cal data
# exp data
###################################################################
#   fig = plt.figure() # Figure オブジェクトの作成
#   plt.figure(figsize=(10, 7.5))
#   plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)
#   # 余白のセット
#   plt.subplots_adjust(left=0.1, right=0.9)
#   # 余白の確認
#   top = fig.subplotpars.top
#   wspace = fig.subplotpars.wspace
#   plt.title('')
#   plt.show()
#   plt.savefig('IN+".png", transparent=True, dpi=300)
if __name__ == "__main__":
    IN, IN_FIT, IN_CALC = options()
    # *.fit ファイルのデーターとしての読み込み開始行
    sfit = 12
    # *.calcdat ファイルのデーターとしての読み込み開始行
    scalc = 13
    # ファイルの行数確認
    nfit0 = sum((1 for line in open(IN_FIT)))
    fitdat = np.zeros((nfit0, 5))
    nfit = TextFiles().read_dat5(IN_FIT, fitdat, sfit)
    # ファイルの行数確認
    ncalc0 = sum((1 for line in open(IN_CALC)))
    calcdat = np.zeros((ncalc0, 2))
    ncalc = TextFiles().read_dat2(IN_CALC, calcdat, scalc)
    x0 = np.zeros(ncalc)
    y0 = np.zeros(ncalc)
    for i in range(ncalc):
        # Q
        x0[i] = calcdat[scalc + i, 0]
        # S(Q)
        y0[i] = calcdat[scalc + i, 1]
    cal_y = np.zeros(nfit)
    for i in range(nfit):
        # S(Q) RMC++
        cal_y[i] = fitdat[sfit + i, 1]
    exp_y = np.zeros(nfit)
    for i in range(nfit):
        # original exp. S(Q)
        exp_y[i] = fitdat[sfit + i, 3]
    plt.rcParams["font.family"] = "Times New Roman"
    # ラベル等のフォントサイズ
    plt.rcParams["font.size"] = 20
    # レジェンドのフォントサイズ
    plt.rcParams["legend.fontsize"] = 18
    # 軸の太さを設定。目盛りは変わらない
    plt.rcParams["axes.linewidth"] = 1.5
    # 原点(x,y), 幅(x,y)
    plt.axes([0.105, 0.125, 0.85, 0.8])
    plt.plot(x0, cal_y, color="red", linewidth=2, label="cal S(Q)")
    plt.plot(x0, exp_y, color="green", linewidth=2, label="obs S(Q)")
    plt.plot(x0, y0, color="blue", linewidth=2, label="initial cal S(Q)")
    import matplotlib

    tmp = matplotlib.__version__
    version = tmp.split(".")
    if int(version[0]) > 0:
        plt.xlabel("Q/$\\AA^{-1}$", fontsize=20, fontname="Times New Roman")
    else:
        plt.xlabel("Q/A^-1", fontsize=20, fontname="Times New Roman")
    plt.ylabel("S(Q)", fontsize=20, fontname="Times New Roman")
    plt.legend()
    plt.savefig(IN + "_fit.eps")
    plt.savefig(IN + "_fit.pdf")
    plt.close("all")
