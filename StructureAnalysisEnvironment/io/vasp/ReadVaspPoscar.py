#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
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
################################################################################
# POSCAR 読み込み class
#
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
# 2018.08.15
#  Python2/3 両対応暫定
#
# 2015.08.25
#  統合化＆Method化でいろいろと分離整理
#
# 2015.08.19
#  原子番号リストを atoms_number_j に保存しておく(通し番号で)
#
# 2015.07.08
#  supercell 対応で sp_j 変数をインスタンス変数化で追加
#
# 2015.07.08
#   method に print_poscar
#             conv_direct2car
#             conv_supercell
#
#   を追加。
#   本格的に ReadPoscar クラスで閉じて仕事できるようにした
#
# 2015.07.06
#  ReadPoscar class のリファクタ
#  超コンパクトな instance をやめて、基本インスタンスで初シリする形に変更
#  データーのパースは instance で、データーの二次処理は Method にする
#  基本的には get_***() しなくても instance.** でインスタンス変数をそのまま使える
#
# 2015.02.12
#  conv_rot_euler(alpha,beta,gamma) method を実装
#  とりあえずは意図したように動く
#  func_rotate.py で定義した関数を色々呼び出す。
#  バグ修正のつもりが一周りして元に戻った
#
# 2015.02.12
#  get_position() の機能を get_fix() と分離した
#  fix はappend するのではなく numpy で初期化に変更
#
# 2015.02.12
#  get_selective() の機能を get_direct() と分離した
#
# 2015.02.09
#  read_poscar.py ( read_poscar_param.py ) をベースに class 化
#  基本的な method は先行する ReadDoscar や ReadOutcar などと同じくする
#
# 2015.01.20
#  gzip 対応版
#
# 2014.10.30 1st
#
################################################################################
from __future__ import print_function

try:
    from ...copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.5"

################################################################################

import sys
import os
import re
# import gzip
import numpy as np

# import SpaceGroup
# Environment as SGE
try:
    # sys.path.append('../..')
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    import StructureAnalysisEnvironment as SAEnv
    from StructureAnalysisEnvironment.io import *
    from StructureAnalysisEnvironment.Method import Method
except ImportError:
    import StructureAnalysisEnvironment as SAEnv
    from StructureAnalysisEnvironment.io import *
    from StructureAnalysisEnvironment.Method import Method


