#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#
# VfindNN2FNC.py
#   VfindNN1.py がベース
#    FNC 用の出力＆入力形式
#
#    find Nearest Neighbor
#   （範囲指定）近接原子一覧表示
#     引数に与えた原子間距離の範囲で近接原子一覧を表示
#     原子種の指定は -a オプション
#     もしくは距離範囲は -d オプションでも指定可能
#
#     ゾーンバウンダリーも考慮している
#     元セルの番号で表示
#
#     RMC_POT FNC 形式用
#
################################################################################
#
# 2014.10.17
#  1) 入力リストファイルの用意
#  2) FNC のリスト作成は完成(*.fncへ出力)
#
#  3) ボンド長の情報入力はダミーのマトリックスを用意
#     I/F のアイデアなし
#
# 2014.10.15
#  FNC のリストは手動入力ではなくて、リストファイルを用意する
#
#    1 2.5
#    3 2.7
#    . .
#    . .
#
#    元セルの原子の通し番号  さーちする原子間距離
#    の順番で並べる
#
#    ファイル名は FNC.list
#
#
# 2014.10.15 (17:30)
#  VfindNN2FNC.py
#    ボンド出力のFNC形式を準備
#
#    ソースコードの関数化は途中で断念
#    やり方は十分わかるのだが、いまいちスマートなほうほうが思いつかばない
#    class 化も念頭に入れると意外に初動で労力を使いそうなので、一旦やめておく。
#
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
# 2018.08.15
#  Python2/3 両対応
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
from copy import deepcopy

#from numpy import *

###############################################
## default parameter
##
cname  = "POSCAR" # OUTPUT BASE filename
POSCAR = "POSCAR" # INPUT (BASE) filename
FNClist = "FNC.list"

EPS =  0.0001

###############################################
## VfindNN2FNC.py 化に伴いファイルからの入力へ変更 (2014.10.15)
##
distance = "2.5"  # 検索する領域
find = 1          # (元のセルで)通しでn番目の原子(1から始まるindex)からの近接原子検索


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
#parser.add_option(  '-a','--atom',     ## VfindNN2FNC.py 化にともなって停止
#                    dest='NN',         ## find はリスト化して手動入力
#                    default=find,      ## 2014.10.15
#)
#parser.add_option(  '-d','--distance', ## VfindNN2FNC.py 化で停止
#                    dest='DISTANCE',   ## distance はリスト化して入力
#                    default=distance,  ## 2014.10.15
#)
options,  args = parser.parse_args()

if options.INPUT:
    POSCAR=options.INPUT

if options.OUTPUT:
    cname=options.OUTPUT

#if options.NN:                        ## VfindNN2.FNC.py 化にともなって停止
#    find=int(options.NN)              ## find はリスト化して手動入力

#if options.DISTANCE:                  ## VfindNN2FNC.py 化で停止
#    distance=float(options.DISTANCE)  ## distance はリスト化して入力
distance=float(distance)

#print args,options
#if len(args) > 0:
#   print "script name:",argvs[0]
#  POSCAR=argv[0]
#   distance = float(args[0])

if not os.path.exists(POSCAR):
    if os.path.exists(POSCAR+".vasp"):
        POSCAR="POSCAR.vasp"
    else:
        sys.exit(POSCAR+" file not found")

if not os.path.exists(FNClist):
    sys.path.exit(FNClist+"file not found")

print("INPUT file name    : %s" % str(POSCAR))
print("OUTPUT file name   : %s" % str(cname+"_nn_"+str(find)+".out"))
print("SEARCH DISTANCE    : %s" % str(distance))


################################################################################
## find リスト
##
tmp = open(FNClist)
datfile = tmp.read()
tmp.close
datlines = datfile.split('\n')
nfnc=int(len(datlines)) -1


## fnc 保存matrixの通し番号
## 

