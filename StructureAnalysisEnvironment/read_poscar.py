# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# POSCAR 読み込み
#
#   1) 事前に read_parm_poscar() を実行して natom と nion の取得
#   2) atoms[natom], atoms_index[natom], ion[nion], ion_local[nion]
#      を引数として用意
#
# [in]     POSCAR         : 読み込みファイル(POSCAR形式)
# [in]     VASP           : VASPのバージョン
#
# [in/out] t[3,3]         :  基本並進ベクトル(注意:配列内indexは0から)
#                            POSCAR 入力形式
#
#                                  x   y   z
#                            t1 = a11 a21 a31  ! lattice vector t1
#                            t2 = a12 a22 a32  ! lattice vector t2
#                            t3 = a13 a23 a33  ! lattice vector t3
# 注意)
#         t(基本並進行列)
#                                 t11, t12, t13
#                                 t21, t22, t23
#                                 t31, t32, t33
#
# [in/out] atoms[i]       : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
# [in/out] atoms_index[i] : 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
# [in/out] ion[j]          : 通し番号(max=natom)を与えると原子の種類番号を返す
# [in/out] ion_local[j]    : 通し番号(max=natom)を与えるとサイト内のローカル通し番号を返す
#
# [in/out] position[j,3]  : 通し番号(max=natom)とx,y,z 指定で内部座標
# [in/out] fix[j,3]       : 通し番号(max=natom)とx,y,z 指定でForceのFix/non-Fix 指定
#
# [return] title          : タイトル
# [return] scale          : 格子定数(スケールファクター)
# [return] selective      : selective mode
# [return] direct         : direct or cartesian
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
#
# 2015.01.20
#  gzip 対応版
#
# 2014.10.30 1st
#
################################################################################
from copyright import *

__status__ = "alpha"
__version__ = "0.0.2"

################################################################################

import sys
import os
import re
import gzip


# from numpy import *

def read_poscar(POSCAR, VASP, t, atoms, atoms_index, ion, ion_local, position, fix):
    ###############################################
    ## Open POSCAR file
    ##
    if os.path.exists(POSCAR):
        GZIP = False
    elif os.path.exists(POSCAR + ".gz"):
        GZIP = True
    else:
        sys.exit("STOP: " + POSCAR + " or " + POSCAR + ".gz file not found")

    try:
        if GZIP:
            tmp = gzip.open(POSCAR + ".gz")
        else:
            tmp = open(POSCAR)

        datfile = tmp.read()
    except:
        tmp.close()
        sys.exit("STOP: " + POSCAR + " does'nt open")
    finally:
        tmp.close()

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

    # t = zeros((3,3))
    t[0, 0] = t1_x
    t[1, 0] = t1_y
    t[2, 0] = t1_z

    t[0, 1] = t2_x
    t[1, 1] = t2_y
    t[2, 1] = t2_z

    t[0, 2] = t3_x
    t[1, 2] = t3_y
    t[2, 2] = t3_z

    ###############################################
    ## get VASP version, atoms and index
    ##
    i = 5
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
    nion = int(len(atoms))
    natom = 0
    for j in range(nion):
        sum = int(atoms[j])
        natom = natom + sum
    # print "natom= ",natom

    ###############################################
    ## makes index
    ##
    # ion_local = zeros(natom)
    # ion = zeros(natom)
    tmp = -1
    for j in range(nion):
        local = -1
        for k in range(int(atoms[j])):
            tmp += 1
            local += 1
            ion[tmp] = int(j)
            ion_local[tmp] = int(local)
        # print tmp, int(ion[tmp]), int(ion_local[tmp])

    ###############################################
    ## makes re rule
    ##
    num_reg = re.compile('^[+-]?(\d*\.\d+|\d+\.?\d*)([eE][+-]?\d+|)\Z')
    selective_reg = re.compile('^S.*', re.IGNORECASE)
    direct_reg = re.compile('^D.*', re.IGNORECASE)
    car_reg = re.compile('^C.*', re.IGNORECASE)

    ###############################################
    ## get atomc coordinate mode
    ##
    i += 1
    tmp = datlines[i].split()
    if bool(num_reg.match(tmp[0])):
        print("%s" % str(tmp[0]))
        sys.exit("Format Error")
    else:
        if bool(selective_reg.match(tmp[0])):
            # print "selective True"
            i += 1
            tmp = datlines[i].split()
            selective = True
        else:
            # print "selective False"
            selective = False

        if bool(num_reg.match(tmp[0])):
            print("%s" % str(tmp[0]))
            sys.exit("Format Error")
        if bool(direct_reg.match(tmp[0])):
            # print "Direct Mode"
            direct = True
        elif bool(car_reg.match(tmp[0])):
            # print "Cartesian Mode"
            direct = False

    ###############################################
    ## get atomic coordinate position
    ##
    # position = zeros((int(natom),3))
    i += 1
    for j in range(natom):
        xyz = datlines[i + j].split()
        position[j, 0] = xyz[0]
        position[j, 1] = xyz[1]
        position[j, 2] = xyz[2]
        if selective:
            fix[j, 0] = str(xyz[3])
            fix[j, 1] = str(xyz[4])
            fix[j, 2] = str(xyz[5])
    # print j,
    # print " %16.12f %16.12f %16.12f" %(position[j,0],position[j,1],position[j,2]),
    # print fix[j,0],fix[j,1],fix[j,2]

    return [title, scale, selective, direct]
