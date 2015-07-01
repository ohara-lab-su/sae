#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com, kengo.nakada@spring8.or.jp
#
# vasprun.xml ファイルを適当な情報から作成するルーチン
#
#   OpenMX の *.md ファイルを vasprun.xml へコンバート
#   基本並進情報を *.out or *.dat から取得
#
#  注意)
#    OpenMX 専用版: MXmd2vasprun.py
#    汎用 *.md 版 : md2vasprun.py
#
################################################################################
#
# 2015.06.30
#  == None --> is None
#
# 2015.06.16
#  VASP --> OpenMX (cartesian) 変換した後の計算結果を vasprun.xml に乗せるとき
#  は scale 1.0 の基本並進をそのまま用いるときは direct --> cartesian すると
#  うまくいく。
#
# 2015.06.16
#  MXmd2vasprun.py と md2vasprun.py を明確にブランチ
#
# 2015.06.16
#   汎用の *md ファイルではなくて openMX の *md ファイル専用にチェンジ
#   (もともとの基本並進情報を *.dat *.out から取得)
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

    name = 'openmx'
    MD_suffix = 'md'      # ここでの suffix 指定は dot を付けない
    MD = name+'.'+MD_suffix

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT',)
    options,  args = parser.parse_args()

    # オプション処理(指定したファイルが存在してない時はsuffixをつけてみる)
    # 指定したファイルが存在したときは suffix を外した名前を作成する
    if options.INPUT:
        MD0 = options.INPUT
        if not os.path.exists(MD0):
            MD = MD0+'.'+MD_suffix
            if os.path.exists(MD):
                name = MD0
            else:
                sys.exit("STOP: INPUT "+MD0+" file not found.")
        else:
            name = MD0.replace('.'+MD_suffix,'')
            MD = MD0

    # オプション指定なしのコマンドライン引数は全てに優先して明示的に指定
    if len(args) > 0:
        MD=args[0]
        name = MD.replace('.'+MD_suffix,'')

    # デフォルト名 or 入力名が存在しない時の入力ファイル名自動探索
    if not os.path.exists(MD):
        name0 = SAE.find_datfile(MD_suffix)
        if not name0 is None:
            name = name0
            MD = name+'.'+MD_suffix
        else:
            sys.exit("STOP: "+MD+" not found.")

    print "INPUT :",MD
    print "OUTPUT:",OUTPUT

    title = MD

    # MD ファイル読み込み
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

    # dat or out ファイル読み込み
    # 基本並進ベクトルとスケールファクターの入手が主目的
    if os.path.exists(name+'.dat'):
        file_name = name+'.dat'
        class_name = 'ReadMxDat'
    elif os.path.exists(name+'.out'):
        file_name = name+'.out'
        class_name = 'ReadMxOut'
    else:
        sys.exit("STOP: "+name+".out or "+name+".dat file not fond")

    module_name = 'StructureAnalysisEnvironment'
    module = __import__(module_name,globals(),locals(),[class_name],-1)
    klass = getattr(module,class_name)

    out = klass(file_name)
    t = out.get_t()
    scale = out.get_scale()
    direct = out.get_direct()

    if not direct:
        for loop in range(nloop):
            SAE.conv_car2direct(scale,t,natom,direct,position_loop[loop,:,:])


    ################ output ######################
    print ""
    print "TITLE = ",title
    print "NLOOP = ",nloop
    print "NATOM = ",natom
    print "NION  = ",nion
    print "SCALE = ",scale
    print "ATOM"
    print "  ",
    for atom in range(nion):
        print atoms_index[atom],
    print ""
    print "  ",
    for atom in range(nion):
        print atoms[atom],
    print ""

    print ""
    print t

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