#print nfnc
dist = np.zeros((nfnc))
atom_fnc  = np.zeros((nfnc))
for i in range(nfnc):
   #print i,datlines[i]
    tmp = datlines[i].split()
    atom_fnc[i] = tmp[0]
    dist[i] = tmp[1]
   #print " %5d  %8.3f" %( atom_fnc[i], dist[i])


################################################################################
## VASP 形式
##
## title          : タイトル
## scale          : 格子定数(スケールファクター)
##
## a[3,3]         :  基本並進ベクトル(注意:配列内indexは0から)
##                       x   y   z
##                 t1 = a11 a21 a31
##                 t2 = a12 a22 a32
##                 t3 = a13 a23 a33
##
## natom          : 原子の数(j)
## nion           : 原子の種類数(i)
## atoms[i]       : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
## atoms_index[i] : 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
## ion[j]         : 通し番号(max=natom)を与えると原子の種類番号を返す
## ion_local[j]   : 通し番号(max=natom)を与えるとサイト内のローカル通し番号を返す
##
## position[j,3]  : 通し番号(max=natom)とx,y,z 指定で内部座標
##
################################################################################


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
##
##         x   y   z
##   t1 = a11 a21 a31
##   t2 = a12 a22 a32
##   t3 = a13 a23 a33
##
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

a = np.zeros((3,3))
a[0,0] = t1_x
a[1,0] = t1_y
a[2,0] = t1_z

a[0,1] = t2_x
a[1,1] = t2_y
a[2,1] = t2_z

a[0,2] = t3_x
a[1,2] = t3_y
a[2,2] = t3_z


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


###############################################
## makes index
##
ion_local = np.zeros(natom)
ion       = np.zeros(natom)
tmp       = -1
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
    print(tmp[0])
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
        print(tmp[0])
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
position = np.zeros((int(natom),3))
i += 1
for j in range(natom):
    xyz = datlines[i+j].split()
    position[j,0] = xyz[0]
    position[j,1] = xyz[1]
    position[j,2] = xyz[2]
   #print j,
   #print " %16.12f %16.12f %16.12f" %(position[j,0],position[j,1],position[j,2])


###############################################
## 座標系を 1) direct --> cartesian
##          2) cartesian のまま
##
## 変換後に scale して絶対座標にする
## (入力がAngstrom 系なので A 単位になる)
##
car = np.zeros((natom,3))
dic = deepcopy(position)  ## original の direct posion を一応保存(意味はなし)
if direct:
    for j in range(natom):
        car[j,0] = t1_x*position[j,0] + t2_x*position[j,1] + t3_x*position[j,2]
        car[j,1] = t1_y*position[j,0] + t2_y*position[j,1] + t3_y*position[j,2]
        car[j,2] = t1_z*position[j,0] + t2_z*position[j,1] + t3_z*position[j,2]
else:
    car[j,0] = position[j,0]
    car[j,1] = position[j,1]
    car[j,2] = position[j,2]


###############################################
## scale を掛けて car の絶対座標系へなおす
## --> scale=1.0 とするので必須作業
##
for j in range(natom):
    position[j,0] = car[j,0]*scale
    position[j,1] = car[j,1]*scale
    position[j,2] = car[j,2]*scale


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


###############################################
## スーパーセル作成用の準備
## super index
##
#super_x=int(super_x)
#super_y=int(super_y)
#super_z=int(super_z)

super_x=3   ## ゾーンバウンダリーをすべてカバーするための 3x3x3 セル
super_y=3   ## 何も考えなければ 3x3x3 がベスト(固定値とする)
super_z=3   ## ここを変更した時は下記の for in in range(*) の範囲(*)
            ## を修正しないと意味は無い
            ## 3x3x3 を想定し、-1,0,1 までの範囲を想定している。

super=int(super_x*super_y*super_z)


