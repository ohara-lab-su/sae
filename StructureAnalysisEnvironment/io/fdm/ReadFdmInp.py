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
from __future__ import print_function
###############################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
#
__status__ = "alpha"
__version__ = "0.1.1"
###############################################################################

import sys
#import gzip
#import os
import re
import optparse
import numpy as np
#import copy
import collections

import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE

# for coorsys
from ase.io.wien2k import *  # suing coorsys

###############################################################################


class ReadFdmInp(SAEnv.Method):

    def __init__(self, inpname, suffix='.inp',
                 sort=True, atoms_index=None):

        self.datlines, self.num = SAEnv.read_dataline(inpname)
        self.datlines, self.num = SAEnv.del_comment(self.datlines)

        nonexec_reg = re.compile('.*Nonexc.*', re.IGNORECASE)
        magnetism_reg = re.compile('.*Magnetism.*', re.IGNORECASE)
        energygpho_reg = re.compile('.*Energpho.*', re.IGNORECASE)
        absorber_reg = re.compile('.*Absorber.*', re.IGNORECASE)
#       filout_reg = re.compile('.*Filout.*',re.IGNORECASE)
        filout_reg = re.compile('.*Fil.*out.*', re.IGNORECASE)
        atom_reg = re.compile('^\S*Atom', re.IGNORECASE)
        crystal_reg = re.compile('.*crystal .*', re.IGNORECASE) # include space
        crystal_p_reg = re.compile('.*crystal_p.*', re.IGNORECASE) # include space
        mole_reg = re.compile('.*molecule.*', re.IGNORECASE)
        char_reg = re.compile('\D', re.IGNORECASE)
        comment_reg = re.compile('^!.*', re.IGNORECASE)
        allsite_reg = re.compile('^.*allsite.*', re.IGNORECASE)
        calculation_reg = re.compile('^.*Calculation.*', re.IGNORECASE)
        conv_out_reg = re.compile('^.*Conv_out.*', re.IGNORECASE)
        convolution_reg = re.compile('^.*Convolution.*', re.IGNORECASE)
        center_abs_reg = re.compile('^.*Center_abs.*', re.IGNORECASE)

        self.ispin = 1
        self.allsite = False
        self.energygpho = False
        self.position = []
        self.convolution = False
        self.center_abs = False
        self.nonexc = False

        for i in range(self.num):

            if bool(nonexec_reg.match(self.datlines[i])):
                self.nonexc = True

            if bool(energygpho_reg.match(self.datlines[i])):
                self.energygpho = True

            # Atom TAG があるときは停止(未対応)
            if bool(atom_reg.match(self.datlines[i])) \
                    and not bool(comment_reg.match(self.datlines[i])):
                sys.exit("STOP(ReadFdmInp): non support Atom tag")

            # Magnetism ( Atom タグがない Magnetism は SOC のみ )
            if bool(magnetism_reg.match(self.datlines[i])):
                self.ispin = 2

            # allsite
            if bool(allsite_reg.match(self.datlines[i])):
                self.allsite = True

            # Filout 名確保
            if bool(filout_reg.match(self.datlines[i])):
                if len(self.datlines[i].split()) > 1:
                    self.filout = self.datlines[i].split()[1].strip()
                else:
                    self.filout = self.datlines[i + 1].strip()

            # Calculation (以前の計算結果を引き継ぐ) 名の確保
            if bool(calculation_reg.match(self.datlines[i])):
                self.calculation = str(self.datlines[i + 1].split()[0])

            # conv_out
            if bool(conv_out_reg.match(self.datlines[i])):
                self.conv_out = self.datlines[i + 1].split()[0]

            # convolution flag
            if bool(convolution_reg.match(self.datlines[i])):
                self.convolution = True

            # center_abs flag
            if bool(center_abs_reg.match(self.datlines[i])):
                self.center_abs = True

            # Absorber
            if bool(absorber_reg.match(self.datlines[i])):
                if len(self.datlines[i].split()) > 1:
                    self.absorber = int(self.datlines[i].split()[1].strip())
                else:
                    self.absorber = int(self.datlines[i + 1].strip())

            ############################################### START Crystal #####
            # Crystal 行を検索 (position の スペース行コメント行も対応)
            if bool(crystal_reg.match(self.datlines[i])) \
                    and not bool(comment_reg.match(self.datlines[i])):

                # crystal 行を見つけたらそれは molecule モードではない
                self.MOL = False

                # ここで想定しているのは a,b,c,alpha,beta,gamma 記述モード
                if not len(self.datlines[i + 1].split()) >= 6:
                    print(self.datlines[i + 1].split())
                    sys.exit("STOP(ReadFdmInp): \
                            a,b,c,alpha,beta,gamma INPUT LINE error")

                i += 1

                # conventional cell パラメーターをゲット
                lattice_a = float(self.datlines[i].split()[0])
                lattice_b = float(self.datlines[i].split()[1])
                lattice_c = float(self.datlines[i].split()[2])
                alpha = float(self.datlines[i].split()[3])
                beta = float(self.datlines[i].split()[4])
                gamma = float(self.datlines[i].split()[5])

                self.cellparam = \
                    [lattice_a, lattice_b, lattice_c, alpha, beta, gamma]
                self.t = coorsys(self.cellparam)

                self.atoms_index_j = []
                while 1:
                    i += 1
                    if len(self.datlines[i].split()) > 0:  # 空白行はスキップ

                        if bool(char_reg.match(self.datlines[i].split()[0])):
                            break  # 数字以外は スキップ

                        zz = int(self.datlines[i].split()[0])
                        x = float(self.datlines[i].split()[1])
                        y = float(self.datlines[i].split()[2])
                        z = float(self.datlines[i].split()[3])

                        self.atoms_index_j.append(SAEnv.get_atomic_symbol0(zz))
                        self.position.append([x, y, z])

                    if i == self.num:
                        break

               #self.position = np.array(self.position)

            # Mol 行を検索 (position の スペース行コメント行も対応)
            elif bool(mole_reg.match(self.datlines[i])) \
                    and not bool(comment_reg.match(self.datlines[i])):

                # molecule mode (ただし、現状ではcrystal と変わりない形式しか読まない)
                self.MOL = True

                # ここで想定しているのは a,b,c,alpha,beta,gamma 記述モード
                if not len(self.datlines[i + 1].split()) >= 6:
                    print(self.datlines[i + 1].split())
                    sys.exit("STOP: a,b,c,alpha,beta,gamma INPUT LINE error")

                i += 1

                # conventional cell パラメーターをゲット
                lattice_a = float(self.datlines[i].split()[0])
                lattice_b = float(self.datlines[i].split()[1])
                lattice_c = float(self.datlines[i].split()[2])
                alpha = float(self.datlines[i].split()[3])
                beta = float(self.datlines[i].split()[4])
                gamma = float(self.datlines[i].split()[5])

                self.cellparam = \
                    [lattice_a, lattice_b, lattice_c, alpha, beta, gamma]
                self.t = coorsys(self.cellparam)

                self.atoms_index_j = []
                print('====')
                while 1:
                    i += 1
                    if len(self.datlines[i].split()) > 0:  # 空白行はスキップ

                        if bool(char_reg.match(self.datlines[i].split()[0])):
                            break  # 数字以外は スキップ

                        zz = int(self.datlines[i].split()[0])
                        x = float(self.datlines[i].split()[1])
                        y = float(self.datlines[i].split()[2])
                        z = float(self.datlines[i].split()[3])

                        self.atoms_index_j.append(SAEnv.get_atomic_symbol0(zz))
                        self.position.append([x, y, z])

                    if i == self.num:
                        break

            else:
                ########
                # 2019.03.14 2019.03.14 commented out
                #self.position = []
                #self.atoms_index_j = []
                ########
                pass

               #self.position = np.array(self.position)
            ################################################# END Crystal #####

            if bool(crystal_p_reg.match(self.datlines[i])):
                self.position = []
                self.atoms_index_j = []

        # convolution などで filout 項目がないときは
        # filout に calculation 名を渡す
        try:
            self.filout = self.filout
        except:
            self.filout = self.calculation

        ########################################
        # position を numpy array 化
        self.position = np.array(self.position)

        # すべてのサイトの原子数
        self.natom = len(self.position)

        ########################################
       # ION 数および atoms, atoms_index の作成
        counter = collections.Counter(self.atoms_index_j)
        self.nion = len(counter)
        self.atoms = np.zeros(self.nion, dtype=int)
        self.atoms_index = []
        self.atoms_number = np.zeros(self.nion, dtype=int)
        i = 0
        for atom, cnt in counter.most_common():
            self.atoms_index.append(atom)
            self.atoms_number[i] = SAEnv.get_atomic_number1(atom)
            self.atoms[i] = cnt
            i += 1

        self.atoms_number_j = np.zeros(self.natom, dtype=int)
        for i in range(self.natom):
            self.atoms_number_j[i] = \
                SAEnv.get_atomic_number1(str(self.atoms_index_j[i]))

        # natom までの通し番号で原子種(原子の種類番号を返す)
        self.atoms_j = np.zeros(self.natom, dtype=int)
        j = 0
        for ion in range(self.nion):
            for atom in range(self.atoms[ion]):
                self.atoms_j[j] = int(ion)
                j += 1

        ########################################
        # fix 情報のダミー
        self.fix = np.zeros((self.natom, 3), dtype='S')
        self.fix[:, :] = 'F'

        ########################################
        # 原子種ごとのソートスイッチが入っているとき
        if sort:
            self.sort_index, self.sort_index_r,\
                self.atoms,\
                self.atoms_index,\
                self.atoms_index_j = \
                SAEnv.sort_atom_index_j(self.atoms_index_j)

            self.sort_index, self.sort_index_r,\
                self.atoms,\
                self.atoms_index,\
                self.atoms_number_j = \
                SAEnv.sort_atom_number_j(self.atoms_number_j)

            self.position = \
                SAEnv.sort_position(self.sort_index_r, self.position)
            self.fix = SAEnv.sort_fix(self.sort_index_r, self.fix)

        ########################################
        # ion[j]: 通し番号(max=nmax)を与えると原子の種類番号を返す
        self.ion = np.zeros(self.natom, dtype=int)
        tmp = -1
        for j in range(self.nion):
            local = -1
            for k in range(int(self.atoms[j])):
                tmp += 1
                local += 1
                self.ion[tmp] = int(j)

        ########################################
        # ion_local[j]: 通し番号(max=nmax)を与えるとサイト内のローカル通し番号を返す
        self.ion_local = np.zeros(self.natom, dtype=int)
        tmp = -1
        for j in range(self.nion):
            local = -1
            for k in range(int(self.atoms[j])):
                tmp += 1
                local += 1
                self.ion_local[tmp] = int(local)

        # 共通仕様
        self.title = self.filout
        self.nspin = self.ispin
        self.system = self.title
        self.vasp_version = None
        self.selective = False
        self.direct = True
        self.scale = 1.0
        self.sort_index = None
        self.sort_index_r = None

       #########################
       # test print atom_index_j
       #########################
       # j=0
       # for i in scaled_position:
       #    print atoms_index_j[j],i
       #    j += 1

    # for FDMNES  infomation
    def get_ispin(self):
        return self.ispin

    def get_nonexc(self):
        return self.nonexc

    def get_allsite(self):
        return self.allsite

    def get_energygpho(self):
        return self.energygpho

    def get_absorber(self):
        self.absorber = self.absorber if hasattr(self, 'absorber') else 1
        return self.absorber

    def get_convolution(self):
        return self.convolution

    def get_conv_out(self):
        self.conv_out = self.conv_out if hasattr(self, 'conv_out') else None
        return self.conv_out

    def get_calculation(self):
        self.calculation = \
            self.calculation if hasattr(self, 'calculation') else None
        return self.calculation

    def get_filout(self):
        self.filout = self.filout if hasattr(self, 'filout') else None
        return self.filout

    # for structure infomation

    def get_cellparam(self):
        return self.cellparam

    # for structure convert

    def sort_atoms_index_j(self):

        self.sort_index, self.sort_index_r,\
            self.atoms,\
            self.atoms_index,\
            self.atoms_index_j = \
            SAEnv.sort_atom_index_j(self.atoms_index_j)

        return self.sort_index, self.sort_index_r,\
            self.atoms,\
            self.atoms_index,\
            self.atoms_index_j

    def sort_position(self):
        if self.sort_index_r is None:
            self.sort_atoms_index_j()
        self.position = SAEnv.sort_position(self.sort_index_r, self.position)
        return self.position

    # add 2019.03.14
    def get_atoms_index_j(self):
        return self.atoms_index_j

    # add 2019.03.14
    def get_natom(self):
        return self.natom

