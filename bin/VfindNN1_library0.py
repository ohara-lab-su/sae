#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# VfindNN1.py の 関数化化(途中バージョン version 0 )
#   関数化の最初のテスト
#   実用的に使えない
#
################################################################################
#
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
import re
import optparse
import numpy as np

#from numpy import *
#from copy import deepcopy

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

print "INPUT file name    :",POSCAR
print "OUTPUT file name   :",cname+"_nn_"+str(find)+".out"
print "SEARCH DISTANCE    :",distance




################################################################################
# POSCAR 読み込みのための事前準備関数 1
#
#   nion (retun)     : number of ion
#   natom (return)   : number of atom
#   VASP (return)    : VASP version
#
################################################################################
def read_param_poscar():

    ###############################################
    ## Open POSCAR file
    ##
    tmp = open(POSCAR)
    datfile = tmp.read()
    tmp.close
    datlines = datfile.split('\n')

    ###############################################
    ## get VASP version, atoms and index
    ##
    i=5
    atoms = datlines[i].split()
    if atoms[0].isdigit():
        VASP = 4
    else:
        VASP = 5
        atoms_index=list(atoms)
        i += 1
        atoms = datlines[i].split()
        #print atoms_index[0]," ", atoms_index[1]

    ###############################################
    ## TEST print
    ##
    #if VASP > 4:
    #    for j in range(len(atoms)):
    #        print atoms_index[j],
    #    print ""
    #
    #for j in range(len(atoms)):
    #    print atoms[j],
    #print ""
    
    ###############################################
    ## get number of atoms
    ##
    nion=int(len(atoms))
    natom = 0
    for j in range(nion):
        sum = int(atoms[j])
        natom = natom + sum
    #print "natom= ",natom

    return [nion,natom,VASP]



