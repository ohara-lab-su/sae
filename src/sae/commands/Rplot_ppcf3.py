#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
###################################################################################
from __future__ import print_function
from sae.common.text import TextFiles

#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Rplot_psq3.py
#   *.psq
#   *.calcdat
#   *.fit 
#   ３つのファイルをプロットする
#
# 2014.12.16
#  1) matplotlib のバージョンチェックを追加(イマイチ)
#  2) Rplot_ppcf.py からブランチ(グラフを二段組にする)
#  3) Rplot_ppcf2.py からブランチ(グラフを三段組にする)
#
# 2014.12.15                                                                              
#  1) numpy のインポート方法を変更  
#  2) 古いmatplotlib でのplotの問題解決のために labelで用いている値
#     をint から str に変更
#
# 2014.11.19 1st
#
###################################################################################
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
#import matplotlib.mlab as mlab
#from LIB_vasp.read_dat import *
#import SpaceGroupEnvironment as SGE 
###################################################################################
def options():
    IN = "igzo"
    IN_PSQ = IN + ".psq"
    IN_FIT = IN + ".fit"
    IN_CALC = IN + ".calcdat"
    IN_PPCF = IN + ".ppcf"
    return [IN, IN_PSQ, IN_FIT, IN_CALC, IN_PPCF]


###################################################################################
# Default & OptionParser
################### psq ファイルの部分S(Q)の要素数 *.dat を参照
################### (ppcfでも同等) 物質毎に変更せよ
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
### Y 軸 partial g(r) を設定
###
### Y 軸 partial g(r) を設定
###
### Y 軸 partial g(r) を設定
###
# matplitlib のバージョンチェック(ベーター版)                                         
### プロット
###
#   plt.show()
#   plt.savefig('IN+".png", transparent=True, dpi=300)
if __name__ == "__main__":
    IN, IN_PSQ, IN_FIT, IN_CALC, IN_PPCF = options()
    dimm = 11
    # *.psq ファイルのデーターとしての読み込み開始行
    spsq = 5
    # *.fit ファイルのデーターとしての読み込み開始行
    sfit = 12
    # *.calcdat ファイルのデーターとしての読み込み開始行
    scalc = 13
    # *.ppcf ファイルのデーター読み込み開始行
    sppcf = 8
    # ファイルの行数確認
    nppcf0 = sum((1 for line in open(IN_PPCF)))
    ppcfdat = np.zeros((nppcf0, dimm))
    nppcf = TextFiles().read_dat(IN_PPCF, dimm, ppcfdat, sppcf)
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
    psq_x = np.zeros(nppcf)
    for i in range(nppcf):
        # psq 0 (Q)
        psq_x[i] = ppcfdat[sppcf + i, 0]
    # 原点(x,y), 幅(x,y)  
    plt.axes([0.105, 0.705, 0.85, 0.27])
    for d in range(1, dimm / 3 + 1):
        psq_y = np.zeros(nppcf)
        for i in range(nppcf):
            psq_y[i] = ppcfdat[sppcf + i, d]
        plt.plot(psq_x, psq_y, linewidth=1, label=str(d))
    plt.xticks([])
    plt.legend()
    plt.ylabel("partial g(r)", fontsize=20, fontname="Times New Roman")
    # 原点(x,y), 幅(x,y)  
    plt.axes([0.105, 0.415, 0.85, 0.27])
    for d in range(dimm / 3 + 1, 2 * (dimm / 3) + 1):
        psq_y = np.zeros(nppcf)
        for i in range(nppcf):
            psq_y[i] = ppcfdat[sppcf + i, d]
        plt.plot(psq_x, psq_y, linewidth=1, label=str(d))
    plt.xticks([])
    plt.legend()
    plt.ylabel("partial g(r)", fontsize=20, fontname="Times New Roman")
    # 原点(x,y), 幅(x,y)  
    plt.axes([0.105, 0.125, 0.85, 0.27])
    for d in range(2 * (dimm / 3) + 1, dimm):
        psq_y = np.zeros(nppcf)
        for i in range(nppcf):
            psq_y[i] = ppcfdat[sppcf + i, d]
        plt.plot(psq_x, psq_y, linewidth=1, label=str(d))
    plt.legend()
    plt.ylabel("partial g(r)", fontsize=20, fontname="Times New Roman")
    import matplotlib

    tmp = matplotlib.__version__
    version = tmp.split(".")
    if int(version[0]) > 0:
        plt.xlabel("r[$\\AA$]", fontsize=20, fontname="Times New Roman")
    else:
        plt.xlabel("r[A]", fontsize=20, fontname="Times New Roman")
    plt.savefig(IN + "_ppcf3.eps")
    plt.savefig(IN + "_ppcf3.pdf")
    plt.close("all")
