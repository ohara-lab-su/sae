#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
################################################################################
# CHGCAR/ELFCAR 読み込み class
#
# 先頭部分は POSCAR と同じなので以下は同じ
#
# t[3,3]            :  基本並進ベクトル(注意:配列内indexは0から)
#
#                              x   y   z
#                        t1 = a11 a21 a31  ! lattice vector t1
#                        t2 = a12 a22 a32  ! lattice vector t2
#                        t3 = a13 a23 a33  ! lattice vector t3
# 注意)
#    t(基本並進行列)
#                             t11, t12, t13
#                             t21, t22, t23
#                             t31, t32, t33
#
# atoms[i]          : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
# atoms_index[i]    : 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
# atoms_index_j[i]  : 通し番号(max=natom)を与えると、原子種の元素記号を返す
# ion[j]            : 通し番号(max=natom)を与えると原子の種類番号を返す
# ion_local[j]      : 通し番号(max=natom)を与えるとサイト内のローカル通し番号を返す
#
# position[j,3]     : 通し番号(max=natom)とx,y,z 指定で内部座標
# fix[j,3]          : 通し番号(max=natom)とx,y,z 指定でForceのFix/non-Fix 指定
#
# title             : タイトル
# scale             : 格子定数(スケールファクター)
# selective         : selective mode
# direct            : direct or cartesian
#
################################################################################
# 2018.08.18 新インスタンス変数
#
# t1_len         : 格子定数a
# t2_len         : 格子定数b
# t3_len         : 格子定数c
#
# 2018.08.18 新Method
#
# get_lattice_a()
# get_lattice_b()
# get_lattice_c()
#
# get_t1_len()
# get_t2_len()
# get_t3_len()
#
################################################################################
#
# 1) 基本構造情報読み込み Method : get_*()
#
# 2) 並進ベクトル回転Method
#     conv_rot_euler(self,alpha,beta,gamma)
#
# 3) POSCAR print method
#     print_poscar()
#
# 4) conv Direct --> Cartesian
#     conv_direct2car()
#
# 5) makes SuperCell method
#     conv_supercell()
#
################################################################################
#
# 2022.03.13:
#   メモリ消費が多くて実質使ってないルーチンを止
#
# 2018.08.17
#  startup
#
################################################################################
################################################################################
# import gzip
# sys.path.append('../..')
# スーパーセルに関していくつかルーチンを殺す。メモリ消費を少なくするため。
# reduced_memory = True
# import SpaceGroupEnvironment as SGE
# from numba import jit
# super の通し番号を与えると元cellの通し番号を与える)
################################################################################
# name = 'POSCAR'
# 反転した CHGCAR を作る
#   poscar = ReadVaspChgcar(name)
#   poscar.print_chgcar(outname='ELFCAR_NEW') # 読み込んだメモリ上の内容をそのまま書き出す(for TEST)
#   poscar.init_ave_elf()  # ELF 積算のための準備
#   print('================================================= 1.0')
#   newchg = poscar.sphere_integral_elf(r_diff=1.0)  # 半径 1.0A にて積算サーチ
#   poscar.print_chgcar(chgcar=newchg, outname='ELFCAR_NEW_1.0') # 読み込んだメモリ上の内容をそのまま書き出す(for TEST)
#   print('================================================= 1.5')
#   newchg = poscar.sphere_integral_elf(r_diff=1.5)  # 半径 1.5A にて積算サーチ
#   poscar.print_chgcar(chgcar=newchg, outname='ELFCAR_NEW_1.5') # 読み込んだメモリ上の内容をそのまま書き出す(for TEST)
#   print('================================================= 2.0')
#   newchg = poscar.sphere_integral_elf(r_diff=2.0)  # 半径 1.5A にて積算サーチ
#   poscar.print_chgcar(chgcar=newchg, outname='ELFCAR_NEW_2.0') # 読み込んだメモリ上の内容をそのまま書き出す(for TEST)
#   print('================================================= 0.5')
#   newchg = poscar.sphere_integral_elf(r_diff=0.5)  # 半径 1.5A にて積算サーチ
#   poscar.print_chgcar(chgcar=newchg, outname='ELFCAR_NEW_0.5') # 読み込んだメモリ上の内容をそのまま書き出す(for TEST)
#   poscar.print_super_chgcar(outname='ELFCAR_NEW')    # 積算結果をVASP形式にて(FFT-mesh上)保存
##     title = poscar.get_title()
##     scale = poscar.get_scale()
##     t = poscar.get_t()
##     vasp = poscar.get_vasp_version()
##     nion = poscar.get_nion()
##     atoms = poscar.get_atoms()
##     atoms_index = poscar.get_atoms_index()
##     natom = poscar.get_natom()
##     selective = poscar.get_selective()
##     direct = poscar.get_direct()
##     position = poscar.get_position()
##     fix = poscar.get_fix()
##
##     ion = poscar.get_ion()
##     ion_local = poscar.get_ion_local()
##     atoms_index_j = poscar.get_atoms_index_j()
##
## #   for i in range(natom):
## #       print i, atoms_index_j[i]
##
##     ############################################################################
##     out = sys.stdout
##
##     print("%s" % str(title), file=out)
##     print(" %s" % str(scale), file=out)
##     print("  %13.9f %13.9f %13.9f" %(t[0,0],t[1,0],t[2,0]), file=out)
##     print("  %13.9f %13.9f %13.9f" %(t[0,1],t[1,1],t[2,1]), file=out)
##     print("  %13.9f %13.9f %13.9f" %(t[0,2],t[1,2],t[2,2]), file=out)
##
##     if vasp >= 5:
##         print(" ", file=out, end="")
##         for i in range(nion):
##             print("%s " % str(atoms_index[i]), file=out, end="")
##         print(" ", file=out)
##
##     print(" ", file=out, end="")
##     for i in range(nion):
##         print("%s " % str(atoms[i]), file=out, end="")
##     print(" ", file=out)
##
##     if selective:
##         print("Selective Dynamics", file=out)
##     if direct:
##         print("Direct", file=out)
##     else:
##         print("Cartesian", file=out)
##
##     for j in range(natom):
##         print(" %13.9f %13.9f %13.9f"
##                 %(position[j,0], position[j,1], position[j,2]), file=out, end="")
##         if selective:
##             print("", file=out, end="")
##             print("%s %s %s" % (str(fix[j,0]), str(fix[i,1]), str(fix[i,2])), file=out, end="")
##         print("", file=out)
##     ############################################################################
##
## #   print ion
#   print ion_local
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.structure.base import Method
import sys
import os
import re
import multiprocessing
import math
import numpy as np

