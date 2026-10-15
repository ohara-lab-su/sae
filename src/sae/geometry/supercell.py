# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# make_supercell0
# スーパーセル作成ルーチン[内部座標作成]
#
# [in]      super_x
# [in]      super_y
# [in]      super_z
#
# [in/out]  sp [natom*super,3]          : SuPer cell position 保存用のverctor
# [in/out]  ion_sp [natom*super]        : SPセルの通し番号に対する原子種番号保存index
# [in/out]  ion_local_sp [natom*super]   : ion_local[j] の super cel index 対応版
# [in/out]  sp_j [natom*super]          : 通し番号の対応( 元のセル <---> SPセル )
#
################################################################################
#
# 2014.10.31
#   Vmake_SuperCell2.py ベース
#   1st version
#
################################################################################
################################################################################
## for TEST print
# x=sp[nsp,0]
# y=sp[nsp,1]
# z=sp[nsp,2]
# print " %d,%d,  %d,%d,%s, %d,%d, %d  %s %12.8f %12.8f %12.8f" \
#        %(j,nsp, k,ion_local_sp[nsp],atoms_index[k],  ion[j],ion_sp[nsp], kk,"  ",x,y,z)
## 元index と super index の対応を見る(テストプリント)
# for k in range(nsp):
#    print int(k), int(sp_j[k])
#
################################################
### TEST: print super cell (VASP POSCAR, cartesian MODE)
###
# print  " Makes Super Cell"
# print  " 1.0"
# print  "   %16.12f %16.12f %16.12f" %(t1_x*super_x, t1_y*super_y, t1_z*super_z)
# print  "   %16.12f %16.12f %16.12f" %(t2_x*super_x, t2_y*super_y, t2_z*super_z)
# print  "   %16.12f %16.12f %16.12f" %(t3_x*super_x, t3_y*super_y, t3_z*super_z)
# if VASP > 4:
#    for j in range(nion):
#        print atoms_index[j],
#    print ""
# for j in range(nion):
#    tmp = int(atoms[j])*int(super_x)*int(super_y)*int(super_z)
#    print int(tmp),
# print  ""
# print  "Car"
#
# for j in range(natom*super):
#    print "  %12.8f  %12.8f  %12.8f "  %(sp[j,0], sp[j,1], sp[j,2])
#################################################
### TEST: write original cell
###
# for j in range(natom):
#    print "  %12.8f  %12.8f  %12.8f "  %(s[j,0], s[j,1], s[j,2])
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# make_supercell1
# スーパーセル作成ルーチン
#    内部座標スーパーセル化
#    FIX情報スーパーセル化 (for VASP) <-- make_supercell0 のフォース情報(VASP)対応版
#
#  (注意) 対称性によって原子に働く力の移動の有無(FIX)を選択しているわけではない
#         単純に同一のスーパーポジションにある原子のFIXを同じにしているだけ
#         注意が必要である。
#
# [in]      super_x
# [in]      super_y
# [in]      super_z
#
# [in/out]  sp [natom*super,3]          : SuPer cell position 保存用のverctor
# [in/out]  ion_sp [natom*super]        : SPセルの通し番号に対する電子主番号保存index
# [in/out]  ion_local_sp [natom*super]   : ion_local[j] の super cel index 対応版
# [in/out]  sp_j [natom*super]          : 通し番号の対応( 元のセル <---> SPセル )
#
# [in/out]  fix [natom,3]
# [in/out]  fix [natom*supr,3]
#
################################################################################
#
# 2014.10.31
#   make_supercell0.py ベース
#   フォース情報対応版(for VASP)
#   1st version
#
################################################################################
################################################################################
## for TEST print
# x=sp[nsp,0]
# y=sp[nsp,1]
# z=sp[nsp,2]
# print " %d,%d,  %d,%d,%s, %d,%d, %d  %s %12.8f %12.8f %12.8f" \
#        %(j,nsp, k,ion_local_sp[nsp],atoms_index[k],  ion[j],ion_sp[nsp], kk,"  ",x,y,z)
## 元index と super index の対応を見る(テストプリント)
# for k in range(nsp):
#    print int(k), int(sp_j[k])
#
################################################
### TEST: print super cell (VASP POSCAR, cartesian MODE)
###
# print  " Makes Super Cell"
# print  " 1.0"
# print  "   %16.12f %16.12f %16.12f" %(t1_x*super_x, t1_y*super_y, t1_z*super_z)
# print  "   %16.12f %16.12f %16.12f" %(t2_x*super_x, t2_y*super_y, t2_z*super_z)
# print  "   %16.12f %16.12f %16.12f" %(t3_x*super_x, t3_y*super_y, t3_z*super_z)
# if VASP > 4:
#    for j in range(nion):
#        print atoms_index[j],
#    print ""
# for j in range(nion):
#    tmp = int(atoms[j])*int(super_x)*int(super_y)*int(super_z)
#    print int(tmp),
# print  ""
# print  "Car"
#
# for j in range(natom*super):
#    print "  %12.8f  %12.8f  %12.8f "  %(sp[j,0], sp[j,1], sp[j,2])
#################################################
### TEST: write original cell
###
# for j in range(natom):
#    print "  %12.8f  %12.8f  %12.8f "  %(s[j,0], s[j,1], s[j,2])
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# スーパーセル用の
#     1) 基本並進ベクトル
#     2) 原子種数
#
# を作成するモジュール
#
# [in]      super_x
# [in]      super_y
# [in]      super_z
#
# [in/out] atoms[i]   : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
#
# [in]     nion       : 原子種の数
# [in/out] atoms[i]   : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
#
# [in/out] t[3,3]     :  基本並進ベクトル(注意:配列内indexは0から)
#                              x   y   z
#                        t1 = a11 a21 a31
#                        t2 = a12 a22 a32
#                        t3 = a13 a23 a33
#
################################################################################
#
# 2014.10.31
#
################################################################################
################################################################################
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# スーパーセル作成ルーチン (zone境界処理専用)
#
#  ゾーン境界のみ
#     1) 3x3x3 スーパーセルのみ
#     2) 基本並進ベクトル原点で増やすのではなくて、-1,0,1 倍の範囲で大きくした
#
# [in/out]  sp(natom*super,3)          : SuPer cell position 保存用のverctor
# [in/out]  ion_sp(natom*super)        : SPセルの通し番号に対する原子種番号保存index
# [in/out]  ion_local_sp(natom*super)  : ion_local[j] の super cel index 対応版
# [in/out]  sp_j(natom*super)          : 通し番号の対応( 元のセル <---> SPセル )
#
################################################################################
#
# 2014.10.30 1st
#
################################################################################
################################################################################
#          # TEST print
#           x=sp[nsp,0]
#           y=sp[nsp,1]
#           z=sp[nsp,2]
#           print " %d,%d,  %d,%d,%s, %d,%d, %d  %s %12.8f %12.8f %12.8f" \
#                   %(j,nsp, k,ion_local_sp[nsp],atoms_index[k],  ion[j],ion_sp[nsp], kk,"  ",x,y,z)
## 元index と super index の対応を見る(テストプリント)
# for k in range(nsp):
#    print int(k), int(sp_j[k])
#
################################################
### TEST: print super cell (VASP POSCAR, cartesian MODE)
###
# print  " Makes Super Cell"
# print  " 1.0"
# print  "   %16.12f %16.12f %16.12f" %(t1_x*super_x, t1_y*super_y, t1_z*super_z)
# print  "   %16.12f %16.12f %16.12f" %(t2_x*super_x, t2_y*super_y, t2_z*super_z)
# print  "   %16.12f %16.12f %16.12f" %(t3_x*super_x, t3_y*super_y, t3_z*super_z)
# if VASP > 4:
#    for j in range(nion):
#        print atoms_index[j],
#    print ""
# for j in range(nion):
#    tmp = int(atoms[j])*int(super_x)*int(super_y)*int(super_z)
#    print int(tmp),
# print  ""
# print  "Car"
#
# for j in range(natom*super):
#    print "  %12.8f  %12.8f  %12.8f "  %(sp[j,0], sp[j,1], sp[j,2])
#################################################
### TEST: write original cell
###
# for j in range(natom):
#    print "  %12.8f  %12.8f  %12.8f "  %(s[j,0], s[j,1], s[j,2])
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import optparse
from numpy import *
from copy import deepcopy


