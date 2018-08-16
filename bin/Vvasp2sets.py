#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# convert from VASP-POSCAR to HiLAPW-tsp.in file
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2014.10.09
#    1st version
#    主にxsets での対称性関係の情報を引き出すための支援ツール
#
#    1) VASP の基本並進は cubic のみ対応
#    2) HiLAP TSP は P1 なので注意
#    3) スピンは強制的に 1
#    4) k points は強制的に 8 8 8
#    5) 原子種の名前は VASP の PP 名になる
#
#    A) ~/vasp1/bin/Vvasp2sets.py
#       ~/hilapw1/bin/LAvasp2sets.py
#         ---> ハードリンクにしておく(メインマシン上では)
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
POSCAR = "POSCAR" # INPUT filename
cname  = "sets" # OUTPUT BASE filename


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
options,  args = parser.parse_args()

if options.INPUT:
    POSCAR=options.INPUT

if options.OUTPUT:
    cname=options.OUTPUT

#print args,options
if len(args) > 0:
    #print "script name:",argvs[0]
    POSCAR=args[0]

if not os.path.exists(POSCAR):
    if os.path.exists(POSCAR+".vasp"):
        POSCAR="POSCAR.vasp"
    else:
        sys.exit(POSCAR+" file not found")

if POSCAR:
    print "INPUT file name :",POSCAR

if cname:
    print "OUTPUT file name:",cname+".in"


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
## ion_site[j]    : 通し番号(max=natom)を与えるとサイト内のローカル通し番号を返す
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
for j in range(len(atoms)):
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
        print tmp, int(ion[tmp]), int(ion_site[tmp])


###############################################
## makes re rule
##
num_reg = re.compile('^[+-]?(\d*\.\d+|\d+\.?\d*)([eE][+-]?\d+|)\Z')
selective_reg = re.compile('^S.*')
direct_reg = re.compile('^D.*')
car_reg = re.compile('^C.*')


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
        selective = 1
    else:
       #print "selective False"
        selective = 0

    if bool(num_reg.match(tmp[0])):
        print tmp[0]
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
## write tsp.in (HiLAPW) file


## open cfg files
##
sets = open(cname+'.in','w')
print >> sets, title
print >> sets, "-----nspin"
print >> sets, "1"
print >> sets, "-----space group"
print >> sets, "P1"
print >> sets, " ",t1_x*scale," ",t2_y*scale," ",t3_z*scale
print >> sets, " 90.0 90.0 90.0"
print >> sets, "-----atoms"
print >> sets, "   ", nion

l=0
for j in range(nion):
    print >> sets, " ", atoms_index[j], " ", int(atoms[j])
    for k in range(int(atoms[j])):
        print >> sets, "    %14.11f %14.11f %14.11f" %(position[l,0],position[l,1],position[l,2])
        l += 1

print >> sets, "-----k points"
print >> sets, " 0"
print >> sets, " 8 8 8"

sets.close()

