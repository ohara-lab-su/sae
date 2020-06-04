# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# *.cfg ファイル読み込み
#
# [in/out] cname          : *.cfg filename
#
# [in/out] atoms[i]       : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
# [in/out] ion_site[i]    : 原子の通し番号を与えると、原子のサイト番号を与える
#                           [注意] *.cfg形式は種類を与えないので 0 番から違う種類毎
#                                    に(仮に)無理やりナンバリングする
#
# [in/out] t[3,3]         :  基本並進ベクトル(注意:配列内indexは0から)
#                                  x   y   z
#                            t1 = a11 a21 a31
#                            t2 = a12 a22 a32
#                            t3 = a13 a23 a33
#
# [in/out] position[j,3]  : 通し番号(max=natom)とx,y,z 指定で内部座標
#
# [return] header         : ヘッダー(1)
# [return] comment        : ヘッダー(2)
#
################################################################################
#
# 2014.10.30/31 1st
#
################################################################################
from __future__ import print_function
from copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import sys
import os
import optparse
from numpy import *


def read_cfg(cname, t, atoms, ion_site, position):
    ###############################################
    ## Open RMC_POT cfg file
    ##
    try:
        tmp = open(cname + '.cfg')
    except:
        tmp.close()
        sys.exit("Error(read_cfg.py): " + cname + ".cfg not open")

    datfile = tmp.read()
    tmp.close()
    datlines = datfile.split('\n')

    ###############################################
    ## Read Header
    ##
    header = str(datlines[0])
    comment = str(datlines[1])
    tmp = datlines[2]
    tmp = datlines[3]

    moves = datlines[4]
    saved = datlines[5]
    tmp = datlines[6]

    a = datlines[7].split()
    natom = int(a[0])

    a = datlines[8].split()
    nion = int(a[0])

    nmoles = datlines[9]
    angles = datlines[10]
    tmp = datlines[11]

    tmp = datlines[12]
    tmp = datlines[13]

    ###############################################
    ## Read Lattice Vector
    ##
    v = datlines[14].split()
    t1_x = float(v[0])  # lattice constant/2
    t1_y = float(v[1])
    t1_z = float(v[2])

    v = datlines[15].split()
    t2_x = float(v[0])
    t2_y = float(v[1])
    t2_z = float(v[2])

    v = datlines[16].split()
    t3_x = float(v[0])
    t3_y = float(v[1])
    t3_z = float(v[2])

    t[0, 0] = float(t1_x)
    t[1, 0] = float(t1_y)
    t[2, 0] = float(t1_z)

    t[0, 1] = float(t2_x)
    t[1, 1] = float(t2_y)
    t[2, 1] = float(t2_z)

    t[0, 2] = float(t3_x)
    t[1, 2] = float(t3_y)
    t[2, 2] = float(t3_z)

    tmp = datlines[17]

    ###############################################
    ## 原子の種類ごとの読み込み
    ##
    lines = 17
    # atoms = zeros((int(nion)+1))
    for i in range(int(nion)):
        lines += 1
        n = datlines[lines].split()
        atoms[i] = int(n[0])
        lines += 1
        tmp = datlines[lines]
        lines += 1
        tmp = datlines[lines]
        lines += 1
        tmp = datlines[lines]

    ###############################################
    ## 原子種の (仮) Index を作成する
    ##
    index = 0
    for j in range(nion):
        for k in range(atoms[j]):
            ion_site[index] = j  # イオン種別の通し番号を与えておく
            # print ion_site[index],index
            index += 1

    ###############################################
    ## Read Internal Coordinate
    ##
    # position = zeros((int(natom)+1,3))
    for i in range(int(natom)):
        lines += 1
        xyz = datlines[lines].split()
        position[i, 0] = xyz[0]
        position[i, 1] = xyz[1]
        position[i, 2] = xyz[2]
    # print position[i,0], position[i,1], position[i,2]

    return [header, comment]
