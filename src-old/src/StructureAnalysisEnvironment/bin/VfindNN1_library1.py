#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# VfindNN1.py の Library 化(途中バージョン version 1 )
#   関数化の２番目のテスト(ライブラリ化したものを呼び出す
#   実用的に使えない
#
################################################################################
# find Nearest Neighbor
#   （範囲指定）近接原子一覧表示
#     引数に与えた原子間距離の範囲で近接原子一覧を表示
#     原子種の指定は -a オプション
#     もしくは距離範囲は -d オプションでも指定可能
#
#     ゾーンバウンダリーも考慮している
#     元セルの番号で表示
#
#     (もともとは RMC_POT 用)
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.02.27
#  conv_direct2car --> conv_direct2car0
#
# 2014.10.30 Library 化 1st
#  VfindNN1_librar1.py
#    Libray 化開発の中心を LIB_vasp.py を移行(完全分離)
#    派生系で Vdirect2car.py を別途作成
#
# 2014.10.30 Library 化 1st
#   VfindNN1_library0.py
#     Library 化の第一歩(機能の一部を部分的に関数化)
#
# 2014.10.15 (10:58 スクリプトとしては一応完成、実用的に閉じて使える)
#  VfindNN1.py
#    VmakeSuperCell2.py をベースにしてスーパーセル作成パートを正常化
#    スーパーセルを作り、正しく動作するようにした
#
# 2014.10.09
#   VfindNN1.py
#
#     1) 遠くの原子を検索しない(検索距離の指定)
#        --> ゾーン境界のスーパーセル化を念頭として
#            特定空間内での小さいソートMatrixの作成のための部品作り
#
#     2) 検索距離内のunit-cell外の原子の探索
#
#     問題点) ゾーン境界で正しく動作しない
#     原因)   スーパーセル化が正しく動作してない
#
# 2014.10.09
#   VfindNN0.py
#
#    vasp POSCAR format 対応
#    1) VASP のみ対応
#    2) 特定の原子の近接原子一覧出力のみ対応(すべて表示)
#
#    *) 周期境界条件は考慮しない("端"の原子の近接はひとつの箱のなかだけ考慮)
#
################################################################################
from __future__ import print_function
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"
################################################################################

import sys
import os
import optparse
import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

#import re
#from copy import deepcopy

################################################################################
def options():

    ###############################################
    ## default parameter
    ##
    cname  = "POSCAR" # OUTPUT BASE filename
    POSCAR = "POSCAR" # INPUT (BASE) filename

    distance = "2.5"  # 検索する領域

    find = 1   # (元のセルで)通しでn番目の原子(1から始まるindex)からの近接原子検索

    ###############################################
    ## optparse
    ##
    parser = optparse.OptionParser()

    parser.add_option(  '-i','--input',
                        dest='INPUT',
                        default=POSCAR,
    )
    parser.add_option(  '-o','--output',
                        dest='OUTPUT',
                        default=cname,
    )
    parser.add_option(  '-a','--atom',
                        dest='NN',
                        default=find,
    )
    parser.add_option(  '-d','--distance',
                        dest='DISTANCE',
                        default=distance,
    )
    options,  args = parser.parse_args()

    if options.INPUT:
        POSCAR=options.INPUT

    if options.OUTPUT:
        cname=options.OUTPUT

    if options.NN:
        find=int(options.NN)

    if options.DISTANCE:
        distance=float(options.DISTANCE)

    #print args,options
    if len(args) > 0:
        #print "script name:",argvs[0]
        #POSCAR=argv[0]
        distance = float(args[0])

    if not os.path.exists(POSCAR):
        if os.path.exists(POSCAR+".vasp"):
            POSCAR="POSCAR.vasp"
        else:
            sys.exit(POSCAR+" file not found")

    print("INPUT file name    : %s" % str(POSCAR))
    print("OUTPUT file name   : %s" % str(cname+"_nn_"+str(find)+".out"))
    print("SEARCH DISTANCE    : %s" % str(distance))
    print("")

    return [POSCAR,cname,distance,find]


################################################################################
if __name__ == '__main__':

    # Default & OptionParser
    POSCAR,cname,distance,find = options()

    # POSCAR の事前読み込み
    nion,natom,VASP = SAE.read_poscar_param(POSCAR)

    # POSCAR 読み込みのための準備
    t           = np.zeros((3,3))
    atoms       = []
    atoms_index = []
    ion         = np.zeros(natom)
    ion_local   = np.zeros(natom)
    position    = np.zeros((natom,3))
    fix         = np.zeros((natom,3),dtype='S')

    # POSCAR の読み込み
    title,scale,selective,direct = \
       SAE.read_poscar(POSCAR,VASP,t,atoms,atoms_index,ion,ion_local,position,fix)

    # Direct to Cartesian
    if direct:
       #ABS=False # for VASP
        ABS=True  # for SuperCell
        scale,direct = SAE.conv_direct2cara(ABS,scale,t,natom,direct,position)

    if direct:
        sys.exit("Error: current mode is Direct")

    # supercell_zb 作成準備(1)
    super        = int(3*3*3)
    sv           = np.zeros((super,3))
    sp           = np.zeros((natom*super,3))
    ion_sp       = np.zeros(natom*super)
    ion_local_sp = np.zeros(natom*super)
    sp_j         = np.zeros(natom*super)

    # zone boundary 処理専用の super-cell
    SAE.make_supercell_zb(t,natom,nion,atoms,ion,ion_local,position,\
                          sv,ion_sp,ion_local_sp,sp_j,sp)

    # 近接原子間距離の計算: 特定距離内の部分空間index 作成準備
#   find_nn_distance()

################################################################################


