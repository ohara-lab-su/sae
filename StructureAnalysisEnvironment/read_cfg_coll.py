#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# *_coll.cfg (RMC_POT) を読み込み, ION-LOOP 毎の原子位置出力
#
# [in]     canme          : OUTCARの名前
# [in]     nloop          : ループ数(read_cfg_coll_param にて算出)
#
# [in/out] t[3,3]         :  基本並進ベクトル(注意:配列内indexは0から)
#                                  x   y   z
#                            t1 = a11 a21 a31
#                            t2 = a12 a22 a32
#                            t3 = a13 a23 a33
#
# [in]     natom          : 総原子数
# [in]     nion           : 原子の種類の数
#
# [in/out] atoms[i]       : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
# [in/out] ion_site[i]    : 原子の通し番号を与えると、原子のサイト番号を与える
# [in/out] position_loop  : ループごとの原子位置(loop,ion,3)
#
# [return] header
# [return] comment
#
# [return] scale
# [return] direct
#
################################################################################
#
# 2014.11.21
#   ion_site[i] を追加 (read_cfg.py と互換機能および互換引数化)
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
import os
import re
from numpy import *


################################################################################
def read_cfg_coll(cname,nloop,t,natom,nion,atoms,ion_site,position_loop):

    try:
        tmp = open(cname+'.cfg')
    except:
        tmp.close()
        sys.exit("Error(read_cfg_coll.py): "+cname+".cfg not open")

    datfile = tmp.read()
    tmp.close()
    datlines = datfile.split('\n')

    num = len(datlines) -1

    lines=0

    for loop in range(nloop):

        header = datlines[lines]
        comment = datlines[lines+1]
        moves = datlines[lines+4]
        saved = datlines[lines+5]

        # 全原子数
        tmp = datlines[lines+7].split()
        natom0 = int(tmp[0])
        if natom0 != natom:
            sys.exit("NATOM is inconsistent (read_cfg_coll.py)")

        # 原子の種類の数
        tmp = datlines[lines+8].split()
        nion0 = int(tmp[0])
        if nion0 != nion:
            sys.exit("NION is inconsistent (read_cfg_coll.py)")

        nmoles = datlines[lines+9]
        angles = datlines[lines+10]

        # 基本並進ベクトル(box size vector)
        t1 = datlines[lines+14].split()
        t1_x = float(t1[0])  # lattice constant/2
        t1_y = float(t1[1])
        t1_z = float(t1[2])

        t2 = datlines[lines+15].split()
        t2_x = float(t2[0])
        t2_y = float(t2[1])
        t2_z = float(t2[2])

        t3 = datlines[lines+16].split()
        t3_x = float(t3[0])
        t3_y = float(t3[1])
        t3_z = float(t3[2])

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
        ## 原子の種類ごとの読み込み
        ##
        lines = lines+18
       #atoms = zeros((nion),dtype=int)
        for i in range(nion):
            tmp = datlines[lines].split()
            atoms[i] = int(tmp[0])
           #print atoms[i],
            lines = lines + 4
       #print ""

        ###############################################
        ## 原子種の (仮) Index を作成する
        ##
        index = 0
        for j in range(nion):
            for k in range(int(atoms[j])):
                ion_site[index] = j # イオン種別の通し番号を与えておく
               #print ion_site[index],index
                index += 1

        ###############################################
        ## Read Internal Coordinate (Direct)
        ##
       #position = zeros((natom,3))
        for i in range(natom):
            xyz = datlines[lines].split()
            position_loop[loop,i,0] = xyz[0]
            position_loop[loop,i,1] = xyz[1]
            position_loop[loop,i,2] = xyz[2]
            lines += 1
           #print " %19.15f %19.15f %19.15f" %(position_loop[loop,i,0], \
           #                                   position_loop[loop,i,1], \
           #                                   position_loop[loop,i,2])

        # 空白行のスキップ
        lines = lines + 1

#   t[1,0] = t1_y
#   t[2,0] = t1_z

#   t[0,1] = t2_x
#   t[1,1] = t2_y
#   t[2,1] = t2_z

#   t[0,2] = t3_x
#   t[1,2] = t3_y
#   t[2,2] = t3_z
#
#   print datlines[lines]

    scale = 1.0
    direct = True

    return [header,comment,scale,direct]

################################################################################

