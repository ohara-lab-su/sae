#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vtemp.py
#
#   OUTCAR から temperature と ETOTAL を吸い出す
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.02.24
#  method 名ルール変更に伴い get_iter_num()  --> get_n_ion_loop()
#
# 2015.01.26 1st run
#  Vtemp.py 1st version 作成
#  Vtemp.py 1st version をベースに 温度とエネルギーのプロットをmatplotlib で
#  行うようにする
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
#import re
#import optparse

import numpy as np
import matplotlib.pyplot as plt

#from LIB_vasp.read_dat import *

#import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE 


################################################################################
if __name__ == '__main__':

    name_out = 'OUTCAR'
    name_osz = 'OSZICAR'

    module_name = 'StructureAnalysisEnvironment'

    if os.path.exists(name_osz) or os.path.exists(name_osz+".gz"):
        class_name ='ReadOszicar'
        name = name_osz
    else:
        class_name = 'ReadOutcar'
        name = name_out

    module = __import__(module_name, globals(), locals(), [class_name], -1)
    klass = getattr(module,class_name)

    outfile = klass(name)
    MD_FLAG = outfile.get_md_mode()

    if not MD_FLAG:
        sys.exit("STOP: current is  non MD mode")

    n_ion_loop = outfile.get_n_ion_loop()
    etotal = outfile.get_etotal()
    temperature = outfile.get_temperature()

    tmp_max = max(temperature)
    tmp_min = min(temperature)
    etot_max = max(etotal)
    etot_min = min(etotal)

    int_etot_max = abs(int(etot_max))                 # 整数化
    dec_etot_max = abs(int_etot_max) - abs(etot_max)  # 小数点以下取り出し
    int_etot_min = abs(int(etot_min))                 # 整数化
    dec_etot_min = abs(int_etot_min) - abs(etot_min)  # 小数点以下取り出し


#   for i in range(n_ion_loop):
#       print "%5d %6.2f  %15.8f" % (i+1, temperature[i], etotal[i])

    md_x = np.zeros(n_ion_loop)
    for i in range(n_ion_loop):
        md_x[i] = i

    ############################################################################
    # matplitlib

#   plt.rcParams['font.family']       = 'Times New Roman'                       
    plt.rcParams['font.size']         = 14  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize']   = 5   # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']    = 1.5 # 軸の太さを設定。目盛りは変わらない


    rect = [ 0.155,0.105, 0.69,0.80 ] 

    fig = plt.figure()

    ax1_color='blue'
    ax2_color='red'

#   ax1 = fig.add_subplot(111)
    ax1 = fig.add_axes(rect)
    ax1.plot(md_x,temperature, '-o',linewidth=1,color=ax1_color,\
            markeredgecolor=ax1_color,markerfacecolor='None')
    ax1.set_ylabel('Temperature [k]',color=ax1_color)
    ax1.set_xlabel('MD Step')
    for tl in ax1.get_yticklabels():
        tl.set_color(ax1_color)

    # ax1(Temperature) 描画軸の上限下限の変更
    xmin,xmax,ymin,ymax = ax1.axis()
    ymin = ymin
    ymax = ymax*2
    ax1.set_ylim(ymin,ymax*2)

    ax2 = ax1.twinx()
    ax2.plot(md_x,etotal, linewidth=2, color=ax2_color)
    ax2.set_ylabel('Total Energy [eV]',color=ax2_color)
    for tl in ax2.get_yticklabels():
        tl.set_color(ax2_color)

    # ax2(ETOT) 描画軸の上限下限の変更
    xmin,xmax,ymin,ymax = ax2.axis()
    ymin_int = abs(int(ymin))
    ymin_dec = abs(ymin) - abs(ymin_int)
    ymin = ymin - ymin_dec/2
    ymax = ymax + ymin_dec/3
    ax2.set_ylim(ymin,ymax)


    plt.savefig("temperature.eps")
    plt.savefig("temperature.pdf")
    plt.savefig("temperature.png")

    plt.show()

    plt.close('all')

    
################################################################################
