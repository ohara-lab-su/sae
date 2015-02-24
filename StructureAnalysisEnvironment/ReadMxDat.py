#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OpenMX 3.7 *.dat 形式ファイル 読み込み class
#
#  ReadDatMx (ReadMxDat)
#    *.dat 名の重複があるので DatMx とする( 例 RMC_POT の *.dat 形式 )
#    ==> MxDat へルール変更
#
################################################################################
#
# 2015.02.24
#  *.dat / *.out 共通method (主に *.dat 部分) を ReadMxDatMethod.py へ
#  分離し、そちらをスーパークラスとする。class ReadMxDat ではsuperclass
#  を継承してそれら method を実装する形にする。
#
# 2015.02.24
#   spin チェックmethod
#
# 2015.02.17
#  get_position_max(), get_position_min 追加
#   position[atom,3] のそれぞれ x,y,z の最大値を返す
#
# 2015.02.17
#  get_t() を初めいくつかの method で *.dat のコメントアウト処理に正しく
#  対応してなかったため意図しない動作になっていたのを修正
#
# 2015.02.17
#  Al-Si111-ESM.dat が正しく読めないエラー
#  ReadDatMx class, get_t, get_position のバグ(仕様)を修正
#
# 2015.02.17
#  get_fix() も get_position() と同様に atoms_index の順番に合わせる
#
# 2015.02.17
#  get_atom() の新方式に合わせて get_position() の順番もソートしなおして
#  atoms_index に矛盾なく並べ直した情報を返すように変更
#
#  オリジナルの順番とatoms_indexに合わせてソートしなおした配列の対応は
#  get_position() 後の self.position_index にてアクセス可能
#
# 2015.02.16
#  get_atom() の分類方法を変更
#   古: 連続して並んでいる元素記号のみを一つのサイトとしてひとくくりにした
#   新: atoms_index (Atomic.Species タグ) の情報のみでサイトのグルーピング
#
# 2015.02.12 1st
#
#  注意)
#     get_fix() は必ず get_position() の後に実行する
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014,2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.9"
################################################################################

import sys
import os
#import re
import gzip
#import numpy as np
import optparse 

import StructureAnalysisEnvironment as SAE

################################################################################
class ReadMxDat(SAE.ReadMxDatMethod):

    ###############################################
    ## init and Read POSCAR
    def __init__(self,datname):

        if os.path.exists(datname):
            GZIP=False
        elif os.path.exists(datname+".gz"):
            GZIP=True
        else:
            sys.exit("STOP: "+datname+" or "+datname+".gz file not found")

        try:
            if GZIP:
                tmp = gzip.open(datname+".gz")
            else:
                tmp = open(datname)

            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: "+datname+" does'nt open")
        finally:
            tmp.close()

        self.datlines = datfile.split('\n')
        self.num = int(len(self.datlines)) -1



################################################################################
if __name__ == '__main__':

    name = 'openmx.dat'
    parser = optparse.OptionParser()
    parser.add_option( '-i','--input',
                        dest='INPUT',
                        default=name,
                        )
    options, args = parser.parse_args()
    name = options.INPUT

    dat = ReadMxDat(name)

    title = dat.get_title()
    nion = dat.get_nion()
    natom = dat.get_natom()
    atoms = dat.get_atoms()
    atoms_index = dat.get_atoms_index()
    scale = dat.get_scale()
    t = dat.get_t()
    selective = dat.get_selective()
    direct = dat.get_direct()
    position = dat.get_position()
    fix = dat.get_fix()
    position_max = dat.get_position_max()
    position_min = dat.get_position_min()

    print title
    print " ",scale

#   print ""
#   print "max_x", position_max[0]
#   print "max_y", position_max[1]
#   print "max_z", position_max[2]
#   print ""
#   print "min_x", position_min[0]
#   print "min_y", position_min[1]
#   print "min_z", position_min[2]
    if dat.FLAG_t:
        print "  %13.9f %13.9f %13.9f" %( t[0,0],t[1,0],t[2,0] )
        print "  %13.9f %13.9f %13.9f" %( t[0,1],t[1,1],t[2,1] )
        print "  %13.9f %13.9f %13.9f" %( t[0,2],t[1,2],t[2,2] )
    else:
        t[1,0] = 0.0
        t[2,0] = 0.0
        t[0,1] = 0.0
        t[2,1] = 0.0
        t[0,2] = 0.0
        t[1,2] = 0.0
        t[0,0] = abs(position_max[0]-position_min[0])*1.20
        t[1,1] = abs(position_max[1]-position_min[1])*1.20
        t[2,2] = abs(position_max[2]-position_min[2])*1.20
        print "  %13.9f %13.9f %13.9f" %( t[0,0],t[1,0],t[2,0] )
        print "  %13.9f %13.9f %13.9f" %( t[0,1],t[1,1],t[2,1] )
        print "  %13.9f %13.9f %13.9f" %( t[0,2],t[1,2],t[2,2] )

    print " ",
    for i in range(nion):
        print atoms_index[i],
    print " "

    print " ",
    for i in range(nion):
        print atoms[i],
    print " "

    if selective:
        print "Selective Dynamics"
    if direct:
        print "Direct"
    else:
        print "Cartesian"

    for i in range(natom):
        print " %13.9f %13.9f %13.9f" \
                % ( position[i,0],position[i,1],position[i,2] ),
        if selective:
            print "",
            print fix[i,0],fix[i,1],fix[i,2],
        print ""


#   for i in range(natom):
#       print fix[i][0], fix[i][1], fix[i][2]

