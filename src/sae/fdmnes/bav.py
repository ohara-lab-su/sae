#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
# *_bav.txt ファイル
#
###############################################################################
#
# 2020.08.11: バージョン切り替えのバグフィックス
#
# 2020.07.17
#  2016.08.01 以降に sd? のナンバリングルールが変わったのでそれに対する対応
#  - バージョンチェック(ReadFdmBav.py) のための改修
#  - バージョン切り替えのために ReadFdmBav2016()
#  - バージョン切り替えのために ReadFdmBav2020() 切り替え
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.09.11
#  scf ループ関係の情報吸い出しを追加
#
# 2015.06.25
#  R2 bases に対応した cluster: atom positions 吸い出しに対応
#
# 2015.06.23 startup
#
###############################################################################
# トップディレクトリ関係のエラーは ImportError ではキャッチ出来ない
###############################################################################
# import gzip
# import StructureAnalysisEnvironment as SAE
# import SpaceGroupEnvironment as SGE
###############################################################################
#   name = 'POSCAR.txt'
###############################################################################
#   for i in range(natom):
#       print "%s %10.6f %10.6f %10.6f" \
#         % (atoms_index_j[i], position[i, 0], position[i, 1], position[i, 2])
#       print position[i][0],position[i][1],position[i][2]
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import optparse
import numpy as np


#
# get attribute
#
class ReadFdmBav(object):

    # suffix がすでにセットされているときと、suffix がセットされてないときで切り替える
    # for default
    # FDMNES のバージョン取得
    def __init__(self, cname, suffix="_bav.txt"):
        """

        :param cname:  入力の bav ファイル(FDMNESの全ログ情報)
        :param suffix:
        """
        from sae.common.text import TextFiles
        from sae.fdmnes.bav_2016 import ReadFdmBav2016
        from sae.fdmnes.bav_2020 import ReadFdmBav2020

        if cname.endswith(suffix):
            bav_name = cname
        else:
            bav_name = cname + suffix
        self.__datlines, self.__num = TextFiles().read_dataline(bav_name)
        fdmnes_ver_reg = re.compile(".*FDMNES.*program,.*")
        fdm_version = 2020
        # Version チェック
        for i in range(self.__num):
            if bool(fdmnes_ver_reg.match(self.__datlines[i])):
                print("")
                print("get fdmnes version")
                self.__fdmnes_ver = re.sub(".*,", "", self.__datlines[i]).strip()
                fdm_version = self.__fdmnes_ver.strip("")
                print("version = %s" % fdm_version)
                break
        try:
            year = int(fdm_version.split(" ")[-1])
            print(year)
        except:
            print("*** fail *** get fdmnes version")
            new = True
        else:
            if year > 2016:
                new = True
            else:
                new = False
        # 2016.09.01 〜 (動作テストは 2020.06.12-2 version)
        #  〜2016.01.08
        if new:
            print("load NEW format: sd2020")
            print("")
            self.__bav = ReadFdmBav2020(
                cname, suffix, datline=self.__datlines, num=self.__num
            )
        else:
            print("load OLD format: befor sd2016.01.08")
            print("")
            self.__bav = ReadFdmBav2016(
                cname, suffix, datline=self.__datlines, num=self.__num
            )

    def set_n_scf_loop(self, _val):
        self.__bav.n_scf_loop = _val

    def get_n_scf_loop(self):
        return self.__bav.n_scf_loop

    n_scf_loop = property(get_n_scf_loop, set_n_scf_loop)

    def get_scf_toten(self):
        return self.__bav.scf_toten

    def set_scf_toten(self, _val):
        self.__bav.scf_toten = _val

    scf_toten = property(get_scf_toten, set_scf_toten)

    def get_nspin(self):
        return self.__bav.nspin

    def get_natom(self):
        return self.__bav.natom

    def get_ngroup(self):
        return self.__bav.ngroup

    def get_t(self):
        return self.__bav.t

    @property
    def t(self):
        return self.__bav.t

    def get_edge(self):
        return self.__bav.edge

    @property
    def edge(self):
        return self.__bav.edge

    def get_e_edge(self):
        return self.__bav.e_edge

    @property
    def e_edge(self):
        return self.__bav.e_edge

    def get_lmax(self):
        return self.__bav.lmax

    @property
    def lmax(self):
        return self.__bav.lmax

    def get_position(self):
        return self.__bav.position

    def get_atoms_index_j(self):
        return self.__bav.atoms_index_j

    def get_fdmnes_ver(self):
        return self.__fdmnes_ver

    @property
    def fdmnes_ver(self):
        return self.__fdmnes_ver