################################################################################
# POSCAR 読み込み
#
#   1) 事前に read_param_poscar() を実行して natom と nion の取得
#   2) atoms[natom], atoms_index[natom], ion[nion], ion_local[nion]
#      を引数として用意
#
# [return] title          : タイトル
# [return] scale          : 格子定数(スケールファクター)
# [return] selective      : selective mode
# [return] direct         : direct or cartesian
#          
# [in/out] t[3,3]         :  基本並進ベクトル(注意:配列内indexは0から)
#                                  x   y   z
#                            t1 = a11 a21 a31
#                            t2 = a12 a22 a32
#                            t3 = a13 a23 a33
#          
# [in/out] atoms[i]       : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
# [in/out] atoms_index[i] : 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
# [in/out] ion[j]         : 通し番号(max=natom)を与えると原子の種類番号を返す
# [in/out] ion_local[j]    : 通し番号(max=natom)を与えるとサイト内のローカル通し番号を返す
#
# [in/out] position[j,3]  : 通し番号(max=natom)とx,y,z 指定で内部座標
# [in/out] fix[j,3]       : 通し番号(max=natom)とx,y,z 指定でForceのFix/non-Fix 指定
#
################################################################################
def read_poscar(VASP,t,atoms,atoms_index,ion,ion_local,position,fix):

    ###############################################
    ## Open POSCAR file
    ##
    tmp = open(POSCAR)
    datfile = tmp.read()
    tmp.close
    datlines = datfile.split('\n')

    ###############################################
    ## Read Header
    ##
    title = datlines[0]
    scale = float(datlines[1])

    ###############################################
    ## Read Translation Vector
    ##         x   y   z
    ##   t1 = t11 t21 t31
    ##   t2 = t12 t22 t32
    ##   t3 = t13 t23 t33
    ##
    v = datlines[2].split()
    t1_x = float(v[0])
    t1_y = float(v[1])
    t1_z = float(v[2])
    
    v = datlines[3].split()
    t2_x = float(v[0])
    t2_y = float(v[1])
    t2_z = float(v[2])
    
    v = datlines[4].split()
    t3_x = float(v[0])
    t3_y = float(v[1])
    t3_z = float(v[2])
    
   #t = zeros((3,3))
    t[0,0] = t1_x
    t[1,0] = t1_y
    t[2,0] = t1_z
    
    t[0,1] = t2_x
    t[1,1] = t2_y
    t[2,1] = t2_z
    
    t[0,2] = t3_x
    t[1,2] = t3_y
    t[2,2] = t3_z


    ###############################################
    ## get VASP version, atoms and index
    ##
    i=5
    if VASP == 4:
        atoms.extend(datlines[i].split())
    elif VASP == 5:
        atoms_index.extend(datlines[i].split())
        i += 1
        atoms.extend(datlines[i].split())
    else:
        sys.exit("Error: unknown VASP format")

    
    ###############################################
    ## get number of atoms
    ##
    nion=int(len(atoms))
    natom = 0
    for j in range(nion):
        sum = int(atoms[j])
        natom = natom + sum
    #print "natom= ",natom


    ###############################################
    ## makes index
    ##
   #ion_local = zeros(natom)
   #ion = zeros(natom)
    tmp = -1
    for j in range(nion):
        local = -1
        for k in range(int(atoms[j])):
            tmp += 1
            local += 1
            ion[tmp] = int(j)
            ion_local[tmp] = int(local)
           #print tmp, int(ion[tmp]), int(ion_local[tmp])


    ###############################################
    ## makes re rule
    ##
    num_reg = re.compile('^[+-]?(\d*\.\d+|\d+\.?\d*)([eE][+-]?\d+|)\Z')
    selective_reg = re.compile('^S.*',re.IGNORECASE)
    direct_reg = re.compile('^D.*',re.IGNORECASE)
    car_reg = re.compile('^C.*',re.IGNORECASE)
    
    
    ###############################################
    ## get atomc coordinate mode
    ##
    i += 1
    tmp = datlines[i].split()
    if bool(num_reg.match(tmp[0])):
        print tmp[0]
        sys.exit("Format Error")
    else:
        if bool(selective_reg.match(tmp[0])):
           #print "selective True"
            i += 1
            tmp = datlines[i].split()
            selective = True
        else:
           #print "selective False"
            selective = False
    
        if bool(num_reg.match(tmp[0])):
            print tmp[0]
            sys.exit("Format Error")
        if bool(direct_reg.match(tmp[0])):
           #print "Direct Mode"
            direct = True
        elif bool(car_reg.match(tmp[0])):
           #print "Cartesian Mode"
            direct = False
    
    
    ###############################################
    ## get atomic coordinate position
    ##
   #position = zeros((int(natom),3))
    i += 1
    for j in range(natom):
        xyz = datlines[i+j].split()
        position[j,0] = xyz[0]
        position[j,1] = xyz[1]
        position[j,2] = xyz[2]
        if selective:
            fix[j,0] = str(xyz[3])
            fix[j,1] = str(xyz[4])
            fix[j,2] = str(xyz[5])
       #print j,
       #print " %16.12f %16.12f %16.12f" %(position[j,0],position[j,1],position[j,2]),
       #print fix[j,0],fix[j,1],fix[j,2]
    
    return [title,scale,selective,direct]


################################################################################
# POSCAR 書き込み
#
# [return] title          : タイトル
# [return] scale          : 格子定数(スケールファクター)
# [return] selective      : selective mode
# [return] direct         : direct or cartesian
#          
# [in/out] t[3,3]         :  基本並進ベクトル(注意:配列内indexは0から)
#                                  x   y   z
#                            t1 = a11 a21 a31
#                            t2 = a12 a22 a32
#                            t3 = a13 a23 a33
#          
# [in/out] atoms[i]       : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
# [in/out] atoms_index[i] : 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
#
# [in/out] position[j,3]  : 通し番号(max=natom)とx,y,z 指定で内部座標
# [in/out] fix[j,3]       : 通し番号(max=natom)とx,y,z 指定でForceのFix/non-Fix 指定
#
################################################################################
def print_poscar(title,scale,selective,direct,VASP,t,atoms,atoms_index,position,fix):
    print title
    print " ",scale
    print "  %13.9f %13.9f %13.9f" %(t[0,0],t[1,0],t[2,0])
    print "  %13.9f %13.9f %13.9f" %(t[0,1],t[1,1],t[2,1])
    print "  %13.9f %13.9f %13.9f" %(t[0,2],t[1,2],t[2,2])

    if VASP == 5:
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

    for i in range(int(natom)):
        print " %13.9f %13.9f %13.9f" %(position[i,0],position[i,1],position[i,2]),
        if selective:
            print "",
            print fix[i,0],fix[i,1],fix[i,2],
        print ""


