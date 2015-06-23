#!/usr/bin/env python
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#  MD(xyz) 形式の読み込み(テスト)
#   OpenMX の *.md 出力ファイル(および汎用 xyz(md) 形式)
#
# [in]     cname         : MD ファイル( xyz 形式 ) ファイル名
# [in]     loop:         : トータルのループ数
# [in]     natom         : トータルの原子数
# [in/out] atoms_index_j : atoms_index (サイト番号で元素記号を返す) の全原子番号版
#                        : 全通し番号から元素名を返す
#
# [return] natom : (セル内)トータルの原子数
# [return] nloop : トータルのループ数
#
################################################################################
#
# 2015.06.16
#   *.md ファイル自動取得ルーチンを追加
#
# 2015.01.07
#   MXreadMD.py に分離整理
#
# 2015.01.07
#   Library: read_md2(): 座標(x,y,z) + フォース(x,y,z) 形式に対応
#
# 2014.11.18 1st
#   Library: read_md():  xyz 情報の読み込み
#
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

#import sys
import optparse
import os
#import re
#from numpy import *
import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE


################################################################################
if __name__ == '__main__':

    name = 'openmx'
    suffix = 'md'  # dot を付けない
    MD = name+'.'+suffix

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input',dest='INPUT', )
    options,  args = parser.parse_args()

    # デフォルト名より適切なデフォルトファイル名の推定ルーチン
    if not os.path.exists(MD):
        name0 = SAE.find_datfile('md')
        if not name0 == None:
            name = name0
            MD = name+'.'+suffix

    if options.INPUT:
        MD=options.INPUT

    if len(args) > 0:
        MD=args[0]

    # MD(xyz) ファイルの事前読み込み
    nloop,natom = SAE.read_md_param(MD)

    # MD(xyz) ファイルの事前準備
    atoms_index_j  = np.zeros((natom),dtype='S2')  # 通し番号(max=atom)で元素名(記号)を保存する
    position_loop = np.zeros((nloop,natom,3))
    force_loop = np.zeros((nloop,natom,3))

    print "NLOOP :",nloop
    print "NATOM :",natom

    # MD(xyz) ファイル読み込み + Force 対応
    natom,nlist = \
            SAE.read_md2(MD,nloop,atoms_index_j,position_loop,force_loop)

    print nlist

    if nlist >= 7:
        for l in range(nloop):
            print "------- LOOP "+str(l)+" ------"
            for j in range(natom):
                print " %3s %12.8f %12.8f %12.8f  %12.8f %12.8f %12.8f" \
                      % ( atoms_index_j[j],\
                          position_loop[l,j,0],\
                          position_loop[l,j,1],\
                          position_loop[l,j,2],\
                          force_loop[l,j,0],\
                          force_loop[l,j,1],\
                          force_loop[l,j,2] )
    else:
        for l in range(nloop):
            print "------- LOOP "+str(l)+" ------"
            for j in range(natom):
                print " %3s %12.8f %12.8f %12.8f " \
                      % ( atoms_index_j[j],\
                          position_loop[l,j,0],\
                          position_loop[l,j,1],\
                          position_loop[l,j,2] )

