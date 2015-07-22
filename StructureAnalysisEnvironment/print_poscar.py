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
# 2015.07.08
#  stdout の close を修正
#
# 2014.10.30/31 1st
#
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
#import os
#import re
#from numpy import *


def print_poscar(cname,STD,\
                 title,scale,natom,nion,selective,direct,VASP,\
                 t,atoms,atoms_index,position,fix):

    ## open poscar file
    ##
    if STD:
        out = sys.stdout
    else:
        try:
            out = open(cname+'.vasp','w')
        except:
            out.close()
            sys.exit("STOP:"+cname+".vasp can't open")

    print >> out, title
    print >> out, " ",scale
    print >> out, "  %13.9f %13.9f %13.9f" %(t[0,0],t[1,0],t[2,0])
    print >> out, "  %13.9f %13.9f %13.9f" %(t[0,1],t[1,1],t[2,1])
    print >> out, "  %13.9f %13.9f %13.9f" %(t[0,2],t[1,2],t[2,2])

    if VASP == 5:
        print >> out, " ",
        for i in range(nion):
            print >> out, atoms_index[i],
        print >> out, " "
    print >> out, " ",

    for i in range(nion):
        print >> out, atoms[i],
    print >> out, " "

    if selective:
        print >> out, "Selective Dynamics"

    if direct:
        print >> out, "Direct"
    else:
        print >> out, "Cartesian"

    for i in range(int(natom)):
        print >> out, " %13.9f %13.9f %13.9f" %(position[i,0],position[i,1],position[i,2]),
        if selective:
            print >> out, "",
            print >> out, fix[i,0],fix[i,1],fix[i,2],
        print >> out, ""

    if STD:
        sys.stdout = sys.__stdout__
    else:
        out.close()

