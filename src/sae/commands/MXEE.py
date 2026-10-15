#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
#   for i in range(n_ion_loop):
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
# MXEE
# VEE と似たようなセンス
#  (イオンステップごとのSCFのEnergy も含めて出力する)
#  OpexnMX だと
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

#
################################################################################
#import gzip
#import numpy as np
#import SpaceGroupEnvironment as SGE
################################################################################
# デフォルト名より最適なデフォルトファイル名の推定ルーチン
# dat ファイル捜索
# オプションでファイル名を入力した時
# *.out が存在しないとき、かつ *.dat ファイルが存在するとき
# dat ファイルの中身を読んで systemname (*.out)を検索する
# 計算途中での DFTSCF ファイル読み込み or 通常の *.out ファイル読み込み
# makes instance
#  module = __import__(module_name,globals(),locals(),[class_name],-1)
# module の動的ロード
# class の動的ロード
#   max_n_scf = out.get_max_n_scf()
#   uele,uele_index = out.get_uele()
if __name__ == "__main__":
    name = "openmx"
    suffix = ".out"
    mxname = name + suffix
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    if not os.path.exists(mxname):
        # *.dat はかならずあるのでそれをトリガーに
        try:
            name0 = FileDiscovery().find_datfile("dat")
            if not name0 == None:
                name = name0
                mxname = name + suffix
        except:
            pass
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
    else:
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
    utot = out.get_utot()
    #       print "***************** md = ",md+1,'**********************'
    #       print ""
    #       print "# md =",md+1
    #       for scf in range(uele_index[md]):
    #           print "    scf=%d, Uele = %14.11f" %(scf+1,uele[md,scf])
    #           print "    %14.11f" %(uele[md,scf])
    #       print " Utot = %14.11f" %(utot[md])
    for md in range(n_ion_loop):
        print(" %14.11f" % utot[md])
