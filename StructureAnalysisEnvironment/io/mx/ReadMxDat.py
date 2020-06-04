#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OpenMX 3.7 *.dat 形式ファイル 読み込み class
#
#
#  class ReadMxDatMethod ----- class RreadMxDat
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.08.25
#  コンストラクタ大改修（統合化互換）終了
#
# 2015.08.24
#  統合＆大改修直前の安定バージョン
#   1) Method の継承を止めて 自前のコンストラクタで実装
#      インスタンス変数の重視化
#
# 2015.02.24
#  *.dat / *.out 共通method (主に *.dat 部分) を ReadMxDatMethod.py へ
#  分離し、そちらをスーパークラスとする。class ReadMxDat ではsuperclass
#  を継承してそれら method を実装する形にする。
#
# 2015.02.24
#   spin チェックmethod
#
# 2015.02.17
#
#  旧名) ReadDatMx (ReadMxDat)
#    *.dat 名の重複があるので DatMx とする( 例 RMC_POT の *.dat 形式 )
#    ==> MxDat へルール変更
#
# 2015.02.17
#  get_position_max(), get_position_min 追加
#   position[atom,3] のそれぞれ x,y,z の最大値を返す
#
# 2015.02.17
#  get_t() を初めいくつかの method で *.dat のコメントアウト処理に正しく
#  対応してなかったため意図しない動作になっていたのを修正
#
# 2015.02.17
#  Al-Si111-ESM.dat が正しく読めないエラー
#  ReadDatMx class, get_t, get_position のバグ(仕様)を修正
#
# 2015.02.17
#  get_fix() も get_position() と同様に atoms_index の順番に合わせる
#
# 2015.02.17
#  get_atom() の新方式に合わせて get_position() の順番もソートしなおして
#  atoms_index に矛盾なく並べ直した情報を返すように変更
#
#  オリジナルの順番とatoms_indexに合わせてソートしなおした配列の対応は
#  get_position() 後の self.position_index にてアクセス可能
#
# 2015.02.16
#  get_atom() の分類方法を変更
#   古: 連続して並んでいる元素記号のみを一つのサイトとしてひとくくりにした
#   新: atoms_index (Atomic.Species タグ) の情報のみでサイトのグルーピング
#
# 2015.02.12 1st
#
#  注意)
#     get_fix() は必ず get_position() の後に実行する
#
################################################################################
from __future__ import print_function
try:
    from ...copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.9"

################################################################################

import sys
import os
import re
# import gzip
import numpy as np

try:
    sys.path.append('../../')
    import StructureAnalysisEnvironment as SAEnv
    from StructureAnalysisEnvironment.io import *
    from StructureAnalysisEnvironment.io.mx.ReadMxDatMethod import ReadMxDatMethod
except ImportError:
    import StructureAnalysisEnvironment as SAEnv
    from StructureAnalysisEnvironment.io import *
    from StructureAnalysisEnvironment.io.mx.ReadMxDatMethod import ReadMxDatMethod


