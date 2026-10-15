#!/usr/bin/env python
# -*- coding: utf-8 -*
###############################################################################
# K.NAKADA, kengo.nakada@gmail.com
#  〜 2016.01.08 までのバージョンのsdファイルの解析
#  +
#  〜 新しいバージョンの sdファイル形式に対応
#
# FDMNES
#   *_sd*.txt ファイル( pw.x 入力ファイル 読み込み)
#   Ver_0.0.2 以降 FDMNS のバージョンの違いによるログの違いを吸収
#
# Energy
# Int_t
# n(0, 0)
# Intn(0, 0)
# n_l(0)
# Intn_l(0)
# n(1, -1)
# Intn(1, -1)
# n(1, 0)
# Intn(1, 0)
# n(1, 1)
# Intn(1, 1)
# n_l(1)
# Intn_l(1)
# n(2, -2)
# Intn(2, -2)
# n(2, -1)
# Intn(2, -1)
# n(2, 0)
# Intn(2, 0)
# n(2, 1)
# Intn(2, 1)
# n(2, 2)
# Intn(2, 2)
# n_l(2)
# Intn_l(2)
#
###############################################################################
#
# 2020.07.17 (Ver_0.0.2)
#  2016.08.01 以降に sd? のナンバリングルールが変わったのでそれに対する対応
#  - バージョンチェック(ReadFdmBav.py) を用いる
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
# トップディレクトリ関係のエラーは ImportError ではキャッチ出来ない
###############################################################################
# import gzip
# sys.path.append('../..')
# import SpaceGroupEnvironment as SGE
###############################################################################
#   name = 'Fe'
###############################################################################
#tmp = sd.get_pdos(l=0,lm='s', spin=0)
#print(tmp)
#   eng = conv.get_eng()
#   xas = conv.get_xas()
#   print "NAME",name
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import optparse
import numpy as np


