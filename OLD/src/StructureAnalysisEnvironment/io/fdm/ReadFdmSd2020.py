#!/usr/bin/env python
# -*- coding: utf-8 -*
###############################################################################
# K.NAKADA, kengo.nakada@gmail.com
# FDMNES 2020.06.16-2 を解析できるように修正したバージョン
# それ以前特に 2016.01.08 などとは大きく異なるので注意
# データ読み込み整理に Pandas を使って大幅に簡略化
#
# FDMNES
#   *_sd*.txt ファイル( pw.x 入力ファイル 読み込み)
#   Ver_0.0.2 以降 FDMNS のバージョンの違いによるログの違いを吸収
#
# 2016,2019 までと異なっていて、積算部分状態密度の情報がごっそり消されている。
#
# Energy
# (0, 0)  s
#        Int(s)
# (1, 1) px
# (1,-1) py
# (1, 0) pz
#        p
#        Int(p)
# (2, 2) dx2 - y2
# (2, 0) dz2
# (2,-1) dyz
# (2, 1) dxz
# (2,-2) dxy
#        d
#        Int(d)
# total
# Int(total)
#
###############################################################################
#
# 2020.07.17-19 (Ver_0.0.2)
#  2016.08.01 以降に sd? のナンバリングルールが変わったのでそれに対する対応
#  - バージョンチェック(ReadFdmBav.py) を用いる
#  - sd0 ファイルそれ自体のフォーマットが2020では大きく変わっている
#  - pandas 利用に全面書き換え
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.09.11
#   lmax 判定の新バージョン(2015.08.18)が
#   spin に対して動作が不完全だったので修正
#
# 2015.09.09
#   TDOS および INTTDOS が未完成だったので修正した
#
# 2015.09.08
#   DOS の最大レンジ自動取得
#
# 2015.09.08
#   非平均化もーどで DOS の Weight の計算が出来るようにした
#
# 2015.09.08
#  sd 平均化情報の出力（ファイル出力）を修正
#  それにあせて sd ファイルのヘッダー出力なども追加
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
from __future__ import print_function

# トップディレクトリ関係のエラーは ImportError ではキャッチ出来ない
try:
    from ...copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.2"

###############################################################################

import sys
# import gzip
import os
import re
import optparse
import numpy as np
import pandas as pd

try:
    # sys.path.append('../..')
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    import StructureAnalysisEnvironment as SAE
except ImportError:
    import StructureAnalysisEnvironment as SAE


# import SpaceGroupEnvironment as SGE

###############################################################################


