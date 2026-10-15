#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#  Method --- ReadVaspPoscar
#  Method --- ReadFdmInp
#  Method --- ReaMxDatMethod -- ReadMxDat
#                            -- ReadMxDftscf
#                            -- ReadMxOut
#                            -- ReadMxPdos
#                            -- ReadMxTdos
#  Method --- ReadRmcpotCfg
#  Method --- ReadPwIn
#
###############################################################################
#
# FDMNES
# *.in ファイル
#
# 主に Crystal の部分の解析と読み込み
#
###############################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.11.20
#  convolution 用の結晶構造情報が無いファイルに対する対応
#
# 2015.08.25
#  統合化&Method でいろいろと分離
#
# 2015.08.20
#  Read.py との統合化のためのすりあわせ
#  position のソートルーチンの追加＆分離
#
# 2015.08.19
#  cellparam の基本並進ベクトル変換を ASE の coorsys を採用
#
# 2015.06.24
#  allsite 計算をしているか否かの判断を*.inp かおこなう
#
# 2015.06.19
#   読み込むタグをいくつか追加
#   コメントアウトの処理
#   タグ名とタグの内容が同一行でも対応可能に
#
# 2015.05.19 startup
#   cellpar(a,b,c,alpha,beta,gamma) --> cell(基本並進) への変換が意外に鬼門
#   ---> とりあえずこのルーチンの開発は一旦サスペンド
#
###############################################################################
# トップディレクトリ関係のエラーは ImportError ではキャッチ出来ない
###############################################################################
# import gzip
# import os
# import copy
# import SpaceGroupEnvironment as SGE
# for coorsys
# suing coorsys
###############################################################################
##########################################################################
#   name = 'POSCAR.inp'
##########################################################################
#   out = ReadFdmInp(name,sort=True)
#   cal = np.cos(alpha * np.pi / 180.0)
#   cbe = np.cos(beta * np.pi / 180.0)
#   cga = np.cos(gamma * np.pi /180.0)
#   sga = np.sin(gamma * np.pi /180.0)
#   t = np.array([
#                 [a, b * cga, c * cbe],\
#                 [0, b * sga, c * (cal - cbe * cga) / sga],\
#                 [0, 0, c * np.sqrt(1 - cal**2 -cbe**2 - cga**2 +\
#                                    2 * cal * cbe * cga) / sga],\
#                ]).transpose()
#   out.sort_atoms_index_j()
#   out.sort_atoms_number_j()
#   out.sort_fix()
#       print "NAME",name
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.structure.base import Method
import sys
import re
import optparse
import numpy as np
import collections

try:
    Method = Method
except ImportError:
    Method = Method
from ase.io.wien2k import *


