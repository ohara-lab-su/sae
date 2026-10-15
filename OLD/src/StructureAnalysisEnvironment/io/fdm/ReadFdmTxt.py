#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
# *.txt ファイル
#
###############################################################################
#
# 2020.08.12: カプセル化推進
#
# 2019.01.08
#  新しい FDMNES における
#  Cu.txt などのログから E_Fermi が消えたことによる対応
#  （フェルミレベルが強制ゼロ、自動シフトに対する対応）
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.11.12
#  L2,3に対応
#
# 2015.09.11
#  .txt の生データーのスピン対応
#    XAS のデーター構造が変わるので注意
#
# 2015.09.08
#  .txt の平均化 Method を追加
#
# 2015.08.11
#  fdmnes_win64.exe を windows7 で動かした時と windows8 で動かしたときの
#  動作の違いを吸収するように重名に記述を変更しなおした。
#
# 2015.06.23 startup
#
###############################################################################
from __future__ import print_function

# トップディレクトリ関係のエラーは ImportError ではキャッチ出来ない
try:
    from ...copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

###############################################################################

import sys
# import gzip
import os
import re
import optparse
import numpy as np

try:
    # sys.path.append('../..')
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    import StructureAnalysisEnvironment as SAEnv
except ImportError:
    import StructureAnalysisEnvironment as SAEnv

# import SpaceGroupEnvironment as SGE

###############################################################################


class ReadFdmTxt(object):

    def __init__(self, cname, suffix='.txt', edge='K', weight=None):
        """
        注意) convolution した 横軸（エネルギー）は生データ(txt)と異なるので、
             生データXAS をプロットするときは、 生データ(eng) を横軸にすること
        :param cname:
        :param suffix:
        :param edge:
        :param weight:
        """

        name = cname.replace(suffix, '')
        suffix0 = cname.replace(name, '')
        if suffix0 != suffix:
            suffix = '.txt'
            cname = name + suffix

        self.suffix = suffix
        self.__datlines, self.num = SAEnv.read_dataline(cname)
        self.__header = self.__datlines[0]

        self.__eng = np.zeros(self.num - 2)

        if weight is None:
            weight = 1.0
        else:
            # print 'ReadFdmTxt(weight='+str(weight)+')'
            print("ReadFdmTxt(weight=%s)" % str(weight))

        # 一行目のイコールで結ばれたところまでの変数の数のカウント
        count = 0
        for i in self.__datlines[0].split():
            count += 1
            if i == '=':
                break

        ###########################
        # 一行目のイコールで結ばれた値=変数名を、動的に変数＝値としてセット
        #
        # for i in range(count,len(self.datlines[0].split())):
        # var = str(self.datlines[0].split()[i].strip()).replace(',','')
        # value = float(self.datlines[0].split()[i-count])
        #
        self.__param = {}
        for i in range(count, len(self.__datlines[0].replace(',', ' ').split())):
            key = str(self.__datlines[0].replace(',', ' ').split()[i].strip())
            value = float(self.__datlines[0].replace(',', ' ').split()[i - count])
            # self.__dict__[key] = value  # インスタンス変数に直接作る
            self.__param[key] = value

        # 2020/2016 互換で、E_Fermi がないとき(2020)は互換値として 0.0 を入れる
        try:
            self.__param['E_Fermi']
        except:
            self.__param['E_Fermi'] = 0.0

        # スピン計算の有無を類推 & XANES の複数エッジの処理
        #  L23 mode の spin ありには未対応(2015.11.12)
        #
        # print 'Edge mode = ', edge
        if isinstance(edge, str):
            if edge == 'K':
                edge = 0
            if edge == 'L2':
                edge = 0
            if edge == 'L3':
                edge = 1

        # エッジの把握
        if len(self.__datlines[1].split()) == 3:
            if bool(re.match('.*\<xanes\>_L', self.__datlines[1].split()[1])):
                self.__nspin = 1
            else:
                self.__nspin = 2

        # 複数エッジ with spin
        elif len(self.__datlines[1].split()) >= 4:
            self.__nspin = 2
        else:
            self.__nspin = 1

        # XANES スペクトル(生データを読み込み)
        self.__xas_all = np.zeros((self.num - 2, self.__nspin))

        for i in range(2, self.num):
            self.__eng[i - 2] = float(self.__datlines[i].split()[0])

            # 複数エッジ未対応
            for spin in range(self.__nspin):
                self.__xas_all[i - 2, spin] = \
                    float(self.__datlines[i].split()[1 + spin + edge]) / weight

        # self.E_fermi = self.E_Fermi if hasattr(self, 'E_Fermi') else None
        # self.__E_fermi = self.__E_Fermi if hasattr(self, 'E_Fermi') else 0.0
        self.__E_Fermi = self.__param['E_Fermi']
        self.__E_edge = self.__param['E_edge']
        self.__Z = self.__param['Z']

        self.__ispin = self.__nspin
        self.__xas = self.__xas_all[:, 0]

    # ヘッダー項目
    def get_eedge(self):
        # self.__E_edge = self.__E_edge if hasattr(self, 'E_edge') else None
        return self.__E_edge

    @property
    def eedge(self):
        return self.__E_edge

    @property
    def e_edge(self):
        return self.__E_edge

    @property
    def E_edge(self):
        return self.__E_edge

    # ヘッダー項目
    def get_efermi(self):
        # self.E_Fermi = self.E_Fermi if hasattr(self, 'E_Fermi') else None
        # self.__E_Fermi = self.__E_Fermi if hasattr(self, 'E_Fermi') else 0.0
        return self.__E_Fermi

    @property
    def efermi(self):
        # self.__E_Fermi = self.__E_Fermi if hasattr(self, 'E_Fermi') else 0.0
        return self.__E_Fermi

    # ヘッダー項目
    def get_e_fermi(self):
        # self.E_Fermi = self.E_Fermi if hasattr(self, 'E_Fermi') else None
        # self.E_Fermi = self.E_Fermi if hasattr(self, 'E_Fermi') else 0.0
        return self.__E_Fermi

    @property
    def e_fermi(self):
        # self.E_Fermi = self.E_Fermi if hasattr(self, 'E_Fermi') else 0.0
        return self.__E_Fermi

    @property
    def E_Fermi(self):
        return self.__E_Fermi

    @property
    def E_fermi(self):
        return self.__E_Fermi

    # ヘッダー項目
    def get_z(self):
        # self.Z = self.Z if hasattr(self, 'Z') else None
        return self.__Z

    # ヘッダー項目
    def get_eng(self):
        return self.__eng

    @property
    def eng(self):
        return self.__eng

    def get_xas_all(self):
        return self.__xas_all

    @property
    def xas_all(self):
        return self.__xas_all

    def get_xas(self, spin=0):
        return self.__xas_all[:, spin]

    @property
    def xas(self):
        return self.__xas

    def get_header(self):
        return self.__header

    @property
    def header(self):
        return self.__header

    def get_nspin(self):
        return self.__nspin

    @property
    def nspin(self):
        return self.__nspin

    def get_ispin(self):
        return self.__ispin

    @property
    def ispin(self):
        return self.__ispin

    def average(self, name, absorber, spin=0, weight=None):
        """
        allsite のときの複数の *.txt の平均を取る
        filout = Pd のとき allsite ならばとして結果を出力したとする
        Pd_1.txt
        Pd_2.txt
        Pd_3.txt
        このとき、average_txt(1,2,3) とすると Pd_1,Pd_2,Pd_3 の self.xas の
        平均を self.xas に返す

        non-spin

        :param name:
        :param absorber:
        :param spin:
        :param weight:
        :return:
        """
        if weight is None:
            n_site = float(len(absorber))
        else:
            print("weight : %s" % str(weight))
            n_site = float(weight)

        s_xas = np.zeros((self.num - 2, self.__nspin))
        for site in absorber:

            txtname = name + "_" + str(site) + self.suffix
            datlines, num = SAEnv.read_dataline(txtname)
            print("sum : %s" % str(txtname))

            for i in range(2, self.num):
                s_xas[i - 2, spin] = float(datlines[i].split()[1 + spin - 1]) \
                                     + s_xas[i - 2, spin]
        self.__xas = s_xas / n_site
        return self.__xas


