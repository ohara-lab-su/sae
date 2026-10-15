#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.geometry.coordinates import CoordinateTransforms
from sae.rmcpot.cfg_fields import RmcConfigFields

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 結晶構造の描画プログラム+アニメーション
#  RplotCrystal.py
#
#     RMC_POT (*.cfg) 形式を入力とする、変換なしの直接描画ソフト
#      ---> VASPの名前を冠した変換ルーチンを読んでいないだけで
#           やっている内容は VASP の変換ルーチンと一緒
#
################################################################################
#
# 2018.08.23
#  Python2/3 両対応
#
# 2015.02.27
#  conv_direct2car --> conv_direct2car0
#
# 2014.11.18
#   xyz(MD)形式ファイルを読み込んでプロットする形に VplotCrystal.py を改変
#   改変というよりは簡略化
#
# 2014.11.16 1st (VplotCrystal.py)
#    vpython,wxpython 利用
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
import visual as vp
import wx

#
################################################################################
#from __future__ import division
#import sys
#import os
#import re
#import optparse
#from copy import deepcopy
#import SpaceGroupEnvironment as SGE
################################################################################
############################################
###########################################
###########################################
# *.cfg (RMC_POT) ファイル読み込み準備
# *_coll.cfg (RMC_POT) ファイル読み込み準備
# *_coll.cfg (RMC_POT) ファイル読み込み
# 座標系を記述する他に RMC の t 行列を基本並進に拡張
# ベクトルの長さが倍になるので比率を1/2 にして、中心を中心へずらす
# Direct (RMC_POTのcfgはDirect Coordinate)
#   for j in range(natom):
#       print " %14.10f %14.10f %14.10f " \
#             % ( position[j,0],\
#                 position[j,1],\
#                 position[j,2] )
# Direct to Cartesian 変換
#   for j in range(natom):
#       print " %14.10f %14.10f %14.10f " \
#             % ( position[j,0],\
#                 position[j,1],\
#                 position[j,2] )
############################################################################
# 結晶描画の基礎プログラム
# VPython のフレーム作成
# 結晶描画の単位胞の座標原点
# 単位胞の描画ルーチン
# 結晶の描画
if __name__ == "__main__":
    app = wx.App(True, None)
    frame0 = wx.Frame(None, -1, "Plot_Crystal")
    frame0.Show()
    cname = "igzo"
    print("INPUT file name   :", cname)
    natom, nion = RmcConfigFields().read_cfg_param(cname)
    # 基本並進ベクトル
    t = np.zeros((3, 3))
    # 原子種毎の原子の数の保存
    atoms = np.zeros(nion, dtype=int)
    # 原子種毎の原子の種類番号の保存(仮)
    atoms_j = np.zeros(natom, dtype=int)
    # 原子位置(loop,全原子のインデックス)
    position = np.zeros((natom, 3))
    header, comment = RmcConfigFields().read_cfg(cname, t, atoms, atoms_j, position)
    t1_x = t[0, 0] * 2.0
    t1_y = t[1, 0] * 2.0
    t1_z = t[2, 0] * 2.0
    t2_x = t[0, 1] * 2.0
    t2_y = t[1, 1] * 2.0
    t2_z = t[2, 1] * 2.0
    t3_x = t[0, 2] * 2.0
    t3_y = t[1, 2] * 2.0
    t3_z = t[2, 2] * 2.0
    x_offset = 0.5
    y_offset = 0.5
    z_offset = 0.5
    for i in range(natom):
        position[i, 0] = position[i, 0] / 2.0 + x_offset
        position[i, 1] = position[i, 1] / 2.0 + y_offset
        position[i, 2] = position[i, 2] / 2.0 + z_offset
    ABS = False
    scale = 1.0
    direct = True
    CoordinateTransforms().conv_direct2cara(ABS, scale, t, natom, direct, position)
    f = vp.frame()
    O = [-3, -3, 0]
    R = 0.03
    # white
    C = [255, 255, 2555]
    crystal_make_unit(t, O, R, C)
    RATIO = 0.3
    # 描画の原点位置修正
    # 原子の色設定(RGB)を適当に自動化(ファクターは適当なので適当に変えること)
    for ion in range(natom):
        xp = position[ion, 0] + O[0]
        yp = position[ion, 1] + O[1]
        zp = position[ion, 2] + O[2]
        atom = vp.sphere(frame=f, pos=(xp, yp, zp), radius=0.2)
        factor = 5
        num = atoms_j[ion] + 1 + atoms_j[ion] + 1 + atoms_j[ion] + 1
        num = factor * num
        print(ion, num)
        atom.red = 0.05 * num
        atom.green = 0.01 * num * num
        atom.blue = 10 / num
