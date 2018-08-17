#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# find Nearest Neighbor
#   近接原子一覧表示
#     引数に与えた（通し番号での指定）原子の近接原子一覧
#     (もともとは RMC_POT 用)
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2014.10.14
#    正規表現を修正(大文字と小文字を区別しない)
#
# 2014.10.09 
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


###############################################
## default name
##
cname  = "POSCAR" # OUTPUT BASE filename
POSCAR = "POSCAR" # INPUT (BASE) filename

find = 1   # 通しで2番目の原子(1から始まるindex)からの近接原子検索

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
options,  args = parser.parse_args()

if options.INPUT:
    POSCAR=options.INPUT

if options.OUTPUT:
    cname=options.OUTPUT

if options.NN:
    find=int(options.NN)

#print args,options
if len(args) > 0:
    #print "script name:",argvs[0]
    #POSCAR=argv[0]
    find = int(args[0])

if not os.path.exists(POSCAR):
    if os.path.exists(POSCAR+".vasp"):
        POSCAR="POSCAR.vasp"
    else:
        sys.exit(POSCAR+" file not found")

if POSCAR:
    print("INPUT file name : %s" % str(POSCAR))

if cname:
   #print "OUTPUT file name:",cname+"_nn_"+str(find)+".out"
    print("OUTPUT file name: %s_nn_%s.out"  % (cname, str(find)))


##################################################################################
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
## ion_site[j]    : 通し番号(max=natom)を与えるとサイト内のローカル通し番号を返す
##
## position[j,3]  : 通し番号(max=natom)とx,y,z 指定で内部座標
##
##################################################################################


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
ion_site = np.zeros(natom)
ion = np.zeros(natom)
tmp = -1
for j in range(nion):
    local = -1
    for k in range(int(atoms[j])):
        tmp += 1
        local += 1
        ion[tmp] = int(j)
        ion_site[tmp] = int(local)
       #print tmp, int(ion[tmp]), int(ion_site[tmp])


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
        selective = 1
    else:
       #print "selective False"
        selective = 0

    if bool(num_reg.match(tmp[0])):
        print(tmp[0])
        sys.exit("Format Error")
    if bool(direct_reg.match(tmp[0])):
       #print "Direct Mode"
        direct = 1
    elif bool(car_reg.match(tmp[0])):
       #print "Cartesian Mode"
        direct = 0


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
for j in range(natom):
    car[j,0] = t1_x*position[j,0] + t2_x*position[j,1] + t3_x*position[j,2]
    car[j,1] = t1_y*position[j,0] + t2_y*position[j,1] + t3_y*position[j,2]
    car[j,2] = t1_z*position[j,0] + t2_z*position[j,1] + t3_z*position[j,2]

for j in range(natom):
    position[j,0] = car[j,0]*scale
    position[j,1] = car[j,1]*scale
    position[j,2] = car[j,2]*scale



###############################################
## 近接原子間距離の計算
##
find0 = find -1 # 1から初めている番号系を 0 からに変換
r = np.zeros(natom)
r_index = np.zeros(natom)

for j in range(natom):
    x1 = float(position[find0,0])
    y1 = float(position[find0,1])
    z1 = float(position[find0,2])

    x2 = float(position[j,0])
    y2 = float(position[j,1])
    z2 = float(position[j,2])

    r0 = (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) + (z2-z1)*(z2-z1)
    r1 = np.sqrt(r0)

    r[j] = r1
    r_index[j] = j

   #print j+1, int(ion[j])+1, atoms_index[int(ion[j])], int(ion_site[j])+1, r[j]


#for j in range(natom):
#    print " %5d  %14.11f " %( int(r_index[j]), r[j] )


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
n = natom -1
for j in range(n):
    for k in range(n,j,-1):
        if r[k-1] > r[k]:
            tmp = r[k]
            r[k] = r[k-1]
            r[k-1] = tmp

            tmp_index = r_index[k]
            r_index[k] = r_index[k-1]
            r_index[k-1] = tmp_index



################################################
## pre data print
##
print("scale              : %s" % str(scale))
print("translation vector : %11.9f %11.9f %11.9f" %(t1_x, t1_y, t1_z))
print("                     %11.9f %11.9f %11.9f" %(t2_x, t2_y, t2_z))
print("                     %11.9f %11.9f %11.9f" %(t3_x, t3_y, t3_z))


################################################
## data print
##    r_index[j] は 0 から始まる通しの index 番号なので注意
##    通し番号＆サイト内番号は1から始まるように出力
##
nn = open(cname+'_nn_'+str(find)+'.out','w')

#print >> nn, atoms_index[int(ion[int(find0)])],int(ion_site[find0])+1,"(",int(ion_site[find0])+1,")"
#print >> nn, "   ", "   t-index site site-index      r"
#print >> nn, "   ", "  -------------------------------------"

print("%s %d (%d)"
      % (atoms_index[int(ion[int(find0)])], int(ion_site[find0])+1, int(ion_site[find0])+1),
      file=nn)
print("      t-index site site-index      r", file=nn)
print("     -------------------------------------", file=nn)

for j in range(natom):
    print("   ","     %5d  %2s %5d    %14.11f"
                        %( int(r_index[j]) +1 ,
                           atoms_index[int(ion[int(r_index[j])])],
                           int(ion_site[int(r_index[j])]) +1,
                           r[j] ), file=nn)
nn.close


