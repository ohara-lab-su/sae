# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# *.dat (RMC_POT) ファイル読み込み、density を書きなおして *.dat 出力する
#
# ほぼ再利用できない （しにくい）特化型アホルーチン (2014.11.07)
#
# [in]     STD     : 標準出力するかどうかのフラグ
# [in]     datname : 読み込む、基本となる *.dat ファイル
# [in]     outname : 出力する *.dat ファイル名
#
# [in]     density : 新しい density の値
#
################################################################################
#
# 2018.08.21
#  Python2/3 両対応
#
# 2014.10.11.07 1st
#
################################################################################
################################################################################
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# RMC_POT 形式の座標系からVASP形式の座標系へ変換
#   VASP 以外でも同じ、cartesian 系の並進＆内部座標系
#   基本並進ベクトル＆内部座標
#   scale factor は自動的に 1.0 になる( 1.0 としている)
#
#   RMC_POT 形式は direct mode のみ(のはず)
#
# [in]     scale          : scale
# [in]     natom          : number of atom
#
# [in]     direct         : Direct モードのみ対応なのは前提なので必要ない
#                           ただし、他のライブラリとの整合性のためにこの引数を入れる
#
# [in/out] t[3,3]         : 基本並進ベクトル(注意:配列内indexは0から)
#                                  x   y   z
#                            t1 = a11 a21 a31
#                            t2 = a12 a22 a32
#                            t3 = a13 a23 a33
#
# [in/out] position[j,3]  : 通し番号(max=natom)とx,y,z 指定で内部座標
#
# [return] scale          : scale
# [return] direct         : Direct mode は Trune を返す(一応)
#
################################################################################
#
# 2015.08.24
#  戻り値版と引数版のルールの再統一に合わせる
#    引数版 conv_cfg2vasp()  --> conv_cfg2vaspa()
#
# 2014.10.31 bug fix
# 2014.10.30 1st
#
################################################################################
################################################################################
# 戻り値版 (cfg2vaspa() <---> cfg2vasp() )
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# VPAS 形式での座標から RMC_POT 形式の座標系への変換
#   基本並進ベクトル＆内部座標
#
# [in]     scale          : スケールファクター
# [in/out] t[3,3]         : 基本並進ベクトル(注意:配列内indexは0から)
#                                  x   y   z
#                            t1 = a11 a21 a31
#                            t2 = a12 a22 a32
#                            t3 = a13 a23 a33
#
# [in]     natom          : number of atom
# [in/out] position[j,3]  : 通し番号(max=natom)とx,y,z 指定で内部座標
#
# [return] scale          : direct mode は True を返す
# [return] direct         : direct mode は True を返す
#
################################################################################
#
# 2015.08.24
#  戻り値版と引数版のルールの再統一に合わせる
#   引数版   conv_vasp2cfg()  --> conv_vasp2cfga()
#   戻り値版 conv_vasp2cfg1() --> conv_vasp2cfg()
#
# 2015.03.10
#  戻り値と引数を1:1にしたバージョンの関数を作成
#   conv_vasp2cfg
#
# 2014.10.31 bug fix
# 2014.10.30 1st
#
################################################################################
################################################################################
# import os
# import re
# import optparse
# from numpy import *
################################################################################
# 引数版
################################################################################
# 戻り値版
#
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import optparse
import numpy as np
import re
from numpy import *


