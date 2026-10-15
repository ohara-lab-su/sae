# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# POSCAR 書き込み
#   VASP4/VASP5/force/direct/car , VASP 形式フル対応版
#
#
# [in] cname              : STD=False のときの出力ファイル名
# [in] STD                : 結果出力がstdoutのときは STD=True
#
# [in] title              : タイトル
# [in] scale              : 格子定数(スケールファクター)
# [in] natom              : number of atom
# [in] nion               : number of ion
# [in] selective          : selective mode
# [in] direct             : direct or cartesian
# [in] VASP               : VASP のバージョン
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
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.07.08
#  stdout の close を修正
#
# 2014.10.30/31 1st
#
################################################################################
from __future__ import print_function

try:
    from .copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import sys


# import os
# import re
# from numpy import *


def print_poscar(cname, STD,
                 title, scale, natom, nion, selective, direct, VASP,
                 t, atoms, atoms_index, position, fix):
    """
    画面出力(ファイル出力にも使う）結果の出力ルーチン

    :param cname:
    :param STD:
    :param title:
    :param scale:
    :param natom:
    :param nion:
    :param selective:
    :param direct:
    :param VASP:
    :param t:
    :param atoms:
    :param atoms_index:
    :param position:
    :param fix:
    :return:
    """
    # open poscar file
    #
    if STD:
        out = sys.stdout
    else:
        try:
            out = open(cname + '.vasp', 'w')
        except:
            out.close()
            sys.exit("STOP:" + cname + ".vasp can't open")

    print("------------------------------------------------- START")
    print(title, file=out)
    print(" ", scale, file=out)
    print("  %13.9f %13.9f %13.9f" % (t[0, 0], t[1, 0], t[2, 0]), file=out)
    print("  %13.9f %13.9f %13.9f" % (t[0, 1], t[1, 1], t[2, 1]), file=out)
    print("  %13.9f %13.9f %13.9f" % (t[0, 2], t[1, 2], t[2, 2]), file=out)

    if VASP == 5:
        print(" ", file=out, end="")
        for i in range(nion):
            print("%s " % atoms_index[i], file=out, end="")
        print(" ", file=out)
    print(" ", file=out, end="")

    for i in range(nion):
        print("%s " % atoms[i], file=out, end="")
    print(" ", file=out)

    if selective:
        print("Selective Dynamics", file=out)

    if direct:
        print("Direct", file=out)
    else:
        print("Cartesian", file=out)

    for i in range(int(natom)):
        print(" %13.9f %13.9f %13.9f" % (position[i, 0], position[i, 1], position[i, 2]), file=out, end="")
        if selective:
            print(" ", file=out, end="")
            print(fix[i, 0].decode('ascii'), fix[i, 1].decode('ascii'), fix[i, 2].decode('ascii'), file=out, end="")
        print("", file=out)

    if STD:
        sys.stdout = sys.__stdout__
    else:
        out.close()