###############################################
## super cell 作成用のベクトルを作る
##
## Find 専用
## バウンダリーでの接続のために
## 3x3x3 を想定して -1,0,1 までの範囲で作る
## Find 以外にも 3x3x3 としては一応そのまま使える
##
sv = np.zeros((super,3)) # super cell vector
nsv = 0
#for n in range((super_x)):
#    for l in range((super_y)):
#        for m in range((super_z)):
for n in range(-1,2):
    for l in range(-1,2):
        for m in range(-1,2):
            sv[nsv,0] = t1_x*n + t2_x*l + t3_x*m
            sv[nsv,1] = t1_y*n + t2_y*l + t3_y*m
            sv[nsv,2] = t1_z*n + t2_z*l + t3_z*m
           #print nsv, " ", n,l,m," ",sv[nsv,0]
           #print nsv, " ", n,l,m," ",sv[nsv,1]
           #print nsv, " ", n,l,m," ",sv[nsv,2]
            nsv += 1


###############################################
## スーパーセルの内部座標作成
##
sp = np.zeros((natom*super,3)) # super cell position 保存用のvector
ion_sp= np.zeros(natom*super)  # SPセルの通し番号に対する原子種番号保存index
ion_local_sp = np.zeros(natom*super) # ion_local[j] の super cell index 対応版

sp_j = np.zeros(natom*super)  # 通し番号の対応( 元のセル <---> スーパーセル )

# super cell の内部座標を作る
j=-1
nsp=-1
for k in range(nion):
    for kk in range(int(atoms[k])):

        j += 1

        for nsv in range(super):
            nsp += 1
            nsp_ = natom*nsv+j

            sp[nsp,0] = position[j,0] + sv[nsv,0]
            sp[nsp,1] = position[j,1] + sv[nsv,1]
            sp[nsp,2] = position[j,2] + sv[nsv,2]

            # 元セルの通し番号を与えると、原子種番号を返す
            ion_sp[nsp] = ion[j]
            ion_local_sp[nsp] = ion_local[j]

            sp_j[nsp] = j

#          # TEST print
#           x=sp[nsp,0]
#           y=sp[nsp,1]
#           z=sp[nsp,2]
#           print " %d,%d,  %d,%d,%s, %d,%d, %d  %s %12.8f %12.8f %12.8f" \
#                   %(j,nsp, k,ion_local_sp[nsp],atoms_index[k],  ion[j],ion_sp[nsp], kk,"  ",x,y,z)


## 元index と super index の対応を見る(テストプリント)
#for k in range(nsp):
#    print int(k), int(sp_j[k])
#


################################################
### TEST: print super cell (VASP POSCAR, cartesian MODE)
###
#print  " Makes Super Cell"
#print  " 1.0"
#print  "   %16.12f %16.12f %16.12f" %(t1_x*super_x, t1_y*super_y, t1_z*super_z)
#print  "   %16.12f %16.12f %16.12f" %(t2_x*super_x, t2_y*super_y, t2_z*super_z)
#print  "   %16.12f %16.12f %16.12f" %(t3_x*super_x, t3_y*super_y, t3_z*super_z)
#if VASP > 4:
#    for j in range(nion):
#        print atoms_index[j],
#    print ""
#for j in range(nion):
#    tmp = int(atoms[j])*int(super_x)*int(super_y)*int(super_z)
#    print int(tmp),
#print  ""
#print  "Car"
#
#for j in range(natom*super):
#    print "  %12.8f  %12.8f  %12.8f "  %(sp[j,0], sp[j,1], sp[j,2])


#################################################
### TEST: write original cell
###
#for j in range(natom):
#    print "  %12.8f  %12.8f  %12.8f "  %(s[j,0], s[j,1], s[j,2])



###############################################
## 近接原子間距離の計算
##
## サーチ範囲が Super Cell の全範囲になるので index が natom から
## natom*super になるので注意
##


## サーチ範囲のエリア (FNC suffix 追加)
##
r = np.zeros((natom*super,nfnc))
r_index = np.zeros((natom*super,nfnc))