def plot_fdm_xas(eng, xas):
    import matplotlib.pyplot as plt

    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 16  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize'] = 14  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth'] = 1.5  # 軸の太さを設定。目盛りは変わらない

    plt.figure(figsize=(7.00, 9.89))  # for portrait

    orgx = 0.170
    orgy = 0.080
    off = 0.010
    xsize = 0.75
    ysize = 0.83 / 2.

    plt.axes([orgx, orgy, xsize, ysize])

    plt.plot(eng, xas, linewidth=2, label='XAS')

    plt.xlabel("Energy above Fermi [eV]")
    plt.ylabel("Absorption [arb. unit]")
    plt.axvline(x=0, color='black', linewidth=1)

    leg = plt.legend(fontsize=12, loc='lower right')
    leg.get_frame().set_alpha(0.5)

    plt.savefig("XAS.eps")
    plt.savefig("XAS.pdf")
    plt.savefig("XAS.png")

    plt.show()

    plt.close('all')


def options():
    #   name = 'POSCAR.txt'
    name = 'Cu'
    suffix = '.txt'

    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest='INPUT', )
    options, args = parser.parse_args()

    #   if not os.path.exists(name):
    #       name0 = SAE.find_datfile1('_conv.txt')
    #       if name0 is None:
    #           name0 = name
    #   name = name0

    if options.INPUT: name = options.INPUT
    if len(args) > 0: name = args[0]

    return name, suffix


if __name__ == '__main__':
    name, suffix = options()
    conv = ReadFdmTxt(name, suffix)

    eng = conv.get_eng()
    xas = conv.get_xas()

    print("E-Edge  = %s" % str(conv.get_eedge()))
    print("E-Fermi = %s" % str(conv.get_efermi()))

#   plot_fdm_xas(eng,xas)

#   print "NAME",name
