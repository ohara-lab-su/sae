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
################################################################################
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
################################################################################
################################################################################
################################################################################
#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# *_coll.cfg (RMC_POT) 読み込み, ION-LOOP 毎の原子位置(&力)読み込み専用の事前準備
#
#  LOOP 回数を算出
#
# [in]     canme  : OUTCARの名前
#
# [return] nloop  : LOOP数
# [return] natom  : 総原子数
# [return] nion   : 原子の種類
#
################################################################################
################################################################################
################################################################################
################################################################################
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# *.cfg ファイル読み込みのための準備関数
#
# [in/out] cname    : *.cfg filename
#
# [return] natom    : number of atom
# [return] nion    : number of ion
#
################################################################################
#
# 2014.10.30 1st
#
################################################################################
################################################################################
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import optparse
from numpy import *
import re


class RmcConfigFields:

    def read_cfg(self, cname, t, atoms, ion_site, position):
        ###############################################
        ## Open RMC_POT cfg file
        ##
        try:
            tmp = open(cname + ".cfg")
        except:
            tmp.close()
            sys.exit("Error(read_cfg.py): " + cname + ".cfg not open")
        datfile = tmp.read()
        tmp.close()
        datlines = datfile.split("\n")
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
        # lattice constant/2
        t1_x = float(v[0])
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
            # print ion_site[index],index
            for k in range(atoms[j]):
                # イオン種別の通し番号を与えておく
                ion_site[index] = j
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

    def read_cfg_coll(
        self, cname, nloop, t, natom, nion, atoms, ion_site, position_loop
    ):
        try:
            tmp = open(cname + ".cfg")
        except:
            tmp.close()
            sys.exit("Error(read_cfg_coll.py): " + cname + ".cfg not open")
        datfile = tmp.read()
        tmp.close()
        datlines = datfile.split("\n")
        num = len(datlines) - 1
        lines = 0
        # 全原子数
        # 原子の種類の数
        # 基本並進ベクトル(box size vector)
        ###############################################
        ## 原子の種類ごとの読み込み
        ##
        # atoms = zeros((nion),dtype=int)
        # print ""
        ###############################################
        ## 原子種の (仮) Index を作成する
        ##
        ###############################################
        ## Read Internal Coordinate (Direct)
        ##
        # position = zeros((natom,3))
        # print " %19.15f %19.15f %19.15f" %(position_loop[loop,i,0], \
        #                                   position_loop[loop,i,1], \
        #                                   position_loop[loop,i,2])
        # 空白行のスキップ
        for loop in range(nloop):
            header = datlines[lines]
            comment = datlines[lines + 1]
            moves = datlines[lines + 4]
            saved = datlines[lines + 5]
            tmp = datlines[lines + 7].split()
            natom0 = int(tmp[0])
            if natom0 != natom:
                sys.exit("NATOM is inconsistent (read_cfg_coll.py)")
            tmp = datlines[lines + 8].split()
            nion0 = int(tmp[0])
            if nion0 != nion:
                sys.exit("NION is inconsistent (read_cfg_coll.py)")
            nmoles = datlines[lines + 9]
            angles = datlines[lines + 10]
            t1 = datlines[lines + 14].split()
            # lattice constant/2
            t1_x = float(t1[0])
            t1_y = float(t1[1])
            t1_z = float(t1[2])
            t2 = datlines[lines + 15].split()
            t2_x = float(t2[0])
            t2_y = float(t2[1])
            t2_z = float(t2[2])
            t3 = datlines[lines + 16].split()
            t3_x = float(t3[0])
            t3_y = float(t3[1])
            t3_z = float(t3[2])
            t[0, 0] = t1_x
            t[1, 0] = t1_y
            t[2, 0] = t1_z
            t[0, 1] = t2_x
            t[1, 1] = t2_y
            t[2, 1] = t2_z
            t[0, 2] = t3_x
            t[1, 2] = t3_y
            t[2, 2] = t3_z
            lines = lines + 18
            # print atoms[i],
            for i in range(nion):
                tmp = datlines[lines].split()
                atoms[i] = int(tmp[0])
                lines = lines + 4
            index = 0
            for j in range(nion):
                # print ion_site[index],index
                for k in range(int(atoms[j])):
                    # イオン種別の通し番号を与えておく
                    ion_site[index] = j
                    index += 1
            for i in range(natom):
                xyz = datlines[lines].split()
                position_loop[loop, i, 0] = xyz[0]
                position_loop[loop, i, 1] = xyz[1]
                position_loop[loop, i, 2] = xyz[2]
                lines += 1
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
        return [header, comment, scale, direct]

    def read_cfg_coll_param(self, cname):
        try:
            tmp = open(cname + ".cfg")
        except:
            tmp.close()
            sys.exit("Error(read_cfg_coll_param.py): " + cname + " not open")
        datfile = tmp.read()
        tmp.close()
        datlines = datfile.split("\n")
        num = len(datlines) - 1
        # 読み込みスタート行
        lines = 0
        # 全原子数
        t = datlines[lines + 7].split()
        natom = int(t[0])
        # 原子の種類の数
        t = datlines[lines + 8].split()
        nion = int(t[0])
        # ヘッダー部分(固定行)のまとめてスキップ
        lines = lines + 18
        # 原子種ごとの読み込み行
        lines = lines + nion * 4
        # 内部座標(ループごとの原子数)
        lines = lines + natom
        # ファイルの最後の空白行
        lines = lines + 1
        # 一つのループ毎の*.cfg行数
        max_lines = lines
        # ループ数
        nloop = num / max_lines
        #   print "MAX_LINES      : ", num
        #   print "MAX_LINES/LOOP : ", max_lines
        #   print "NUM. OF LOOP   : ", nloop
        #   次のループの先頭
        #   print datlines[lines]
        return (nloop, natom, nion)

    def read_cfg_param(self, cname):
        ###############################################
        ## Open RMC_POT cfg file
        ##
        try:
            tmp = open(cname + ".cfg")
        except:
            tmp.close()
            sys.exit("Error(read_cfg_param.py): " + cname + ".cfg not open")
        datfile = tmp.read()
        tmp.close()
        datlines = datfile.split("\n")
        ###############################################
        ## Read Header
        ##
        a = datlines[7].split()
        natom = int(a[0])
        a = datlines[8].split()
        nion = int(a[0])
        return [natom, nion]