## サーチ用の範囲限定の探索原子範囲における原子数のカウンタ
#nsmax = 0
nsmax = np.zeros(nfnc)

###########################
## サーチ
for fnc in range(nfnc):

    ## 原点となる原子の番号(元セルでの通し番号で必要)
    find0 = atom_fnc[fnc] - 1 # 元のセルで(1から初めている番号系を 0 からに変換)

    ## 原点となる原子ごとのサーチ範囲
    distance = float(dist[fnc])

    ## 原点となる原子の内部座標(絶対座標系(car,scale=1.0))
    x1 = position[find0,0]
    y1 = position[find0,1]
    z1 = position[find0,2]

    for j in range(natom*super):

        x2 = sp[j,0]
        y2 = sp[j,1]
        z2 = sp[j,2]
    
        r0 = np.fabs( (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) + (z2-z1)*(z2-z1) )
        r1 = np.sqrt(r0)
    
        r[j,fnc] = r1
        r_index[j,fnc] = j
       #print j+1, int(ion[j])+1, atoms_index[int(ion_sp[j])], int(ion_local_sp[j])+1, r[j,fnc]
    
        if r[j,fnc] < distance:
            nsmax[fnc] += 1
    
           #ion_num = ion[j]    # for original-cell
            ion_num = ion_sp[j] # for super-cell
    
           ## TEST: super cell の番号体系で情報の確認
           ##
           #print " %6d %4d %3s %4d %10.6f    ( %8.5f %8.5f %8.5f - %8.5f %8.5f %8.5f )" \
           #       %(j+1, int(ion_num)+1, atoms_index[int(ion_num)], int(ion_local_sp[j])+1, \
           #         r[j,fnc], \
           #         position[find0,0], position[find0,1], position[find0,2], \
           #         sp[j,0],     sp[j,1],     sp[j,2])
    
    
           ## TEST(RESUT): 元のセルの原子の通し番号index に直した形で出力
           ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
           ## もし、ソートをしなければ近接原子のリザルトはこれ
           ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
           ##
           ## ただし、このルーチンでは特定範囲の原子数の最大index numbetr : nsmax
           ## を作成するのが主目的になる
           ##
           ## 実際に、ソートされるべき部分空間の Matrix は nsmax を最大とした
           ## 新たな配列で定義され直される
           ##
           #print " %6d %4d %3s %4d %10.6f    ( %8.5f %8.5f %8.5f - %8.5f %8.5f %8.5f )" \
           #       %( sp_j[j]+1, int(ion_num)+1, atoms_index[int(ion_num)], ion_local[sp_j[j]]+1, \
           #          r[j,fnc], \
           #          position[find0,0], position[find0,1], position[find0,2], \
           #          sp[j,0],     sp[j,1],     sp[j,2])
   #print ""    

#for fnc in range(nfnc):
#    print "=== max ns :",nsmax[fnc]
#    for j in range(natom*super):
#        print " %5d  %14.11f " %( int(r_index[j,fnc]), r[j,fnc] )
#


###############################################
## nsmax の最大値
#
nsmax_tmp = 0
for fnc in range(nfnc):
   #print fnc,int(nsmax[fnc])
    if nsmax[fnc] >= nsmax_tmp:
        nsmax_max = nsmax[fnc]


###############################################
## distance の領域内でソートするべき配列を作り直す
##  全領域の全原子インデックス j は部分空間インデックスで指定可能
##
##  部分空間index MAX : nsmax[fnc]
##  部分空間index     : num
##  部分空間matrix    : rs[num,fnc]
##
##  全空間index       :  rs_index[num,fnc]
##

rs = np.zeros((int(nsmax_max),nfnc))
rs_index = np.zeros((int(nsmax_max),nfnc))

