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


class ReadFdmBav2020(object):

    def __init__(self, cname, suffix='_bav.txt', datline=None, num=None):
        """

        :param datline: バージョン切り替え時に読んだ datline 情報を引き継ぐ
        :param cname:  入力の bav ファイル(FDMNESの全ログ情報)
        :param suffix:
        """
        if datline is None or num is None:
            self.datlines, self.num = SAEnv.read_dataline(cname + suffix)
        else:
            self.datlines = datline
            self.num = num

        fdmnes_ver_reg = re.compile('.*FDMNES.*program,.*')
        ngroup_reg = re.compile('.*ngroup =.*')
        excited_atom_reg = re.compile('.*Excited atom.*')
        atom_type_reg = re.compile('.*Atom type.*')
        threshold_reg = re.compile('.*Threshold:.*')
        r2_reg = re.compile('.*Transformation Crystal Bases.*Bases R2.*')
        positions_reg = re.compile('.*Cluster: atom positions in order.*')
        scf_flag_reg = re.compile('.*Self consistent calculation')
        scf_max_reg = re.compile('.*Maximum number of iteration')
        scf_end_reg = re.compile('.*Begining of cycle.*')
        scf_toten_reg = re.compile('.*Unit cell energy.*')

        nspin_reg = re.compile('.*Magnetic calculation')

        self.t = np.zeros((3, 3))
        #       self.position = []

        self.nspin = 1  # default nonmag
        self.SCF = False
        self.n_scf_loop = 0
        self.scf_toten = []

        # ログファイル読み込みのアホなループ
        for i in range(self.num):
            # print(self.datlines[i])

            # Version チェック
            if bool(fdmnes_ver_reg.match(self.datlines[i])):
                print(self.datlines[i])
                self.fdmnes_ver = re.sub('.*,', '', self.datlines[i]).strip()
                print(self.fdmnes_ver)

            # SCF 計算のチェック
            if bool(scf_flag_reg.match(self.datlines[i])):
                self.SCF = True

            # scf ループの最大値
            if bool(scf_max_reg.match(self.datlines[i])):
                self.nsw = int(self.datlines[i].split()[5])

            # scf ループ数のカウント
            if bool(scf_end_reg.match(self.datlines[i])):
                self.n_scf_loop = int(self.datlines[i].split()[3])
                print("num. scf loop = %s" % self.n_scf_loop)

            # scf ループ毎の unit cell の全エネルギー
            if bool(scf_toten_reg.match(self.datlines[i])):
                self.scf_toten.append(self.datlines[i])

            # 全原子数の検索
            if bool(ngroup_reg.match(self.datlines[i])):
                if self.datlines[i].split()[0] == 'ngroup':
                    self.ngroup = int(self.datlines[i].split()[2].replace(',', ''))
                else:
                    sys.exit("STOP(ReadFdmBav): ngroup tag not found.")

            # 吸収原子の最大のlを探す
            if bool(excited_atom_reg.match(self.datlines[i])):
                j = 2
                l = 0
                while 1:
                    _l = int(self.datlines[i + j].split()[1])
                    if l < _l:
                        l = _l
                    j += 1
                    if bool(atom_type_reg.match(self.datlines[i + j + 1])):
                        break
                self.lmax = l
                print("l max = %s" % self.lmax)

            # Magnetic? or Nonmag
            if bool(nspin_reg.match(self.datlines[i])):
                self.nspin = 2

            # 吸収端
            if bool(threshold_reg.match(self.datlines[i])):
                self.edge = self.datlines[i].split()[2]
                print("Edge = %s" % self.edge)

            # absorber を原点とした時の基本並進ベクトル
            if bool(r2_reg.match(self.datlines[i])):
                t1_x = float(self.datlines[i + 1].split()[0])
                t1_y = float(self.datlines[i + 1].split()[1])
                t1_z = float(self.datlines[i + 1].split()[2])

                t2_x = float(self.datlines[i + 2].split()[0])
                t2_y = float(self.datlines[i + 2].split()[1])
                t2_z = float(self.datlines[i + 2].split()[2])

                t3_x = float(self.datlines[i + 3].split()[0])
                t3_y = float(self.datlines[i + 3].split()[1])
                t3_z = float(self.datlines[i + 3].split()[2])

                self.t[0, 0] = t1_x
                self.t[1, 0] = t1_y
                self.t[2, 0] = t1_z

                self.t[0, 1] = t2_x
                self.t[1, 1] = t2_y
                self.t[2, 1] = t2_z

                self.t[0, 2] = t3_x
                self.t[1, 2] = t3_y
                self.t[2, 2] = t3_z

                print("t =")
                print(self.t)

            # positon (絶対座標系)
            if bool(positions_reg.match(self.datlines[i])):

                self.position = []
                self.atoms_index_j = []

                j = 0
                while 1:
                    zz = int(self.datlines[2 + i + j].split()[0])
                    self.atoms_index_j.append(SAEnv.get_atomic_symbol0(zz))
                    px = float(self.datlines[2 + i + j].split()[1])
                    py = float(self.datlines[2 + i + j].split()[2])
                    pz = float(self.datlines[2 + i + j].split()[3])
                    self.position.append([px, py, pz])
                    j += 1
                    if len(self.datlines[2 + i + j].split()) <= 0:
                        break
                self.natom = j
                self.position = np.array(self.position)

        # ispin は現在値で nspin はトータル
        self.ispin = self.nspin
        self.__scf_toten = np.array(self.scf_toten)

    #
    # property (added: 2020.07.17)
    #

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

    #
    # get attribute
    #

    def get_nspin(self):
        return self.nspin

    def get_natom(self):
        self.natom = self.natom if hasattr(self, 'natom') else 0
        return self.natom

    def get_ngroup(self):
        self.ngroup = self.ngroup if hasattr(self, 'ngroup') else 0
        return self.ngroup

    def get_t(self):
        return self.t

    def get_edge(self):
        self.edge = self.edge if hasattr(self, 'edge') else None
        return self.edge

    def get_lmax(self):
        self.lmax = self.lmax if hasattr(self, 'lmax') else None
        return self.lmax

    def get_position(self):
        return self.position

    def get_atoms_index_j(self):
        return self.atoms_index_j

    def get_fdmnes_ver(self):
        return self.fdmnes_ver


###############################################################################


def options():
    #   name = 'POSCAR.txt'
    name = 'Cu'
    suffix = '_bav.txt'

    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest='INPUT', )
    options, args = parser.parse_args()

    if not os.path.exists(name + suffix):
        name0 = SAEnv.find_datfile1(suffix)
        name = name0.replace(suffix, '')

    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]

    return name, suffix


###############################################################################
if __name__ == '__main__':

    name, suffix = options()
    bav = SAEnv.ReadFdmBav2020(name, suffix)
    print('')

    natom = bav.get_natom()
    lmax = bav.get_lmax()
    edge = bav.get_edge()
    t = bav.get_t()
    position = bav.get_position()
    atoms_index_j = bav.get_atoms_index_j()

    print("n_ion_loop %s" % str(bav.n_scf_loop))
    for i in range(bav.n_scf_loop):
        print("%s" % str(bav.scf_toten[i]))

    print("natom = %s" % str(natom))
    print("lmax  = %s" % str(lmax))
    print("edge  = %s" % str(edge))
    print("t     = %s" % str(t))

#   for i in range(natom):
#       print "%s %10.6f %10.6f %10.6f" \
#         % (atoms_index_j[i], position[i, 0], position[i, 1], position[i, 2])
#       print position[i][0],position[i][1],position[i][2]
