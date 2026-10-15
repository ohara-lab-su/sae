# -*- coding: utf-8 -*-
##################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# POSCAR 書き込み
#  print_poscar.py の簡易版 ( 非FORCE, VASP4形式+dummy )
#
#
# [in] cname              : STD=False のときの出力ファイル名
# [in] STD                : 結果出力がstdoutのときは STD=True
#
# [in] title              : タイトル
# [in] scale              : scale factor
#
# [in] natom              : number of atom
# [in] nion               : number of ion
#
# [in] direct             : Direct Mode on/off FLAG
# [in] PV5FLAG            : 擬似VASP5 on/off FLAG
#
# [in/out] t[3,3]         : 基本並進ベクトル(注意:配列内indexは0から)
#                                  x   y   z
#                            t1 = a11 a21 a31
#                            t2 = a12 a22 a32
#                            t3 = a13 a23 a33
#
# [in/out] atoms[i]       : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
# [in] dummy              : 擬似VASP5 対応(原子種記号の手動入力)
#
# [in/out] position[j,3]  : 通し番号(max=natom)とx,y,z 指定で内部座標
#
##################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2014.10.30/31 1st
#
##################################################################################
from __future__ import print_function
try:
    from .copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

###################################################################################

import sys
import os
import re
from numpy import *


def print_poscar4(cname, STD, title, scale, natom, nion, direct, PV5FLAG, t, atoms, dummy, position):
    ## open poscar file
    ##
    if STD:
        out = sys.stdout
    else:
        out = open(cname + '.vasp', 'w')

    print(str(title), file=out)
    print(" ", scale, file=out)
    print("  %13.9f %13.9f %13.9f" % (t[0, 0], t[1, 0], t[2, 0]), file=out)
    print("  %13.9f %13.9f %13.9f" % (t[0, 1], t[1, 1], t[2, 1]), file=out)
    print("  %13.9f %13.9f %13.9f" % (t[0, 2], t[1, 2], t[2, 2]), file=out)

    if PV5FLAG:
        print(" ", dummy, file=out)

    for i in range(int(nion)):
        print(int(atoms[i]), file=out, end="")
    print("", file=out)

    if direct:
        print("Direct", file=out)
    else:
        print("Cartesian", file=out)

    for i in range(int(natom)):
        #       print(" %13.9f %13.9f %13.9f" %(position[i,0],position[i,1],position[i,2]), file=out)
        print(" %13.9f %13.9f %13.9f" % (position[i, 0], position[i, 1], position[i, 2]), file=out)
        print("")

    out.close()