for fnc in range(nfnc):

    r_count = 0
    for j in range(natom*super):
        if r[j,fnc] < distance:
            rs[r_count,fnc]=r[j,fnc]
            rs_index[r_count,fnc]=r_index[j,fnc]
            r_count += 1
    
    for num in range(int(nsmax_max)):
        j = rs_index[num,fnc]
       ## 最大値が nsmax_max である配列に結果が再導入されたことの確認
       ## (番号体系は sp_j[] を用いて、全て元セルに引き戻した値を表示)
       ##
       ## 新しい原子距離配列
       ##  --> rs[num,fnc]
       ## スーパーセル全部の通し番号とあたらし部分空間投資番号の対応index
       ##  --> rs_index[num,fnc]                
       ##
       #print " %4d %4d %4d %3s %4d %10.6f" %( num+1,\
       #                                       int(sp_j[j])+1,\
       #                                       int(ion[sp_j[j]])+1,\
       #                                       atoms_index[int(ion[sp_j[j]])],\
       #                                       int(ion_local[sp_j[j]])+1,\
       #                                       rs[num,fnc])
    
   #print ""



#######################
# マトリックスのバックアップ
# を停止 (VfindNN1.py では導入指定が使わない)
#
# rs[] --> r[]
# r_index[] --> r[]

nmax = int(nsmax_max)

################################################
# Aho buble-sort
#
#  r[j] をソートする
#     ソートに対応して、元の j のインデックスと対応している
#     r_index[j] も並べ替える
#
# j は通し番号
#    ソート前)
#        r[j]       = 2.3 1.1 3.3
#        r_index[j] =  0   1   2
#   
#    ソート後)
#        r[j]       = 1.1 2.3 3.3
#        r_index[j] =  1   0   2
#
for fnc in range(nfnc):   
    n = nmax -1
    for j in range(n):
        for k in range(n,j,-1):
            if rs[k-1,fnc] > rs[k,fnc]:
                tmp = rs[k,fnc]
                rs[k,fnc] = rs[k-1,fnc]
                rs[k-1,fnc] = tmp
    
                tmp_index = rs_index[k,fnc]
                rs_index[k,fnc] = rs_index[k-1,fnc]
                rs_index[k-1,fnc] = tmp_index
    
    ## TEST print
    ## ソートの一時確認
    ## r_index で示される元のスーパーセルindexはアホみたいにでかいので注意
    ## (巨大なのは 3x3x3 セルなのでほぼ仕様といっていい)
    ## 今結果がソート後のリザルト、あとはこれを整形して、各種インデックスを用いて
    ## 必要な情報を出すだけ
    ##
    #for num in range(nmax):
    #    print " %5d %5d %4d %14.11f " %( num, rs_index[num,fnc], sp_j[rs_index[num,fnc]]+1, r[num,fnc] )
    #print ""


################################################
## pre data print
##
#print "scale              :",scale
#print "translation vector : %11.9f %11.9f %11.9f" %(t1_x, t1_y, t1_z)
#print "                     %11.9f %11.9f %11.9f" %(t2_x, t2_y, t2_z)
#print "                     %11.9f %11.9f %11.9f" %(t3_x, t3_y, t3_z)


################################################
## それぞれのfncにおいて、ソートされた部分空間の上限と下限を調べて
## それぞれのfncにおける最大のボンド長と最小のボンド長を出力する
##

print("")
#print "=== fnc, nsmax[fnc]"
fnc_max = np.zeros(nfnc)
fnc_min = np.zeros(nfnc)
for fnc in range(nfnc):
    fnc_max[fnc] = rs[int(int(nsmax[fnc]))-1,fnc] 
    fnc_min[fnc] = rs[1,fnc]
   #print "fnc:",fnc," max:",int(nsmax[fnc]),fnc_max[fnc]," min:",fnc_min[fnc]
print("")

## ボンド長の種類数を指定
nbond = 2

fnc_bond_max = np.zeros(nbond)
fnc_bond_min = np.zeros(nbond)

fnc_bond_max[0] = fnc_max[0]
fnc_bond_min[0] = fnc_min[0]

