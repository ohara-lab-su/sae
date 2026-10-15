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
# sys.path.append('../..')
# import SpaceGroupEnvironment as SGE
###############################################################################
#   name = 'POSCAR.txt'
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
# property (added: 2020.07.17)
#
#
# get attribute
#
class ReadFdmBav2016(object):

    # 吸収端のエネルギー(2020と互換)
    # self.position = []
    # ログファイル読み込みのアホなループ
    def __init__(self, cname, suffix="_bav.txt", datline=None, num=None):
        """

        :param datline: バージョン切り替え時に読んだ datline 情報を引き継ぐ
        :param cname:  入力の bav ファイル(FDMNESの全ログ情報)
        :param suffix:
        """
        from sae.common.text import TextFiles
        from sae.structure.elements import ElementTable

        print("===== bav2016 =====")
        if datline is None or num is None:
            self.__datlines, self.num = TextFiles().read_dataline(cname + suffix)
        else:
            self.__datlines = datline
            self.num = num
        fdmnes_ver_reg = re.compile(".*FDMNES.*program,.*")
        ngroup_reg = re.compile(".*ngroup =.*")
        excited_atom_reg = re.compile(".*Excited atom.*")
        atom_type_reg = re.compile(".*Atom type.*")
        threshold_reg = re.compile(".*Threshold:.*")
        r2_reg = re.compile(".*Transformation Crystal Bases.*Bases R2.*")
        positions_reg = re.compile(".*Cluster: atom positions in order.*")
        scf_flag_reg = re.compile(".*Self consistent calculation")
        scf_max_reg = re.compile(".*Maximum number of iteration")
        scf_end_reg = re.compile(".*Begining of cycle.*")
        scf_toten_reg = re.compile(".*Unit cell energy.*")
        e_edge_reg = re.compile(".*E_edge.*")
        nspin_reg = re.compile(".*Magnetic calculation")
        self.__t = np.zeros((3, 3))
        # default nonmag
        self.__nspin = 1
        self.SCF = False
        self.__n_scf_loop = 0
        self.__scf_toten = []
        # print(self.datlines[i])
        # Version チェック
        # SCF 計算のチェック
        # scf ループの最大値
        # scf ループ数のカウント
        # scf ループ毎の unit cell の全エネルギー
        # 全原子数の検索
        # 吸収原子の最大のlを探す
        # Magnetic? or Nonmag
        # 吸収端(記号)
        # 吸収端のエネルギー(Kによる固定値)
        # absorber を原点とした時の基本並進ベクトル
        # positon (絶対座標系)
        for i in range(self.num):
            if bool(fdmnes_ver_reg.match(self.__datlines[i])):
                print(self.__datlines[i])
                self.fdmnes_ver = re.sub(".*,", "", self.__datlines[i]).strip()
                print(self.fdmnes_ver)
            if bool(scf_flag_reg.match(self.__datlines[i])):
                self.SCF = True
            if bool(scf_max_reg.match(self.__datlines[i])):
                self.nsw = int(self.__datlines[i].split()[5])
            if bool(scf_end_reg.match(self.__datlines[i])):
                self.__n_scf_loop = int(self.__datlines[i].split()[3])
                print("num. scf loop = %s" % self.__n_scf_loop)
            if bool(scf_toten_reg.match(self.__datlines[i])):
                self.__scf_toten.append(self.__datlines[i])
            if bool(ngroup_reg.match(self.__datlines[i])):
                if self.__datlines[i].split()[0] == "ngroup":
                    self.ngroup = int(self.__datlines[i].split()[2].replace(",", ""))
                else:
                    sys.exit("STOP(ReadFdmBav): ngroup tag not found.")
            if bool(excited_atom_reg.match(self.__datlines[i])):
                j = 2
                l = 0
                while 1:
                    _l = int(self.__datlines[i + j].split()[1])
                    if l < _l:
                        l = _l
                    j += 1
                    if bool(atom_type_reg.match(self.__datlines[i + j + 1])):
                        break
                self.lmax = l
                print("l max = %s" % self.lmax)
            if bool(nspin_reg.match(self.__datlines[i])):
                self.__nspin = 2
            if bool(threshold_reg.match(self.__datlines[i])):
                self.__edge = self.__datlines[i].split()[2]
                print("Edge = %s" % self.__edge)
            if bool(e_edge_reg.match(self.__datlines[i])):
                self.__e_edge = self.__datlines[i].split()[2]
                print("E_Edge = %s [eV]" % self.__e_edge)
            if bool(r2_reg.match(self.__datlines[i])):
                t1_x = float(self.__datlines[i + 1].split()[0])
                t1_y = float(self.__datlines[i + 1].split()[1])
                t1_z = float(self.__datlines[i + 1].split()[2])
                t2_x = float(self.__datlines[i + 2].split()[0])
                t2_y = float(self.__datlines[i + 2].split()[1])
                t2_z = float(self.__datlines[i + 2].split()[2])
                t3_x = float(self.__datlines[i + 3].split()[0])
                t3_y = float(self.__datlines[i + 3].split()[1])
                t3_z = float(self.__datlines[i + 3].split()[2])
                self.__t[0, 0] = t1_x
                self.__t[1, 0] = t1_y
                self.__t[2, 0] = t1_z
                self.__t[0, 1] = t2_x
                self.__t[1, 1] = t2_y
                self.__t[2, 1] = t2_z
                self.__t[0, 2] = t3_x
                self.__t[1, 2] = t3_y
                self.__t[2, 2] = t3_z
                print("t =")
                print(self.__t)
            if bool(positions_reg.match(self.__datlines[i])):
                self.__position = []
                self.atoms_index_j = []
                j = 0
                while 1:
                    zz = int(self.__datlines[2 + i + j].split()[0])
                    self.atoms_index_j.append(ElementTable().get_atomic_symbol0(zz))
                    px = float(self.__datlines[2 + i + j].split()[1])
                    py = float(self.__datlines[2 + i + j].split()[2])
                    pz = float(self.__datlines[2 + i + j].split()[3])
                    self.__position.append([px, py, pz])
                    j += 1
                    if len(self.__datlines[2 + i + j].split()) <= 0:
                        break
                self.natom = j
                self.__position = np.array(self.__position)
        self.ispin = self.__nspin
        self.__scf_toten = np.array(self.__scf_toten)

    def set_n_scf_loop(self, _val):
        self.__n_scf_loop = _val

    def get_n_scf_loop(self):
        return self.__n_scf_loop

    n_scf_loop = property(get_n_scf_loop, set_n_scf_loop)

    def get_scf_toten(self):
        return self.__scf_toten

    def set_scf_toten(self, _val):
        self.__scf_toten = _val

    scf_toten = property(get_scf_toten, set_scf_toten)

    def get_nspin(self):
        return self.__nspin

    @property
    def nspin(self):
        return self.__nspin

    def get_natom(self):
        self.natom = self.natom if hasattr(self, "natom") else 0
        return self.natom

    def get_ngroup(self):
        self.ngroup = self.ngroup if hasattr(self, "ngroup") else 0
        return self.ngroup

    def get_t(self):
        return self.__t

    @property
    def t(self):
        return self.__t

    def get_edge(self):
        self.__edge = self.__edge if hasattr(self, "edge") else None
        return self.__edge

    @property
    def edge(self):
        return self.__edge

    def get_e_edge(self):
        return float(self.__e_edge)

    @property
    def e_edge(self):
        return float(self.__e_edge)

    def get_lmax(self):
        self.lmax = self.lmax if hasattr(self, "lmax") else None
        return self.lmax

    def get_position(self):
        return self.__position

    @property
    def position(self):
        return self.__position

    def get_atoms_index_j(self):
        return self.atoms_index_j

    def get_fdmnes_ver(self):
        return self.fdmnes_ver
