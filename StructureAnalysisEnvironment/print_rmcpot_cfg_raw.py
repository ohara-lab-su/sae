# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# RMC_POT(cfg) 形式への出力
#   並進ベクトルや内部座標は事前に RMC_POT(cfg)形式にしておく必要がある
#   変換は conv_vasp2cfg() にて行う
#
# [in] cname              : STD=False のときの出力ファイル名
# [in] STD                : 結果出力がstdoutのときは STD=True
#
# [in] title              : タイトル
#
# [in/out] t[3,3]         : 基本並進ベクトル(注意:配列内indexは0から)
#                                  x   y   z
#                            t1 = a11 a21 a31
#                            t2 = a12 a22 a32
#                            t3 = a13 a23 a33
#
#
# [in]     natom          : number of atom
# [in]     nion           : number of atom
# [in/out] atoms[i]       : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
# [in/out] position[j,3]  : 通し番号(max=natom)とx,y,z 指定で内部座標
#
################################################################################
#
# 2018.08.21
#  Python2/3 両対応
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


# import os
# import re
# import optparse
# from numpy import *

def print_rmcpot_cfg_raw(cname, STD, title, t, natom, nion, atoms, position):
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
    ## write cfg (RMC_POT) file

    ## open cfg files
    ##
    if STD:
        out = sys.stdout
    else:
        cfg = open(cname + '.cfg', 'w')

    print(title, file=cfg)
    print(cname, file=cfg)
    print("", file=cfg)
    print("", file=cfg)

    moves = 0
    tried = 0
    accepted = 0
    saved = 0
    print("        ", moves, "        ", tried, "        ", accepted, file=cfg)
    print("        ", saved, "        ", "configurations saved", file=cfg)
    print("", file=cfg)
    print("        ", natom, " ", "molecules of all types", file=cfg)
    print("        ", nion, " ", "types of molecules", file=cfg)
    print("        ", "1", " ", "is the largest number of atoms in a molecule", file=cfg)
    print("        ", "0", " ", "Euler angles are provided", file=cfg)
    print("", file=cfg)
    print("        ", "F (box is cubic)	", file=cfg)
    print("        ", "  Defining vectors are:", file=cfg)
    print("        ", "  %13.9f %13.9f %13.9f" % (t1_x, t1_y, t1_z), file=cfg)
    print("        ", "  %13.9f %13.9f %13.9f" % (t2_x, t2_y, t2_z), file=cfg)
    print("        ", "  %13.9f %13.9f %13.9f" % (t3_x, t3_y, t3_z), file=cfg)
    print("", file=cfg)

    for j in range(int(nion)):
        print("        ", atoms[j], " ", "molecules of types  ", j + 1, file=cfg)
        print("        ", "1", " ", "atomic sites", file=cfg)
        print("        ", "     ", "0.000000   0.000000   0.000000", file=cfg)
        print("", file=cfg)

    for j in range(natom):
        print("%15.12f %15.12f %15.12f" % (position[j, 0], position[j, 1], position[j, 2]), file=cfg)

    cfg.close()