class SupercellOperations:

    def make_supercell0(
        self,
        super_x,
        super_y,
        super_z,
        t,
        natom,
        nion,
        atoms,
        ion,
        ion_local,
        position,
        sv,
        ion_sp,
        ion_local_sp,
        sp_j,
        sp,
    ):
        t1_x = t[0, 0]
        t1_y = t[1, 0]
        t1_z = t[2, 0]
        t2_x = t[0, 1]
        t2_y = t[1, 1]
        t2_z = t[2, 1]
        t3_x = t[0, 2]
        t3_y = t[1, 2]
        t3_z = t[2, 2]
        ###############################################
        ## スーパーセル作成用の準備
        ## super index
        ##
        super = int(super_x) * int(super_y) * int(super_z)
        ###############################################
        ## super cell 作成用のベクトルを作る
        ##
        # sv = zeros((super,3)) # super cell vector
        nsv = 0
        for n in range(super_x):
            for l in range(super_y):
                # print nsv, " ", n,l,m," ",sv[nsv,0]
                # print nsv, " ", n,l,m," ",sv[nsv,1]
                # print nsv, " ", n,l,m," ",sv[nsv,2]
                for m in range(super_z):
                    sv[nsv, 0] = t1_x * n + t2_x * l + t3_x * m
                    sv[nsv, 1] = t1_y * n + t2_y * l + t3_y * m
                    sv[nsv, 2] = t1_z * n + t2_z * l + t3_z * m
                    nsv += 1
        ###############################################
        ## スーパーセルの内部座標作成
        ##
        # sp = zeros((natom*super,3)) # super cell position 保存用のvector
        # ion_sp= zeros(natom*super)  # super cell 通し番号に対する原子種番号保存index
        # ion_local_sp = zeros(natom*super) # ion_local[j] の super cell index 対応版
        # super cell の内部座標を作る
        j = -1
        nsp = -1
        for k in range(nion):
            for kk in range(int(atoms[k])):
                j += 1
                # 元セルの通し番号を与えると、原子種番号を返す
                for nsv in range(super):
                    nsp += 1
                    nsp_ = natom * nsv + j
                    sp[nsp, 0] = position[j, 0] + sv[nsv, 0]
                    sp[nsp, 1] = position[j, 1] + sv[nsv, 1]
                    sp[nsp, 2] = position[j, 2] + sv[nsv, 2]
                    ion_sp[nsp] = ion[j]
                    ion_local_sp[nsp] = ion_local[j]
                    sp_j[nsp] = j

    def make_supercell1(
        self,
        super_x,
        super_y,
        super_z,
        t,
        natom,
        nion,
        atoms,
        ion,
        ion_local,
        position,
        sv,
        ion_sp,
        ion_local_sp,
        sp_j,
        sp,
        fix,
        fix_sp,
    ):
        t1_x = t[0, 0]
        t1_y = t[1, 0]
        t1_z = t[2, 0]
        t2_x = t[0, 1]
        t2_y = t[1, 1]
        t2_z = t[2, 1]
        t3_x = t[0, 2]
        t3_y = t[1, 2]
        t3_z = t[2, 2]
        ###############################################
        ## スーパーセル作成用の準備
        ## super index
        ##
        super = int(super_x) * int(super_y) * int(super_z)
        ###############################################
        ## super cell 作成用のベクトルを作る
        ##
        # sv = zeros((super,3)) # super cell vector
        nsv = 0
        for n in range(super_x):
            for l in range(super_y):
                # print nsv, " ", n,l,m," ",sv[nsv,0]
                # print nsv, " ", n,l,m," ",sv[nsv,1]
                # print nsv, " ", n,l,m," ",sv[nsv,2]
                for m in range(super_z):
                    sv[nsv, 0] = t1_x * n + t2_x * l + t3_x * m
                    sv[nsv, 1] = t1_y * n + t2_y * l + t3_y * m
                    sv[nsv, 2] = t1_z * n + t2_z * l + t3_z * m
                    nsv += 1
        ###############################################
        ## スーパーセルの内部座標作成
        ##
        # sp = zeros((natom*super,3)) # super cell position 保存用のvector
        # ion_sp= zeros(natom*super)  # super cell 通し番号に対する原子種番号保存index
        # ion_local_sp = zeros(natom*super) # ion_local[j] の super cell index 対応版
        # super cell の内部座標を作る
        j = -1
        nsp = -1
        for k in range(nion):
            for kk in range(int(atoms[k])):
                j += 1
                # 原子に働く力の有無による移動パラメーターの super cell 化
                # 元セルの通し番号を与えると、原子種番号を返す
                for nsv in range(super):
                    nsp += 1
                    nsp_ = natom * nsv + j
                    sp[nsp, 0] = position[j, 0] + sv[nsv, 0]
                    sp[nsp, 1] = position[j, 1] + sv[nsv, 1]
                    sp[nsp, 2] = position[j, 2] + sv[nsv, 2]
                    fix_sp[nsp, 0] = fix[j, 0]
                    fix_sp[nsp, 1] = fix[j, 1]
                    fix_sp[nsp, 2] = fix[j, 2]
                    ion_sp[nsp] = ion[j]
                    ion_local_sp[nsp] = ion_local[j]
                    sp_j[nsp] = j

    def make_supercell_param(self, super_x, super_y, super_z, nion, atoms, t):
        # t1_x
        t[0, 0] = t[0, 0] * super_x
        # t1_y
        t[1, 0] = t[1, 0] * super_y
        # t1_z
        t[2, 0] = t[2, 0] * super_z
        # t2_x
        t[0, 1] = t[0, 1] * super_x
        # t2_y
        t[1, 1] = t[1, 1] * super_y
        # t2_z
        t[2, 1] = t[2, 1] * super_z
        # t3_x
        t[0, 2] = t[0, 2] * super_x
        # t3_y
        t[1, 2] = t[1, 2] * super_y
        # t3_z
        t[2, 2] = t[2, 2] * super_z
        for j in range(nion):
            atoms[j] = int(atoms[j]) * super_x * super_y * super_z

    def make_supercell_zb(
        self,
        t,
        natom,
        nion,
        atoms,
        ion,
        ion_local,
        position,
        sv,
        ion_sp,
        ion_local_sp,
        sp_j,
        sp,
    ):
        t1_x = t[0, 0]
        t1_y = t[1, 0]
        t1_z = t[2, 0]
        t2_x = t[0, 1]
        t2_y = t[1, 1]
        t2_z = t[2, 1]
        t3_x = t[0, 2]
        t3_y = t[1, 2]
        t3_z = t[2, 2]
        ###############################################
        ## スーパーセル作成用の準備
        ## super index
        ##
        # super_x=int(times[0])
        # super_y=int(times[1])
        # super_z=int(times[2])
        ## ゾーンバウンダリーをすべてカバーするための 3x3x3 セル
        super_x = 3
        ## 何も考えなければ 3x3x3 がベスト(固定値とする)
        super_y = 3
        ## ここを変更した時は下記の for in in range(*) の範囲(*)
        super_z = 3
        ## を修正しないと意味は無い
        ## 3x3x3 を想定し、-1,0,1 までの範囲を想定している。
        super = int(super_x * super_y * super_z)
        ###############################################
        ## super cell 作成用のベクトルを作る
        ##
        ## Find 専用
        ## バウンダリーでの接続のために
        ## 3x3x3 を想定して -1,0,1 までの範囲で作る
        ## Find 以外にも 3x3x3 としては一応そのまま使える
        ##
        # sv = zeros((super,3)) # super cell vector
        nsv = 0
        # for n in range((super_x)):
        #    for l in range((super_y)):
        #        for m in range((super_z)):
        for n in range(-1, 2):
            for l in range(-1, 2):
                # print nsv, " ", n,l,m," ",sv[nsv,0]
                # print nsv, " ", n,l,m," ",sv[nsv,1]
                # print nsv, " ", n,l,m," ",sv[nsv,2]
                for m in range(-1, 2):
                    sv[nsv, 0] = t1_x * n + t2_x * l + t3_x * m
                    sv[nsv, 1] = t1_y * n + t2_y * l + t3_y * m
                    sv[nsv, 2] = t1_z * n + t2_z * l + t3_z * m
                    nsv += 1
        ###############################################
        ## スーパーセルの内部座標作成
        ##
        # sp = zeros((natom*super,3)) # super cell position 保存用のvector
        # ion_sp= zeros(natom*super)  # SPセルの通し番号に対する原子種番号保存index
        # ion_local_sp = zeros(natom*super) # ion_local[j] の super cell index 対応版
        # sp_j = zeros(natom*super)  # 通し番号の対応( 元のセル <---> スーパーセル )
        # super cell の内部座標を作る
        j = -1
        nsp = -1
        for k in range(nion):
            for kk in range(int(atoms[k])):
                j += 1
                # 元セルの通し番号を与えると、原子種番号を返す
                for nsv in range(super):
                    nsp += 1
                    nsp_ = natom * nsv + j
                    sp[nsp, 0] = position[j, 0] + sv[nsv, 0]
                    sp[nsp, 1] = position[j, 1] + sv[nsv, 1]
                    sp[nsp, 2] = position[j, 2] + sv[nsv, 2]
                    ion_sp[nsp] = ion[j]
                    ion_local_sp[nsp] = ion_local[j]
                    sp_j[nsp] = j
