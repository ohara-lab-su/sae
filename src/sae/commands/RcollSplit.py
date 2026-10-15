#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.rmcpot.cfg_fields import RmcConfigFields
from sae.rmcpot.cfg_writer import RmcConfigWriter

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# RcollSplit.py
#   *_coll.cfg ファイルを分割する方式で出力
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2014.11.18
#     ライブラリ化
#
# 2014.10.01 - 2014.10.28
#    split *_coll.cfg and convert VASP format
#     ループごとにファイル分割する方式で無理やり出力
#   
#    2014.10.28
#        引数処理のバグを修正
#   
#    2014.10.09
#        引数処理(入力ファイル名の入力)
#   
#    2014.10.01
#        1st version
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

#                                                                                         
################################################################################
#import SpaceGroupEnvironment as SGE 
#import sys
#import os
#from numpy import *
#from LIB_vasp.read_cfg_coll_param import *
#from LIB_vasp.read_cfg_coll import *
#from LIB_vasp.print_cfg import *
################################################################################
# *_coll.cfg (RMC_POT) ファイル読み込み準備
# *_coll.cfg (RMC_POT) ファイル読み込み準備
#atoms         = np.zeros((nion),dtype='S2')  # 原子種毎の原子の数の保存
# *_coll.cfg (RMC_POT) ファイル読み込み
# ループごとの出力
if __name__ == "__main__":
    cname = "igzo_coll"
    nloop, natom, nion = RmcConfigFields().read_cfg_coll_param(cname)
    # 基本並進ベクトル
    t = np.zeros((3, 3))
    # 原子種毎の原子の数の保存
    atoms = np.zeros(nion, dtype=int)
    # 原子の通し番号に対してのサイト番号の保存
    ion_site = np.zeros(natom, dtype=int)
    # 原子位置(loop,全原子のインデックス)
    position_loop = np.zeros((nloop, natom, 3))
    header, comment, scale, direct = RmcConfigFields().read_cfg_coll(
        cname, nloop, t, natom, nion, atoms, ion_site, position_loop
    )
    # *.cfg 形式でファイルへ書き出し
    #SAE.print_cfg(name,STD,comment,t,natom,nion,atoms,position)
    for loop in range(nloop):
        name = cname + "_" + str(loop)
        print("split --> " + name)
        position = np.zeros((natom, 3))
        for ion in range(natom):
            position[ion, 0] = position_loop[loop, ion, 0]
            position[ion, 1] = position_loop[loop, ion, 1]
            position[ion, 2] = position_loop[loop, ion, 2]
        STD = False
        RmcConfigWriter().print_rmcpot_cfg(
            name, STD, comment, t, natom, nion, atoms, position
        )