##########################################################################
def options():
    #   name = 'POSCAR.inp'
    name = 'read_pdb.inp'

    parser = optparse.OptionParser()

    parser.add_option('-i', '--input', dest='INPUT', default=name,)
    options, args = parser.parse_args()

    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]

    return name

##########################################################################
if __name__ == '__main__':

    name = options()

#   out = ReadFdmInp(name,sort=True)
    out = ReadFdmInp(name)

    absorber = out.get_absorber()
    filout = out.get_filout()
    atoms_index_j = out.get_atoms_index_j()
    atoms_number_j = out.get_atoms_number_j()
    natom = out.get_natom()
    position = out.get_position()
    energygpho = out.get_energygpho()
    ispin = out.get_ispin()

    allsite = out.get_allsite()
    calculation = out.get_calculation()
    convolution = out.get_convolution()
    conv_out = out.get_conv_out()

    a = out.cellparam[0]
    b = out.cellparam[1]
    c = out.cellparam[2]
    alpha = out.cellparam[3]
    beta = out.cellparam[4]
    gamma = out.cellparam[5]

    print('allsite    : %s' % str(allsite))
    print('absorber   : %s' % str(absorber))
    print('energygpho : %s' % str(energygpho))

    print('filout     : %s' % str(filout))
    print('natom      : %s' % str(natom))
    print('')
    print('a          : %s' % str(out.cellparam[0]))
    print('b          : %s' % str(out.cellparam[1]))
    print('c          : %s' % str(out.cellparam[2]))
    print('alpha      : %s' % str(out.cellparam[3]))
    print('beta       : %s' % str(out.cellparam[4]))
    print('gamma      : %s' % str(out.cellparam[5]))
    print('')
    print('t          :')
    print(out.t)
    print('')
    print(out.atoms_number)
    print(out.atoms_index)

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

    for i in range(natom):
        print(" %s %d  %14.10f %14.10f %14.10f"
            % (atoms_index_j[i], atoms_number_j[i],
                position[i, 0], position[i, 1], position[i, 2]))

#   out.sort_atoms_index_j()

#   out.sort_atoms_number_j()
    out.sort_position()
#   out.sort_fix()

    print(out.atoms_number)
    print(out.atoms_index)

    print(" %s %d  %14.10f %14.10f %14.10f"
            % (out.atoms_index_j[i],
               out.atoms_number_j[i],
               out.position[i, 0],
               out.position[i, 1],
               out.position[i, 2]))

    if convolution:
        print("")
        print("convolution: %s" % str(convolution))
        print('calculation: %s' % str(calculation))
        print('conv_out   : %s' % str(conv_out))
#       print "NAME",name