################################################################################
class ReadMxDat(ReadMxDatMethod):

    ###############################################
    ## init and Read POSCAR
    def __init__(self, datname, suffix='.dat', sort=True, atoms_index=None):

        self.datlines, self.num = SAEnv.read_dataline(datname)

        BOHR = 0.529177  # Bohr radius in Angstrom

        comment_reg = re.compile('^#.*', re.IGNORECASE)
        reg_switch_off = re.compile('Off', re.IGNORECASE)
        reg_switch_on = re.compile('On', re.IGNORECASE)

        reg_title = re.compile('.*System\.Name')
        reg_spin = re.compile('.*scf\.SpinPolarization', re.IGNORECASE)
        reg_nion = re.compile('.*Species\.Number')

        reg0_atoms_index = re.compile('.*\<Definition\.of\.Atomic\.Species')
        reg1_atoms_index = re.compile('.*Definition\.of\.Atomic\.Species\>')

        reg_natom = re.compile('.*Atoms\.Number')

        reg_unit = re.compile('.*Atoms\.SpeciesAndCoordinates\.Unit')
        reg_unit0 = re.compile('AU', re.IGNORECASE)
        reg_unit1 = re.compile('Ang', re.IGNORECASE)
        reg_unit2 = re.compile('FRAC', re.IGNORECASE)

        reg0_atoms = re.compile('.*\<Atoms\.SpeciesAndCoordinates')
        reg1_atoms = re.compile('.*Atoms\.SpeciesAndCoordinates\>')
        reg_position1 = re.compile('.*\<Atoms\.SpeciesAndCoordinates')  # reg0_atoms

        reg0_unit_vector = re.compile('.*Atoms\.UnitVectors\.Unit')
        reg2_unit_vector = re.compile('.*\<Atoms\.UnitVectors')
        reg3_unit_vector = re.compile('.*Atoms\.UnitVectors\>')

        reg_md0 = re.compile('.*\<MD\.Fixed\.XYZ')
        reg_md1 = re.compile('.*MD\.Fixed\.XYZ\>')

        self.ispin = 1
        self.scale = 1.0
        self.vasp_version = 5  # dummy
        self.atoms_index = []
        self.t = np.zeros((3, 3))
        self.selective = False
        self.t_FLAG = False  # 基本並進の存在があるかどうかのフラグ

        NION_FLAG = False
        NATOM_FLAG = False
        UNIT_FLAG = False

        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):

                # title
                if bool(reg_title.match(self.datlines[i])):
                    src = self.datlines[i].split()[1]
                    self.system = re.sub(' *$', '', src)
                    self.title = self.system

                # spin の有無( SpinPolarization on = 2, off = 1 )
                # scf.SpinPolarization        on
                if not bool(comment_reg.match(self.datlines[i])):
                    if bool(reg_spin.match(self.datlines[i])):
                        if bool(reg_switch_off.match(self.datlines[i].split()[1])):
                            self.ispin = 1
                        elif bool(reg_switch_on.match(self.datlines[i].split()[1])):
                            self.ispin = 2
                        else:
                            sys.exit("STOP: unknown SpinPolarization switch")

                # 擬ポテンシャルのセクション(1)
                #
                #    nion
                #
                if bool(reg_nion.match(self.datlines[i])):
                    self.nion = int(self.datlines[i].split()[1])
                    if not NION_FLAG:
                        NION_FLAG = True
                        self.atoms = np.zeros(self.nion, dtype=int)

                # 擬ポテンシャルのセクション(2)
                #
                #    atoms_index
                #
                if bool(reg0_atoms_index.match(self.datlines[i]) and NION_FLAG):
                    j = 1
                    while not bool(reg1_atoms_index.match(self.datlines[i + j])):
                        self.atoms_index.append(self.datlines[i + j].split()[0])
                        j += 1
                    if self.nion != j - 1:
                        sys.exit("STOP: Atomic.Species Tag Error")

                # 内部座標セクション(1)
                #
                #    position の直前
                #    natom
                #
                if bool(reg_natom.match(self.datlines[i])):
                    self.natom = int(self.datlines[i].split()[1])
                    if not NATOM_FLAG:
                        NATOM_FLAG = True
                        self.atoms_j = np.zeros(self.natom, dtype=int)
                        self.ion = np.zeros(self.natom)
                        self.position = np.zeros((self.natom, 3))
                        # position_index, sort_index --> original_index
                        self.position_index = np.zeros(self.natom, dtype=int)
                        # position_index_r, original_index --> sort_index
                        self.position_index_r = np.zeros(self.natom, dtype=int)
                        self.fix = np.zeros((self.natom, 3), dtype='S')

                # 内部座標セクション(2)
                #
                #    get direct mode & unit
                #
                if bool(reg_unit.match(self.datlines[i])):
                    if bool(reg_unit0.match(self.datlines[i].split()[1])):
                        self.direct = False
                        self.UNIT = BOHR  # 'Atomic Unit'
                    elif bool(reg_unit1.match(self.datlines[i].split()[1])):
                        self.direct = False
                        self.UNIT = 1.0  # 'Ang'
                    elif bool(reg_unit2.match(self.datlines[i].split()[1])):
                        self.direct = True
                        self.UNIT = 1.0
                    else:
                        sys.exit("STOP: Unknown Atoms.SpeciesAndCoordinates.Unit")
                    UNIT_FLAG = True

                # 内部座標セクション(3)-1
                #
                #   atoms (get_atoms version2) 正しく動作
                #    OpenMX 的には Species.Number で区分される PAO/VPS は
                #    同一記号ならばかならず同一サイトとして分類してもよい感じ
                #    なので、そのように分類し直す。この分類変更にともなって
                #    position と fix の行列も整理し直す必要あるので注意
                #
                if bool(reg0_atoms.match(self.datlines[i])) and NION_FLAG and NATOM_FLAG and UNIT_FLAG:
                    for j in range(self.natom):
                        for k in range(self.nion):
                            if self.datlines[i + j + 1].split()[1] == self.atoms_index[k]:
                                self.atoms[k] += 1
                    if not bool(reg1_atoms.match(self.datlines[i + j + 1 + 1])):
                        sys.exit("STOP: Atomic.Number and Atoms.SpeciesAndCoordinates Tag Error")
                    ATOMS_FLAG = True

                # 内部座標セクション(3)-2
                #
                #      atoms で読み込んだところと同じところを再度読む
                #      内部座標の順番を atoms_index (および atoms) と同じく
                #      するために元素記号ごと(atom_indexの順番で)ソートする
                #
                #      内部座標の取得 AU --> Ang 変換だけはここでやる
                #      (カーテシアンとダイレクトの変換はここでは行わない)
                #      並んでいる順番通りに並べる
                #
                if bool(reg_position1.match(self.datlines[i])) and ATOMS_FLAG:
                    l = 0  # sort_index
                    for k in range(self.nion):
                        for j in range(1, self.natom + 1):  # original_index
                            if self.atoms_index[k] == self.datlines[i + j].split()[1]:
                                self.position_index[l] = \
                                    int(self.datlines[i + j].split()[0]) - 1
                                self.position_index_r[j - 1] = l
                                self.position[l, 0] = \
                                    float(self.datlines[i + j].split()[2]) * self.UNIT
                                self.position[l, 1] = \
                                    float(self.datlines[i + j].split()[3]) * self.UNIT
                                self.position[l, 2] = \
                                    float(self.datlines[i + j].split()[4]) * self.UNIT
                                l += 1
                    UNIT_FLAG = False

                # 基本並進ベクトルセクション(1)
                #
                #   基本並進に用いている Unit を調べて AU のときは Ang にする
                #
                if bool(reg0_unit_vector.match(self.datlines[i])):
                    if bool(reg_unit0.match(self.datlines[i].split()[1])):
                        self.UNIT = BOHR  # FLAG_UNIT = True   # 'Atomic Unit'
                    elif bool(reg_unit1.match(self.datlines[i].split()[1])):
                        self.UNIT = 1.0  # FLAG_UNIT = False  # 'Ang'
                    else:
                        sys.exit("STOP: Unknown Atoms.UnitVectors.Unit")
                    UNIT_FLAG = True

                # 基本並進ベクトルセクション(2)
                #
                #   Read Translation Vector
                #         x   y   z
                #   t1 = t11 t21 t31
                #   t2 = t12 t22 t32
                #   t3 = t13 t23 t33
                # get translation vector # 基本並進が存在しない場合があるのでフラグを入れる
                #
                if bool(reg2_unit_vector.match(self.datlines[i])) and UNIT_FLAG:
                    self.t_FLAG = True

                    self.t[0, 0] = float(self.datlines[i + 1 + 0].split()[0]) * self.UNIT
                    self.t[1, 0] = float(self.datlines[i + 1 + 0].split()[1]) * self.UNIT
                    self.t[2, 0] = float(self.datlines[i + 1 + 0].split()[2]) * self.UNIT

                    self.t[0, 1] = float(self.datlines[i + 1 + 1].split()[0]) * self.UNIT
                    self.t[1, 1] = float(self.datlines[i + 1 + 1].split()[1]) * self.UNIT
                    self.t[2, 1] = float(self.datlines[i + 1 + 1].split()[2]) * self.UNIT

                    self.t[0, 2] = float(self.datlines[i + 1 + 2].split()[0]) * self.UNIT
                    self.t[1, 2] = float(self.datlines[i + 1 + 2].split()[1]) * self.UNIT
                    self.t[2, 2] = float(self.datlines[i + 1 + 2].split()[2]) * self.UNIT

                    if not bool(reg3_unit_vector.match(self.datlines[i + 1 + 3])):
                        sys.exit("STOP: Atoms.UnitVectors Error")

                # MD 情報セクション(1)
                #
                #    get selective mode (MD flag)
                #
                if bool(reg_md0.match(self.datlines[i])):
                    self.selective = True

                # MD 情報セクション(2)
                #
                #   fixed
                #    fix の情報は VASP 相当に変更する(F=Fix, T=moving True)
                #    position の取得と別のmethodにする
                #
                #    内部座標を atoms_index と合わせるためにソートする
                #
                #    注意)
                #    ソート用のindexは get_position() で生成される self.position_index
                #    が必要。get_fix 中では get_position() は読まずに self.get_position()
                #    実行後に get_fix が実行されると仮定して self.position_index および
                #    self.position_index_r を用いる
                #
                if self.selective:
                    if bool(reg_md0.match(self.datlines[i])):
                        j = 1
                        while not bool(reg_md1.match(self.datlines[i + j])):
                            fix_x = int(self.datlines[i + j].split()[1])
                            fix_y = int(self.datlines[i + j].split()[2])
                            fix_z = int(self.datlines[i + j].split()[3])

                            if fix_x == 1:
                                fix_x = 'F'  # Moving False ( Fixed )
                            elif fix_x == 0:
                                fix_x = 'T'  # Moving True  ( non Fixed )
                            else:
                                sys.exit("STOP: unknown Fixed Parameter")

                            if fix_y == 1:
                                fix_y = 'F'  # Moving False ( Fixed )
                            elif fix_y == 0:
                                fix_y = 'T'  # Moving True  ( non Fixed )
                            else:
                                sys.exit("STOP: unknown Fixed Parameter")

                            if fix_z == 1:
                                fix_z = 'F'  # Moving False ( Fixed )
                            elif fix_z == 0:
                                fix_z = 'T'  # Moving True  ( non Fixed )
                            else:
                                sys.exit("STOP: unknown Fixed Parameter")

                            # self.fix.append([fix_x, fix_y, fix_z])

                            ### original の index で fix を作るのではなく
                            ### atoms_index の並びで sort した index で fix を作る
                            # self.fix[j-1,0] = fix_x
                            # self.fix[j-1,1] = fix_y
                            # self.fix[j-1,2] = fix_z
                            self.fix[self.position_index_r[j - 1], 0] = fix_x
                            self.fix[self.position_index_r[j - 1], 1] = fix_y
                            self.fix[self.position_index_r[j - 1], 2] = fix_z
                            #########################
                            j += 1
                        if self.natom != j - 1:
                            sys.exit("STOP: Atomic.Number and Atoms.SpeciesAndCoordinates Tag Error")

        ###################################
        # atoms_j (My配列),natomまでの通し番号で原子の種類を返すMethod
        #    ReadMxDatMethod.get_atoms version2 に対応する get_atoms_j
        #    atoms_index (ReadOutcar.get_atoms_index_j に準じる)
        #    ただし、atoms_j は元素記号ではなく原子の種類番号を返す
        #    この機能と互換のMethodは ReadOutcar.atoms_j() となる
        #
        # 混乱するので普通に get_atoms_index_j と命名し直す (2015.03.09)
        # --> さらに混乱した
        #     atoms_index_j はそもそも番号ではなく元素記号で返す変数だったのを忘れいた
        #     元に戻す(2015.03.09)
        #
        j = 0
        for ion in range(self.nion):
            for atom in range(self.atoms[ion]):
                self.atoms_j[j] = int(ion)
                j += 1

        ###################################
        # 2015.03.09
        # ion[j]    : 通し番号(max=natom)を与えると原子の種類番号を返す
        # atoms[i]  : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
        tmp = -1
        for i in range(self.nion):
            for k in range(self.atoms[i]):
                tmp += 1
                self.ion[tmp] = int(i)

        ###############################################
        ## ion_local[j]  : 通し番号(max=natom)を与えるとサイト内のローカル通し番号を返す
        ##
        self.ion_local = np.zeros(self.natom, dtype=int)
        tmp = -1
        for j in range(self.nion):
            local = -1
            for k in range(int(self.atoms[j])):
                tmp += 1
                local += 1
                self.ion_local[tmp] = int(local)
            # print tmp, int(ion[tmp]), int(ion_local[tmp])

        ###################################
        # 2015.03.09
        # atoms[i]          : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
        # atoms_j[j]        : 通し番号(max=natom)を与えると、原子の種類番号を返す
        # atoms_index[i]    : 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
        # atoms_index_j[i]  : 通し番号(max=natom)を与えると、原子種の元素記号を返す
        #
        self.atoms_index_j = []
        for j in range(self.natom):
            self.atoms_index_j.append(self.atoms_index[self.atoms_j[j]])

        ###############################################
        ## atoms_number[i]
        ##   atoms_index の原子番号版
        self.atoms_number = np.zeros(self.nion, dtype=int)
        for i in range(self.nion):
            self.atoms_number[i] = SAEnv.get_atomic_number1(str(self.atoms_index[i]))

        ###############################################
        ## atoms_number_j[j]
        ##   atoms_index_j に併せて記号ではなく原子番号で保存しておく配列を用意
        self.atoms_number_j = []
        for k in range(self.nion):
            for l in range(int(self.atoms[k])):
                num0 = SAEnv.get_atomic_number1(str(self.atoms_index[k]))
                self.atoms_number_j.append(num0)

    ############################################################################
    def get_title(self):
        return self.title

    def get_system(self):
        return self.system

    def get_scale(self):
        return self.scale

    def get_t(self):
        return self.t

    def get_vasp_version(self):
        return self.vasp_version

    def get_atoms(self):
        return self.atoms

    def get_atoms_j(self):
        return self.atoms_j

    def get_atoms_index(self):
        return self.atoms_index

    def get_atoms_number(self):
        return self.atoms_number

    def get_atoms_index_j(self):
        return self.atoms_index_j

    def get_atoms_number_j(self):
        return self.atoms_number_j

    def get_nion(self):
        return self.nion

    def get_natom(self):
        return self.natom

    def get_ion(self):
        return self.ion

    def get_ion_local(self):
        return self.ion_local

    def get_selective(self):
        return self.selective

    def get_direct(self):
        return self.direct

    def get_position(self):
        return self.position

    def get_fix(self):
        return self.fix

    def get_ispin(self):
        return self.ispin

    ############################################################################
    # for Method


