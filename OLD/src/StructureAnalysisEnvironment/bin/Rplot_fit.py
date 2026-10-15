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

#from pylab import *
import matplotlib.pyplot as plt
#import matplotlib.mlab as mlab

#from LIB_vasp.read_dat import *

import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE  

################################################################################
def options():

    IN      = "igzo"

    IN_FIT  = IN+".fit"
    IN_CALC = IN+".calcdat"

    return [IN,IN_FIT,IN_CALC]


################################################################################
if __name__ == '__main__':

    # Default & OptionParser
    IN,IN_FIT,IN_CALC = options()

    sfit   = 12  # *.fit ファイルのデーターとしての読み込み開始行
    scalc  = 13  # *.calcdat ファイルのデーターとしての読み込み開始行

    nfit0  = sum(1 for line in open(IN_FIT))  # ファイルの行数確認
    fitdat = np.zeros((nfit0,5))
    nfit   = SAE.read_dat5(IN_FIT,fitdat,sfit)

    ncalc0  = sum(1 for line in open(IN_CALC))  # ファイルの行数確認
    calcdat = np.zeros((ncalc0,2))
    ncalc   = SAE.read_dat2(IN_CALC,calcdat,scalc)

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
    x0 = np.zeros((ncalc))
    y0 = np.zeros((ncalc))
    for i in range(ncalc):
        x0[i] = calcdat[scalc+i,0]  # Q
        y0[i] = calcdat[scalc+i,1]  # S(Q)

    # cal data
    cal_y = np.zeros((nfit))
    for i in range(nfit):
        cal_y[i] = fitdat[sfit+i,1] # S(Q) RMC++

    # exp data
    exp_y = np.zeros((nfit))
    for i in range(nfit):
        exp_y[i] = fitdat[sfit+i,3] # original exp. S(Q)

    ###################################################################

#   fig = plt.figure() # Figure オブジェクトの作成
#   plt.figure(figsize=(10, 7.5))

    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size']         = 20  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize']   = 18  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']    = 1.5 # 軸の太さを設定。目盛りは変わらない

#   plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)

#   # 余白のセット
#   plt.subplots_adjust(left=0.1, right=0.9)
#   # 余白の確認
#   top = fig.subplotpars.top
#   wspace = fig.subplotpars.wspace

    plt.axes([ 0.105,0.125, 0.85,0.8 ])   # 原点(x,y), 幅(x,y)

    plt.plot(x0,cal_y, color="red",   linewidth=2, label='cal S(Q)')
    plt.plot(x0,exp_y, color="green", linewidth=2, label='obs S(Q)')
    plt.plot(x0,y0,    color="blue",  linewidth=2, label='initial cal S(Q)')

#   plt.title('')
    import matplotlib
    tmp = matplotlib.__version__
    version = tmp.split('.')
    if int(version[0]) > 0:
        plt.xlabel('Q/$\AA^{-1}$',fontsize=20, fontname='Times New Roman')
    else:
        plt.xlabel('Q/A^-1',fontsize=20, fontname='Times New Roman')
    plt.ylabel('S(Q)',        fontsize=20, fontname='Times New Roman')

    plt.legend()

#   plt.show()

    plt.savefig(IN+"_fit.eps")
    plt.savefig(IN+"_fit.pdf")
#   plt.savefig('IN+".png", transparent=True, dpi=300)
    plt.close('all')
    

################################################################################
