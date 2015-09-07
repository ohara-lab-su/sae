#!/usr/bin/env python
# -*- coding: utf-8 -*
###############################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
# *_sd*.txt ファイル( pw.x 入力ファイル 読み込み)
#
###############################################################################
#
# 2015.09.07
#  pdos を軌道成分名 or l,m の指定でゲットできるようにした
#
# 2015.08.18
#  lmax の抽出を _bav.txt ファイルではなくて 実際に計算している _sd*.txt
#  のヘッダから行うように変更。それに伴って _bav.txt の利用を前面停止
#  ただし、内部的には bavname はそのまま用いる(averageなどで使う)
#  --> 明示的に指定しない限り bavname は自動で sdname となる
#
# 2015.07.02
#  spin,ylm,intt,等の全出力の対応を含めた一般化
#
# 2015.07.01
#  spin対応版 startup
#
# 2015.07.01
#  平均化ルーチンで重み(平均する際に割る数)を引数に追加
#  --> 平均化ルーチンはコンストラクタで処理
#
# 2015.07.01
#   absorber 複数のファイル結合モードを追加
#
# 2015.05.21
#   startup (スピン未対応)
#
###############################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
#
__status__ = "alpha"
__version__ = "0.0.1"
###############################################################################

import sys
#import gzip
#import os
import re
import optparse
import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

###############################################################################


class ReadFdmSd(object):

    def __init__(self,
                 sdname,
                 suffix='_sd0.txt',
                 inpname='read_pdb.inp',
                 bavname=None,
                 absorber=None,              ### absorber=[] :matrix
                 weight=None):

        if bavname is None:
            bavname = sdname

        ############################## self.datlines ##########################
        # 複数の sd ファイルを読んで平均化する
        # sum
        if absorber is None:
            print "---- ReadFdmSd ----"
            print "sdname + suffix = ", sdname + suffix
#           print "bavname_bav.txt = ",bavname+'_bav.txt'
            print "inpname         = ", inpname
            print "-------------------"
            self.datlines, self.num = SAE.read_dataline(sdname + suffix)
        else:
            print "--- ReadFdmSd ------"
            print "    average mode ---"
            sdname0 = bavname + '_' + str(absorber[0]) + suffix
            row, num = SAE.read_row(sdname0, column=1)
            if weight is None:
                n_site = float(len(absorber))
            else:
                print "    weight = " + str(weight)
                n_site = float(weight)

            # アホな合計->平均->元の要素が結合したリスト形式への変換
            dsum = np.zeros((num, row))
            dtmp = np.zeros((num, row))
            numdata = np.zeros((num, row))
            for i in range(len(absorber)):
                sdname = bavname + '_' + str(absorber[i]) + suffix
                print "sum : ", sdname
                datatmp, num0 = SAE.read_dataline(sdname)
                for i in range(1, num):     # 一行目は除く
                    for r in range(1, row):  # Energy は除く
                        dtmp[i, r] = datatmp[i].split()[r]
                dsum = dtmp + dsum
            numdata = dsum / n_site  # 平均値を出す

            # 元々の self.datlines 形式に合わせて配列を作りなおす(互換性維持)
            listdata = list(numdata)
            self.datlines = []
            self.datlines.append('')  # dummy '1st-line'
            for i in range(1, num):
                self.datlines.append(''.join(str(listdata[i])).
                                     replace('\n', '').replace('[', '').replace(']', ''))
            self.num = num
        ############################## self.datlines ##########################

        # オービタルの情報(bav) とスピンの情報(inp) を入手
#       bav = SAE.ReadFdmBav(bavname)
        inp = SAE.ReadFdmInp(inpname)

        # get lmax
        # _sd*.txt で実際に出力されている lmax の最大値をゲットする
        nl = len(self.datlines[0].split())
        tmp = self.datlines[0].split()[nl - 1]
        tmp = re.sub('.*\(', '', tmp)
        self.lmax = int(re.sub('\).*', '', tmp))

#      # _bav.txt ファイルから吸収原子の lmax を抽出する
#       self.lmax = int(bav.get_lmax())

        self.ispin = int(inp.get_ispin())
        self.mmax = int(2 * self.lmax + 1)

        # トータルのオービタル数を計算
        tmmax = 0
        for l in range(self.lmax + 1):
            tmmax += (2 * l + 1) * self.ispin
        total_orbit = tmmax

        # _sd0.txt で出力される列数
        total_row = 1 + self.ispin + total_orbit * 2 + (l + 1) * 2 * self.ispin

        # _sd0.txt の一行目のチェック
        if absorber is None:
            if len(self.datlines[0].split()) != total_row:
                print "lmax", self.lmax
                print "ispin", self.ispin
                print "mmax", self.mmax
                print "total_row", total_row
                print "-----------"
                print len(self.datlines[0].split()), "= ", self.datlines[0]
                sys.exit("STOP: unknown type " + sdname + suffix)

        # すべての row 成分の情報を配列に叩きこむ
        self.ylm = \
                np.zeros((self.num - 1, self.lmax + 1, self.mmax, self.ispin))
        self.intylm = \
                np.zeros((self.num - 1, self.lmax + 1, self.mmax, self.ispin))
        self.dos = np.zeros((self.num - 1, self.lmax + 1, self.ispin))
        self.tdos = np.zeros((self.num - 1, self.lmax + 1, self.ispin))
        self.intt = np.zeros((self.num - 1, self.ispin))
        self.eng = np.zeros(self.num - 1)

        for i in range(1, self.num):
            row = 0
            self.eng[i - 1] = float(self.datlines[i].split()[row])
            row += 1

            for s in range(self.ispin):
                self.intt[i - 1, s] = float(self.datlines[i].split()[row])
                row += 1

            for ll in range(self.lmax + 1):
                m0 = 0
                for m in range(-ll, ll + 1):  # m,spin成分分解
                    for s in range(self.ispin):
                        # 成分 and 積分
                        self.ylm[i - 1, ll, m0, s] = \
                            float(self.datlines[i].split()[row])
                        row += 1
                        self.intylm[i - 1, ll, m0, s] = \
                            float(self.datlines[i].split()[row])
                        row += 1
                    m0 += 1
                for s in range(self.ispin):  # l軌道のsum
                    self.dos[i - 1, ll, s] = \
                            float(self.datlines[i].split()[row])
                    row += 1
                    self.tdos[i - 1, ll, s] = \
                            float(self.datlines[i].split()[row])
                    row += 1


    ####################################################
    # lm の順番は -1,0,1, -2,-1,0,2,,,,,
    #
    #  Ylm : 「real」 spherical harmonics
    # l=1
    #  m=-1: p_y
    #  m= 0: p_z
    #  m= 1: p_x
    #
    # l=2
    #  m=-2: d_xy
    #  m=-1: d_yz
    #  m= 0: d_z2
    #  m= 1: d_xz
    #  m= 2: d_x2-y2
    #
    def get_pdos(self, l=0, m=0, lm=None, spin=0):