#    ###################################
#    # natom の Left 版
#    def get_left_natom(self):
#        self.FLAG_left = False
#        self.left_natom = 0
#        comment_reg = re.compile('^#.*',re.IGNORECASE)
#        reg = re.compile('.*LeftLeadAtoms\.Number')
#        for i in range(self.num):
#            if not bool(comment_reg.match(self.datlines[i])):
#                if bool(reg.match(self.datlines[i])):
#                    self.FLAG_left = True
#                    self.left_natom = int(self.datlines[i].split()[1])
#                    break
#        return self.left_natom
#
#    ###################################
#    # Left_atoms_index_j
#    # 通し番号を与えると元素記号を返す
#    # VASP出力は無いので、気にせずにそのまま.dat記述通りに吸い出す
#    def get_left_atoms_index_j(self):
#        self.FLAG_left = False
#        left_natom = self.get_left_natom()
#
#        comment_reg = re.compile('^#.*',re.IGNORECASE)
#        reg0 = re.compile('.*\<LeftLeadAtoms\.SpeciesAndCoordinates')
##       reg1 = re.compile('.*LeadLeftAtoms\.SpeciesAndCoordinates\>')
#
#        self.left_atoms_index_j = []
#        for i in range(self.num):
#            if not bool(comment_reg.match(self.datlines[i])):
#                if bool(reg0.match(self.datlines[i])):
#                    self.FLAG_left = True
#                    for j in range(left_natom):
#                        self.left_atoms_index_j.append(\
#                                self.datlines[i+j+1].split()[1])
#                    break
#        return self.left_atoms_index_j
#
#    ###################################
#    # Left_position
#    # 通し番号を与えると元素記号を返す
#    # VASP出力は無いので、気にせずにそのまま.dat記述通りに吸い出す
#    # self.UNIT を用いるので get_position の後に実行する
#    def get_left_position(self):
#        self.FLAG_left = False
#        left_natom = self.get_left_natom()
#
#        comment_reg = re.compile('^#.*',re.IGNORECASE)
#        reg0 = re.compile('.*\<LeftLeadAtoms\.SpeciesAndCoordinates')
##       reg1 = re.compile('.*LeadLeftAtoms\.SpeciesAndCoordinates\>')
#
#        self.FLAG_left = False
#        self.left_position = np.zeros((left_natom,3))
#        for i in range(self.num):
#            if not bool(comment_reg.match(self.datlines[i])):
#                if bool(reg0.match(self.datlines[i])):
#                    self.FLAG_left = True
#                    for j in range(left_natom):
#                        self.left_position[j,0] = \
#                                float(self.datlines[i+j+1].split()[2])*self.UNIT
#                        self.left_position[j,1] = \
#                                float(self.datlines[i+j+1].split()[3])*self.UNIT
#                        self.left_position[j,2] = \
#                                float(self.datlines[i+j+1].split()[4])*self.UNIT
#                    break
#        return self.left_position
#
#
#    ###################################
#    # natom の Right 版
#    def get_right_natom(self):
#        self.FLAG_right = False
#        self.right_natom = 0
#        comment_reg = re.compile('^#.*',re.IGNORECASE)
#        reg = re.compile('.*RightLeadAtoms\.Number')
#        for i in range(self.num):
#            if not bool(comment_reg.match(self.datlines[i])):
#                if bool(reg.match(self.datlines[i])):
#                    self.FLAG_right = True
#                    self.right_natom = int(self.datlines[i].split()[1])
#                    break
#        return self.right_natom
#
#    ###################################
#    # Right_atoms_index_j
#    # 通し番号を与えると元素記号を返す
#    # VASP出力は無いので、気にせずにそのまま.dat記述通りに吸い出す
#    def get_right_atoms_index_j(self):
#        self.FLAG_right = False
#        right_natom = self.get_right_natom()
#
#        comment_reg = re.compile('^#.*',re.IGNORECASE)
#        reg0 = re.compile('.*\<RightLeadAtoms\.SpeciesAndCoordinates')
#
#        self.right_atoms_index_j = []
#        for i in range(self.num):
#            if not bool(comment_reg.match(self.datlines[i])):
#                if bool(reg0.match(self.datlines[i])):
#                    self.FLAG_right = True
#                    for j in range(right_natom):
#                        self.right_atoms_index_j.append(\
#                                self.datlines[i+j+1].split()[1])
#                    break
#        return self.right_atoms_index_j
#
#    ###################################
#    # Right_position
#    # 通し番号を与えると元素記号を返す
#    # VASP出力は無いので、気にせずにそのまま.dat記述通りに吸い出す
#    # self.UNIT を用いるので get_position の後に実行する
#    def get_right_position(self):
#        self.FLAG_right = False
#        right_natom = self.get_right_natom()
#
#        comment_reg = re.compile('^#.*',re.IGNORECASE)
#        reg0 = re.compile('.*\<RightLeadAtoms\.SpeciesAndCoordinates')
#
#        self.right_position = np.zeros((right_natom,3))
#        for i in range(self.num):
#            if not bool(comment_reg.match(self.datlines[i])):
#                if bool(reg0.match(self.datlines[i])):
#                    self.FLAG_right = True
#                    for j in range(right_natom):
#                        self.right_position[j,0] = \
#                                float(self.datlines[i+j+1].split()[2])*self.UNIT
#                        self.right_position[j,1] = \
#                                float(self.datlines[i+j+1].split()[3])*self.UNIT
#                        self.right_position[j,2] = \
#                                float(self.datlines[i+j+1].split()[4])*self.UNIT
#                    break
#        return self.right_position
#
#

