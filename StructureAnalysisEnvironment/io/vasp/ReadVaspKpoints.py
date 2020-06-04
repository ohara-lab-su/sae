#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# VASP
# ReadKpoints.py
#
#  KPOINTS 読み込みクラス
#
#    KPOINTS ファイル自体すべてのモードを使いこなしているわけではないので、
#    よく使う一部機能のみ読み込み可能な形で実装。
#     auto-mode
#     line-mode
#    は最低限読み込む。ただし、ウェイトのところは読まない。
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応暫定
#
# 2015.10.21
#  インスタンス重視の方針変更にしたがって大幅改変
#
# 2015.01.28
#  title の取得における末尾までの空白削除を追加
#
# 2015.01.28
#
#   # もし line-mode ならば line の分割数(num_line) をゲットする
#   def get_div_kpoints_line(self):
#
# 2015.01.28
#
#    # KPOINTS に記述した K-POINTS のゾーン数をゲットする
#    def get_num_kpoints_line(self):
#
# 2015.01.28
#
#   # KPOINTS の各ゾーンの比率(全部足しあわせて1.0となる)
#   def get_kpoints_vector_ratio(self,outcarname):
#
# 2015.01.27
#  kpoints_array で求めたKPOINTS の line 情報から
#  各逆格子のゾーンにおける距離を求める method の実装
#
#  get_kpoints_vector()
#
#  注意)
#     ただし、逆格子の基本並進ベクトルの情報を必要とするので
#     OUTCAR を読み込む(必須)
#
# 2015.01.27 startup
#   get_title()
#   get_kpoints_mode()
#   get_kpoints()
#   get_kpoints_array()
#   get_kpoints_array_num()
#
################################################################################
from __future__ import print_function
###############################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.5"
################################################################################

import sys
import os
import gzip
import re
import numpy as np

#import re
#from copy import deepcopy
import StructureAnalysisEnvironment as SAEnv

################################################################################
class ReadVaspKpoints(object):

    def __init__(self, KPOINTS='KPOINTS'):

        self.datlines, self.num = SAEnv.read_dataline(KPOINTS)

        # 一行目: コメント(実質的には K-POINTS としか書かない)
        self.title = re.sub(' *$','', str(self.datlines[0]))

        ############################### K-Mesh 作成情報
        # mode-チェック (auto-mode or line-mode のチェック)
        # 二行目が0のときは auto-mode, 0以外の時は手動(hand) or line-mode
        auto_FLAG = False  # FLAGS[0]  auto
        line_FLAG = False  # FLAGS[1]  line
        hand_FLAG = False  # FLAGS[2]  hand
        car_FLAG = False   # FLAGS[3]  cartesian
        rec_FLAG = False   # FLAGS[4]  reciprocal
        gamma_FLAG = False # FLAGS[5]  gamma
        monk_FLAG = False  # FLAGS[6]  monk

        i = 0
        # 非auto-mode の時
        if int(self.datlines[1]) > 0:
            mode_line = str(self.datlines[2].split()[0])

            if mode_line[0:1] == 'L' or mode_line[0:1] == 'l':
                line_FLAG = True
                i += 1
            else:
                hand_FLAG = True

            mode_line = str(self.datlines[2+i].split()[0])

            if mode_line[0:1] == 'c' or mode_line[0:1] == 'C':
                car_FLAG = True
            elif mode_line[0:1] == 'r' or mode_line[0:1] == 'R':
                rec_FLAG = True

        # auto-mode の時
        else:
            auto_FLAG = True
            mode_line = str(self.datlines[2].split()[0])

            if mode_line[0:1] == 'g' or mode_line[0:1] == 'G':
                gamma_FLAG = True
            elif mode_line[0:1] == 'm' or mode_line[0:1] == 'M':
                monk_FLAG = True

        self.FLAGS = auto_FLAG, line_FLAG, hand_FLAG,\
                car_FLAG, rec_FLAG, gamma_FLAG, monk_FLAG

        ############################# K-Mesh 情報 (手動 or 自動)
        # 四行目 for auto-mode
        self.kx = 0
        self.ky = 0
        self.kz = 0
        if auto_FLAG:
            self.kx = int(self.datlines[3].split()[0])
            self.ky = int(self.datlines[3].split()[1])
            self.kz = int(self.datlines[3].split()[2])
            self.kpoints_array = np.zeros((1,3))
            self.kpoints_array[0,:] = self.kx, self.ky, self.kz
        else:
            start = 3
            if line_FLAG:
                start += 1

            # 空白行を削除したことによる行数の減少を考慮した、K点配列数の確保
            j = 0
            for i in range(start,self.num):
                if len(self.datlines[i]) > 0:
                    j += 1

            self.kpoints_array_num = j

            if line_FLAG:
                self.kpoints_array = np.zeros((self.kpoints_array_num,3))
            elif hand_FLAG:
                self.kpoints_array_num = int(self.datlines[1])
                self.kpoints_array = np.zeros((self.kpoints_array_num,3))

            j = 0
            for i in range(start,self.num):
                if len(self.datlines[i]) > 0:
                    self.kpoints_array[j,0] = float(self.datlines[i].split()[0])
                    self.kpoints_array[j,1] = float(self.datlines[i].split()[1])
                    self.kpoints_array[j,2] = float(self.datlines[i].split()[2])
                    j += 1
                    if j >= self.kpoints_array_num:
                        break

    ############################################################################

    def get_title(self):
        return self.title

    def get_kpoints_mode(self): # auto-mode, cartesian, monk, gamma,,,
        return self.FLAGS

    def get_kpoints(self):
        return [self.kx,self.ky,self.kz]

    def get_kpoints_array(self):
        return self.kpoints_array

    def get_kpoints_array_num(self):
        return self.kpoints_array_num

    ############################################################################
    #  kpoints_array で求めたKPOINTS の line 情報から
    #  各逆格子のゾーンにおける距離を求める method の実装
    #  OUTCAR の読み込みが必須
    def get_kpoints_vector(self,outcarname):

        import StructureAnalysisEnvironment as SAEnv
        import math

        # get kpoints
        kpoints_array = self.get_kpoints_array()

        # get reciprocal vector