class RmcConversions:

    def change_density(self, STD, datname, outname, density):
        ###############################################
        ## Open RMC_POT cfg file
        ##
        tmp = open(datname + ".dat")
        datfile = tmp.read()
        tmp.close
        datlines = datfile.split("\n")
        nline = len(datlines)
        header = datlines[0]
        lines = datlines[1].split()
        n = len(lines)
        ###
        if STD:
            out = sys.stdout
        else:
            out = open(outname + ".dat", "w")
        print(datlines[0].rstrip(), file=out)
        lines[0] = density
        for i in range(n):
            print(lines[i], file=out, end="")
        print("", file=out)
        for i in range(2, nline):
            print(datlines[i].rstrip(), file=out)
        out.close
        return

    def conv_cfg2vaspa(self, scale, t, natom, direct, position):
        """
        :param scale:
        :param t:
        :param natom:
        :param direct:
        :param position:
        :return:
        """
        if not direct:
            sys.exit("STOP: input file is not direct mode")
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
        ## DATA convert (RMC_POT to VASP )
        ##
        t1_x = t1_x * 2
        t1_y = t1_y * 2
        t1_z = t1_z * 2
        t2_x = t2_x * 2
        t2_y = t2_y * 2
        t2_z = t2_z * 2
        t3_x = t3_x * 2
        t3_y = t3_y * 2
        t3_z = t3_z * 2
        x_offset = 0.5
        y_offset = 0.5
        z_offset = 0.5
        # for Direct
        for i in range(int(natom)):
            position[i, 0] = position[i, 0] / 2 + x_offset
            position[i, 1] = position[i, 1] / 2 + y_offset
            position[i, 2] = position[i, 2] / 2 + z_offset
        t[0, 0] = t1_x
        t[1, 0] = t1_y
        t[2, 0] = t1_z
        t[0, 1] = t2_x
        t[1, 1] = t2_y
        t[2, 1] = t2_z
        t[0, 2] = t3_x
        t[1, 2] = t3_y
        t[2, 2] = t3_z
        scale = scale
        direct = True
        return (scale, direct)

    def conv_vasp2cfga(self, scale0, t, natom, direct, position):
        if not direct:
            sys.exit("STOP: input file is not direct mode")
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
        ## data convert for cfg (RMC_POT) format
        ## from direct to direct coordinate
        ##
        t1_x = scale0 * t1_x / 2.0
        t1_y = scale0 * t1_y / 2.0
        t1_z = scale0 * t1_z / 2.0
        t2_x = scale0 * t2_x / 2.0
        t2_y = scale0 * t2_y / 2.0
        t2_z = scale0 * t2_z / 2.0
        t3_x = scale0 * t3_x / 2.0
        t3_y = scale0 * t3_y / 2.0
        t3_z = scale0 * t3_z / 2.0
        x_offset = 0.5
        y_offset = 0.5
        z_offset = 0.5
        for j in range(int(natom)):
            position[j, 0] = (position[j, 0] - x_offset) * 2.0
            position[j, 1] = (position[j, 1] - y_offset) * 2.0
            position[j, 2] = (position[j, 2] - z_offset) * 2.0
        # print " %16.12f %16.12f %16.12f" %(position[j,0],position[j,1],position[j,2])
        t[0, 0] = t1_x
        t[1, 0] = t1_y
        t[2, 0] = t1_z
        t[0, 1] = t2_x
        t[1, 1] = t2_y
        t[2, 1] = t2_z
        t[0, 2] = t3_x
        t[1, 2] = t3_y
        t[2, 2] = t3_z
        scale = 1.0
        direct = True
        return [scale, direct]

    def conv_vasp2cfg(self, scale0, t, natom, direct, position):
        if not direct:
            sys.exit("STOP: input file is not direct mode")
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
        ## data convert for cfg (RMC_POT) format
        ## from direct to direct coordinate
        ##
        t1_x = scale0 * t1_x / 2.0
        t1_y = scale0 * t1_y / 2.0
        t1_z = scale0 * t1_z / 2.0
        t2_x = scale0 * t2_x / 2.0
        t2_y = scale0 * t2_y / 2.0
        t2_z = scale0 * t2_z / 2.0
        t3_x = scale0 * t3_x / 2.0
        t3_y = scale0 * t3_y / 2.0
        t3_z = scale0 * t3_z / 2.0
        x_offset = 0.5
        y_offset = 0.5
        z_offset = 0.5
        for j in range(int(natom)):
            position[j, 0] = (position[j, 0] - x_offset) * 2.0
            position[j, 1] = (position[j, 1] - y_offset) * 2.0
            position[j, 2] = (position[j, 2] - z_offset) * 2.0
        # print " %16.12f %16.12f %16.12f" %(position[j,0],position[j,1],position[j,2])
        t[0, 0] = t1_x
        t[1, 0] = t1_y
        t[2, 0] = t1_z
        t[0, 1] = t2_x
        t[1, 1] = t2_y
        t[2, 1] = t2_z
        t[0, 2] = t3_x
        t[1, 2] = t3_y
        t[2, 2] = t3_z
        scale = 1.0
        direct = True
        return (scale, t, natom, direct, position)
