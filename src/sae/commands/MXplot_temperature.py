#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.common.paths import FileDiscovery
from sae.openmx.md import ReadMd

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# MXplot_temperature.py
#   MXtemp.py ベースで matplotlib  (基本は Vplot_temperature.py ベース)
#
#   *.md
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.03.03
#  startup
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import optparse
import numpy as np
import matplotlib.pyplot as plt

#
################################################################################
#import re
#from LIB_vasp.read_dat import *
#import SpaceGroupEnvironment as SGE 
################################################################################
# デフォルト名 or 入力名が存在しない時の入力ファイル名自動探索
#   for i in range(n_ion_loop):
#       print "%5d %6.2f  %15.8f" % (i+1, temperature[i], etotal[i])
############################################################################
# matplitlib
#   plt.rcParams['font.family']       = 'Times New Roman'                       
# ax1(tempture) の描画
#   ax1 = fig.add_subplot(111)
# ax1(Temperature) 描画軸の上限下限の変更
# ax2(energy) の描画
# ax2(ETOT) 描画軸の上限下限の変更
if __name__ == "__main__":
    name = "openmx"
    suffix = "md"
    mdname = name + "." + suffix
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    if options.INPUT:
        mdname = options.INPUT
        if not os.path.exists(mdname):
            mdname = mdname + "." + suffix
    if not os.path.exists(mdname):
        mdname0 = FileDiscovery().find_datfile(suffix)
        if mdname0 != None:
            mdname = mdname0 + "." + suffix
        else:
            sys.exit("STOP: " + mdname + " not found.")
    print("INPUT:", mdname)
    md = ReadMd(mdname)
    natom = md.get_natom()
    nion = md.get_nion()
    nloop = md.get_nloop()
    energy = md.get_energy_loop()
    temp = md.get_temp_loop()
    given = md.get_temp_given_loop()
    tmp_max = max(temp)
    tmp_min = min(temp)
    etot_max = max(energy)
    etot_min = min(energy)
    # 整数化
    int_etot_max = abs(int(etot_max))
    # 小数点以下取り出し
    dec_etot_max = abs(int_etot_max) - abs(etot_max)
    # 整数化
    int_etot_min = abs(int(etot_min))
    # 小数点以下取り出し
    dec_etot_min = abs(int_etot_min) - abs(etot_min)
    md_x = np.zeros(nloop)
    for i in range(nloop):
        md_x[i] = i
    # ラベル等のフォントサイズ
    plt.rcParams["font.size"] = 14
    # レジェンドのフォントサイズ
    plt.rcParams["legend.fontsize"] = 5
    # 軸の太さを設定。目盛りは変わらない
    plt.rcParams["axes.linewidth"] = 1.5
    rect = [0.155, 0.105, 0.69, 0.8]
    fig = plt.figure()
    ax1_color1 = "blue"
    ax1_color2 = "green"
    ax2_color = "red"
    ax1 = fig.add_axes(rect)
    ax1.plot(
        md_x,
        temp,
        "-o",
        linewidth=1,
        color=ax1_color1,
        markeredgecolor=ax1_color1,
        markerfacecolor="None",
    )
    ax1.plot(
        md_x,
        given,
        "-o",
        linewidth=1,
        color=ax1_color2,
        markeredgecolor=ax1_color2,
        markerfacecolor="None",
    )
    ax1.set_ylabel("Temperature [k]", color=ax1_color1)
    ax1.set_xlabel("MD Step")
    for tl in ax1.get_yticklabels():
        tl.set_color(ax1_color1)
    xmin, xmax, ymin, ymax = ax1.axis()
    ymin = ymin
    ymax = ymax * 2
    ax1.set_ylim(ymin, ymax * 2)
    ax2 = ax1.twinx()
    ax2.plot(md_x, energy, linewidth=2, color=ax2_color)
    ax2.set_ylabel("Total Energy [eV]", color=ax2_color)
    for tl in ax2.get_yticklabels():
        tl.set_color(ax2_color)
    xmin, xmax, ymin, ymax = ax2.axis()
    ymin_int = abs(int(ymin))
    ymin_dec = abs(ymin) - abs(ymin_int)
    ymin = ymin - ymin_dec / 2
    ymax = ymax + ymin_dec / 3
    ax2.set_ylim(ymin, ymax)
    plt.savefig("temperature.eps")
    plt.savefig("temperature.pdf")
    plt.savefig("temperature.png")
    plt.show()
    plt.close("all")