# END OF __init__()
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
####################################################
#       return self.ylm[:,l,m,spin]
#
# get/set attribute (2)
#
#
# property
#
# 読み込んだ sd ファイル丸ごと(平均化したら、平均化した値)
# 読み込んだ sd ファイルに基づいて lmax を抽出
class ReadFdmSd2016(object):

    # input に書かれている情報を取得する
    ############################## self.datlines ##########################
    # 複数の sd ファイルを読んで平均化する
    # sum
    ############################## self.datlines ##########################
    # 合計した sd ファイルを丸ごと保存
    # オービタルの情報(bav) とスピンの情報(inp) を入手
    #       bav = SAE.ReadFdmBav(bavname)
    #################
    #
    # get lmax
    # _sd*.txt で実際に出力されている lmax の最大値をゲットする
    # ヘッダの一番最後のrawをゲットして加工する
    #
    # print('lmax (bav) = %s' % int(bav.get_lmax()))
    #  _bav.txt ファイルから吸収原子の lmax を抽出する
    # self.lmax = int(bav.get_lmax())
    # トータルのオービタル数を計算
    # _sd0.txt で出力される列数
    # _sd0.txt の一行目のチェック
    # すべての row 成分の情報を配列に叩きこむ
    def __init__(
        self,
        sdname,
        suffix="_sd0.txt",
        inpname=None,
        bavname=None,
        absorber=None,
        weight=None,
    ):
        """
        :param sdname:  材料名(ex: Cu)
        :param suffix:  default '_sd0.txt'
        :param inpname:
        :param bavname:
        :param absorber: absorber=[] :matrix (複数の吸収端の同時読み込みに対応する)
        :param weight:
        """
        from sae.fdmnes.fdmfile import ReadFdmFdmfile
        from sae.fdmnes.inp import ReadFdmInp
        from sae.common.text import TextFiles

        print("===== sd2016 =====")
        if bavname is None:
            bavname = sdname
        if inpname is None:
            if os.path.exists("fdmfile.txt"):
                fdmfiletxt = ReadFdmFdmfile()
                inpname = fdmfiletxt.get_filout()
            else:
                inpname = "read_pdb.inp"
        print("sd name  = %s" % sdname)
        print("inp name = %s" % inpname)
        inpfile = inpname
        inpdir = os.path.dirname(sdname)
        if inpdir:
            inpname = inpdir + "/" + inpfile
        else:
            inpname = inpfile
        #
        # absoer が None --> 読み込んだファイルが一つだけの時
        #
        # weight で各要素を割る(datlinesに詰め直す)
        #
        # absoer not None --> 読み込んだファイルが複数の時
        #
        # アホな合計->平均->元の要素が結合したリスト形式への変換
        # 元々の self.datlines 形式に合わせて配列を作りなおす(互換性維持)
        # 最後に header を追加
        if absorber is None:
            print("")
            print("---- ReadFdmSd ----")
            print("sdname + suffix = %s" % sdname + suffix)
            print("bavname_bav.txt = %s" % bavname + "_bav.txt")
            print("inpname         = %s" % inpname)
            print("-------------------")
            self.datlines, self.__num = TextFiles().read_dataline(sdname + suffix)
            self.__header = self.datlines[0]
            # 全要素の数値データーを配列に入れる
            # Energy 行追加
            # 元々の self.datlines 形式に合わせて配列を作りなおす(互換性維持)
            # 最後に header を追加
            if weight is not None:
                print("--- ReadFdmSd ------")
                print("--- weight mode ----")
                print(" weight = %s" % str(weight))
                sdname0 = sdname + suffix
                row, num = TextFiles().read_row(sdname0, column=1)
                print(" num = %s" % num)
                print(" row = %s" % row)
                numdata = np.zeros((num, row))
                # 一行目は除く(ヘッダなので)
                for j in range(1, num):
                    # Energy は除く
                    for r in range(1, row):
                        numdata[j, r] = float(self.datlines[j].split()[r]) / float(
                            weight
                        )
                for i in range(1, num):
                    numdata[i, 0] = float(self.datlines[i].split()[0])
                listdata = list(numdata)
                self.datlines = []
                # dummy '1st-line'
                self.datlines.append("")
                for i in range(1, num):
                    self.datlines.append(
                        "".join(str(listdata[i]))
                        .replace("\n", "")
                        .replace("[", "")
                        .replace("]", "")
                    )
                self.datlines[0] = self.__header
        else:
            print("--- ReadFdmSd ------")
            print("--- average mode ---")
            sdname0 = bavname + "_" + str(absorber[0]) + suffix
            row, num = TextFiles().read_row(sdname0, column=1)
            if weight is None:
                n_site = float(len(absorber))
            else:
                print("    weight = %s" % str(weight))
                n_site = float(weight)
            dsum = np.zeros((num, row))
            dtmp = np.zeros((num, row))
            numdata = np.zeros((num, row))
            # 間違い？を発見、明らかに間違いっぽいが念のため取っておく(15.09.08)
            # for i in range(1, num):     # 一行目は除く
            #    for r in range(1, row):  # Energy は除く
            #        dtmp[i, r] = datatmp[i].split()[r]
            # dsum = dtmp + dsum
            for i in range(len(absorber)):
                sdname = bavname + "_" + str(absorber[i]) + suffix
                print("sum : %s" % str(sdname))
                datatmp, num0 = TextFiles().read_dataline(sdname)
                if i == 0:
                    self.__header = datatmp[0]
                # 一行目は除く
                for j in range(1, num):
                    # Energy は除く
                    for r in range(1, row):
                        dtmp[j, r] = datatmp[j].split()[r]
                dsum = dtmp + dsum
            # 平均値を出す
            numdata = dsum / n_site
            for i in range(1, num):
                # Energy行
                numdata[i, 0] = datatmp[i].split()[0]
            listdata = list(numdata)
            self.datlines = []
            # dummy '1st-line'
            self.datlines.append("")
            for i in range(1, num):
                self.datlines.append(
                    "".join(str(listdata[i]))
                    .replace("\n", "")
                    .replace("[", "")
                    .replace("]", "")
                )
            self.datlines[0] = self.__header
            self.__num = num
        print("START GET LDOS/DOS")
        self.sd = self.datlines
        inp = ReadFdmInp(inpname)
        nl = len(self.__header.split())
        tmp = self.__header.split()[nl - 1]
        tmp = re.sub(".*\\(", "", tmp)
        try:
            # nonmag 版
            self.__lmax = int(re.sub("\\).*", "", tmp))
        except:
            # spin 版
            self.__lmax = int(re.sub(",.*\\).*", "", tmp))
        print("lmax       = %s" % self.__lmax)
        self.__ispin = int(inp.get_ispin())
        self.__mmax = int(2 * self.__lmax + 1)
        tmmax = 0
        for l in range(self.__lmax + 1):
            tmmax += (2 * l + 1) * self.__ispin
        total_orbit = tmmax
        total_row = 1 + self.__ispin + total_orbit * 2 + (l + 1) * 2 * self.__ispin
        if absorber is None:
            # print len(self.datlines[0].split()), "= ", self.datlines[0]
            if len(self.datlines[0].split()) != total_row:
                print("lmax %s" % str(self.__lmax))
                print("ispin %s" % str(self.__ispin))
                print("mmax %s" % str(self.__mmax))
                print("total_row %s" % str(total_row))
                print("-----------")
                print(
                    "%s = %s"
                    % (str(len(self.datlines[0].split())), str(self.datlines[0]))
                )
                sys.exit("STOP: unknown type " + sdname + suffix)
        self.ylm = np.zeros(
            (self.__num - 1, self.__lmax + 1, self.__mmax, self.__ispin)
        )
        self.intylm = np.zeros(
            (self.__num - 1, self.__lmax + 1, self.__mmax, self.__ispin)
        )
        self.ldos_all = np.zeros((self.__num - 1, self.__lmax + 1, self.__ispin))
        self.tdos_all = np.zeros((self.__num - 1, self.__ispin))
        self.intldos_all = np.zeros((self.__num - 1, self.__lmax + 1, self.__ispin))
        self.inttdos_all = np.zeros((self.__num - 1, self.__ispin))
        self.eng = np.zeros(self.__num - 1)
        # INTTDOS  Int_t(u), Int_t(d)
        # PDOS & INTPDOS
        for i in range(1, self.__num):
            row = 0
            self.eng[i - 1] = float(self.datlines[i].split()[row])
            row += 1
            for s in range(self.__ispin):
                self.inttdos_all[i - 1, s] = float(self.datlines[i].split()[row])
                row += 1
            for ll in range(self.__lmax + 1):
                m0 = 0
                # m,spin成分分解 n(0,0),,,
                for m in range(-ll, ll + 1):
                    for s in range(self.__ispin):
                        self.ylm[i - 1, ll, m0, s] = float(
                            self.datlines[i].split()[row]
                        )
                        row += 1
                        self.intylm[i - 1, ll, m0, s] = float(
                            self.datlines[i].split()[row]
                        )
                        row += 1
                    m0 += 1
                # l軌道のsum n_l(0,0),,,
                for s in range(self.__ispin):
                    self.ldos_all[i - 1, ll, s] = float(self.datlines[i].split()[row])
                    self.tdos_all[i - 1, s] = (
                        float(self.datlines[i].split()[row]) + self.tdos_all[i - 1, s]
                    )
                    row += 1
                    self.intldos_all[i - 1, ll, s] = float(
                        self.datlines[i].split()[row]
                    )
                    self.inttdos_all[i - 1, s] = (
                        float(self.datlines[i].split()[row])
                        + self.inttdos_all[i - 1, s]
                    )
                    row += 1
        self.__emax = max(self.eng)
        self.__emin = min(self.eng)
        self.__ymax = 0.0

    def get_pdos(self, l=0, m=0, lm=None, spin=0):
        """
        pdos = np.zeros((self.nedos, self.lmax, self.mmax, self.nspin))

        :param l:
        :param m:
        :param lm:
        :param spin:
        :return:
        """
        if lm != None and isinstance(lm, str):
            orbit_name = lm
            lml = lm.lower()
            if lml == "s":
                orbit_name = "s"
                l = 0
                m = 0
            if lml == "py" or lml == "p_y":
                orbit_name = "p_y"
                l = 1
                m = -1
            if lml == "pz" or lml == "p_z":
                orbit_name = "p_z"
                l = 1
                m = 0
            if lml == "px" or lml == "p_x":
                orbit_name = "p_x"
                l = 1
                m = 1
            if (
                lml == "dxy"
                or lml == "d_xy"
                or lml == "xy"
                or (lml == "yx")
                or (lml == "dyx")
                or (lml == "d_yx")
            ):
                orbit_name = "d_xy"
                l = 2
                m = -2
            if (
                lml == "dyz"
                or lml == "d_yz"
                or lml == "yz"
                or (lml == "zy")
                or (lml == "dzy")
                or (lml == "d_zy")
            ):
                orbit_name = "d_yz"
                l = 2
                m = -1
            if (
                lml == "dz2"
                or lml == "d_z^2"
                or lml == "d_z2"
                or (lml == "dz^2")
                or (lml == "z2")
                or (lml == "z^2")
                or (lml == "d_3z2")
                or (lml == "d3z^2")
                or (lml == "3z2")
                or (lml == "3z^2")
                or (lml == "r2")
                or (lml == "r^2")
                or (lml == "dr^2")
                or (lml == "d_r^2")
                or (lml == "d_r2")
                or (lml == "3z2-r2")
                or (lml == "3z^2-r^2")
                or (lml == "d_3z2-r2")
                or (lml == "d_3z^2-r^2")
            ):
                orbit_name = "d_z^2"
                l = 2
                m = 0
            if (
                lml == "dxz"
                or lml == "d_xz"
                or lml == "xz"
                or (lml == "dzx")
                or (lml == "zx")
                or (lml == "d_zx")
            ):
                orbit_name = "d_xz"
                l = 2
                m = 1
            if (
                lml == "x^2-y^2"
                or lml == "d_x^2-y^2"
                or lml == "d_x2-y2"
                or (lml == "x2-y2")
                or (lml == "dx2")
                or (lml == "x2")
                or (lml == "x^2")
                or (lml == "dx^2")
                or (lml == "dy2")
                or (lml == "y2")
                or (lml == "y^2")
                or (lml == "dy^2")
            ):
                orbit_name = "d_x^2-y^2"
                l = 2
                m = 2
        self.pdos = self.ylm[:, l, m, spin]
        self.ymax = max(self.pdos)
        return self.pdos

    def get_ldos(self, l=0, spin=0):
        """LDOS(NEDOS,L,SPIN)"""
        if isinstance(l, str):
            if l == "s" and self.__lmax >= 0:
                l = 0
            if l == "p" and self.__lmax >= 1:
                l = 1
            if l == "d" and self.__lmax >= 2:
                l = 2
            if l == "f" and self.__lmax >= 3:
                l = 3
        if isinstance(spin, str):
            if spin == "nonmag":
                spin = 0
            if spin == "non":
                spin = 0
            if spin == "up":
                spin = 0
            if spin == "dn":
                spin = 1
            if spin == "down":
                spin = 1
        self.ldos = self.ldos_all[:, l, spin]
        return self.ldos

    def get_intldos(self, l=0, spin=0):
        """INTLDOS(NEDOS,L,SPIN)"""
        if isinstance(l, str):
            if l == "s" and self.__lmax >= 0:
                l = 0
            if l == "p" and self.__lmax >= 1:
                l = 1
            if l == "d" and self.__lmax >= 2:
                l = 2
            if l == "f" and self.__lmax >= 3:
                l = 3
        if isinstance(spin, str):
            if spin == "nonmag":
                spin = 0
            if spin == "non":
                spin = 0
            if spin == "up":
                spin = 0
            if spin == "dn":
                spin = 1
            if spin == "down":
                spin = 1
        self.intldos = self.intldos_all[:, l, spin]
        return self.intldos

    def get_tdos(self, spin=0):
        """TODS(NEDOS,SPIN)"""
        return self.tdos_all[:, spin]

    def get_inttdos(self, spin=0):
        """INTDOS(NEDOS,SPIN)"""
        return self.inttdos_all[:, spin]

    def get_eng(self):
        return self.eng

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
        """読み込んだ sd ファイルの行数"""
        return self.__num

    @property
    def num(self):
        return self.__num

    def get_sd(self):
        return self.sd

    def get_lmax(self):
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
