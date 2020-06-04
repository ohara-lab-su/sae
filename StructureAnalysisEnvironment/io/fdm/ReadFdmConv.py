#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
# *_conv.txt ファイル( pw.x 入力ファイル 読み込み)
#
###############################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.07.22
#  入力ファイル名にsuffixを付けても、つけなくても(別オプションでsuffix指定)
#  どちらでも動作するように変更。
#
# 2015.07.01
#  平均化ルーチンで重み(平均する際に割る数)を引数に追加
#
# 2015.06.30
#   == Noneo --> is None
#
# 2015.05.21 startup
#
###############################################################################
from __future__ import print_function

try:
    from ...copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

###############################################################################

import sys
# import gzip
import os
# import re
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


class ReadFdmConv(object):

    def __init__(self, cname, suffix='_conv.txt', weight=None):

        if not os.path.exists(cname + suffix):
            cname = cname.replace(suffix, '')

        self.datlines, self.num = SAEnv.read_dataline(cname + suffix)

        self.name = cname
        self.suffix = suffix
        self.eng = np.zeros(self.num - 1)
        self.xas = np.zeros(self.num - 1)

        if weight is None:
            weight = 1.0

        for i in range(1, self.num):
            self.eng[i - 1] = float(self.datlines[i].split()[0])
            self.xas[i - 1] = float(self.datlines[i].split()[1]) / float(weight)

    def get_eng(self):
        return self.eng

    def get_xas(self):
        return self.xas

    ###########################################################################
    # allsite のときの複数の *_conv.txt の平均を取る
    # filout = Pd のとき allsite ならばとして結果を出力したとする
    # Pd_1_conv.txt
    # Pd_2_conv.txt
    # Pd_3_conv.txt
    # このとき、average_conv(1,2,3) とすると Pd_1,Pd_2,Pd_3 の self.xas の
    # 平均を self.xas に返す
    #
    # non-spin
    #   def average_conv(self,name,*allsite):
    def average_conv(self, name, absorber, weight=None):
        if weight is None:
            n_site = float(len(absorber))
        else:
            print("weight : %s" % str(weight))
            n_site = float(weight)
        s_xas = np.zeros(self.num - 1)
        # print absorber
        for site in absorber:
            convname = name + "_" + str(site) + self.suffix
            datlines, num = SAEnv.read_dataline(convname)
            print("sum : %s" % str(convname))
            for i in range(1, self.num):
                s_xas[i - 1] = float(datlines[i].split()[1]) + s_xas[i - 1]
        self.xas = s_xas / n_site
        return self.xas


###############################################################################
def plot_fdm_xas(eng, xas):
    import matplotlib.pyplot as plt

    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 16  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize'] = 14  # レジェンドのフォントサイズ
    # 軸の太さを設定。目盛りは変わらない
    plt.rcParams['axes.linewidth'] = 1.5

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
    name = 'POSCAR'
    suffix = '_conv.txt'

    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest='INPUT', )
    options, args = parser.parse_args()

    if not os.path.exists(name):
        name0 = SAEnv.find_datfile1(suffix)
        name0 = name0.replace(suffix, '')
        if name0 is not None:
            name0 = name
        name = name0

    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]

    return name, suffix


###############################################################################
if __name__ == '__main__':
    name, suffix = options()
    #   print name,suffix
    conv = ReadFdmConv(name, suffix)

    eng = conv.get_eng()
    xas = conv.get_xas()

    av = conv.average_conv(1, 2, 3, 4, 5)

#   plot_fdm_xas(eng,xas)

#   print "NAME",name