################################################################################
class ReadVaspPoscar(Method):

    ###############################################
    # init and Read POSCAR
    def __init__(self, POSCAR='POSCAR', suffix='.vasp', sort=False, atoms_index=None, code=None):

        self.datlines, self.num = SAEnv.read_dataline(POSCAR)

        self.system = self.datlines[0]
        self.title = self.system
        self.scale = float(self.datlines[1])

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
        # VASP のバージョン番号確認(記号があるか否か)
        #
        i = 5
        atoms = self.datlines[i].split()
        if atoms[0].isdigit():
            self.vasp_version = 4
        else:
            self.vasp_version = 5
        del atoms

        print("vasp version = %s" % self.vasp_version)
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
            # print("atoms_index[%d] = %s" % (i, self.atoms_index[i]))
            self.atoms_number[i] = SAEnv.get_atomic_number1(str(self.atoms_index[i]))

        ###############################################
        # atoms_index の通し番号版
        #    atoms_index_j[i]  : 通し番号(max=natom)を与えると、原子種の元素記号を返す
        self.atoms_index_j = []
        if self.vasp_version == 5:
            for k in range(self.nion):
                for l in range(int(self.atoms[k])):
                    self.atoms_index_j.append(str(self.atoms_index[k]))

        ###############################################
        # atoms_index_j に併せて記号ではなく原子番号で保存しておく配列を用意
        self.atoms_number_j = []
        if self.vasp_version == 5:
            for k in range(self.nion):
                for l in range(int(self.atoms[k])):
                    num0 = SAEnv.get_atomic_number1(str(self.atoms_index[k]))
                    self.atoms_number_j.append(num0)

        ###############################################
        # 全原子数の確認
        self.natom = 0
        for j in range(self.nion):
            sum = int(self.atoms[j])
            self.natom = self.natom + sum

        ###############################################
        # get ion (makes index)
        # ion[j] : 通し番号(max=natom)を与えると原子の種類番号を返す
        #
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
        self.atoms_j = np.zeros(self.natom, dtype=int)
        j = 0
        for ion in range(self.nion):
            for atom in range(self.atoms[ion]):
                self.atoms_j[j] = int(ion)
                j += 1

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
            print("Direct")
            self.__direct = True
        elif bool(car_reg.match(self.datlines[i].split()[0])):
            print("Cartesian")
            self.__direct = False

        ###############################################
        # get atomic coordinate position
        #
        if self.vasp_version == 4:
            i = 5
        else:
            i = 6
        if self.selective: i += 1

        self.position = np.zeros((int(self.natom), 3))
        self.fix = np.zeros((int(self.natom), 3), dtype='S')

        i += 2
        for j in range(self.natom):
            self.position[j, 0] = float(self.datlines[i + j].split()[0])
            self.position[j, 1] = float(self.datlines[i + j].split()[1])
            self.position[j, 2] = float(self.datlines[i + j].split()[2])
            if self.selective:
                if len(self.datlines[i + j].split()) < 6:
                    sys.exit("STOP: corrdinate line Format Error")
                self.fix[j, 0] = str(self.datlines[i + j].split()[3])
                self.fix[j, 1] = str(self.datlines[i + j].split()[4])
                self.fix[j, 2] = str(self.datlines[i + j].split()[5])
        # print j,
        # print " %16.12f %16.12f %16.12f" \
        #        %(self.position[j,0],self.position[j,1],self.position[j,2]),
        # print ""

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
        R = SAEnv.rotate_euler(alpha, beta, gamma)

        # 基本並進ベクトルの変換
        t = self.get_t()

        # print "t"
        # print t
        # print ""

        # t1 = np.matrix( [ t[0,0],t[1,0],t[2,0] ] )
        t1 = np.matrix([t[0, 0], t[0, 1], t[0, 2]])
        t1r = t1 * R
        # print " t1r = %14.8f %14.8f %14.8f" % (t1r[0,0],t1r[0,1],t1r[0,2])

        # t2 = np.matrix( [ t[0,1],t[1,1],t[2,1] ] )
        t2 = np.matrix([t[1, 0], t[1, 1], t[1, 2]])
        t2r = t2 * R
        # print " t2r = %14.8f %14.8f %14.8f" % (t2r[0,0],t2r[0,1],t2r[0,2])

        # t3 = np.matrix( [ t[0,2],t[1,2],t[2,2] ] )
        t3 = np.matrix([t[2, 0], t[2, 1], t[2, 2]])
        t3r = t3 * R
        # print " t3r = %14.8f %14.8f %14.8f" % (t3r[0,0],t3r[0,1],t3r[0,2])

        # print ""

        # オイラー角で基本並進ベクトルを回したときの基本並進ベクトル
        #       R_t = np.matrix([
        #               [ t1r[0,0],t2r[0,0],t3r[0,0] ],
        #               [ t1r[0,1],t2r[0,1],t3r[0,1] ],
        #               [ t1r[0,2],t2r[0,2],t3r[0,2] ]
        #               ])
        R_t = np.matrix([
            [t1r[0, 0], t1r[0, 1], t1r[0, 2]],
            [t2r[0, 0], t2r[0, 1], t2r[0, 2]],
            [t3r[0, 0], t3r[0, 1], t3r[0, 2]]
        ])

        # print "R_t"
        # print R_t

        # 内部座標の変換
        position = self.get_position()
        natom = self.get_natom()
        R_position = np.zeros((natom, 3))
        for j in range(natom):
            p = np.matrix([position[j, 0], position[j, 1], position[j, 2]])
            pr = p * R
            R_position[j, 0] = pr[0, 0]
            R_position[j, 1] = pr[0, 1]
            R_position[j, 2] = pr[0, 2]

        return R_t, R_position

    ############################################################################
    # direct to cartesian method
    ############################################################################

    def conv_direct2car(self, ABS=None):
        """
        Direct 座標を cartesian 座標となる

        :param ABS:  True/False
                     VASP のときは、scale-factor で割った値が座標となる
                     scale-factor=1.0 ならば正しい、cartesian 表記(絶対値表現)となる
                     もし、scale-factor が 1.0 意外ならば VASP だと、実は
                     scale-factor でスケールされている直交座標表現となる
        :return:
        """

        if ABS is not None:
            ABS = False
        else:
            if isinstance(ABS, str):
                if ABS == 'vasp' or ABS == 'VASP':
                    ABS = True

        self.scale, self.__direct = SAEnv.conv_direct2cara(
            ABS,
            self.scale,
            self.t,
            self.natom,
            self.__direct,
            self.position)

    def conv_scale21(self):
        """
        scale factor を 1 に変換する
        :return:
        """
        self.scale = SAEnv.conv_scale21a(self.scale, self.t)

    @property
    def direct(self):
        return self.__direct

    ############################################################################
    # print POSCAR
    def print_poscar(self, outname='POSCAR', STD=True):

        SAEnv.print_poscar(
            outname, STD,
            self.title,
            self.scale,
            self.natom,
            self.nion,
            self.selective,
            self.__direct,
            self.vasp_version,
            self.t,
            self.atoms,
            self.atoms_index,
            self.position,
            self.fix)

    ############################################################################
    # スーパーセル作成 Method
    # 関数版を持ってきただけのやっつけ対応
    def conv_supercell(self, times=(1, 1, 1)):

        super_x = int(times[0])
        super_y = int(times[1])
        super_z = int(times[2])

        # direct --> cartesian
        if self.__direct:
            ABS = True
            self.scale, self.__direct = SAEnv.conv_direct2cara(
                ABS,
                self.scale,
                self.t,
                self.natom,
                self.__direct,
                self.position)

        # super 用の配列
        supers = super_x * super_y * super_x
        sv = np.zeros((supers, 3))  # (super) t
        sp = np.zeros((self.natom * supers, 3))  # (super) position
        ion_sp = np.zeros(self.natom * supers)  # (super) ion
        ion_local_sp = np.zeros(self.natom * supers)  # (super) ion_local
        fix_sp = np.zeros((self.natom * supers, 3), dtype='S')  # (super) fix
        sp_j = np.zeros(self.natom * supers)  # super cell と orijinal cell の対応

        # super 用の内部座標作成
        SAEnv.make_supercell1(
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
            fix_sp)

        # super 用の基本並進ベクトル/原子種数を作る
        SAEnv.make_supercell_param(
            super_x, super_y, super_z,
            self.nion,
            self.atoms,
            self.t)

        self.natom = self.natom * supers

        # cartesian --> direct
        if not self.__direct:
            self.scale, self.__direct = SAEnv.conv_car2direct(
                self.scale,
                self.t,
                self.natom,
                self.__direct,
                sp)

        self.ion = ion_sp
        self.ion_local = ion_local_sp
        self.position = sp
        self.fix = fix_sp
        self.sp_j = sp_j  # super cell と orijinal cell の対応
        # super の通し番号を与えると元cellの通し番号を与える)


