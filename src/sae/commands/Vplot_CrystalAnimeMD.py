#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.openmx.md_fields import MolecularDynamicsFields
from sae.structure.elements import ElementTable

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 結晶構造の描画プログラム+アニメーション
#  VplotCrystalMD.py
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.01.07
#  コマンドラインから引数処理をしてなかったので追加
#
# 2014.11.18
#   xyz(MD)形式ファイルを読み込んでプロットする形に VplotCrystal.py を改変
#   --> 改変というよりはコード自体の簡略化
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
__copyright__ = "Copyright 2014,2015, Kengo NAKADA"
__license__ = "MIT"
import wx
import numpy as np
import visual as vp
import optparse


#
################################################################################
#from __future__ import division
#import SpaceGroupEnvironment as SGE
#from crystal_make_unit import *
#import sys
#import os
#import re
#from copy import deepcopy
#from numpy import *
#from visual import *
################################################################################
def options():
    # default name
    XYZ = "C60_position.xyz"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT", default=XYZ)
    options, args = parser.parse_args()
    if options.INPUT:
        XYZ = options.INPUT
    if len(args) > 0:
        XYZ = args[0]
    return XYZ


################################################################################
############################################
###########################################
#cname = 'C60_position.xyz'
###########################################
# MD(xyz) ファイルの事前読み込み
# MD(xyz) ファイルの事前準備
# MD(xyz) ファイル読み込み
#   for l in range(nloop):
#       print "------- LOOP "+str(l)+" ------"
#       for j in range(natom):
#           print " %3s %14.10f %14.10f %14.10f " \
#                 % ( atoms_index_j[j],\
#                     position_loop[l,j,0],\
#                     position_loop[l,j,1],\
#                     position_loop[l,j,2] )
############################################################################
# 結晶描画の基礎プログラム
# 複数のオブジェクトをまとめるためにフレームを作る
# 結晶描画の単位胞の座標原点
# 単位胞の描画ルーチン
#   crystal_make_unit(t,O,R,C)
if __name__ == "__main__":
    app = wx.App(True, None)
    frame0 = wx.Frame(None, -1, "Plot_Crystal")
    frame0.Show()
    cname = options()
    print("INPUT file name   :", cname)
    nloop, natom = MolecularDynamicsFields().read_md_param(cname)
    position_loop = np.zeros((nloop, natom, 3))
    print("NLOOP :", nloop)
    print("NATOM :", natom)
    # 通し番号(max=atom)で元素名(記号)を保存する
    atoms_index_j = np.zeros(natom, dtype="S2")
    # 原子のx,y,z 座標
    position_loop = np.zeros((nloop, natom, 3))
    MolecularDynamicsFields().read_md(cname, nloop, atoms_index_j, position_loop)
    f = vp.frame()
    O = [-3, -3, 0]
    R = 0.05
    # white
    C = [255, 255, 2555]
    RATIO = 0.3
    # 結晶の描画
    # アニメーション速度の設定(loop 内のatomの描画が終わったらアニメ)
    # 描画が終わったら前回の画像をクリア(これをしないとアニメが残像になる)
    for loop in range(nloop):
        # 描画の原点位置修正
        # 原子の種類を取得
        # 原子半径を取得
        # 原子番号を取得
        # 原子の色設定(RGB)を適当に自動化
        for ion in range(natom):
            xp = position_loop[loop, ion, 0] + O[0]
            yp = position_loop[loop, ion, 1] + O[1]
            zp = position_loop[loop, ion, 2] + O[2]
            atom_type = str(atoms_index_j[ion])
            radius = ElementTable().get_atomic_radius1(atom_type)
            R = radius * RATIO
            num = ElementTable().get_atomic_number1(atom_type)
            atom = vp.sphere(frame=f, pos=(xp, yp, zp), radius=R)
            atom.red = 0.5 * num * num
            atom.green = 0.1 * num
            atom.blue = 1 / num
        vp.rate(10)
        for obj in f.objects:
            obj.visible = 0
