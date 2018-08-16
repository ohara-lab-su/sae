#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com, kengo.nakada@spring8.or.jp
#
# vasprun.xml ファイルを適当な情報から作成するルーチン
#
#   *.xyz or * .md ファイルを vasprun.xml へコンバート
#
#   vasprun.xml で用いる基本並進(simulation box サイズと形状)
#   を手動で変更する必要があるので注意
#
#  注意)
#    OpenMX 専用版: MXmd2vasprun.py  (simulation box 自動取得)
#    汎用 *.md 版 : md2vasprun.py
#
################################################################################
#
# 2015.06.30
#  == None --> is None
#
# 2015.06.16
#  関数ライブラリを用いた read_md ではなく、ReadMd クラスの仕様へチェンジ
#
# 2015.06.16
#  ファイル名の自動取得ルーチンの追加
#
# 2015.02.24
#  デフォルトの md 名をテスト用の co.md から openmx.md へ変更
#
# 2015.02.12
#  暫定的に正しく動作するように修正( print_vasprun.py 関数の修正)
#  コメント関係(change log) を print_vasprun.py へ移行
#
#  基本的に使っている関数や方法論が古いので注意
#
# 2015.01.08 startup
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
__version__    = "0.0.4"
################################################################################

import sys
import os
import optparse
#import re

#import xml.etree.ElementTree as ET
import numpy as np
#import math

#from copy import deepcopy

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE


################################################################################
if __name__ == '__main__':

    OUTPUT = 'vasprun.xml'

#   MD_base = 'co'
    name = 'openmx'
    MD_suffix = 'md'      # ここでの suffix 指定は dot を付けない
    MD = name+'.'+MD_suffix

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT',)
    options,  args = parser.parse_args()

    # オプション処理(指定したファイルが存在してない時はsuffixをつけてみる)
    if options.INPUT:
        MD = options.INPUT
        if not os.path.exists(MD):
            MD = MD+'.'+MD_suffix

    # デフォルト名 or 入力名が存在しない時の入力ファイル名自動探索
    if not os.path.exists(MD):
        name0 = SAE.find_datfile(MD_suffix)
        if not name0 is None:
            name = name0
            MD = name+'.'+MD_suffix
        else:
            sys.exit("STOP: "+MD+" not found.")

    # オプション指定なしのコマンドライン引数は全てに優先して明示的に指定
    if len(args) > 0:
        MD=args[0]

    print "INPUT :",MD
    print "OUTPUT:",OUTPUT

    title = MD

#################################################### OLD version ###############
#   # MX(xyz) ファイルの事前読み込み
#   nloop,natom = SAE.read_md_param(MD)

#   # MD(xyz) ファイルの事前準備
#   atoms_index_j  = np.zeros((natom),dtype='S2')
#   position_loop = np.zeros((nloop,natom,3))
#   force_loop = np.zeros((nloop,natom,3))

#   # MD(xyz) ファイル読み込み + Force 対応
#   natom,nlist,elist,nion,atoms,atoms_index,energy_loop = \
#               SAE.read_md3(MD,nloop,atoms_index_j,position_loop,force_loop)
################################################################################

    md = SAE.ReadMd(MD)

    natom = md.get_natom()
    nion  = md.get_nion()
    nloop = md.get_nloop()
    atoms_index_j = md.get_atoms_index_j()
    atoms_index = md.get_atoms_index()
    atoms = md.get_atoms()
    energy_loop = md.get_energy_loop()
    position_loop = md.get_position_loop()
    selective = md.get_selective()
    force_loop = md.get_force_loop()

    # MD(x,y,z) のそれぞれの x,y,z の最大値を取得
    position_max,position_min = SAE.get_max_md(nloop,natom,position_loop)
    max_range = abs(position_min)+position_max
#   box_size = max_range*2.0
    box_size = 10.0

    # 分子/原子を収納する箱を作る。ダミーの基本並進ベクトル作成(cubic)
    #       t0 = a00 a10 a20  ! lattice vector t0
    #       t1 = a01 a11 a21  ! lattice vector t1
    #       t2 = a02 a12 a22  ! lattice vector t2
    t = np.zeros((3,3))
    t[0,0] = 1.0*box_size
    t[1,1] = 1.0*box_size
    t[2,2] = 1.0*box_size
    scale = 1.0

    # MD(x,y,z) の座標系をcartesian基本並進系に変換する
    # MD(直交系)からVASP(直交系)への変換なのでスケールするだけ
    # using numpy
    # 注意) VASP のデーターから引っ張った時は逆に scale でスケールされてないので
    #       box_size で割ってはいけない
    position_loop = position_loop/box_size
#   position_loop = position_loop

    # position の initial と final を分けておく
#   for l in range(nloop):
#       print natom
#       print "   setp=",l
#       for j in range(natom):
#           print " %3s %12.8f %12.8f %12.8f " \
#                 % ( atoms_index_j[j],\
#                     position_loop[l,j,0],\
#                     position_loop[l,j,1],\
#                     position_loop[l,j,2] )

    # vasprun.xml の最低出力をする(OpenMX *.md 形式から引き出せる最低の形式)
    SAE.print_vasprun0(OUTPUT,title,nloop,\
            natom,nion,atoms,atoms_index,atoms_index_j,\
            t,position_loop,force_loop,energy_loop)


