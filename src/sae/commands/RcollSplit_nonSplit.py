#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.rmcpot.cfg_fields import RmcConfigFields
import numpy as np

#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#
# 2014.11.18
#
#  RcollSplit_nonSplit.py
#    1) *.cfg ファイルを LOOP 毎に分割させずに、配列にまとめて放り込む方式に変更
#    2) 関数化&分離
#
# 2014.10.01 - 2014.10.28
#   RcollSplit.py
#     split *_coll.cfg and convert VASP format
#     ループごとにファイル分割する方式で無理やり出力
#
#     2014.10.28
#         引数処理のバグを修正
#
#     2014.10.09
#         引数処理(入力ファイル名の入力)
#
#     2014.10.01
#         1st version
#
###################################################################################
################################################################################
#import SpaceGroupEnvironment as SGE
#import sys
#import os
#from numpy import *
#from LIB_vasp.read_cfg_coll_param import *
#from LIB_vasp.read_cfg_coll import *
###################################################################################
# *_coll.cfg (RMC_POT) ファイル読み込み準備
# *_coll.cfg (RMC_POT) ファイル読み込み準備
#atoms         = np.zeros((nion),dtype='S2')  # 原子種毎の原子の数の保存
# *_coll.cfg (RMC_POT) ファイル読み込み
if __name__ == "__main__":
    cname = "igzo_coll"
    nloop, natom, nion = RmcConfigFields().read_cfg_coll_param(cname)
    # 基本並進ベクトル
    t = np.zeros((3, 3))
    # 原子種毎の原子の数の保存
    atoms = np.zeros(nion, dtype=int)
    # 原子の通し番号に対してのサイト番号の保存
    atoms_site = np.zeros(natom, dtype=int)
    # 原子位置(loop,全原子のインデックス)
    position_loop = np.zeros((nloop, natom, 3))
    RmcConfigFields().read_cfg_coll(
        cname, nloop, t, natom, nion, atoms, atoms_site, position_loop
    )
