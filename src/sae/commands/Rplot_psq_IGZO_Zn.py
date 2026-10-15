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
# Rplot_psq.py
#   *.psq
#   *.calcdat
#   *.fit 
#   ３つのファイルをプロットする
#
#  ===> IGZO 特化版 (Zn)
#                                                                               
# 2014.12.25                                                                    
#  IGZO 特化版  
#
# 2014.12.16                                                                              
#  matplotlib のバージョンチェックを追加(イマイチ)  
#
# 2014.12.15                                                                              
#  1) numpy のインポート方法を変更                                                        
#  2) 古いmatplotlib でのplotの問題解決のために labelで用いている値                      
#     をint から str に変更 
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
import sys
import os
import re
import optparse
import numpy as np
import matplotlib.pyplot as plt
from LIB_vasp.read_dat import *


#                                                                                         
################################################################################
#from pylab import *
################################################################################
def options():
    IN = "igzo"
    IN_PSQ = IN + ".psq"
    IN_FIT = IN + ".fit"
    IN_CALC = IN + ".calcdat"
    return [IN, IN_PSQ, IN_FIT, IN_CALC]


################################################################################
# Default & OptionParser
################### 物質毎に変更せよ
################### psq ファイルの部分S(Q)の要素数 *.dat を参照
###################
###################
###################################################################
# initial caldata
# exp & cal data
###################################################################
#   fig = plt.figure() # Figure オブジェクトの作成
#   plt.figure(figsize=(10, 7.5))
#   plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)
#   # 余白のセット
#   plt.subplots_adjust(left=0.1, right=0.9)
#   # 余白の確認
#   top = fig.subplotpars.top
#   wspace = fig.subplotpars.wspace
### X 軸 Q を設定
############################################################################
### Y軸, exp S(Q) & cal total S(Q)
###
#   plt.subplot(2,1,1) # 2*1 のグラフの 一段目
############################################################################
#   plt.title('')
############################################################################
### Y 軸 pS(Q) を設定 : 要素すべてをプロット
###
#   plt.subplot(2,1,2) # 2*1 のグラフの 二段目
############################################################################
# In-
# matplitlib のバージョンチェック(ベーター版)
### プロット
###
#   plt.show()
#   plt.savefig('IN+".png", transparent=True, dpi=300)
if __name__ == "__main__":
    IN, IN_PSQ, IN_FIT, IN_CALC = options()
    dimm = 11
    # *.psq ファイルのデーターとしての読み込み開始行
    spsq = 5
    # *.fit ファイルのデーターとしての読み込み開始行
    sfit = 12
    # *.calcdat ファイルのデーターとしての読み込み開始行
    scalc = 13
    # ファイルの行数確認
    npsq0 = sum((1 for line in open(IN_PSQ)))
    psqdat = np.zeros((npsq0, dimm))
    npsq = TextFiles().read_dat(IN_PSQ, dimm, psqdat, spsq)
    # ファイルの行数確認
    nfit0 = sum((1 for line in open(IN_FIT)))
    fitdat = np.zeros((nfit0, 5))
    nfit = TextFiles().read_dat5(IN_FIT, fitdat, sfit)
    # ファイルの行数確認
    ncalc0 = sum((1 for line in open(IN_CALC)))
    calcdat = np.zeros((ncalc0, 2))
    ncalc = TextFiles().read_dat2(IN_CALC, calcdat, scalc)
    maxq = psqdat[npsq0 - 1, 0]
    init_y = np.zeros(ncalc)
    for i in range(ncalc):
        # initial cal S(Q)
        init_y[i] = calcdat[scalc + i, 1]
    cal_y = np.zeros(nfit)
    exp_y = np.zeros(nfit)
    for i in range(nfit):
        # S(Q) RMC++
        cal_y[i] = fitdat[sfit + i, 1]
        # original exp. S(Q)
        exp_y[i] = fitdat[sfit + i, 3]
    plt.rcParams["font.family"] = "Times New Roman"
    # ラベル等のフォントサイズ
    plt.rcParams["font.size"] = 20
    # レジェンドのフォントサイズ
    plt.rcParams["legend.fontsize"] = 11
    # 軸の太さを設定。目盛りは変わらない
    plt.rcParams["axes.linewidth"] = 1.5
    psq_x = np.zeros(npsq)
    for i in range(npsq):
        # psq 0 (Q)
        psq_x[i] = psqdat[spsq + i, 0]
    # 原点(x,y), 幅(x,y)
    plt.axes([0.105, 0.5575, 0.85, 0.4])
    plt.plot(psq_x, exp_y, linewidth=2, label="exp S(Q)")
    plt.plot(psq_x, init_y, linewidth=2, label="init cal S(Q)")
    plt.plot(psq_x, cal_y, linewidth=2, label="cal total S(Q)")
    plt.xticks([])
    plt.legend()
    plt.ylabel("S(Q)", fontsize=20, fontname="Times New Roman")
    # 原点(x,y), 幅(x,y)
    plt.axes([0.105, 0.125, 0.85, 0.4])
    for d in range(8, 10):
        psq_y = np.zeros(npsq)
        for i in range(npsq):
            psq_y[i] = psqdat[spsq + i, d]
        plt.plot(psq_x, psq_y, linewidth=1, label=str(d))
    plt.legend()
    plt.ylabel("partial S(Q)", fontsize=20, fontname="Times New Roman")
    import matplotlib

    tmp = matplotlib.__version__
    version = tmp.split(".")
    if int(version[0]) > 0:
        plt.xlabel("Q/$\\AA^{-1}$", fontsize=20, fontname="Times New Roman")
    else:
        plt.xlabel("Q/A^-1", fontsize=20, fontname="Times New Roman")
    plt.savefig(IN + "_psq_Zn.eps")
    plt.savefig(IN + "_psq_Zn.pdf")
    plt.close("all")