fnc_bond_max[1] = fnc_max[1]
fnc_bond_min[1] = fnc_min[1]


################################################
## data print
##    r_index[j] は 0 から始まる通しの index 番号なので注意
##    通し番号＆サイト内番号は1から始まるように出力
##

for fnc in range(nfnc):
    #nn = open(cname+'_nn_'+str(find)+'.out','w')

    find0 = int(atom_fnc[fnc]) - 1

    print("")
    print( atoms_index[int(ion[int(find0)])],int(ion_local[find0])+1,"(",int(ion_local[find0])+1,")")
    print( "   ", "  -------------------------------------")
    print( "   ", "  [original cell numter]")
    print( "   ", "   t-index site site-index      r")
    print( "   ", "  -------------------------------------")
 
    # sp_j     : 元セル <--> スーパーセル 通し番号対応 
    # rs_index : ソート後の通し番号index
    # ion_local : サイト内ローカルの通し番号
    for num in range(nmax):
        print( "   ","     %5d  %2s %5d    %14.11f"
                      %( sp_j[int(rs_index[num,fnc])] +1 ,
                         atoms_index[int(ion[sp_j[rs_index[num,fnc]]])],
                         ion_local[sp_j[rs_index[num,fnc]]] +1,
                         rs[num,fnc] ))
    ## #nn.close


# FNC 形式のテストプリント(ボンドしているものだけ出力)
# この形式のまま *.fnc ファイルに出力する
# 
#print ""
#for fnc in range(nfnc):
#
#    find0 = int(atom_fnc[fnc]) -1 
#    print "     %3d %3d" %(find0+1,nmax-1)
#    for num in range(1,nmax):
#        print "    ", int(sp_j[int(rs_index[num,fnc])] +1 ),
#    print ""
#    
#    print "      ",
#    for num in range(1,nmax):
#        print "1",
#    print ""



##  index_bond
##
##   全原子の出力(ボンドするものはボンド情報も加える)をするために
##   ボンド情報があるかないか？のindexを全原子通し番号のインデックス
##   でフラグを作る
##
index_bond = np.zeros(natom)
fnc_atom  = np.zeros(natom)
for j in range(natom):
    index_bond[j] = 0
    for fnc in range(nfnc):
        find0 = int(atom_fnc[fnc]) - 1
        if j == find0:
            fnc_atom[atom_fnc[fnc]-1] = fnc
           #print int(fnc_atom[atom_fnc[fnc]-1])
            index_bond[j] = 1
   #print j,int(index_bond[j])

    
################################################
## RMC_POT 用 FNC フォーマット出力
##
outfnc = open(cname+'.fnc','w')

print("     ",title, file=outfnc)
print("")
print("     ","No. of possible rmin-rmax pairs:", file=outfnc)
print("     ",nbond, file=outfnc)

#### max
print("     ", file=outfnc, end="")
for ib in range(nbond):
    print("%2.3f " %( fnc_bond_min[ib] ), file=outfnc, end="")
print("", file=outfnc)

#### min
print("     ", file=outfnc, end="")
for ib in range(nbond):
    print("%2.3f " %( fnc_bond_max[ib] ), file=outfnc, end="")
print("", file=outfnc)

print("", file=outfnc)
print("     %3d" %(natom), file=outfnc)
print("", file=outfnc)

for j in range(natom):
    if index_bond[j] == 1:
       #print j,"bond"
        find0 = j
        fnc0 = fnc_atom[find0]
        print("     %3d %3d" %(find0+1,nmax-1), file=outfnc)
        for num in range(1,nmax):
            print("    ", int(sp_j[int(rs_index[num,int(fnc0)])] +1 ), file=outfnc, end="")
        print("", file=outfnc)
        
        print("      ", file=outfnc, end="")
        for num in range(1,nmax):
            print("1", file=outfnc, end="")
        print("", file=outfnc)

    else:
        print("     %3d %3d" %(j+1,0), file=outfnc)

outfnc.close()

