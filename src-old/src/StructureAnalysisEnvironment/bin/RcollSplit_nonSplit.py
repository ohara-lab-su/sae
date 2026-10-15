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
from __future__ import print_function
################################################################################

import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

#import sys
#import os

#from numpy import *
#from LIB_vasp.read_cfg_coll_param import *
#from LIB_vasp.read_cfg_coll import *

###################################################################################
if __name__ == '__main__':

    cname='igzo_coll'

    # *_coll.cfg (RMC_POT) ファイル読み込み準備
    nloop,natom,nion = SAE.read_cfg_coll_param(cname)

    # *_coll.cfg (RMC_POT) ファイル読み込み準備
    t             = np.zeros((3,3))              # 基本並進ベクトル
   #atoms         = np.zeros((nion),dtype='S2')  # 原子種毎の原子の数の保存
    atoms         = np.zeros((nion),dtype=int)   # 原子種毎の原子の数の保存
    atoms_site    = np.zeros((natom),dtype=int)  # 原子の通し番号に対してのサイト番号の保存
    position_loop = np.zeros((nloop,natom,3))    # 原子位置(loop,全原子のインデックス)

    # *_coll.cfg (RMC_POT) ファイル読み込み
    SAE.read_cfg_coll(cname,nloop,t,natom,nion,atoms,atoms_site,position_loop)

