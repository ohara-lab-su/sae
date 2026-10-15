#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Read Athena Normalize Data ( *.txt.nor )
#
# コメントアウトを除いて energy, XANES 形式に並んだだけのファイル
# Athena の Normlized Data の読み込みプロット
#
###############################################################################
#
# 2020.08.10: カプセル化
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.06.30
#   == Noneo --> is None
#
# 2015.05.21
#  ファイル名の自動取得&基本プロットのサンプル追加
#
# 2015.03.30
#  startup
#
###############################################################################
###############################################################################
# import gzip
# import optparse
# sys.path.append('../..')
# import SpaceGroupEnvironment as SGE
###############################################################################
###############################################################################
# ラベル等のフォントサイズ
# レジェンドのフォントサイズ
# 軸の太さを設定。目盛りは変わらない
# for portrait
#   plt.axvline(x=0,color='black',linewidth=1)
###############################################################################
###############################################################################
#   plot_athena_nor(spec.eng,spec.nor)
#   for i in range(ndata):
#       print eng[i],nor[i]
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import numpy as np


class ReadAthenaNor(object):

    def __init__(self, name="case.txt.nor"):
        from sae.common.text import TextFiles

        self.datlines, self.num = TextFiles().read_dataline(name)
        comment_reg = re.compile("^#.*")
        E0_reg = re.compile("^#.*E0.*")
        self.__eng = []
        self.__nor = []
        self.__ndata = 0
        # コメントアウトを除いて x,y 形式に並んだだけのファイル
        for i in range(self.num):
            line = self.datlines[i]
            if bool(E0_reg.match(line)):
                self.__e0 = float(re.sub("E0=", "", line.split()[2]))
            if not bool(comment_reg.match(line)):
                self.__eng.append(float(line.split()[0]))
                self.__nor.append(float(line.split()[1]))
                self.__ndata += 1
        self.__nor = np.array(self.__nor)
        self.__eng = np.array(self.__eng)
        self.__xas = self.__nor

    def open(self, name=None):
        pass

    def set_nor(self, _val):
        self.__nor = _val
        self.__xas = _val

    def get_nor(self):
        return self.__nor

    nor = property(get_nor, set_nor)

    def set_xas(self, _val):
        self.__xas = _val
        self.__nor = _val

    def get_xas(self):
        return self.__xas

    xas = property(get_xas, set_xas)

    def set_eng(self, _val):
        self.__eng = _val

    def get_eng(self):
        return self.__eng

    eng = property(get_eng, set_eng)

    def get_ndata(self):
        return self.__ndata

    @property
    def ndata(self):
        return self.__ndata

    def get_e0(self):
        return self.__e0

    @property
    def e0(self):
        return self.__e0


class NorOperations:

    def plot_athena_nor(self, eng, nor):
        import matplotlib.pyplot as plt

        plt.rcParams["font.family"] = "Times New Roman"
        plt.rcParams["font.size"] = 16
        plt.rcParams["legend.fontsize"] = 14
        plt.rcParams["axes.linewidth"] = 1.5
        plt.figure(figsize=(7.0, 9.89))
        orgx = 0.17
        orgy = 0.08
        off = 0.01
        xsize = 0.75
        ysize = 0.83 / 2.0
        plt.axes([orgx, orgy, xsize, ysize])
        plt.plot(eng, nor, linewidth=2, label="XAS")
        plt.xlabel("E")
        plt.ylabel(" chi mu (E)")
        leg = plt.legend(fontsize=12, loc="lower right")
        leg.get_frame().set_alpha(0.5)
        plt.savefig("XAS.eps")
        plt.savefig("XAS.pdf")
        plt.savefig("XAS.png")
        plt.show()
        plt.close("all")