##################################################################################
# POSCAR の内部座標を direct 系から cartesian 系へ変換
# (スケールファクターを1 にする(基本並進ベクトルを直接スケール))
#
# [in]     scale          : scale factor
# [in]     natom          : number of atom
# [in/out] t[3,3]         : 基本並進ベクトル(注意:配列内indexは0から)
#                                  x   y   z
#                            t1 = a11 a21 a31
#                            t2 = a12 a22 a32
#                            t3 = a13 a23 a33
#
# [in/out] position[j,3]  : 通し番号(max=natom)とx,y,z 指定で内部座標
#
##################################################################################
def conv_direct2car(scale,natom,t,position):

    ###############################################
    ## 座標系を 1) direct --> cartesian
    ##          2) cartesian のまま
    ##
    ## 変換後に scale して絶対座標にする
    ## (入力がAngstrom 系なので A 単位になる)
    ##
    t1_x = t[0,0]
    t1_y = t[1,0]
    t1_z = t[2,0]

    t2_x = t[0,1]
    t2_y = t[1,1]
    t2_z = t[2,1]

    t3_x = t[0,2]
    t3_y = t[1,2]
    t3_z = t[2,2]

    for j in range(natom):
        position[j,0] = t1_x*position[j,0] + t2_x*position[j,1] + t3_x*position[j,2]
        position[j,1] = t1_y*position[j,0] + t2_y*position[j,1] + t3_y*position[j,2]
        position[j,2] = t1_z*position[j,0] + t2_z*position[j,1] + t3_z*position[j,2]
    
    ###############################################
    ## scale を掛けて car の絶対座標系へなおす
    ## --> scale=1.0 とするので必須作業
    ##
    for j in range(natom):
        position[j,0] = position[j,0]*scale
        position[j,1] = position[j,1]*scale
        position[j,2] = position[j,2]*scale
    
    ###############################################
    ## 基本並進ベクトルをスケールしておく
    ## --> scale=1.0 とするため
    ##
    t1_x = t1_x*scale
    t1_y = t1_y*scale
    t1_z = t1_z*scale
    
    t2_x = t2_x*scale
    t2_y = t2_y*scale
    t2_z = t2_z*scale
    
    t3_x = t3_x*scale
    t3_y = t3_y*scale
    t3_z = t3_z*scale

    t[0,0] = t1_x
    t[1,0] = t1_y
    t[2,0] = t1_z

    t[0,1] = t2_x
    t[1,1] = t2_y
    t[2,1] = t2_z

    t[0,2] = t3_x
    t[1,2] = t3_y
    t[2,2] = t3_z


################################################################################
if __name__ == '__main__':

    # POSCAR の事前読み込み
    nion,natom,VASP = read_param_poscar()

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
       read_poscar(VASP,t,atoms,atoms_index,ion,ion_local,position,fix)

    # Direct to Cartesian
    if direct:
        conv_direct2car(scale,natom,t,position)
        scale = 1.0

    # POSCAR の標準出力
    print_poscar(title,scale,selective,direct,VASP,t,atoms,atoms_index,position,fix)

        
################################################################################
     