#       outcarname = 'OUTCAR'
        outcar = SAEnv.ReadVaspOutcar(outcarname)
        kpoints_type = outcar.get_kpoints_type()
        rec_t = outcar.get_reciprocal_t_init()

#       print kpoints_type
#       print " reciprocal lattice vectors "
#       print " %12.9f %12.9f %12.9f" % ( rec_t[0,0], rec_t[1,0], rec_t[2,0])
#       print " %12.9f %12.9f %12.9f" % ( rec_t[0,1], rec_t[1,1], rec_t[2,1])
#       print " %12.9f %12.9f %12.9f" % ( rec_t[0,2], rec_t[1,2], rec_t[2,2])

        if len(kpoints_array) % 2 != 0:
            sys.exit("STOP: num of kpoints is odd")

        v = np.zeros(int(len(kpoints_array)/2))
        j = 0
        a_x = 0
        a_y = 0
        a_z = 0
        for i in range(len(kpoints_array)):
            ################### even
            if (i+1) % 2 == 0:
                if kpoints_type == 'reciprocal':

                    b_x0 = kpoints_array[i,0]
                    b_y0 = kpoints_array[i,1]
                    b_z0 = kpoints_array[i,2]

                    rec_t1_x = rec_t[0,0]
                    rec_t1_y = rec_t[1,0]
                    rec_t1_z = rec_t[2,0]

                    rec_t2_x = rec_t[0,1]
                    rec_t2_y = rec_t[1,1]
                    rec_t2_z = rec_t[2,1]

                    rec_t3_x = rec_t[0,2]
                    rec_t3_y = rec_t[1,2]
                    rec_t3_z = rec_t[2,2]

                    b_x = 1.0*( b_x0*rec_t1_x + b_y0*rec_t2_x + b_z0*rec_t3_x )
                    b_y = 1.0*( b_x0*rec_t1_y + b_y0*rec_t2_y + b_z0*rec_t3_y )
                    b_z = 1.0*( b_x0*rec_t1_z + b_y0*rec_t2_z + b_z0*rec_t3_z )

                else:
                    b_x = kpoints_array[i,0]
                    b_y = kpoints_array[i,1]
                    b_z = kpoints_array[i,2]

                v0 = (b_x - a_x)**2 + (b_y - a_y)**2 + (b_z - a_z)**2
                v[j] = math.sqrt( math.fabs(v0))
                j +=1
            ################### odd
            else:
                if kpoints_type == 'reciprocal':
                    a_x0 = kpoints_array[i,0]
                    a_y0 = kpoints_array[i,1]
                    a_z0 = kpoints_array[i,2]

                    rec_t1_x = rec_t[0,0]
                    rec_t1_y = rec_t[1,0]
                    rec_t1_z = rec_t[2,0]

                    rec_t2_x = rec_t[0,1]
                    rec_t2_y = rec_t[1,1]
                    rec_t2_z = rec_t[2,1]

                    rec_t3_x = rec_t[0,2]
                    rec_t3_y = rec_t[1,2]
                    rec_t3_z = rec_t[2,2]

                    a_x = 1.0*( a_x0*rec_t1_x + a_y0*rec_t2_x + a_z0*rec_t3_x )
                    a_y = 1.0*( a_x0*rec_t1_y + a_y0*rec_t2_y + a_z0*rec_t3_y )
                    a_z = 1.0*( a_x0*rec_t1_z + a_y0*rec_t2_z + a_z0*rec_t3_z )

                else:
                    a_x = kpoints_array[i,0]
                    a_y = kpoints_array[i,1]
                    a_z = kpoints_array[i,2]
        return v

    # KPOINTS に記述した K-POINTS のゾーン数をゲットする
    def get_num_kpoints_line(self):
        kpoints_array = self.get_kpoints_array()
        self.num_kpoints_line = len(kpoints_array)/2
        return self.num_kpoints_line

    # もし line-mode ならば line の分割数(num_line) をゲットする
    def get_div_kpoints_line(self):
        flags = self.get_kpoints_mode()
        if flags[1]:
            self.num_line = int(self.datlines[1])
        else:
            self.num_line = 0

        return self.num_line

    # KPOINTS の各ゾーンの比率(全部足しあわせて1.0となる)
    def get_kpoints_vector_ratio(self,outcarname):
        vector = self.get_kpoints_vector(outcarname)
        num_vector = len(vector)
        total_vector = 0
        for i in range(num_vector):
            total_vector = vector[i] + total_vector

        self.zone_ratio = np.zeros(num_vector)
        for i in range(num_vector):
            self.zone_ratio[i] = vector[i]/total_vector

        return self.zone_ratio

