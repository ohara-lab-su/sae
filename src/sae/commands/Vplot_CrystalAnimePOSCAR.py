#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.geometry.coordinates import CoordinateTransforms
from sae.structure.elements import ElementTable
from sae.vasp.outcar_fields import OutcarFields
from sae.vasp.poscar_fields import PoscarFields

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 結晶構造の描画プログラム
#  VplotCrystal のアニメーション対応版(IONループごとのアニメ)
#
################################################################################
#
# 2018.08.15, 08.23
#  Python2/3 両対応
#
# 2015.02.27
#    conv_direct2car --> conv_direct2car0
#
# 2014.11.18
#    VplotCrystalMove.py へブランチ
#    座標系変換ルーチン作成たのめに Vforce.py Vforce2md.py を作成&マージ
#
# 2014.11.16 1st
#    VplotCrystal.py (vpython,wxpython 利用)
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import wx
import sys
import numpy as np
import visual as vp


#
################################################################################
#from __future__ import division
#import os
#import re
#import optparse
#import SpaceGroupEnvironment as SGE
#from crystal_make_unit import *
#from visual import *
#from numpy import *
#from copy import deepcopy
################################################################################
###############################################
## default parameter
##
def options():
    # OUTPUT BASE filename
    cname = "POSCAR"
    OUTCAR = "OUTCAR"
    # INPUT (BASE) filename
    POSCAR = "POSCAR"
    print("INPUT POSCAR file  :", POSCAR)
    print("INPUT OUTCAR file  :", OUTCAR)
    print("OUTPUT file name   :", cname + ".vasp")
    return [POSCAR, OUTCAR, cname]


################################################################################
############################################
# Default & OptionParser
#   POSCAR,cname = options()
############################################
# POSCAR の事前読み込み
# POSCAR 読み込みのための準備
# POSCAR の読み込み
# OUTCAR 事前読み込み
# OUTCAR 読み込み準備
# OUTCAR 読み込み
# VASP の場合はVASP5以上の書式が必要(原子番号情報が必要)
#   # Cartesian to Direct 変換
#   if direct:
#       ABS=False
#       scale,direct = conv_direct2cara(ABS,scale,t,natom,direct,position)
#   # 絶対座標系へ変換( cartesian and scale=1.0 ),引数版
#   scale = conv_car2carABSa(scale,t,natom,direct,position)
############################################################################
# 結晶描画の基礎プログラム
# 複数のオブジェクトをまとめるためにフレームを作る
#   s = display(title=title, width=800, heigh=800)
# 結晶描画の単位胞の座標原点
# 単位胞の描画ルーチン
#   crystal_make_unit(t,O,R,C)
# Ion ループごとの処理(座標変換&表示)
#####################################
#####################################
# 結晶の描画
#
if __name__ == "__main__":
    app = wx.App(True, None)
    frame0 = wx.Frame(None, -1, "Plot_Crystal")
    frame0.Show()
    cname = "POSCAR"
    POSCAR = "POSCAR"
    OUTCAR = "OUTCAR"
    print("INPUT POSCAR file  :", POSCAR)
    print("INPUT OUTCAR file  :", OUTCAR)
    nion, natom, VASP = PoscarFields().read_poscar_param(POSCAR)
    t = np.zeros((3, 3))
    atoms = []
    atoms_index = []
    ion = np.zeros(natom)
    ion_local = np.zeros(natom)
    position = np.zeros((natom, 3))
    fix = np.zeros((natom, 3), dtype="S")
    title, scale, selective, direct = PoscarFields().read_poscar(
        POSCAR, VASP, t, atoms, atoms_index, ion, ion_local, position, fix
    )
    nloop = OutcarFields().read_outcar_param(OUTCAR, natom)
    position_loop = np.zeros((nloop, natom, 3))
    force_loop = np.zeros((nloop, natom, 3))
    OutcarFields().read_outcar_position(OUTCAR, natom, nloop, position_loop, force_loop)
    if VASP < 5:
        sys.exit("STOP: VASP version < 5 ")
    f = vp.frame()
    O = [-3, -3, 0]
    R = 0.05
    # white
    C = [255, 255, 2555]
    RATIO = 0.3
    direct0 = direct
    conv = True
    # ループ数だけループ
    # 座標変換のための準備
    # アニメーション速度の設定(loop 内のatomの描画が終わったらアニメ)
    # 描画が終わったら前回の画像をクリア(これをしないとアニメが残像になる)
    for l in range(nloop):
        if conv:
            position0 = np.zeros((natom, 3))
        # すべての原子位置を描画
        # ループごとの座標変換
        # 描画の原点位置修正
        # 原子の種類を取得
        # 原子半径を取得
        # 原子番号を取得
        for i in range(natom):
            if conv:
                direct = direct0
                position0[i, 0] = position_loop[l, i, 0]
                position0[i, 1] = position_loop[l, i, 1]
                position0[i, 2] = position_loop[l, i, 2]
                ABS = False
                scale, direct = CoordinateTransforms().conv_direct2cara(
                    ABS, scale, t, natom, direct, position0
                )
                position_loop[l, i, 0] = position0[i, 0]
                position_loop[l, i, 1] = position0[i, 1]
                position_loop[l, i, 2] = position0[i, 2]
            xp = position_loop[l, i, 0] + O[0]
            yp = position_loop[l, i, 1] + O[1]
            zp = position_loop[l, i, 2] + O[2]
            atom_type = str(atoms_index[int(ion[i])])
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