#########################
# test print atom_index_j
#########################
# j=0
# for i in scaled_position:
#    print atoms_index_j[j],i
#    j += 1
# for FDMNES  infomation
# for structure infomation
# for structure convert
# add 2019.03.14
# add 2019.03.14
class ReadFdmInp(Method):
    """
    FDMNES の input ファイル名を読み込む
    """

    # filout_reg = re.compile('.*Filout.*',re.IGNORECASE)
    ## 2020.06.23 修正
    # crystal_reg = re.compile('.*crystal .*', re.IGNORECASE)  # include space
    # convolution などで filout 項目がないときは
    # filout に calculation 名を渡す
    ########################################
    # position を numpy array 化
    # すべてのサイトの原子数
    ########################################
    # ION 数および atoms, atoms_index の作成
    # natom までの通し番号で原子種(原子の種類番号を返す)
    ########################################
    # fix 情報のダミー
    ########################################
    # 原子種ごとのソートスイッチが入っているとき
    ########################################
    # ion[j]: 通し番号(max=nmax)を与えると原子の種類番号を返す
    ########################################
    # ion_local[j]: 通し番号(max=nmax)を与えるとサイト内のローカル通し番号を返す
    # 共通仕様
    def __init__(self, inpname, suffix=".inp", sort=True, atoms_index=None):
        from sae.common.text import TextFiles
        from sae.structure.elements import ElementTable
        from sae.structure.ordering import AtomOrdering

        self.datlines, self.num = TextFiles().read_dataline(inpname)
        self.datlines, self.num = TextFiles().del_comment(self.datlines)
        nonexec_reg = re.compile(".*Nonexc.*", re.IGNORECASE)
        magnetism_reg = re.compile(".*Magnetism.*", re.IGNORECASE)
        energygpho_reg = re.compile(".*Energpho.*", re.IGNORECASE)
        absorber_reg = re.compile(".*Absorber.*", re.IGNORECASE)
        filout_reg = re.compile(".*Fil.*out.*", re.IGNORECASE)
        atom_reg = re.compile("^\\S*Atom", re.IGNORECASE)
        # include space
        crystal_reg = re.compile(".*crystal.*", re.IGNORECASE)
        # include space
        crystal_p_reg = re.compile(".*crystal_p.*", re.IGNORECASE)
        mole_reg = re.compile(".*molecule.*", re.IGNORECASE)
        char_reg = re.compile("\\D", re.IGNORECASE)
        comment_reg = re.compile("^!.*", re.IGNORECASE)
        allsite_reg = re.compile("^.*allsite.*", re.IGNORECASE)
        calculation_reg = re.compile("^.*Calculation.*", re.IGNORECASE)
        conv_out_reg = re.compile("^.*Conv_out.*", re.IGNORECASE)
        convolution_reg = re.compile("^.*Convolution.*", re.IGNORECASE)
        center_abs_reg = re.compile("^.*Center_abs.*", re.IGNORECASE)
        self.ispin = 1
        self.allsite = False
        self.energygpho = False
        self.position = []
        self.convolution = False
        self.center_abs = False
        self.nonexc = False
        # print RAW DATA for debug
        # Noexe
        # PhotoEnergy
        # Atom TAG があるときは停止(未対応)
        # Magnetism ( Atom タグがない Magnetism は SOC のみ )
        # allsite
        # Filout 名確保
        # Calculation (以前の計算結果を引き継ぐ) 名の確保
        # conv_out
        # convolution flag
        # center_abs flag
        # Absorber
        #
        # START Crystal
        #
        # Crystal 行を検索 (position の スペース行コメント行も対応)
        # self.position = np.array(self.position)
        ################################################# END Crystal #####
        for i in range(self.num):
            print("%s" % self.datlines[i])
            if bool(nonexec_reg.match(self.datlines[i])):
                self.nonexc = True
            if bool(energygpho_reg.match(self.datlines[i])):
                self.energygpho = True
            if bool(atom_reg.match(self.datlines[i])) and (
                not bool(comment_reg.match(self.datlines[i]))
            ):
                sys.exit("STOP(ReadFdmInp): non support Atom tag")
            if bool(magnetism_reg.match(self.datlines[i])):
                self.ispin = 2
            if bool(allsite_reg.match(self.datlines[i])):
                self.allsite = True
            if bool(filout_reg.match(self.datlines[i])):
                if len(self.datlines[i].split()) > 1:
                    self.filout = self.datlines[i].split()[1].strip()
                else:
                    self.filout = self.datlines[i + 1].strip()
            if bool(calculation_reg.match(self.datlines[i])):
                self.calculation = str(self.datlines[i + 1].split()[0])
            if bool(conv_out_reg.match(self.datlines[i])):
                self.conv_out = self.datlines[i + 1].split()[0]
            if bool(convolution_reg.match(self.datlines[i])):
                self.convolution = True
            if bool(center_abs_reg.match(self.datlines[i])):
                self.center_abs = True
            if bool(absorber_reg.match(self.datlines[i])):
                if len(self.datlines[i].split()) > 1:
                    self.absorber = int(self.datlines[i].split()[1].strip())
                else:
                    self.absorber = int(self.datlines[i + 1].strip())
            # crystal 行を見つけたらそれは molecule モードではない
            # ここで想定しているのは a,b,c,alpha,beta,gamma 記述モード
            # conventional cell パラメーターをゲット
            # self.position = np.array(self.position)
            # Mol 行を検索 (position の スペース行コメント行も対応)
            if bool(crystal_reg.match(self.datlines[i])) and (
                not bool(comment_reg.match(self.datlines[i]))
            ):
                self.MOL = False
                if not len(self.datlines[i + 1].split()) >= 6:
                    print(self.datlines[i + 1].split())
                    sys.exit(
                        "STOP(ReadFdmInp): a,b,c,alpha,beta,gamma INPUT LINE error"
                    )
                i += 1
                lattice_a = float(self.datlines[i].split()[0])
                lattice_b = float(self.datlines[i].split()[1])
                lattice_c = float(self.datlines[i].split()[2])
                alpha = float(self.datlines[i].split()[3])
                beta = float(self.datlines[i].split()[4])
                gamma = float(self.datlines[i].split()[5])
                self.cellparam = [lattice_a, lattice_b, lattice_c, alpha, beta, gamma]
                self.t = coorsys(self.cellparam)
                self.atoms_index_j = []
                while 1:
                    i += 1
                    # 空白行はスキップ
                    # for TEST
                    # print("%s %f %f %f" % (zz, x, y, z))
                    # 原子番号から元素名を取り出す
                    if len(self.datlines[i].split()) > 0:
                        if bool(char_reg.match(self.datlines[i].split()[0])):
                            # 数字以外は スキップ
                            break
                        zz = int(self.datlines[i].split()[0])
                        x = float(self.datlines[i].split()[1])
                        y = float(self.datlines[i].split()[2])
                        z = float(self.datlines[i].split()[3])
                        symbol_ = ElementTable().get_atomic_symbol0(zz)
                        self.atoms_index_j.append(symbol_)
                        self.position.append([x, y, z])
                    if i == self.num:
                        break
            # molecule mode (ただし、現状ではcrystal と変わりない形式しか読まない)
            # ここで想定しているのは a,b,c,alpha,beta,gamma 記述モード
            # conventional cell パラメーターをゲット
            ########
            # 2019.03.14 2019.03.14 commented out
            # self.position = []
            # self.atoms_index_j = []
            ########
            elif bool(mole_reg.match(self.datlines[i])) and (
                not bool(comment_reg.match(self.datlines[i]))
            ):
                self.MOL = True
                if not len(self.datlines[i + 1].split()) >= 6:
                    print(self.datlines[i + 1].split())
                    sys.exit("STOP: a,b,c,alpha,beta,gamma INPUT LINE error")
                i += 1
                lattice_a = float(self.datlines[i].split()[0])
                lattice_b = float(self.datlines[i].split()[1])
                lattice_c = float(self.datlines[i].split()[2])
                alpha = float(self.datlines[i].split()[3])
                beta = float(self.datlines[i].split()[4])
                gamma = float(self.datlines[i].split()[5])
                self.cellparam = [lattice_a, lattice_b, lattice_c, alpha, beta, gamma]
                self.t = coorsys(self.cellparam)
                self.atoms_index_j = []
                print("====")
                while 1:
                    i += 1
                    # 空白行はスキップ
                    if len(self.datlines[i].split()) > 0:
                        if bool(char_reg.match(self.datlines[i].split()[0])):
                            # 数字以外は スキップ
                            break
                        zz = int(self.datlines[i].split()[0])
                        x = float(self.datlines[i].split()[1])
                        y = float(self.datlines[i].split()[2])
                        z = float(self.datlines[i].split()[3])
                        symbol_ = ElementTable().get_atomic_symbol0(zz)
                        self.atoms_index_j.append(symbol_)
                        self.position.append([x, y, z])
                    if i == self.num:
                        break
                    print(self.atoms_index_j)
            else:
                pass
            if bool(crystal_p_reg.match(self.datlines[i])):
                self.position = []
                self.atoms_index_j = []
        print("=== END of READ INP")
        print("")
        print("input file name = %s" % inpname)
        print("Fileout         = %s" % self.filout)
        print("ISPIN           = %s" % self.ispin)
        print("Allist          = %s" % self.allsite)
        print("Energypho       = %s" % self.energygpho)
        print("Convolutaion    = %s" % self.convolution)
        print("Center_abs      = %s" % self.center_abs)
        print("Noexc           = %s" % self.nonexc)
        print(self.atoms_index_j)
        try:
            self.filout = self.filout
        except:
            self.filout = self.calculation
        self.position = np.array(self.position)
        self.natom = len(self.position)
        counter = collections.Counter(self.atoms_index_j)
        self.nion = len(counter)
        self.atoms = np.zeros(self.nion, dtype=int)
        self.atoms_index = []
        self.atoms_number = np.zeros(self.nion, dtype=int)
        i = 0
        for atom, cnt in counter.most_common():
            self.atoms_index.append(atom)
            self.atoms_number[i] = ElementTable().get_atomic_number1(atom)
            self.atoms[i] = cnt
            i += 1
        self.atoms_number_j = np.zeros(self.natom, dtype=int)
        for i in range(self.natom):
            self.atoms_number_j[i] = ElementTable().get_atomic_number1(
                str(self.atoms_index_j[i])
            )
        self.atoms_j = np.zeros(self.natom, dtype=int)
        j = 0
        for ion in range(self.nion):
            for atom in range(self.atoms[ion]):
                self.atoms_j[j] = int(ion)
                j += 1
        self.fix = np.zeros((self.natom, 3), dtype="S")
        self.fix[:, :] = "F"
        if sort:
            (
                self.sort_index,
                self.sort_index_r,
                self.atoms,
                self.atoms_index,
                self.atoms_index_j,
            ) = AtomOrdering().sort_atom_index_j(self.atoms_index_j)
            (
                self.sort_index,
                self.sort_index_r,
                self.atoms,
                self.atoms_index,
                self.atoms_number_j,
            ) = AtomOrdering().sort_atom_number_j(self.atoms_number_j)
            self.position = AtomOrdering().sort_position(
                self.sort_index_r, self.position
            )
            self.fix = AtomOrdering().sort_fix(self.sort_index_r, self.fix)
        self.ion = np.zeros(self.natom, dtype=int)
        tmp = -1
        for j in range(self.nion):
            local = -1
            for k in range(int(self.atoms[j])):
                tmp += 1
                local += 1
                self.ion[tmp] = int(j)
        self.ion_local = np.zeros(self.natom, dtype=int)
        tmp = -1
        for j in range(self.nion):
            local = -1
            for k in range(int(self.atoms[j])):
                tmp += 1
                local += 1
                self.ion_local[tmp] = int(local)
        self.title = self.filout
        self.nspin = self.ispin
        self.system = self.title
        self.vasp_version = None
        self.selective = False
        self.direct = True
        self.scale = 1.0
        self.sort_index = None
        self.sort_index_r = None

    def get_ispin(self):
        return self.ispin

    def get_nonexc(self):
        return self.nonexc

    def get_allsite(self):
        return self.allsite

    def get_energygpho(self):
        return self.energygpho

    def get_absorber(self):
        self.absorber = self.absorber if hasattr(self, "absorber") else 1
        return self.absorber

    def get_convolution(self):
        return self.convolution

    def get_conv_out(self):
        self.conv_out = self.conv_out if hasattr(self, "conv_out") else None
        return self.conv_out

    def get_calculation(self):
        self.calculation = self.calculation if hasattr(self, "calculation") else None
        return self.calculation

    def get_filout(self):
        self.filout = self.filout if hasattr(self, "filout") else None
        return self.filout

    def get_cellparam(self):
        return self.cellparam

    def sort_atoms_index_j(self):
        from sae.structure.ordering import AtomOrdering

        (
            self.sort_index,
            self.sort_index_r,
            self.atoms,
            self.atoms_index,
            self.atoms_index_j,
        ) = AtomOrdering().sort_atom_index_j(self.atoms_index_j)
        return (
            self.sort_index,
            self.sort_index_r,
            self.atoms,
            self.atoms_index,
            self.atoms_index_j,
        )

    def sort_position(self):
        from sae.structure.ordering import AtomOrdering

        if self.sort_index_r is None:
            self.sort_atoms_index_j()
        self.position = AtomOrdering().sort_position(self.sort_index_r, self.position)
        return self.position

    def get_atoms_index_j(self):
        return self.atoms_index_j

    def get_natom(self):
        return self.natom
