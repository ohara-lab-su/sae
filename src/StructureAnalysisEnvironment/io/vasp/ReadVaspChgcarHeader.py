#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
################################################################################
#
# CHGCAR/ELFCAR 読み込み class の一部、結晶のヘッダ（position情報の手前まで）
# を読み込むルーチン
#
################################################################################
from __future__ import print_function

try:
    from ...copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.0"

################################################################################
import sys
import os
import re
# import gzip
import multiprocessing
import math
import numpy as np

try:
    # sys.path.append('../..')
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    import StructureAnalysisEnvironment as SAEnv
    from StructureAnalysisEnvironment.Method import Method
except ImportError:
    import StructureAnalysisEnvironment as SAEnv
    from StructureAnalysisEnvironment.Method import Method

# スーパーセルに関していくつかルーチンを殺す。メモリ消費を少なくするため。
# reduced_memory = True
reduced_memory = False

# import SpaceGroupEnvironment as SGE
# from numba import jit


class ReadVaspChgcarHeader(Method):

    def __init__(self, CHGCAR='CHGCAR', suffix='.vasp', sort=False, atoms_index=None, logger=None):
        """
        init and Read CHGCAR
        CHGCAR/ELFCAR 読み込み class の一部、結晶のヘッダ（position情報の手前まで）
        を読み込むルーチン

        :param CHGCAR: 読み込みファイルの名前
        :param suffix: 使ってない
        :param sort:
        :param atoms_index:
        """
        if logger is None:
            logger = multiprocessing.get_logger()
        self.__logger = logger

        self.open(CHGCAR=CHGCAR, suffix=suffix, sort=sort, atoms_index=sort)

    def open(self, CHGCAR='CHGCAR', suffix='.vasp', sort=False, atoms_index=None):
        self.datlines, self.num = SAEnv.read_dataline(CHGCAR)

        self.system = self.datlines[0]
        self.title = self.system
        self.scale = float(self.datlines[1])

        print("--- Read STRUCTURE DATA = ", CHGCAR)
        ###############################################
        # Read Translation Vector
        #         x   y   z
        #   t1 = t11 t21 t31
        #   t2 = t12 t22 t32
        #   t3 = t13 t23 t33
        #
        t1_x = float(self.datlines[2].split()[0])
        t1_y = float(self.datlines[2].split()[1])
        t1_z = float(self.datlines[2].split()[2])

        t2_x = float(self.datlines[3].split()[0])
        t2_y = float(self.datlines[3].split()[1])
        t2_z = float(self.datlines[3].split()[2])

        t3_x = float(self.datlines[4].split()[0])
        t3_y = float(self.datlines[4].split()[1])
        t3_z = float(self.datlines[4].split()[2])

        self.t = np.zeros((3, 3))
        self.t[0, 0] = t1_x
        self.t[1, 0] = t1_y
        self.t[2, 0] = t1_z

        self.t[0, 1] = t2_x
        self.t[1, 1] = t2_y
        self.t[2, 1] = t2_z

        self.t[0, 2] = t3_x
        self.t[1, 2] = t3_y
        self.t[2, 2] = t3_z

        ###############################################
        # 単位胞の長さの計算
        #
        self.t1_len = math.sqrt((t1_x * t1_x) + (t1_y * t1_y) + (t1_z * t1_z))
        self.t2_len = math.sqrt((t2_x * t2_x) + (t2_y * t2_y) + (t2_z * t2_z))
        self.t3_len = math.sqrt((t3_x * t3_x) + (t3_y * t3_y) + (t3_z * t3_z))

        # print("lattice a = %s " % str(self.t1_len))
        # print("lattice b = %s " % str(self.t2_len))
        # print("lattice c = %s " % str(self.t3_len))

        ###############################################
        # VASP のバージョン番号確認(記号があるか否か)
        #
        i = 5
        self.vasp_version = 5
        atoms = self.datlines[i].split()
        if atoms[0].isdigit():  # 数字ならば
            self.vasp_version = 4
        del atoms

        self.__logger.debug("    vasp version = %s" % self.vasp_version)
        ###############################################
        # atoms[i]  : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
        # atoms_index[i] : 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
        #
        i = 5
        self.atoms_index = []
        self.atoms = []
        if self.vasp_version == 4:
            self.atoms.extend(self.datlines[i].split())
        elif self.vasp_version == 5:
            self.atoms_index.extend(self.datlines[i].split())
            self.atoms.extend(self.datlines[i + 1].split())
        else:
            sys.exit("Error: unknown VASP format")

        self.atoms = np.array(self.atoms, dtype=int)
        self.nion = len(self.atoms)

        ###############################################
        # atoms_number[i]
        #   atoms_index の原子番号版
        self.atoms_number = np.zeros(self.nion, dtype=int)
        for i in range(self.nion):
            self.__logger.debug("atoms_index[%d] = %s" % (i, self.atoms_index[i]))
            self.atoms_number[i] = SAEnv.get_atomic_number1(str(self.atoms_index[i]))

        ###############################################
        # atoms_index の通し番号版
        #    atoms_index_j[i]  : 通し番号(max=natom)を与えると、原子種の元素記号を返す

        # 2022/03/11 メモリ消費量が多く使ってないルーチンなので、disable する
        # print('makes atoms_index_j[i]')
        # self.atoms_index_j = []
        # if self.vasp_version == 5:
        #     for k in range(self.nion):
        #         for l in range(int(self.atoms[k])):
        #             self.atoms_index_j.append(str(self.atoms_index[k]))

        ###############################################
        # atoms_index_j に併せて記号ではなく原子番号で保存しておく配列を用意
        # 2022/03/11 メモリ消費量が多く使ってないルーチンなので、disable する

        # print('makes atoms_number_j[]')
        # self.atoms_number_j = []
        # if self.vasp_version == 5:
        #     for k in range(self.nion):
        #         for l in range(int(self.atoms[k])):
        #             num0 = SAEnv.get_atomic_number1(str(self.atoms_index[k]))
        #             self.atoms_number_j.append(num0)

        ###############################################
        # 全原子数の確認
        print('Confirmation of the total number of atoms')
        self.natom = 0
        for j in range(self.nion):
            sum = int(self.atoms[j])
            self.natom = self.natom + sum

        print('Total Number of atoms')
        print(self.natom)

        ###############################################
        # get ion (makes index)
        # ion[j] : 通し番号(max=natom)を与えると原子の種類番号を返す
        #
        if not reduced_memory:
            print('Create ion[j]')
            self.ion = np.zeros(self.natom, dtype=int)
            tmp = -1
            for j in range(self.nion):
                local = -1
                for k in range(int(self.atoms[j])):
                    tmp += 1
                    local += 1
                    self.ion[tmp] = int(j)
                # print tmp, int(ion[tmp])

        ###############################################
        # ion_local[j]  : 通し番号(max=natom)を与えるとサイト内のローカル通し番号を返す
        #
        if not reduced_memory:
            print('Create ion_local[j]')
            self.ion = np.zeros(self.natom, dtype=int)
            self.ion_local = np.zeros(self.natom, dtype=int)
            tmp = -1
            for j in range(self.nion):
                local = -1
                for k in range(int(self.atoms[j])):
                    tmp += 1
                    local += 1
                    self.ion_local[tmp] = int(local)
                # print tmp, int(ion[tmp]), int(ion_local[tmp])

        ###############################################
        # natom までの通し番号で原子種を返す(元素記号ではなくて原子の種類番号)
        #                               <---> atoms_index_j() は元素記号を返す
        # ReadOutcar.py, ReadMxDatMethod.py 互換
        #

        # 通常使ってないので停止しても問題は無い
        # 2022/03/11 メモリ消費量が多く使ってないルーチンなので、disable する

        # print('Create atoms_j[j]')
        # self.atoms_j = np.zeros(self.natom, dtype=int)
        # j = 0
        # for ion in range(self.nion):
        #     for atom in range(self.atoms[ion]):
        #         self.atoms_j[j] = int(ion)
        #         j += 1

        ###############################################
        # get atomc coordinate mode
        #
        if self.vasp_version == 4:
            i = 5 + 1
        else:
            i = 6 + 1

        num_reg = re.compile('^[+-]?(\d*\.\d+|\d+\.?\d*)([eE][+-]?\d+|)\Z')
        selective_reg = re.compile('^S.*', re.IGNORECASE)

        if bool(num_reg.match(self.datlines[i].split()[0])):
            print("%s" % str(self.datlines[i].split()[0]))
            sys.exit("Format Error")
        else:
            if bool(selective_reg.match(self.datlines[i].split()[0])):
                self.selective = True
            else:
                self.selective = False

        ###############################################
        # 内部座標のモードを取得
        #
        if self.vasp_version == 4:
            i = 5 + 1
        else:
            i = 6 + 1
        if self.selective: i += 1

        direct_reg = re.compile('^D.*', re.IGNORECASE)
        car_reg = re.compile('^C.*', re.IGNORECASE)

        if bool(num_reg.match(self.datlines[i].split()[0])):
            print("%s" % str(self.datlines[i].split()[0]))
            sys.exit("Format Error")
        if bool(direct_reg.match(self.datlines[i].split()[0])):
            self.direct = True
        elif bool(car_reg.match(self.datlines[i].split()[0])):
            self.direct = False

        # 個々まででヘッダ情報（位置情報を除く）を取り出す

    def get_poscar_info(self):
        """
        POSCAR 情報の取り出し
        リストなので順番維持

        return [title, scale, t, vasp, nion, atoms, atoms_index, natom, selective, direct, position, fix]:
        """
        title = self.get_title()
        scale = self.get_scale()
        t = self.get_t()
        vasp = self.get_vasp_version()
        nion = self.get_nion()
        atoms = self.get_atoms()
        atoms_index = self.get_atoms_index()
        natom = self.get_natom()
        selective = self.get_selective()
        direct = self.get_direct()
        # position = self.get_position()
        # fix = self.get_fix()
        # return [title, scale, t, vasp, nion, atoms, atoms_index, natom, selective, direct, position, fix]
        return [title, scale, t, vasp, nion, atoms, atoms_index, natom, selective, direct]

    @property
    def poscar_info(self):
        """ POSCAR 情報の取り出し
        """
        return self.get_poscar_info()


if __name__ == '__main__':
    import optparse

    name = 'POSCAR'
    # name = 'BvAt2026.dat'

    # Header 部分の取り出し
    print(name)
    chgcar = ReadVaspChgcarHeader(name)
    print(chgcar.title)
    print(chgcar.scale)
    print(chgcar.t)
    print(chgcar.vasp_version)
    print(chgcar.nion)
    print(chgcar.atoms)
    print(chgcar.atoms_index)
    print(chgcar.natom)
    print(chgcar.selective)
    print(chgcar.direct)
    print(chgcar.get_poscar_info())
