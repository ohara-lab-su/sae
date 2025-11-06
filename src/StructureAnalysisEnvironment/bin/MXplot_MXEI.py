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
from __future__ import print_function
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"
################################################################################

import sys
#import gzip
import os
import re
import optparse
#import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

import matplotlib.pyplot as plt

################################################################################
if __name__ == '__main__':

    name = 'openmx'
    suffix = '.out'
    mxname = name+suffix

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT',)
    options,  args = parser.parse_args()

    # デフォルト名より最適なデフォルトファイル名の推定ルーチン
    if not os.path.exists(mxname):
        name0 = SAE.find_datfile('dat')  # *.dat はかならずあるのでそれをトリガーに
        if not name0 is None:
            name = name0
            mxname = name+suffix

    # オプションでファイル名を入力した時
    if options.INPUT:
        mxname = options.INPUT
        name = re.sub('\.out$','',mxname)
        mxname = name+suffix

    if len(args) > 0:
        name=args[0]
        name = re.sub('\.out$','',name)

    mxname = name+suffix


    # *.out が存在しないとき、かつ *.dat ファイルが存在するとき
    # dat ファイルの中身を読んで systemname (*.out)を検索する
    if not os.path.exists(name+'.out'):
        if os.path.exists(name+'.dat'):
            dat = SAE.ReadMxDat(name+'.dat')
            sysname = dat.get_title()
            name = sysname
            mxname = name+suffix
        else:
            sys.exit("STOP: "+name+'.out and '+name+'.dat file not found.')

    # 計算途中での DFTSCF ファイル読み込み or 通常の *.out ファイル読み込み
    module_name = 'StructureAnalysisEnvironment'
    if not os.path.exists(mxname):
        mxname = name+'.DFTSCF'
        class_name = 'ReadMxDftscf'
        FLAG_DFTSCF=True
    else:
        FLAG_DFTSCF=False
        class_name = 'ReadMxOut'

    # makes instance
#   module = __import__(module_name,globals(),locals(),[class_name],-1)
    # module の動的ロード
    try:
        # このリフレクションは python2 方式なので注意
        module = __import__(module_name, globals(), locals(), [class_name], -1)
    except:
        # for Python3
        module = __import__(module_name, fromlist=[class_name])

    # class の動的ロード
    klass = getattr(module,class_name)
    out = klass(mxname)

    n_ion_loop = out.get_n_ion_loop()
    max_n_scf = out.get_max_n_scf()
    utot = out.get_utot()
    uele,uele_index = out.get_uele()

    y=[]
    x=[]
    i=0
    for md in range(n_ion_loop):
       #print "# md =",md+1
        for scf in range(uele_index[md]):
           #print "    %14.11f" %(uele[md,scf])
            x.append(i)
            y.append(uele[md,scf])
           #print x[i], y[i]
            i+=1

    # MDループが途中で終わっているとき(DFTSCFファイルが存在するとき)
    if FLAG_DFTSCF:
        md = n_ion_loop
        for scf in range(uele_index[md]):
            x.append(i)
            y.append(uele[md,scf])
           #print x[i], y[i]
            i+=1

    ############################################################################
    # matplotlib

    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size']         = 20  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize']   = 18  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']    = 1.5 # 軸の太さを設定。目盛りは変わらない

#   plt.figure(figsize=(横, 縦), dpi=解像度, facecolor=背景色)

    plt.axes([ 0.130,0.130, 0.80,0.80 ])   # 原点(x,y), 幅(x,y)

    plt.plot(x,y, color="red", linewidth=2, label='Total Energy')
    plt.ylabel("Band Energy [Hartree]", fontsize=20 )
    plt.xlabel("Total Loop ( ION Loop & SCF Loop) [n]", fontsize=20 )
#   plt.xlabel("Total Loop ( Total SCF(&ION) loop ) [n]", fontsize=20 )

    plt.savefig("convergeION.eps")
    plt.savefig("convergeION.pdf")
    plt.savefig("convergeION.png")

    plt.show()

    plt.close('all')

