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

#import sys
#import gzip
#import os
#import re
import optparse
import numpy as np

import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE

###############################################################################


class ReadFdm(object):

    def __init__(self, cname, suffix='.txt', weight=1.0):

        name = cname.replace(suffix, '')
        suffix0 = cname.replace(name, '')
        if suffix0 != suffix:
            suffix = '.txt'
            cname = name + suffix

        self.suffix = suffix
        self.datlines, self.num = SAEnv.read_dataline(cname)
        self.header = self.datlines[0]

        self.eng = np.zeros(self.num - 2)
        self.xas = np.zeros(self.num - 2)

        # 一行目のイコールで結ばれたところまでの変数の数のカウント
        count = 0
        for i in self.datlines[0].split():
            count += 1
            if i == '=':
                break

        # 一行目のイコールで結ばれた値=変数名を、動的に変数＝値としてセット
       # for i in range(count,len(self.datlines[0].split())):
           #var = str(self.datlines[0].split()[i].strip()).replace(',','')
           #value = float(self.datlines[0].split()[i-count])
        for i in range(count, len(self.datlines[0].replace(',', ' ').split())):
            var = str(self.datlines[0].replace(',', ' ').split()[i].strip())
            value = \
                  float(self.datlines[0].replace(',', ' ').split()[i - count])
            self.__dict__[var] = value

        for i in range(2, self.num):
            self.eng[i - 2] = float(self.datlines[i].split()[0])
            self.xas[i - 2] = float(self.datlines[i].split()[1])

        self.E_fermi = self.E_Fermi if hasattr(self, 'E_Fermi') else None

    # ヘッダー項目
    def get_eedge(self):
        self.E_edge = self.E_edge if hasattr(self, 'E_edge') else None
        return self.E_edge

    # ヘッダー項目
    def get_efermi(self):
        self.E_Fermi = self.E_Fermi if hasattr(self, 'E_Fermi') else None
        return self.E_Fermi

    # ヘッダー項目
    def get_e_fermi(self):
        self.E_Fermi = self.E_Fermi if hasattr(self, 'E_Fermi') else None
        return self.E_Fermi

    # ヘッダー項目
    def get_z(self):
        self.Z = self.Z if hasattr(self, 'Z') else None
        return self.Z

    # ヘッダー項目
    def get_eng(self):
        return self.eng

    def get_xas(self):
        return self.xas

    def get_header(self):
        return self.header

    ###########################################################################
    # allsite のときの複数の *.txt の平均を取る
    # filout = Pd のとき allsite ならばとして結果を出力したとする
    # Pd_1.txt
    # Pd_2.txt
    # Pd_3.txt
    # このとき、average_txt(1,2,3) とすると Pd_1,Pd_2,Pd_3 の self.xas の
    # 平均を self.xas に返す
    #
    # non-spin
    def average_txt(self, name, absorber, weight=None):
        if weight is None:
            n_site = float(len(absorber))
        else:
            print "weight : ", weight
            n_site = float(weight)
        s_xas = np.zeros(self.num - 2)
        for site in absorber:
            txtname = name + "_" + str(site) + self.suffix
            datlines, num = SAEnv.read_dataline(txtname)
            print "sum : ", txtname
            for i in range(2, self.num):
                s_xas[i - 2] = float(datlines[i].split()[1]) + s_xas[i - 2]
        self.xas = s_xas / n_site
        return self.xas

###############################################################################


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

###############################################################################


def options():

    #   name = 'POSCAR.txt'
    name = 'Cu'
    suffix = '.txt'

    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest='INPUT',)
    options, args = parser.parse_args()

#   if not os.path.exists(name):
#       name0 = SAEnv.find_datfile1('_conv.txt')
#       if name0 is None:
#           name0 = name
#   name = name0

    if options.INPUT: name = options.INPUT
    if len(args) > 0: name = args[0]

    return name, suffix


###############################################################################
if __name__ == '__main__':

    name, suffix = options()
    conv = ReadFdm(name, suffix)

    eng = conv.get_eng()
    xas = conv.get_xas()

    print "E-Edge  = ", conv.get_eedge()
    print "E-Fermi = ", conv.get_efermi()

#   plot_fdm_xas(eng,xas)

#   print "NAME",name
