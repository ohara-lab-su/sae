#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Rplot_psq2.py
#   *.psq
#   *.calcdat
#   *.fit 
#   ３つのファイルをプロットする
#
# 2014.12.16
#  1) matplotlib のバージョンチェックを追加(イマイチ)
#  2) Rplot_ppcf.py からブランチ(グラフを二段組にする)
#
# 2014.12.15                                                                              
#  1) numpy のインポート方法を変更  
#  2) 古いmatplotlib でのplotの問題解決のために labelで用いている値
#     をint から str に変更
#
# 2014.11.19 1st
#
###################################################################################
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

#import sys
#import os
#import re
#import optparse

import numpy as np

import matplotlib.pyplot as plt
#import matplotlib.mlab as mlab

#from LIB_vasp.read_dat import *

import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE  

###################################################################################
def options():

    IN      = "igzo"

    IN_PSQ  = IN+".psq"
    IN_FIT  = IN+".fit"
    IN_CALC = IN+".calcdat"
    IN_PPCF = IN+".ppcf"

    return [IN,IN_PSQ,IN_FIT,IN_CALC,IN_PPCF]


###################################################################################
if __name__ == '__main__':

    # Default & OptionParser
    IN,IN_PSQ,IN_FIT,IN_CALC,IN_PPCF = options()

    ################### psq ファイルの部分S(Q)の要素数 *.dat を参照
    ################### (ppcfでも同等) 物質毎に変更せよ
    dimm   = 11
    ###################
    ###################

    spsq   =  5  # *.psq ファイルのデーターとしての読み込み開始行
    sfit   = 12  # *.fit ファイルのデーターとしての読み込み開始行
    scalc  = 13  # *.calcdat ファイルのデーターとしての読み込み開始行
    sppcf  =  8  # *.ppcf ファイルのデーター読み込み開始行

    nppcf0  = sum(1 for line in open(IN_PPCF))  # ファイルの行数確認
    ppcfdat = np.zeros((nppcf0,dimm))
    nppcf   = SAE.read_dat(IN_PPCF,dimm,ppcfdat,sppcf)

    npsq0  = sum(1 for line in open(IN_PSQ))  # ファイルの行数確認
    psqdat = np.zeros((npsq0,dimm))
    npsq   = SAE.read_dat(IN_PSQ,dimm,psqdat,spsq)

    nfit0  = sum(1 for line in open(IN_FIT))  # ファイルの行数確認
    fitdat = np.zeros((nfit0,5))
    nfit   = SAE.read_dat5(IN_FIT,fitdat,sfit)

    ncalc0  = sum(1 for line in open(IN_CALC))  # ファイルの行数確認
    calcdat = np.zeros((ncalc0,2))
    ncalc   = SAE.read_dat2(IN_CALC,calcdat,scalc)


    maxq = psqdat[npsq0-1,0]

    ###################################################################

    # initial caldata
    init_y = np.zeros((ncalc))
    for i in range(ncalc):
        init_y[i] = calcdat[scalc+i,1]  # initial cal S(Q)

    # exp & cal data
    cal_y = np.zeros((nfit))
    exp_y = np.zeros((nfit))
    for i in range(nfit):
        cal_y[i] = fitdat[sfit+i,1] # S(Q) RMC++
        exp_y[i] = fitdat[sfit+i,3] # original exp. S(Q)

    ###################################################################

    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size']         = 20  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize']   = 11  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']    = 1.5 # 軸の太さを設定。目盛りは変わらない

#   fig = plt.figure() # Figure オブジェクトの作成
#   plt.figure(figsize=(10, 7.5))
#   plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)

#   # 余白のセット
#   plt.subplots_adjust(left=0.1, right=0.9)
#   # 余白の確認
#   top = fig.subplotpars.top
#   wspace = fig.subplotpars.wspace


    ### X 軸 Q を設定
    psq_x = np.zeros((nppcf))
    for i in range(nppcf):
        psq_x[i] = ppcfdat[sppcf+i,0] # psq 0 (Q)


    ### Y 軸 partial g(r) を設定 : 要素半分だけプロット
    ###
#   plt.subplot(2,1,1) # 2*1 のグラフの 一段目
    plt.axes([ 0.105,0.5575, 0.85,0.4 ])   # 原点(x,y), 幅(x,y)  
    for d in range(1,dimm/2+1):
        psq_y = np.zeros((nppcf))
        for i in range(nppcf):
            psq_y[i] = ppcfdat[sppcf+i,d]
        plt.plot(psq_x,psq_y, linewidth=1, label=str(d))
    plt.xticks([])    
    plt.legend()
    plt.ylabel('partial g(r)',        fontsize=20, fontname='Times New Roman')


    ### Y 軸 partial g(r) を設定 : 要素半分だけプロット
    ###
#   plt.subplot(2,1,2) # 2*1 のグラフの 二段目
    plt.axes([ 0.105,0.125, 0.85,0.4 ])   # 原点(x,y), 幅(x,y)  
    for d in range(dimm/2+1,dimm):
        psq_y = np.zeros((nppcf))
        for i in range(nppcf):
            psq_y[i] = ppcfdat[sppcf+i,d]
        plt.plot(psq_x,psq_y, linewidth=1, label=str(d))
    plt.legend()
    plt.ylabel('partial g(r)',        fontsize=20, fontname='Times New Roman')


    # matplitlib のバージョンチェック(ベーター版)                                         
    import matplotlib
    tmp = matplotlib.__version__
    version = tmp.split('.')
    if int(version[0]) > 0:
        plt.xlabel('r[$\AA$]',fontsize=20, fontname='Times New Roman')                
    else:
        plt.xlabel('r[A]',fontsize=20, fontname='Times New Roman') 


    ### プロット
    ###
#   plt.show()
    plt.savefig(IN+"_ppcf2.eps")
    plt.savefig(IN+"_ppcf2.pdf")
#   plt.savefig('IN+".png", transparent=True, dpi=300)
    plt.close('all')
    

###################################################################################