class ReadFdmSd2020(object):

    def __init__(self, sdname, suffix='_sd0.txt', inpname=None, bavname=None, absorber=None, weight=None):
        """
        :param sdname:  材料名(ex: Cu)
        :param suffix:  default '_sd0.txt'
        :param inpname: FDMNES input ファイルからいくつかの情報を読み込む
        :param bavname:
        :param absorber: absorber=[] :matrix
        :param weight:
        """
        print('===== sd2020 =====')

        if bavname is None:
            bavname = sdname

        # input に書かれている情報を取得する
        if inpname is None:
            if os.path.exists('fdmfile.txt'):
                fdmfiletxt = SAE.io.fdm.ReadFdmFdmfile()
                inpname = fdmfiletxt.get_filout()
            else:
                inpname = 'read_pdb.inp'

        print("sd name  = %s" % sdname)
        print("inp name = %s" % inpname)

        inpfile = inpname
        inpdir = os.path.dirname(sdname)
        if inpdir:
            inpname = inpdir + '/' + inpfile
        else:
            inpname = inpfile

        print('')
        print('******************************')

        # オービタルの情報(bav) とスピンの情報(inp) を入手
        # bav = SAE.ReadFdmBav(bavname)
        inp = SAE.io.fdm.ReadFdmInp(inpname)

        # 複数の sd ファイルを読んで平均化する
        #   --> weight があるときは各要素を割る
        if absorber is None:
            #
            # Absorbet が None のときは、読み込んだファイルが一つだけの時
            #
            print('')
            print("---- ReadFdmSd ----")
            print("sdname + suffix = %s" % sdname + suffix)
            print("bavname_bav.txt = %s" % bavname+'_bav.txt')
            print("inpname         = %s" % inpname)
            print("-------------------")

            # sd ファイルを読み込んで dataFrame にする
            print("--- ReadFdmSd ------")
            df = self.__read_sd_file(sdname + suffix)

            if weight is not None:
                print(" weight = %s" % str(weight))
                df = df/float(weight)

        # Absorber 指定があるときは指定の sd ファイルを読み込む
        # absoer not None --> 読み込んだファイルが複数の時
        else:
            print("--- ReadFdmSd ------")
            print("--- average mode ---")

            if weight is None:
                n_site = float(len(absorber))
            else:
                print("    weight = %s" % str(weight))
                n_site = float(weight)

            # read sd0
            sdname = bavname + "_" + str(absorber[0]) + suffix
            print("sum : %s" % str(sdname))
            df = self.__read_sd_file(sdname)
            dfsum = df.copy

            # read from sd1 to absorber
            for i in range(1, len(absorber)):

                sdname = bavname + "_" + str(absorber[i]) + suffix
                print("sum : %s" % str(sdname))
                df = self.__read_sd_file(sdname)
                dfsum += df

            # 平均値を出す
            df = dfsum / n_site

        # 2016版と比べるとこちらの num はヘッダ無しの value値になるので
        # num の数は2016版と比べると常に -1 がかかったものになる
        self.__num = len(df.values)

        print('START GET LDOS/DOS')
        ################################################
        #
        # lmax
        #
        # 他:     Energy + total + int(total) = 3
        # s軌道:   s, int(S)  = 2
        # p軌道:   px, py, pz, p, int(p) = 5
        # d軌道:   x2-y2, z2, yz, xz, xy, d, int(d) = 7
        #
        # もし、num = 5 ならば lmax = 0
        #      num = 10 ならば lmax = 1
        #      num = 17 ならば lmax = 2
        ################################################

        _num_split = len(df.columns.values)
        if _num_split == 5:
            self.__lmax = 0
        elif _num_split == 10:
            self.__lmax = 1
        elif _num_split == 17:
            self.__lmax = 2
        else:
            print('*********** ERROR ***********, unknown header type')
            sys.exit(-1)

        print('lmax (sd) = %s' % self.__lmax)

        self.__ispin = int(inp.get_ispin())
        self.__mmax = int(2 * self.__lmax + 1)

        # トータルのオービタル数を計算
        tmmax = 0
        for l in range(self.__lmax + 1):
            tmmax += (2 * l + 1) * self.__ispin
        total_orbit = tmmax

        # _sd0.txt で出力される列数
        total_row = _num_split

        print("lmax %s" % str(self.__lmax))
        print("ispin %s" % str(self.__ispin))
        print("mmax %s" % str(self.__mmax))
        print("total_row %s" % str(total_row))
        print("-----------")
        print("")

        print("index num = %d" % self.__num)

        # 定義
        self.__eng = np.zeros(self.__num)  # 意味が無い定義(標識をあわせるためだけ)
        self.ylm = np.zeros((self.__num, self.__lmax + 1, self.__mmax, self.__ispin))
        self.ldos_all = np.zeros((self.__num, self.__lmax + 1, self.__ispin))
        self.tdos_all = np.zeros((self.__num, self.__ispin))
        self.intldos_all = np.zeros((self.__num, self.__lmax + 1, self.__ispin))
        self.inttdos_all = np.zeros((self.__num, self.__ispin))

        # 2020 版では存在しない
        self.intylm = np.zeros((self.__num, self.__lmax + 1, self.__mmax, self.__ispin))

        ####################################################
        # PDOS
        #    DataFrame を ylm 構造に直す
        #
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

        # s (l=0, m=0, spin=0)
        self.ylm[:, 0, 0, 0] = df['s'].values
        self.ldos_all[:, 0, 0] = df['s'].values  # s
        self.intldos_all[:, 0, 0] = df['Int(s)'].values

        if self.__lmax >=1:
            self.ylm[:, 1, -1, 0] = df['py'].values  # py (l=1, m=-1, spin=0)
            self.ylm[:, 1,  0, 0] = df['pz'].values  # pz (l=1, m=0, spin=0)
            self.ylm[:, 1,  1, 0] = df['px'].values  # px (l=1, m=1, spin=0)
            self.ldos_all[:, 1, 0] = df['p'].values  # p
            self.intldos_all[:, 1, 0] = df['Int(p)'].values

        if self.__lmax >=2:
            self.ylm[:, 2, -2, 0] = df['dxy'].values  # dxy (l=2, m=-2, spin=0)
            self.ylm[:, 2, -1, 0] = df['dyz'].values  # dyz (l=2, m=-1, spin=0)
            self.ylm[:, 2,  0, 0] = df['dz2'].values  # dz2 (l=2, m=0, spin=0)
            self.ylm[:, 2,  1, 0] = df['dxz'].values  # dxz (l=2, m=1, spin=0)
            self.ylm[:, 2,  2, 0] = df['dx2-y2'].values  # dx2-y2 (l=2, m=2, spin=0)
            self.ldos_all[:, 2, 0] = df['d'].values  # d
            self.intldos_all[:, 2, 0] = df['Int(d)'].values

        # 全席分状態密度(LDOS分解からの結果と思われる)
        self.inttdos_all[:, 0] = df['Int(total)'].values

        # エネルギー
        self.__eng = df['Energy'].values

        # DataFrame の保存 ( header を含む )
        self.sd = df

        self.__emax = max(self.__eng)
        self.__emin = min(self.__eng)
        self.__ymax = 0.0

        ############################## self.datlines ##########################
        # END OF __init__()_

    def __read_sd_file(self, name):
        """
        :param name:  sdname + suffix
        :return: dataFrame
        """

        # pandas を用いてデーター構造を取り込む
        # 一行目をヘッダ情報とする, スペース区切り,先頭のスペースを無視する
        df = pd.read_table(name, header=0, sep='\s+', skipinitialspace=True)

        # for TEST
        # print(df)
        self.__header = df.columns.values
        print(self.__header)
        print(df.index.values)
        # print(df.values)
        # print(df['Energy'])   # 列指定
        # print(df['s'])   # 列指定
        # print(df[['s', 'Energy']])   # 列指定
        # a = df[['s', 'Energy']].values
        # print(a)

        return df

    def get_pdos(self, l=0, m=0, lm=None, spin=0):
        """
        2016/2020 互換 I/F
        pdos = np.zeros((self.nedos, self.lmax, self.mmax, self.nspin))

        :param l:
        :param m:
        :param lm: px, py などのキャラクター入力(lとmを個別に入力しなくて良い)
        :param spin:
        :return:
        """
        if lm != None and isinstance(lm, str):

            orbit_name = lm
            lml = lm.lower()
            if lml == 's':
                orbit_name = 's'
                l = 0
                m = 0
            if lml == 'py' or lml == 'p_y':
                orbit_name = 'p_y'
                l = 1
                m = -1
            if lml == 'pz' or lml == 'p_z':
                orbit_name = 'p_z'
                l = 1
                m = 0
            if lml == 'px' or lml == 'p_x':
                orbit_name = 'p_x'
                l = 1
                m = 1
            if lml == 'dxy' or \
                    lml == 'd_xy' or \
                    lml == 'xy' or \
                    lml == 'yx' or \
                    lml == 'dyx' or \
                    lml == 'd_yx':
                orbit_name = 'd_xy'
                l = 2
                m = -2
            if lml == 'dyz' or \
                    lml == 'd_yz' or \
                    lml == 'yz' or \
                    lml == 'zy' or \
                    lml == 'dzy' or \
                    lml == 'd_zy':
                orbit_name = 'd_yz'
                l = 2
                m = -1
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
                l = 2
                m = 0
            if lml == 'dxz' or \
                    lml == 'd_xz' or \
                    lml == 'xz' or \
                    lml == 'dzx' or \
                    lml == 'zx' or \
                    lml == 'd_zx':
                orbit_name = 'd_xz'
                l = 2
                m = 1
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
                l = 2
                m = 2

        self.pdos = self.ylm[:, l, m, spin]
        self.__ymax = max(self.pdos)

        return self.pdos

    def get_ldos(self, l=0, spin=0):
        """
        2016/2020 互換 I/F
        LDOS(NEDOS,L,SPIN)

        :param l:
        :param spin:
        :return:
        """
        if isinstance(l, str):
            if l == 's' and self.__lmax >= 0:
                l = 0
            if l == 'p' and self.__lmax >= 1:
                l = 1
            if l == 'd' and self.__lmax >= 2:
                l = 2
            if l == 'f' and self.__lmax >= 3:
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

        self.ldos = self.ldos_all[:, l, spin]
        return self.ldos

    def get_intldos(self, l=0, spin=0):
        """
        2016/2020 互換 I/F
        INTLDOS(NEDOS,L,SPIN)

        :param l:
        :param spin:
        :return:
        """

        if isinstance(l, str):
            if l == 's' and self.__lmax >= 0:
                l = 0
            if l == 'p' and self.__lmax >= 1:
                l = 1
            if l == 'd' and self.__lmax >= 2:
                l = 2
            if l == 'f' and self.__lmax >= 3:
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

        self.intldos = self.intldos_all[:, l, spin]
        return self.intldos

    #
    # get/set attribute (2)
    #

    def get_tdos(self, spin=0):
        """ TODS(NEDOS,SPIN)"""
        return self.tdos_all[:, spin]

    def get_inttdos(self, spin=0):
        """ INTDOS(NEDOS,SPIN) """
        return self.inttdos_all[:, spin]

    def get_eng(self):
        return self.__eng

    @property
    def eng(self):
        return self.__eng

    #
    # property
    #

    def get_emin(self):
        return self.__emin

    @property
    def emin(self):
        return self.__emin

    def get_emax(self):
        return self.__emax

    @property
    def emax(self):
        return self.__emax

    def get_ymax(self):
        return self.__ymax

    @property
    def ymax(self):
        return self.__ymax

    def get_header(self):
        return self.__header

    @property
    def header(self):
        return self.__header

    def get_num(self):
        """ 読み込んだ sd ファイルの行数 """
        return self.__num

    @property
    def num(self):
        return self.__num

    def get_sd(self):
        """ 読み込んだ sd ファイル丸ごと(平均化したら、平均化した値) """
        return self.sd

    def get_lmax(self):
        """ 読み込んだ sd ファイルに基づいて lmax を抽出 """
        return self.__lmax

    @property
    def lmax(self):
        return self.__lmax

    def get_mmax(self):
        return self.__mmax

    @property
    def mmax(self):
        return self.__mmax

    def get_ispin(self):
        return self.__ispin

    @property
    def ispin(self):
        return self.__ispin


def options():
    name = 'Cu'
    #   name = 'Fe'
    suffix = '_sd0.txt'

    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest='INPUT', )
    options, args = parser.parse_args()

    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]

    return name, suffix


###############################################################################
if __name__ == '__main__':
    name, suffix = options()
    sd = SAE.io.ReadFdmSd2020(name, suffix)
    #tmp = sd.get_pdos(l=0,lm='s', spin=0)
    #print(tmp)

#   eng = conv.get_eng()
#   xas = conv.get_xas()


#   print "NAME",name
