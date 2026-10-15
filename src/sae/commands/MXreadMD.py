#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.common.paths import FileDiscovery
from sae.openmx.md_fields import MolecularDynamicsFields

#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# 2018.08.17
#  Python2/3 両対応
#
# 2015.06.30
#  == None --> is None
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
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import optparse
import os
import numpy as np

#
################################################################################
#import sys
#import re
#from numpy import *
#import SpaceGroupEnvironment as SGE
################################################################################
# デフォルト名より適切なデフォルトファイル名の推定ルーチン
# MD(xyz) ファイルの事前読み込み
# MD(xyz) ファイルの事前準備
# MD(xyz) ファイル読み込み + Force 対応
if __name__ == "__main__":
    name = "openmx"
    # dot を付けない
    suffix = "md"
    MD = name + "." + suffix
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    if not os.path.exists(MD):
        name0 = FileDiscovery().find_datfile("md")
        if not name0 is None:
            name = name0
            MD = name + "." + suffix
    if options.INPUT:
        MD = options.INPUT
    if len(args) > 0:
        MD = args[0]
    nloop, natom = MolecularDynamicsFields().read_md_param(MD)
    # 通し番号(max=atom)で元素名(記号)を保存する
    atoms_index_j = np.zeros(natom, dtype="S2")
    position_loop = np.zeros((nloop, natom, 3))
    force_loop = np.zeros((nloop, natom, 3))
    print("NLOOP :", nloop)
    print("NATOM :", natom)
    natom, nlist = MolecularDynamicsFields().read_md2(
        MD, nloop, atoms_index_j, position_loop, force_loop
    )
    print(nlist)
    if nlist >= 7:
        for l in range(nloop):
            print("------- LOOP " + str(l) + " ------")
            for j in range(natom):
                print(
                    " %3s %12.8f %12.8f %12.8f  %12.8f %12.8f %12.8f"
                    % (
                        atoms_index_j[j],
                        position_loop[l, j, 0],
                        position_loop[l, j, 1],
                        position_loop[l, j, 2],
                        force_loop[l, j, 0],
                        force_loop[l, j, 1],
                        force_loop[l, j, 2],
                    )
                )
    else:
        for l in range(nloop):
            print("------- LOOP " + str(l) + " ------")
            for j in range(natom):
                print(
                    " %3s %12.8f %12.8f %12.8f "
                    % (
                        atoms_index_j[j],
                        position_loop[l, j, 0],
                        position_loop[l, j, 1],
                        position_loop[l, j, 2],
                    )
                )