try:
    Method = Method
except ImportError:
    Method = Method
reduced_memory = False


#   @jit
# @jit
############################################################################
# direct to cartesian method
class ReadVaspChgcar(Method):

    def __init__(
        self, CHGCAR="CHGCAR", suffix=".vasp", sort=False, atoms_index=None, logger=None
    ):
        """init and Read CHGCAR

        :param CHGCAR: 読み込みファイルの名前
        :param suffix: 実はこれは使ってない(2022/05/14)
        :param sort:
        :param atoms_index:
        """
        if logger is None:
            logger = multiprocessing.get_logger()
        self.__logger = logger
        self.open(CHGCAR=CHGCAR, suffix=suffix, sort=sort, atoms_index=sort)

    @property
    # self.__logger.debug("Ngxc = %s" % self.__ngxc)
    def ngxc(self):
        return self.__ngxc

    @property
    # self.__logger.debug("Ngyz = %s" % self.__ngyz)
    def ngyz(self):
        return self.__ngyz

    @property
    # self.__logger.debug("Ngzc = %s" % self.__ngzc)
    def ngzc(self):
        return self.__ngzc

    @property
    def chgdata(self):
        """チャージ情報を取り出す(numpy)"""
        return self.__chgdata

    @property
    def poscar_info(self):
        """POSCAR 情報の取り出し"""
        return self.get_poscar_info()

    ###############################################
    # Read Translation Vector
    #         x   y   z
    #   t1 = t11 t21 t31
    #   t2 = t12 t22 t32
    #   t3 = t13 t23 t33
    #
    ###############################################
    # 単位胞の長さの計算
    #
    # print("lattice a = %s " % str(self.t1_len))
    # print("lattice b = %s " % str(self.t2_len))
    # print("lattice c = %s " % str(self.t3_len))
    ###############################################
    # VASP のバージョン番号確認(記号があるか否か)
    #
    ###############################################
    # atoms[i]  : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
    # atoms_index[i] : 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
    #
    ###############################################
    # atoms_number[i]
    #   atoms_index の原子番号版
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
    ###############################################
    # get ion (makes index)
    # ion[j] : 通し番号(max=natom)を与えると原子の種類番号を返す
    #
    # print tmp, int(ion[tmp])
    ###############################################
    # ion_local[j]  : 通し番号(max=natom)を与えるとサイト内のローカル通し番号を返す
    #
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
    ###############################################
    # 内部座標のモードを取得
    #
    ###############################################
    # get atomic coordinate position
    #
    # self.position = np.zeros((int(self.natom), 3), dtype='float32')
    # print j,
    # print " %16.12f %16.12f %16.12f" \
    #        %(self.position[j,0],self.position[j,1],self.position[j,2]),
    # print ""
    def open(self, CHGCAR="CHGCAR", suffix=".vasp", sort=False, atoms_index=None):
        from sae.common.text import TextFiles
        from sae.structure.elements import ElementTable

        self.datlines, self.num = TextFiles().read_dataline(CHGCAR)
        self.system = self.datlines[0]
        self.title = self.system
        self.scale = float(self.datlines[1])
        self.__logger.debug("--- Read STRUCTURE DATA")
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
        self.t1_len = math.sqrt(t1_x * t1_x + t1_y * t1_y + t1_z * t1_z)
        self.t2_len = math.sqrt(t2_x * t2_x + t2_y * t2_y + t2_z * t2_z)
        self.t3_len = math.sqrt(t3_x * t3_x + t3_y * t3_y + t3_z * t3_z)
        i = 5
        self.vasp_version = 5
        atoms = self.datlines[i].split()
        # 数字ならば
        if atoms[0].isdigit():
            self.vasp_version = 4
        del atoms
        self.__logger.debug("    vasp version = %s" % self.vasp_version)
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
        self.atoms_number = np.zeros(self.nion, dtype=int)
        for i in range(self.nion):
            self.__logger.debug("atoms_index[%d] = %s" % (i, self.atoms_index[i]))
            self.atoms_number[i] = ElementTable().get_atomic_number1(
                str(self.atoms_index[i])
            )
        print("Confirmation of the total number of atoms")
        self.natom = 0
        for j in range(self.nion):
            sum = int(self.atoms[j])
            self.natom = self.natom + sum
        if not reduced_memory:
            print("Create ion[j]")
            self.ion = np.zeros(self.natom, dtype=int)
            tmp = -1
            for j in range(self.nion):
                local = -1
                for k in range(int(self.atoms[j])):
                    tmp += 1
                    local += 1
                    self.ion[tmp] = int(j)
        if not reduced_memory:
            print("Create ion_local[j]")
            self.ion = np.zeros(self.natom, dtype=int)
            self.ion_local = np.zeros(self.natom, dtype=int)
            tmp = -1
            for j in range(self.nion):
                local = -1
                for k in range(int(self.atoms[j])):
                    tmp += 1
                    local += 1
                    self.ion_local[tmp] = int(local)
        if self.vasp_version == 4:
            i = 5 + 1
        else:
            i = 6 + 1
        num_reg = re.compile("^[+-]?(\\d*\\.\\d+|\\d+\\.?\\d*)([eE][+-]?\\d+|)\\Z")
        selective_reg = re.compile("^S.*", re.IGNORECASE)
        if bool(num_reg.match(self.datlines[i].split()[0])):
            print("%s" % str(self.datlines[i].split()[0]))
            sys.exit("Format Error")
        elif bool(selective_reg.match(self.datlines[i].split()[0])):
            self.selective = True
        else:
            self.selective = False
        if self.vasp_version == 4:
            i = 5 + 1
        else:
            i = 6 + 1
        if self.selective:
            i += 1
        direct_reg = re.compile("^D.*", re.IGNORECASE)
        car_reg = re.compile("^C.*", re.IGNORECASE)
        if bool(num_reg.match(self.datlines[i].split()[0])):
            print("%s" % str(self.datlines[i].split()[0]))
            sys.exit("Format Error")
        if bool(direct_reg.match(self.datlines[i].split()[0])):
            self.direct = True
        elif bool(car_reg.match(self.datlines[i].split()[0])):
            self.direct = False
        print("get atomic coordinate position")
        if self.vasp_version == 4:
            i = 5
        else:
            i = 6
        if self.selective:
            i += 1
        print("natom = %d" % self.natom)
        print("init: position")
        self.position = np.zeros((int(self.natom), 3))
        print("init: fix")
        self.fix = np.zeros((int(self.natom), 3), dtype="S")
        i += 2
        current_datlines = i
        for j in range(self.natom):
            print("%s" % j)
            self.position[j, 0] = float(self.datlines[i + j].split()[0])
            self.position[j, 1] = float(self.datlines[i + j].split()[1])
            self.position[j, 2] = float(self.datlines[i + j].split()[2])
            if self.selective:
                if len(self.datlines[i + j].split()) < 6:
                    sys.exit("STOP: corrdinate line Format Error")
                self.fix[j, 0] = str(self.datlines[i + j].split()[3])
                self.fix[j, 1] = str(self.datlines[i + j].split()[4])
                self.fix[j, 2] = str(self.datlines[i + j].split()[5])
            current_datlines = i + j
        self.__logger.debug("--- END (readline = %s)" % current_datlines)
        self.read_mesh_data(startline=current_datlines + 2)

    # print(current_datlines)
    # print(self.datlines[current_datlines+2])
    ####################
    # FFT Mesh の読み込み
    #
    ####################
    # FFT-Mesh 一つあたりの長さ(インスタンス変数の定義)
    #
    # print(self.rate_x)
    # print(self.rate_y)
    # print(self.rate_z)
    ####################
    # 総Mesh数および読み込むべき総ライン数の算出 (一行に10個のデータがある)
    #
    # self.__logger.debug("Ngxc = %s" % self.__ngxc)
    # self.__logger.debug("Ngyz = %s" % self.__ngyz)
    # self.__logger.debug("Ngzc = %s" % self.__ngzc)
    # CHACAR 形式のメッシュデータの読み込み開始行のセット
    ####################
    # アホループ(numpyのmethodを使うと一行で高速に書けるので注意) START
    # 行を全部 join
    # chglist += ''.join(self.datlines[start_mesh_index + i])
    # join後のデーターを split して LIST化
    # 一行足りないケースがあるのでその場合は追加する
    # 読み取りの確認
    # 最終データーの確認
    # ( python だと 0 から index start なので -1 するのを忘れない)
    # print(chgarray[mesh_max-1])
    # 元の Matrix は 1 から始まるので注意
    # WRITE(IU, FORM)(((C(NX, NY, NZ), NX=1, NGXC), NY=1, NGYZ), NZ=1, NGZC)
    #       # CHGCAR 形式でのデータ吐き出しテスト
    #       print("write VASP style CHGCAR files: plase waite...")
    #       ngx_max = self.__ngxc
    #       ngy_max = self.__ngyz
    #       ngz_max = self.__ngzc
    #       inner_counter = 0
    #       for nx in range(0, ngx_max):
    #           for ny in range(0, ngy_max):
    #               for nz in range(0, ngz_max):
    #                   inner_counter += 1
    #                   if self.__chgdata[nx, ny, nz] >= 0.001:
    #                       print("{:<12.5f}".format(self.__chgdata[nx, ny, nz]), end="")
    #                      #print("%11.5f " % self.__chgdata[nx, ny, nz], end="")
    #                   else:
    #                      print("{:<12.5e}".format(self.__chgdata[nx, ny, nz]), end="")
    #                      #print("%12.5e " % self.__chgdata[nx, ny, nz], end="")
    #                   if inner_counter >= 10:
    #                       inner_counter = 0
    #                       print("")
    def read_mesh_data(self, startline=None, mode="CHGCAR"):
        """
        電荷密度構造 の読み込み (2018.08.18)
        VASP マニュアルより下記
        WRITE(IU, FORM)(((C(NX, NY, NZ), NX=1, NGXC), NY=1, NGYZ), NZ=1, NGZC)

        self.__chgdata = np.zeros((self.__ngxc, self.__ngyz, self.__ngzc))

        :param startline:
        :param mode:
        :return:
        """
        self.__logger.debug("--- Read MESH DATA and Makes CELL INDEX")
        if startline is None:
            return
        self.__ngxc = int(self.datlines[startline].split()[0])
        self.__ngyz = int(self.datlines[startline].split()[1])
        self.__ngzc = int(self.datlines[startline].split()[2])
        self.__logger.debug(
            "READ MeshDATA: NGXC=%d, NGYZ=%d, HGZC=%d"
            % (self.__ngxc, self.__ngyz, self.__ngzc)
        )
        self.rate_x = self.t1_len / self.__ngxc
        self.rate_y = self.t2_len / self.__ngyz
        self.rate_z = self.t3_len / self.__ngzc
        mesh_max = self.__ngxc * self.__ngyz * self.__ngzc
        self.__logger.debug("mesh_max = %s" % mesh_max)
        self.__logger.debug("mode     = %s" % mode)
        if mode == "CHGCAR":
            mesh_max_line = int(mesh_max / 5)
        elif mode == "ELFCAR":
            mesh_max_line = int(mesh_max / 10)
        else:
            self.__logger.error("Error")
            return
        start_mesh_index = startline + 1
        self.__chgdata = np.zeros((self.__ngxc, self.__ngyz, self.__ngzc))
        chglist = ""
        # print(tmp_)
        for i in range(mesh_max_line):
            tmp_ = self.datlines[start_mesh_index + i]
            chglist += "".join(tmp_)
        chgarray = chglist.split()
        if len(chgarray) != mesh_max:
            self.__logger.debug("added to read line")
            chglist += "".join(self.datlines[start_mesh_index + i + 1])
            chgarray = chglist.split()
        self.__logger.debug("num. CHG array = %s" % len(chgarray))
        if len(chgarray) != mesh_max:
            print(tmp_)
            print("read error")
        i = 0
        for nx in range(0, self.__ngxc):
            for ny in range(0, self.__ngyz):
                # print(self.__chgdata[nx,ny,nz], chgarray[i])
                for nz in range(0, self.__ngzc):
                    self.__chgdata[nx, ny, nz] = float(chgarray[i])
                    i += 1
        self.__logger.debug("--- END: read_mesh_data()")
        self.__logger.debug("")

    # title = self.get_title()
    # scale = self.get_scale()
    def get_poscar_info(self):
        """POSCAR 情報の取り出し
        リストなので順番維持
        return [title, scale, t, vasp, nion, atoms, atoms_index, natom, selective, direct, position, fix]:
        """
        title = self.title
        scale = self.scale
        t = self.get_t()
        vasp = self.get_vasp_version()
        nion = self.get_nion()
        atoms = self.get_atoms()
        atoms_index = self.get_atoms_index()
        natom = self.get_natom()
        selective = self.get_selective()
        direct = self.get_direct()
        position = self.get_position()
        fix = self.get_fix()
        return [
            title,
            scale,
            t,
            vasp,
            nion,
            atoms,
            atoms_index,
            natom,
            selective,
            direct,
            position,
            fix,
        ]

    #
    # (test) 電荷密度をスーパーセル化する 3x3x3
    # 2018.08.18 12:36 正しく計算されるのを確認
    #
    # 3x3 の super-cell を作った場合の原点 shift
    #
    # 基本セル情報 chgdata[nx,ny,nz] のループを new-cell 内で行う
    #######################################################################
    # ある原点からのある半径内での ELF の平均値 (単独テスト用)
    #  原点 0,0,0 mesh 上を中心とした積算
    #
    #  super-cell さえ作れば計算可能
    #
    # base となる(中心となる) cell = [ nx + sx[2], ny + sy[2], nz + sz[2])
    # ある cell の中心 nx=0, ny=0, nz=0 からある半径 r 内の mesh ポイントを探す
    #
    # 1. 原点と cell 内 mesh 点の差をとする
    #    その際、mesh-mesh の distance を実長さ換算する
    # 2. super_cell と 原点の差を全て探す(mesh-dataのみ)
    #
    #######################################################################
    #       print("search ...")
    #       org = [0 + sx[2], 0 + sy[2], 0 + sz[2]]
    #       r_diff = 2.0 # Angstrom
    #       elf_sum = 0
    #       v = 4.0/3.0*math.pi*r_diff**3 # Volume /A^3
    #       for nx in range(0, self.__ngxc*3):
    #           for ny in range(0, self.__ngyz*3):
    #               for nz in range(0, self.ngzc*3):
    #                   # 二点間の距離
    #                   r = (((org[0] - nx)*self.rate_x)**2
    #                      + ((org[1] - ny)*self.rate_y)**2
    #                      + ((org[2] - nz)*self.rate_z)**2)
    #                   if r < r_diff:
    #                       elf_sum += self.chgdata_s[nx, ny, nz]
    #                       print(nx, ny, nz, self.chgdata_s[nx, ny, nz])
    #       # 体積中のELFの平均値(ELF/A^3)
    #       ave_elf = elf_sum/v
    #       print("Volume         %f" % v)
    #       print("sum elf        %f" % elf_sum)
    #       print("sum elf/Volume %f" % ave_elf)
    def init_ave_elf(self):
        """
        ELF 積算解析（ある原点を中心としたELFの球積分値の解析)用のために
        chgcar/elfcar のデータを 3x3x3 の super-cell とする

        self.__chgdata[nx, ny, nz] にて chg/elf が読み込まれている必要がある

        :return: chgdata_s[nx, ny, nz]: 3x3x3 スーパーセル化した chgdata のマトリックス
        """
        self.chgdata_s = np.zeros((self.__ngxc * 3, self.__ngyz * 3, self.__ngzc * 3))
        # supre-cell 用の Meth 原点
        sx = [0, self.__ngxc, self.__ngxc * 2]
        sy = [0, self.__ngyz, self.__ngyz * 2]
        sz = [0, self.__ngzc, self.__ngzc * 2]
        self.__logger.debug("makes chgcar super-cell: plase waite...")
        for nx in range(0, self.__ngxc):
            for ny in range(0, self.__ngyz):
                for nz in range(0, self.__ngzc):
                    s = self.__chgdata[nx, ny, nz]
                    for i in range(3):
                        for j in range(3):
                            for k in range(3):
                                self.chgdata_s[nx + sx[i], ny + sy[j], nz + sz[k]] = s
        return self.chgdata_s

    def sphere_integral_elf(self, r_diff=1.0):
        """
        ある原点からのある半径内での ELF の平均値

        事前に chg/elf の 3x3x3 スーパーセルを作っておく必要がある
        self.chgdata_s[nx, ny, nz]
        self.__ngxc
        self.__ngyz
        self.__ngzc
        self.rate_x
        self.rate_y
        self.rate_z

        :param r_diff: 半径
        :return: self.ave_elf[nx, ny, nz]: CHGCAR 形式(FFT-MESHパートのみ)のマトリックス
        """
        from sae.vasp.elf import ElfIntegration

        self.ave_elf = ElfIntegration().sphere_integral_of_elf(
            self.chgdata_s,
            self.__ngxc,
            self.__ngyz,
            self.__ngzc,
            self.rate_x,
            self.rate_y,
            self.rate_z,
            r_diff=r_diff,
        )
        return self.ave_elf

    def inverse_chgcar_OLD(self, chgcar=None):
        """
        入力の CHGCAR を各要素毎に 1/CHGCAR して結果を 新しい CHGCAR を返す
        :param chgcar:
        :return:
        """
        if chgcar is None:
            chgcar = self.__chgdata
        return 1 / chgcar

    def inverse_chgcar(self, chgcar=None, offset=None):
        """
        入力の CHGCAR を各要素毎に -1 を掛けて, 最小の CHAEGE(元データで言うところの最大値) を足して
        ゼロとするオフセット処理をして CHGCAR を返す
        :param chgcar:
        :return:
        """
        if chgcar is None:
            if offset is None:
                chgcar = self.__chgdata * -1
            else:
                chgcar = self.__chgdata * -1 + offset
        return chgcar

    def get_chgcar(self, chgcar=None):
        if chgcar is None:
            chgcar = self.__chgdata
        return chgcar

    # 元のPOSCAR情報を取得
    # POSCAR 相当情報の書き込み
    #
    # WRITE CHGCAR/ELFCAR DATA
    def print_chgcar(
        self, chgcar=None, ngx_max=None, ngy_max=None, ngz_max=None, outname=None
    ):
        """
        CHGCAR 形式での出力

        in: 元のPOSCAR情報すべて
        in: self.__ngxc
        in: self.__ngyz
        in: self.__ngzc

        :param: ngx: FFT-mesh, None のときは読み込んだ CHGCAR の mesh そのまま
        :param: ngy: FFT-mesh, None のときは読み込んだ CHGCAR の mesh そのまま
        :param: ngz: FFT-mesh, None のときは読み込んだ CHGCAR の mesh そのまま
        :param: chgcar: chgdata[x,y,z]: FFT-MESH のchgdata
        :param: filename: ファイル名を入れたらファイル書き出し
        """
        if chgcar is None:
            chgcar = self.__chgdata
        if ngx_max is None:
            ngx = self.__ngxc
        if ngy_max is None:
            ngy_max = self.__ngyz
        if ngz_max is None:
            ngz_max = self.__ngzc
        if outname is not None:
            try:
                out = open(outname, "w")
            except:
                sys.exit("STOP: %s can't open." % outname)
        else:
            out = sys.stdout
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
        position = self.get_position()
        fix = self.get_fix()
        ion = self.get_ion()
        ion_local = self.get_ion_local()
        atoms_index_j = self.get_atoms_index_j()
        print("%s" % str(title), file=out)
        print("  %13.9f" % scale, file=out)
        print("  %13.9f %13.9f %13.9f" % (t[0, 0], t[1, 0], t[2, 0]), file=out)
        print("  %13.9f %13.9f %13.9f" % (t[0, 1], t[1, 1], t[2, 1]), file=out)
        print("  %13.9f %13.9f %13.9f" % (t[0, 2], t[1, 2], t[2, 2]), file=out)
        if vasp >= 5:
            print(" ", file=out, end="")
            for i in range(nion):
                print("%s " % str(atoms_index[i]), file=out, end="")
            print(" ", file=out)
        print(" ", file=out, end="")
        for i in range(nion):
            print("%s " % str(atoms[i]), file=out, end="")
        print(" ", file=out)
        if selective:
            print("Selective Dynamics", file=out)
        if direct:
            print("Direct", file=out)
        else:
            print("Cartesian", file=out)
        for j in range(natom):
            print(
                " %13.9f %13.9f %13.9f"
                % (position[j, 0], position[j, 1], position[j, 2]),
                file=out,
                end="",
            )
            if selective:
                print("", file=out, end="")
                print(
                    "%s %s %s" % (str(fix[j, 0]), str(fix[i, 1]), str(fix[i, 2])),
                    file=out,
                    end="",
                )
            print("", file=out)
        print(
            "write VASP style (new) %s files: plase wait..." % outname, file=sys.stdout
        )
        ngx_max = self.__ngxc * 1
        ngy_max = self.__ngyz * 1
        ngz_max = self.__ngzc * 1
        inner_counter = 0
        print("", file=out)
        print("%d %d %d" % (ngx_max, ngy_max, ngz_max), file=out)
        for nx in range(0, ngx_max):
            for ny in range(0, ngy_max):
                for nz in range(0, ngz_max):
                    inner_counter += 1
                    if chgcar[nx, ny, nz] < 0.001:
                        print("{:<12.5e}".format(chgcar[nx, ny, nz]), file=out, end="")
                    # print("%11.5f " % self.__chgdata[nx, ny, nz], end="")
                    elif 0.001 <= chgcar[nx, ny, nz] < 10:
                        print("{:<12.5f}".format(chgcar[nx, ny, nz]), file=out, end="")
                    # print("%12.5e " % self.__chgdata[nx, ny, nz], end="")
                    elif chgcar[nx, ny, nz] >= 10.0:
                        print("{:<12.5e}".format(chgcar[nx, ny, nz]), file=out, end="")
                    else:
                        print("{:<12.5e}".format(chgcar[nx, ny, nz]), file=out, end="")
                    if inner_counter >= 10:
                        inner_counter = 0
                        print("", file=out)
        out.close()

    def print_ave_elfcar(self, outname=None):
        """
        ラッパー関数
        self.ave_elf[nx,ny,nz]: ELF を あるFFT-MESH上で積算した値をその FFT-MESH のマップとして保存したもの
                                CHGCAR と同じ形式

        :param outname:
        :return:
        """
        self.print_chgcar(
            self.ave_elf,
            ngx_max=self.__ngxc,
            ngy_max=self.__ngyz,
            ngz_max=self.__ngzc,
            outname=outname,
        )

    #
    # (test) CHGCAR 形式でのデータ吐き出しテスト type 1 (super)
    # 2018.08.18 12:36 正しく出力されるのを確認
    #
    def print_super_chgcar(self, x_times=3, y_times=3, z_times=3, outname=None):
        """
        (test) 3x3x3 スーパーセルとして作成した CHGCAR mesh を CHGCAR 形式で出力する

        in: self.__ngxc
        in: self.__ngyz
        in: self.__ngzc

        in: self.chgdata_s[x,y,z]: スーパーセル FFT-MESH data
        :param: filename: ファイル名を入れたらファイル書き出し(CHGパートのみ)
        """
        if outname is not None:
            try:
                out = open(outname, "w")
            except:
                sys.exit("STOP: %s can't open." % outname)
        else:
            out = sys.stdout
        self.__logger.debug(
            "write VASP style (new) %s files: plase wait..." % outname, file=sys.stdout
        )
        ngx_max = self.__ngxc * x_times
        ngy_max = self.__ngyz * y_times
        ngz_max = self.__ngzc * z_times
        inner_counter = 0
        print("", file=out)
        print("", file=out)
        print("%d %d %d" % (ngx_max, ngy_max, ngz_max), file=out)
        for nx in range(0, ngx_max):
            for ny in range(0, ngy_max):
                # print("%12.5e " % self.chgdata[nx, ny, nz], end="")
                for nz in range(0, ngz_max):
                    inner_counter += 1
                    # print("%11.5f " % self.chgdata[nx, ny, nz], end="")
                    if self.chgdata_s[nx, ny, nz] >= 0.001:
                        print(
                            "{:<12.5f}".format(self.chgdata_s[nx, ny, nz]),
                            file=out,
                            end="",
                        )
                    else:
                        print(
                            "{:<12.5e}".format(self.chgdata_s[nx, ny, nz]),
                            file=out,
                            end="",
                        )
                    if inner_counter >= 10:
                        inner_counter = 0
                        print("", file=out)
        out.close()

    # 基本並進ベクトルの変換
    # print "t"
    # print t
    # print ""
    # t1 = np.matrix( [ t[0,0],t[1,0],t[2,0] ] )
    # print " t1r = %14.8f %14.8f %14.8f" % (t1r[0,0],t1r[0,1],t1r[0,2])
    # t2 = np.matrix( [ t[0,1],t[1,1],t[2,1] ] )
    # print " t2r = %14.8f %14.8f %14.8f" % (t2r[0,0],t2r[0,1],t2r[0,2])
    # t3 = np.matrix( [ t[0,2],t[1,2],t[2,2] ] )
    # print " t3r = %14.8f %14.8f %14.8f" % (t3r[0,0],t3r[0,1],t3r[0,2])
    # print ""
    # オイラー角で基本並進ベクトルを回したときの基本並進ベクトル
    #       R_t = np.matrix([
    #               [ t1r[0,0],t2r[0,0],t3r[0,0] ],
    #               [ t1r[0,1],t2r[0,1],t3r[0,1] ],
    #               [ t1r[0,2],t2r[0,2],t3r[0,2] ]
    #               ])
    # print "R_t"
    # print R_t
    # 内部座標の変換
    def conv_rot_euler(self, alpha, beta, gamma):
        """
        基本並進ベクトルを、alpha, beta, gamma で回す
        VASP 表記とは転置した形で t ベクトルに入っているの注意
        注意) むしろ VASP 表記が転置している
        ここでは転置したまま,正しい基本並進ベクトルのまま処理をする
        :param alpha:
        :param beta:
        :param gamma:
        :return:
        """
        from sae.geometry.rotation import Rotations

        R = Rotations().rotate_euler(alpha, beta, gamma)
        t = self.get_t()
        t1 = np.matrix([t[0, 0], t[0, 1], t[0, 2]])
        t1r = t1 * R
        t2 = np.matrix([t[1, 0], t[1, 1], t[1, 2]])
        t2r = t2 * R
        t3 = np.matrix([t[2, 0], t[2, 1], t[2, 2]])
        t3r = t3 * R
        R_t = np.matrix(
            [
                [t1r[0, 0], t1r[0, 1], t1r[0, 2]],
                [t2r[0, 0], t2r[0, 1], t2r[0, 2]],
                [t3r[0, 0], t3r[0, 1], t3r[0, 2]],
            ]
        )
        position = self.get_position()
        natom = self.get_natom()
        R_position = np.zeros((natom, 3))
        for j in range(natom):
            p = np.matrix([position[j, 0], position[j, 1], position[j, 2]])
            pr = p * R
            R_position[j, 0] = pr[0, 0]
            R_position[j, 1] = pr[0, 1]
            R_position[j, 2] = pr[0, 2]
        return (R_t, R_position)

    def conv_direct2car(self, ABS=None):
        from sae.geometry.coordinates import CoordinateTransforms

        if ABS is not None:
            ABS = False
        elif isinstance(ABS, str):
            if ABS == "vasp" or ABS == "VASP":
                ABS = True
        self.scale, self.direct = CoordinateTransforms().conv_direct2cara(
            ABS, self.scale, self.t, self.natom, self.direct, self.position
        )

    def print_poscar(self, outname="POSCAR", STD=True):
        """
        POSCAR パートを表示する、outname 入力がある場合はファイル出力
        :param outname:
        :param STD:
        :return:
        """
        from sae.vasp.poscar_writer import PoscarWriter

        PoscarWriter().print_poscar(
            outname,
            STD,
            self.title,
            self.scale,
            self.natom,
            self.nion,
            self.selective,
            self.direct,
            self.vasp_version,
            self.t,
            self.atoms,
            self.atoms_index,
            self.position,
            self.fix,
        )

    # direct --> cartesian
    # super 用の配列
    # super 用の内部座標作成
    # super 用の基本並進ベクトル/原子種数を作る
    # cartesian --> direct
    def conv_supercell(self, times=(1, 1, 1)):
        """
        スーパーセル作成 Method
        関数版を持ってきただけのやっつけ対応

        :param times:
        :return:
        """
        from sae.geometry.coordinates import CoordinateTransforms
        from sae.geometry.supercell import SupercellOperations

        super_x = int(times[0])
        super_y = int(times[1])
        super_z = int(times[2])
        if self.direct:
            ABS = True
            self.scale, self.direct = CoordinateTransforms().conv_direct2cara(
                ABS, self.scale, self.t, self.natom, self.direct, self.position
            )
        supers = super_x * super_y * super_x
        # (super) t
        sv = np.zeros((supers, 3))
        # (super) position
        sp = np.zeros((self.natom * supers, 3))
        # (super) ion
        ion_sp = np.zeros(self.natom * supers)
        # (super) ion_local
        ion_local_sp = np.zeros(self.natom * supers)
        # (super) fix
        fix_sp = np.zeros((self.natom * supers, 3), dtype="S")
        # super cell と orijinal cell の対応
        sp_j = np.zeros(self.natom * supers)
        SupercellOperations().make_supercell1(
            super_x,
            super_y,
            super_z,
            self.t,
            self.natom,
            self.nion,
            self.atoms,
            self.ion,
            self.ion_local,
            self.position,
            sv,
            ion_sp,
            ion_local_sp,
            sp_j,
            sp,
            self.fix,
            fix_sp,
        )
        SupercellOperations().make_supercell_param(
            super_x, super_y, super_z, self.nion, self.atoms, self.t
        )
        self.natom = self.natom * supers
        if not self.direct:
            self.scale, self.direct = CoordinateTransforms().conv_car2direct(
                self.scale, self.t, self.natom, self.direct, sp
            )
        self.ion = ion_sp
        self.ion_local = ion_local_sp
        self.position = sp
        self.fix = fix_sp
        # super cell と orijinal cell の対応
        self.sp_j = sp_j
