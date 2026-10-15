#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.common.paths import FileDiscovery
from sae.openmx.dat import ReadMxDat

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OpenMX3.7
#
# MXEI Vplot
#
#  MXEI の結果を matplotlib でプロット
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.06.30
#  == None --> is None
#
# 2015.06.15
#   *.dat ファイル名と systemname が異なるときの自動処理を追加
#
# 2015.03.13
#   MDループが途中で終わっているとき(DFTSCFファイルが存在するとき)の対応
#
# 2015.03.12
#  *.out が出力される前の 計算途中のファイル *.DFTSCF の読み込みに対応
#
# 2015.02.24
#  startup
#  ReadMxOut クラスを用いる形で作成
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
import re
import optparse
import matplotlib.pyplot as plt

#
################################################################################
#import gzip
#import numpy as np
#import SpaceGroupEnvironment as SGE
################################################################################
# デフォルト名より最適なデフォルトファイル名の推定ルーチン
# オプションでファイル名を入力した時
# *.out が存在しないとき、かつ *.dat ファイルが存在するとき
# dat ファイルの中身を読んで systemname (*.out)を検索する
# 計算途中での DFTSCF ファイル読み込み or 通常の *.out ファイル読み込み
# makes instance
#   module = __import__(module_name,globals(),locals(),[class_name],-1)
# module の動的ロード
# class の動的ロード
# MDループが途中で終わっているとき(DFTSCFファイルが存在するとき)
############################################################################
# matplotlib
#   plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)
#   plt.xlabel("Total Loop ( Total SCF(&ION) loop ) [n]", fontsize=20 )
if __name__ == "__main__":
    name = "openmx"
    suffix = ".out"
    mxname = name + suffix
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    # *.dat はかならずあるのでそれをトリガーに
    if not os.path.exists(mxname):
        name0 = FileDiscovery().find_datfile("dat")
        if not name0 is None:
            name = name0
            mxname = name + suffix
    if options.INPUT:
        mxname = options.INPUT
        name = re.sub("\\.out$", "", mxname)
        mxname = name + suffix
    if len(args) > 0:
        name = args[0]
        name = re.sub("\\.out$", "", name)
    mxname = name + suffix
    if not os.path.exists(name + ".out"):
        if os.path.exists(name + ".dat"):
            dat = ReadMxDat(name + ".dat")
            sysname = dat.get_title()
            name = sysname
            mxname = name + suffix
        else:
            sys.exit("STOP: " + name + ".out and " + name + ".dat file not found.")
    module_name = "sae._class_registry"
    if not os.path.exists(mxname):
        mxname = name + ".DFTSCF"
        class_name = "ReadMxDftscf"
        FLAG_DFTSCF = True
    else:
        FLAG_DFTSCF = False
        class_name = "ReadMxOut"
    # このリフレクションは python2 方式なので注意
    # for Python3
    try:
        module = __import__(module_name, globals(), locals(), [class_name], 0)
    except:
        module = __import__(module_name, fromlist=[class_name])
    klass = getattr(module, class_name)
    out = klass(mxname)
    n_ion_loop = out.get_n_ion_loop()
    max_n_scf = out.get_max_n_scf()
    utot = out.get_utot()
    uele, uele_index = out.get_uele()
    y = []
    x = []
    i = 0
    #print "# md =",md+1
    for md in range(n_ion_loop):
        #print "    %14.11f" %(uele[md,scf])
        #print x[i], y[i]
        for scf in range(uele_index[md]):
            x.append(i)
            y.append(uele[md, scf])
            i += 1
    if FLAG_DFTSCF:
        md = n_ion_loop
        #print x[i], y[i]
        for scf in range(uele_index[md]):
            x.append(i)
            y.append(uele[md, scf])
            i += 1
    plt.rcParams["font.family"] = "Times New Roman"
    # ラベル等のフォントサイズ
    plt.rcParams["font.size"] = 20
    # レジェンドのフォントサイズ
    plt.rcParams["legend.fontsize"] = 18
    # 軸の太さを設定。目盛りは変わらない
    plt.rcParams["axes.linewidth"] = 1.5
    # 原点(x,y), 幅(x,y)
    plt.axes([0.13, 0.13, 0.8, 0.8])
    plt.plot(x, y, color="red", linewidth=2, label="Total Energy")
    plt.ylabel("Band Energy [Hartree]", fontsize=20)
    plt.xlabel("Total Loop ( ION Loop & SCF Loop) [n]", fontsize=20)
    plt.savefig("convergeION.eps")
    plt.savefig("convergeION.pdf")
    plt.savefig("convergeION.png")
    plt.show()
    plt.close("all")
