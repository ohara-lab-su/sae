#!/usr/bin/env python
# -*- coding: utf-8 -*
###############################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
#   *_sd*.txt ファイル( pw.x 入力ファイル 読み込み)
#   Ver_0.0.2 以降 FDMNS のバージョンの違いによるログの違いを吸収
#    - ReadFdmSd2016()
#    - ReadFdmSd2020() 切り替え
#
###############################################################################
#
# 2020.07.17 (Ver_0.0.2)
#  2016.08.01 以降に sd? のナンバリングルールが変わったのでそれに対する対応
#  - バージョンチェック(ReadFdmBav.py) を用いる
#    - ReadFdmSd2016()
#    - ReadFdmSd2020() 切り替え
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

from sae._logging import debug_values as _log_debug

from sae.errors import legacy_error as _legacy_error

# トップディレクトリ関係のエラーは ImportError ではキャッチ出来ない
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

import StructureAnalysisEnvironment as SAE

# import SpaceGroupEnvironment as SGE

###############################################################################


class DensityOfStates(object):

    def __init__(
        self,
        sdname,
        suffix="_sd0.txt",
        inpname=None,
        bavname=None,
        absorber=None,  ### absorber=[] :matrix
        weight=None,
        bav=None,
    ):
        """

        :param sdname: Pd_sd0.txt のとき Pd が sdname となる
        :param suffix:
        :param inpname: FDMNES の入力ファイルからいくつかの情報を取り出す
        :param bavname:
        :param absorber:
        :param weight:
        :param bav:
        """

        # FDMNES のバージョン取得
        _log_debug("")
        _log_debug("get fdmnes version")
        try:
            bav = SAE.ReadFdmBav(sdname, "_bav.txt")
            fdm_version = bav.get_fdmnes_ver().strip("")
            _log_debug("")
            _log_debug("version = %s" % fdm_version)
            year = int(fdm_version.split(" ")[-1])
            _log_debug(year)
        except:
            _log_debug("*** fail *** get fdmnes version")
            new = True
        else:
            if year > 2016:
                new = True
            else:
                new = False

        if new:
            # 2016.09.01 〜 (動作テストは 2020.06.12-2 version)
            _log_debug("load NEW format: sd2020")
            _log_debug("")
            self.__sd = SAE.io.ReadFdmSd2020(
                sdname, suffix, inpname, bavname, absorber, weight
            )
        else:
            #  〜2016.01.08
            _log_debug("load OLD format: ~sd2016.01.08")
            _log_debug("")
            self.__sd = SAE.io.ReadFdmSd2016(
                sdname, suffix, inpname, bavname, absorber, weight
            )

    #
    # Method
    #

    def get_pdos(self, l=0, m=0, lm=None, spin=0):
        return self.__sd.get_pdos(l, m, lm, spin)

    def get_ldos(self, l=0, spin=0):
        """LDOS(NEDOS, L, SPIN"""
        return self.__sd.get_ldos(l, spin)

    def get_intldos(self, l=0, spin=0):
        """INTLDOS(NEDOS,L,SPIN)"""
        return self.__sd.get_intldos(l, spin)

    #
    # get/set attribute (2)
    #

    def get_tdos(self, spin=0):
        """TDOS(NEDOS, SPIN)"""
        self.__sd.get_tdos(spin)

    def get_inttdos(self, spin=0):
        """INTTDOS(NEDOS, SPIN)"""
        return self.__sd.get_inttdos(spin)

    def get_eng(self):
        return self.__sd.eng

    @property
    def eng(self):
        return self.__sd.eng

    #
    # property
    #

    def get_emin(self):
        return self.__sd.emin

    @property
    def emin(self):
        return self.__sd.emin

    def get_emax(self):
        return self.__sd.emax

    @property
    def emax(self):
        return self.__sd.emax

    def get_ymax(self):
        return self.__sd.ymax

    @property
    def ymax(self):
        return self.__sd.ymax

    def get_header(self):
        return self.__sd.header

    @property
    def header(self):
        return self.__sd.header

    def get_num(self):
        """読み込んだ sd ファイルの行数"""
        return self.__sd.num

    @property
    def num(self):
        return self.__sd.num

    def get_sd(self):
        """読み込んだ sd ファイル丸ごと(平均化したら、平均化した値)"""
        return self.__sd.sd

    def get_lmax(self):
        """読み込んだ sd ファイルに基づいて lmax を抽出"""
        return self.__sd.lmax

    @property
    def lmax(self):
        return self.__sd.lmax

    def get_mmax(self):
        return self.__sd.mmax

    @property
    def mmax(self):
        return self.__sd.mmax

    def get_ispin(self):
        return self.__sd.ispin

    @property
    def ispin(self):
        return self.__sd.ispin


def options():
    name = "Cu"
    #   name = 'Fe'
    suffix = "_sd0.txt"

    parser = optparse.OptionParser()
    parser.add_option(
        "-i",
        "--input",
        dest="INPUT",
    )
    options, args = parser.parse_args()

    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]

    return name, suffix


###############################################################################
if __name__ == "__main__":
    name, suffix = options()
    sd = SAE.io.ReadFdmSd(name, suffix)

#   eng = conv.get_eng()
#   xas = conv.get_xas()


#   print "NAME",name


ReadFdmSd = DensityOfStates  # historical spelling