################################################################################
if __name__ == '__main__':

    import optparse
    name = 'KPOINTS'
    outcarname = 'OUTCAR'

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT',)
    parser.add_option(  '-o','--outcar', dest='OUTCAR',)
    options,  args = parser.parse_args()

    if options.INPUT: name=options.INPUT
    if options.OUTCAR: outcarname=options.OUTCAR

#   if len(args) > 0:
#       name=args[0]

    kpoints = ReadVaspKpoints(name)

#   auto_FLAG = False  # FLAGS[0]
#   line_FLAG = False  # FLAGS[1]
#   hand_FLAG = False  # FLAGS[2]
#   car_FLAG  = False  # FLAGS[3]
#   rec_FLAG  = False  # FLAGS[4]

    print("K-Points")
    # K-points 情報の入手(現時点では auto-modeのみ動作)
    FLAGS = kpoints.get_kpoints_mode()
    if FLAGS[0]:
        kp = kpoints.get_kpoints()
        print("0")
        print("%s %s %s" % (str(kp[0]), str(kp[1]), str(kp[2])))

    ### SCF の KPOINTS 情報はここで終了

    print("")
    print("")

    # K-points 情報の入手(auto-mode では kx,ky,kz を返す)
    kpoints_array = kpoints.get_kpoints_array()
    for i in range(len(kpoints_array)):
        print(" %10.7f %10.7f %10.7f "
                % ( kpoints_array[i,0],kpoints_array[i,1],kpoints_array[i,2] ))
        if not i % 2 == 0:
            print("")

    # kpoints_array で求めた KPOINTS の line情報から
    # 各逆格子のゾーンにおける距離を求める method の実装
    v = kpoints.get_kpoints_vector(outcarname)
    for i in range(int(len(kpoints_array)/2)):
        print(" line %d : %10.7f " % ( i, v[i] ))

    print("")
    print("number of lines: %s" % str(kpoints.get_num_kpoints_line()))


    # KPOINTS 各ゾーンの比率(全部足し合わせて 1.0 となる)
    zone_ratio = kpoints.get_kpoints_vector_ratio(outcarname)
    for i in range(len(v)):
        print("%s" % str(zone_ratio[i]))


    num_line = kpoints.get_div_kpoints_line()
    print("")
    print("num_line:%s" % str(num_line))

################################################################################