#       pdos = np.zeros((self.nedos, self.lmax, self.mmax, self.nspin))

        if lm != None and isinstance(lm, str):

            orbit_name = lm
            lml = lm.lower()
            if lml == 's':
                orbit_name = 's'
                l=0
                m=0
            if lml == 'py' or lml == 'p_y':
                orbit_name = 'p_y'
                l=1
                m=-1
            if lml == 'pz' or lml == 'p_z':
                orbit_name = 'p_z'
                l=1
                m=0
            if lml == 'px' or lml == 'p_x':
                orbit_name = 'p_x'
                l=1
                m=1
            if lml == 'dxy' or \
                    lml == 'd_xy' or \
                    lml == 'xy' or \
                    lml == 'yx' or \
                    lml == 'dyx' or \
                    lml == 'd_yx':
                orbit_name = 'd_xy'
                l=2
                m=-2
            if lml == 'dyz' or \
                    lml == 'd_yz' or \
                    lml == 'yz' or \
                    lml == 'zy' or \
                    lml == 'dzy' or \
                    lml == 'd_zy':
                orbit_name = 'd_yz'
                l=2
                m=-1
            if lml == 'dz2' or \
                    lml == 'd_z^2' or \
                    lml == 'd_z2' or \
                    lml == 'dz^2' or \
                    lml == 'z2' or \
                    lml == 'z^2' or \
                    lml == 'd_3z2' or \
                    lml == 'd3z^2' or \
                    lml == '3z2' or \
                    lml == '3z^2' or \
                    lml == 'r2' or \
                    lml == 'r^2' or \
                    lml == 'dr^2' or \
                    lml == 'd_r^2' or \
                    lml == 'd_r2' or \
                    lml == '3z2-r2' or \
                    lml == '3z^2-r^2' or \
                    lml == 'd_3z2-r2' or \
                    lml == 'd_3z^2-r^2':
                orbit_name = 'd_z^2'
                l=2
                m=0
            if lml == 'dxz' or \
                    lml == 'd_xz' or \
                    lml == 'xz' or \
                    lml == 'dzx' or \
                    lml == 'zx' or \
                    lml == 'd_zx':
                orbit_name = 'd_xz'
                l=2
                m=1
            if lml == 'x^2-y^2' or \
                    lml == 'd_x^2-y^2' or \
                    lml == 'd_x2-y2' or \
                    lml == 'x2-y2' or \
                    lml == 'dx2' or \
                    lml == 'x2' or \
                    lml == 'x^2' or \
                    lml == 'dx^2' or \
                    lml == 'dy2' or \
                    lml == 'y2' or \
                    lml == 'y^2' or \
                    lml == 'dy^2':
                orbit_name = 'd_x^2-y^2'
                l=2
                m=2

        return self.ylm[:,l,m,spin]

    ####################################################
    # LDOS(NEDOS,L,SPIN)
    def get_ldos(self, l=0, spin=0):

        if isinstance(l, str):
            if l == 's' and self.lmax >= 0:
                l = 0
            if l == 'p' and self.lmax >= 1:
                l = 1
            if l == 'd' and self.lmax >= 2:
                l = 2
            if l == 'f' and self.lmax >= 3:
                l = 3

        if isinstance(spin, str):
            if spin == 'nonmag':
                spin = 0
            if spin == 'non':
                spin = 0
            if spin == 'up':
                spin = 0
            if spin == 'dn':
                spin = 1
            if spin == 'down':
                spin = 1

        self.ldos = self.dos[:, l, spin]
        return self.ldos

    def get_eng(self):
        return self.eng


###############################################################################
def options():

    name = 'Cu'
#   name = 'Fe'
    suffix = '_sd0.txt'

    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest='INPUT',)
    options, args = parser.parse_args()

    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]

    return name, suffix

###############################################################################
if __name__ == '__main__':

    name, suffix = options()
    conv = ReadFdmSd(name, suffix)

#   eng = conv.get_eng()
#   xas = conv.get_xas()


#   print "NAME",name