################################################################################
if __name__ == '__main__':

    import optparse

    name = 'POSCAR'
    parser = optparse.OptionParser()
    parser.add_option('-i', '--input',
                      dest='INPUT',
                      default=name,
                      )
    options, args = parser.parse_args()
    name = options.INPUT

    poscar = ReadVaspPoscar(name)

    title = poscar.get_title()
    scale = poscar.get_scale()
    t = poscar.get_t()
    vasp = poscar.get_vasp_version()
    nion = poscar.get_nion()
    atoms = poscar.get_atoms()
    atoms_index = poscar.get_atoms_index()
    natom = poscar.get_natom()
    selective = poscar.get_selective()
    direct = poscar.get_direct()
    position = poscar.get_position()
    fix = poscar.get_fix()

    ion = poscar.get_ion()
    ion_local = poscar.get_ion_local()
    atoms_index_j = poscar.get_atoms_index_j()

    #   for i in range(natom):
    #       print i, atoms_index_j[i]

    ############################################################################
    out = sys.stdout

    print("%s" % str(title), file=out)
    print(" %s" % str(scale), file=out)
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
        print(" %13.9f %13.9f %13.9f"
              % (position[j, 0], position[j, 1], position[j, 2]), file=out, end="")
        if selective:
            print("", file=out, end="")
            print("%s %s %s" % (str(fix[j, 0]), str(fix[i, 1]), str(fix[i, 2])), file=out, end="")
        print("", file=out)
    ############################################################################

#   print ion
#   print ion_local