################################################################################
def options():
    import optparse

    name = 'openmx'
    suffix = 'dat'

    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest='INPUT', )
    options, args = parser.parse_args()

    # 'openmx' より最適なデフォルトファイル名の推定ルーチン
    if not os.path.exists(name + '.dat') or not os.path.exists(name + '.dat'):
        name0 = SAEnv.find_datfile('dat')
        if name0 is not None:
            name = name0

    if options.INPUT: name = options.INPUT
    if len(args) > 0: name = args[0]

    if not os.path.exists(name):
        sys.exit("STOP: " + name + " file not found")

    return name, suffix


################################################################################
if __name__ == '__main__':

    name, suffix = options()
    dat = ReadMxDat(name)

    position_max = dat.get_position_max()
    position_min = dat.get_position_min()

    print("%s" % str(dat.title))
    print(" %s" % str(dat.scale))

    #   print ""
    #   print "max_x", position_max[0]
    #   print "max_y", position_max[1]
    #   print "max_z", position_max[2]
    #   print ""
    #   print "min_x", position_min[0]
    #   print "min_y", position_min[1]
    #   print "min_z", position_min[2]

    if dat.t_FLAG:
        print("  %13.9f %13.9f %13.9f" % (dat.t[0, 0], dat.t[1, 0], dat.t[2, 0]))
        print("  %13.9f %13.9f %13.9f" % (dat.t[0, 1], dat.t[1, 1], dat.t[2, 1]))
        print("  %13.9f %13.9f %13.9f" % (dat.t[0, 2], dat.t[1, 2], dat.t[2, 2]))
    else:
        dat.t[1, 0] = 0.0
        dat.t[2, 0] = 0.0
        dat.t[0, 1] = 0.0
        dat.t[2, 1] = 0.0
        dat.t[0, 2] = 0.0
        dat.t[1, 2] = 0.0
        dat.t[0, 0] = abs(position_max[0] - position_min[0]) * 1.20
        dat.t[1, 1] = abs(position_max[1] - position_min[1]) * 1.20
        dat.t[2, 2] = abs(position_max[2] - position_min[2]) * 1.20
        print("  %13.9f %13.9f %13.9f" % (dat.t[0, 0], dat.t[1, 0], dat.t[2, 0]))
        print("  %13.9f %13.9f %13.9f" % (dat.t[0, 1], dat.t[1, 1], dat.t[2, 1]))
        print("  %13.9f %13.9f %13.9f" % (dat.t[0, 2], dat.t[1, 2], dat.t[2, 2]))

    print(" ", end="")
    for i in range(dat.nion):
        print("%s" % str(dat.atoms_index[i]), end="")
    print(" ")

    print(" ", end="")
    for i in range(dat.nion):
        print("%s" % str(dat.atoms[i]), end="")
    print(" ")

    if dat.selective:
        print("Selective Dynamics")
    if dat.direct:
        print("Direct")
    else:
        print("Cartesian")

    for i in range(dat.natom):
        print(" %13.9f %13.9f %13.9f"
              % (dat.position[i, 0], dat.position[i, 1], dat.position[i, 2]), end="")
        if dat.selective:
            print("", end="")
            print("%s %s %s" % (str(dat.fix[i, 0]), str(dat.fix[i, 1]), str(dat.fix[i, 2])), end="")
        print("")

#   for i in range(natom):
#       print fix[i][0], fix[i][1], fix[i][2]