## ###############################################
## ## スーパーセル作成用の準備
## ## super index
## ##
## #super_x=int(super_x)
## #super_y=int(super_y)
## #super_z=int(super_z)
## 
## super_x=3   ## ゾーンバウンダリーをすべてカバーするための 3x3x3 セル
## super_y=3   ## 何も考えなければ 3x3x3 がベスト(固定値とする)
## super_z=3   ## ここを変更した時は下記の for in in range(*) の範囲(*)
##             ## を修正しないと意味は無い
##             ## 3x3x3 を想定し、-1,0,1 までの範囲を想定している。
## 
## super=int(super_x*super_y*super_z)
## 
## 
## ###############################################
## ## super cell 作成用のベクトルを作る
## ##
## ## Find 専用
## ## バウンダリーでの接続のために
## ## 3x3x3 を想定して -1,0,1 までの範囲で作る
## ## Find 以外にも 3x3x3 としては一応そのまま使える
## ##
## sv = zeros((super,3)) # super cell vector
## nsv = 0
## #for n in range((super_x)):
## #    for l in range((super_y)):
## #        for m in range((super_z)):
## for n in range(-1,2):
##     for l in range(-1,2):
##         for m in range(-1,2):
##             sv[nsv,0] = t1_x*n + t2_x*l + t3_x*m
##             sv[nsv,1] = t1_y*n + t2_y*l + t3_y*m
##             sv[nsv,2] = t1_z*n + t2_z*l + t3_z*m
##            #print nsv, " ", n,l,m," ",sv[nsv,0]
##            #print nsv, " ", n,l,m," ",sv[nsv,1]
##            #print nsv, " ", n,l,m," ",sv[nsv,2]
##             nsv += 1
## 
## 
## ###############################################
## ## スーパーセルの内部座標作成
## ##
## sp = zeros((natom*super,3)) # super cell position 保存用のvector
## ion_sp= zeros(natom*super)  # SPセルの通し番号に対する原子種番号保存index
## ion_local_sp = zeros(natom*super) # ion_local[j] の super cell index 対応版
## 
## sp_j = zeros(natom*super)  # 通し番号の対応( 元のセル <---> スーパーセル )
## 
## # super cell の内部座標を作る
## j=-1
## nsp=-1
## for k in range(nion):
##     for kk in range(int(atoms[k])):
## 
##         j += 1
## 
##         for nsv in range(super):
##             nsp += 1
##             nsp_ = natom*nsv+j
## 
##             sp[nsp,0] = position[j,0] + sv[nsv,0]
##             sp[nsp,1] = position[j,1] + sv[nsv,1]
##             sp[nsp,2] = position[j,2] + sv[nsv,2]
## 
##             # 元セルの通し番号を与えると、原子種番号を返す
##             ion_sp[nsp] = ion[j]
##             ion_local_sp[nsp] = ion_local[j]
## 
##             sp_j[nsp] = j
## 
## #          # TEST print
## #           x=sp[nsp,0]
## #           y=sp[nsp,1]
## #           z=sp[nsp,2]
## #           print " %d,%d,  %d,%d,%s, %d,%d, %d  %s %12.8f %12.8f %12.8f" \
## #                   %(j,nsp, k,ion_local_sp[nsp],atoms_index[k],  ion[j],ion_sp[nsp], kk,"  ",x,y,z)
## 
## 
## ## 元index と super index の対応を見る(テストプリント)
## #for k in range(nsp):
## #    print int(k), int(sp_j[k])
## #
## 
## 
## ################################################
## ### TEST: print super cell (VASP POSCAR, cartesian MODE)
## ###
## #print  " Makes Super Cell"
## #print  " 1.0"
## #print  "   %16.12f %16.12f %16.12f" %(t1_x*super_x, t1_y*super_y, t1_z*super_z)
## #print  "   %16.12f %16.12f %16.12f" %(t2_x*super_x, t2_y*super_y, t2_z*super_z)
## #print  "   %16.12f %16.12f %16.12f" %(t3_x*super_x, t3_y*super_y, t3_z*super_z)
## #if VASP > 4:
## #    for j in range(nion):
## #        print atoms_index[j],
## #    print ""
## #for j in range(nion):
## #    tmp = int(atoms[j])*int(super_x)*int(super_y)*int(super_z)
## #    print int(tmp),
## #print  ""
## #print  "Car"
## #
## #for j in range(natom*super):
## #    print "  %12.8f  %12.8f  %12.8f "  %(sp[j,0], sp[j,1], sp[j,2])
## 
## 
## #################################################
## ### TEST: write original cell
## ###
## #for j in range(natom):
## #    print "  %12.8f  %12.8f  %12.8f "  %(s[j,0], s[j,1], s[j,2])
## 
## 
## 
## ###############################################
## ## 近接原子間距離の計算
## ##
## ## サーチ範囲が Super Cell の全範囲になるので index が natom から
## ## natom*super になるので注意
## ##
## 
## ## 原点となる原子の番号
## find0 = find -1 # 元のセルで(1から初めている番号系を 0 からに変換)
## 
## ## 原点となる原子の内部座標(絶対座標系(car,scale=1.0))
## x1 = position[find0,0]
## y1 = position[find0,1]
## z1 = position[find0,2]
## 
## ## サーチ範囲のエリア
## ##
## r = zeros(natom*super)
## r_index = zeros(natom*super)
## 
## ## サーチ用の範囲限定の探索原子範囲における原子数のカウンタ
## nsmax = 0
## 
## 
## for j in range(natom*super):
## 
##     x2 = sp[j,0]
##     y2 = sp[j,1]
##     z2 = sp[j,2]
## 
##     r0 = fabs( (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) + (z2-z1)*(z2-z1) )
##     r1 = sqrt(r0)
## 
##     r[j] = r1
##     r_index[j] = j
##    #print j+1, int(ion[j])+1, atoms_index[int(ion_sp[j])], int(ion_local_sp[j])+1, r[j]
## 
##     if r[j] < distance:
##         nsmax += 1
## 
##        #ion_num = ion[j]    # for original-cell
##         ion_num = ion_sp[j] # for super-cell
## 
##        ## TEST: super cell の番号体系で情報の確認
##        ##
##        #print " %6d %4d %3s %4d %10.6f    ( %8.5f %8.5f %8.5f - %8.5f %8.5f %8.5f )" \
##        #       %(j+1, int(ion_num)+1, atoms_index[int(ion_num)], int(ion_loal_sp[j])+1, \
##        #         r[j], \
##        #         position[find0,0], position[find0,1], position[find0,2], \
##        #         sp[j,0],     sp[j,1],     sp[j,2])
## 
## 
##        ## TEST(RESUT): 元のセルの原子の通し番号index に直した形で出力
##        ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
##        ## もし、ソートをしなければ近接原子のリザルトはこれ
##        ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
##        ##
##        ## ただし、このルーチンでは特定範囲の原子数の最大index numbetr : nsmax
##        ## を作成するのが主目的になる
##        ##
##        ## 実際に、ソートされるべき部分空間の Matrix は nsmax を最大とした
##        ## 新たな配列で定義され直される
##        ##
##        #print " %6d %4d %3s %4d %10.6f    ( %8.5f %8.5f %8.5f - %8.5f %8.5f %8.5f )" \
##        #       %( sp_j[j]+1, int(ion_num)+1, atoms_index[int(ion_num)], ion_local[sp_j[j]]+1, \
##        #          r[j], \
##        #          position[find0,0], position[find0,1], position[find0,2], \
##        #          sp[j,0],     sp[j,1],     sp[j,2])
## 
## 
## #print "=== max ns :",nsmax
## #for j in range(natom*super):
## #    print " %5d  %14.11f " %( int(r_index[j]), r[j] )
## 
## 
## 
## ###############################################
## ## distance の領域内でソートするべき配列を作り直す
## ##  全領域の全原子インデックス j は部分空間インデックスで指定可能
## ##
## ##  部分空間index MAX : nsmax
## ##  部分空間index     : num
## ##  部分空間matrix    : rs(num)
## ##
## ##  全空間index       :  rs_index[num]
## ##
## r_count = 0
## rs = zeros(nsmax)
## rs_index = zeros(nsmax)
## 
## for j in range(natom*super):
##     if r[j] < distance:
##         rs[r_count]=r[j]
##         rs_index[r_count]=r_index[j]
##         r_count += 1
## 
## for num in range(nsmax):
##     j = rs_index[num]
## 
##    ## 最大値が nsmax である配列に結果が再導入されたことの確認
##    ## (番号体系は sp_j[] を用いて、全て元セルに引き戻した値を表示)
##    ##
##    ## 新しい原子距離配列
##    ##  --> rs[num]
##    ## スーパーセル全部の通し番号とあたらし部分空間投資番号の対応index
##    ##  --> rs_index[num]                
##    ##
##    #print " %4d %4d %4d %3s %4d %10.6f" %( num+1,\
##    #                                       int(sp_j[j])+1,\
##    #                                       int(ion[sp_j[j]])+1,\
##    #                                       atoms_index[int(ion[sp_j[j]])],\
##    #                                       int(ion_local[sp_j[j]])+1,\
##    #                                       rs[num])
## 
## #print ""
## 
## # rs[num], rs_index[num] はソートするので
## # 利便のためにソート前を保存してく。
## #
## # rs[num] ---> r[num]
## # rs_index --> r_index[num]
## 
## r       = list(rs)
## r_index = list(rs_index)
## nmax    = nsmax
## 
## ################################################
## # Aho buble-sort
## #
## #  r[j] をソートする
## #     ソートに対応して、元の j のインデックスと対応している
## #     r_index[j] も並べ替える
## #
## # j は通し番号
## #    ソート前)
## #        r[j]       = 2.3 1.1 3.3
## #        r_index[j] =  0   1   2
## #   
## #    ソート後)
## #        r[j]       = 1.1 2.3 3.3
## #        r_index[j] =  1   0   2
## #   
## n = nmax -1
## for j in range(n):
##     for k in range(n,j,-1):
##         if r[k-1] > r[k]:
##             tmp = r[k]
##             r[k] = r[k-1]
##             r[k-1] = tmp
## 
##             tmp_index = r_index[k]
##             r_index[k] = r_index[k-1]
##             r_index[k-1] = tmp_index
## 
## ## TEST print
## ## ソートの一時確認
## ## r_index で示される元のスーパーセルindexはアホみたいにでかいので注意
## ## (巨大なのは 3x3x3 セルなのでほぼ仕様といっていい)
## ## 今結果がソート後のリザルト、あとはこれを整形して、各種インデックスを用いて
## ## 必要な情報を出すだけ
## ##
## #for num in range(nmax):
## #    print " %5d %5d %4d %14.11f " %( num, r_index[num], sp_j[r_index[num]]+1, r[num] )
## #print ""
## 
## 
## ################################################
## ## pre data print
## ##
## #print "scale              :",scale
## #print "translation vector : %11.9f %11.9f %11.9f" %(t1_x, t1_y, t1_z)
## #print "                     %11.9f %11.9f %11.9f" %(t2_x, t2_y, t2_z)
## #print "                     %11.9f %11.9f %11.9f" %(t3_x, t3_y, t3_z)
## 
## 
## ################################################
## ## data print
## ##    r_index[j] は 0 から始まる通しの index 番号なので注意
## ##    通し番号＆サイト内番号は1から始まるように出力
## ##
## #nn = open(cname+'_nn_'+str(find)+'.out','w')
## 
## print ""
## print  atoms_index[int(ion[int(find0)])],int(ion_local[find0])+1,"(",int(ion_local[find0])+1,")"
## print  "   ", "  -------------------------------------"
## print  "   ", "  [original cell numter]"
## print  "   ", "   t-index site site-index      r"
## print  "   ", "  -------------------------------------"
## 
## for num in range(nmax):
##     print  "   ","     %5d  %2s %5d    %14.11f" \
##                   %( sp_j[int(r_index[num])] +1 ,\
##                      atoms_index[int(ion[sp_j[r_index[num]]])], \
##                      ion_local[sp_j[r_index[num]]] +1,\
##                      r[num] )
## ## #nn.close
## 
## 
