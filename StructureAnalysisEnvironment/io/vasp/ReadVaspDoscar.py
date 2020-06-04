#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# VASP
#
#  DOSCAR 読み込みクラス
#   SPIN 情報対応の DOSCAR 読み込みには かならず DOSCAR or vasprun.xml が
#   必要となる
#
##########################################################################
#
# 2018.08.15
#  Python2/3 両対応暫定
#
# 2015.10.28
#  VBM を取得するためのルーチン追加
#
# 2015.10.28
#  軌道成分の対応を f 軌道まで拡張,および一般化
#
# 2015.08.17
#   古いバージョンをブランチ(動作版のバックアップ)
#   新しいブランチ版はインスタンス重視に切り替える
#   ---> ほぼ全面書き直し(昔のスタイルに戻る)
#
# 2015.06.24
#  if statement を少し書き直し
#
# 2015.06.15
#  get_ldos(orbit.atom,spin)
#  にて、orbit に s,p,d 記号でも入力が出来るようにした
#
# 2015.02.25
#  get_emin() で用いているインスタンス変数名を変更
#
# 2015.01.28
#  title の取得における末尾までの空白削除を追加
#
# 2015.01.14
#    PDOS, PDOS_ALL まわりのバグ修正
#
# 2015.01.14
#    get_pdos_all と作成
#    get_pdos におけるループ構造をシンプル化(高速化)
#
# 2015.01.14
#    高速化のために LDOS(get_ldos) と LDOS_ALL(get_ldos_all) の構造を変えた
#    LDOS での無駄な LDOS_ALL 相当のループを排除
#    (ATOM非対応版のときと似たような構造に戻す)
#
# 2015.01.14
#    spin 有りの時に関して致命的なバグ(データー構造そのものの勘違い)
#    を発見したので抜本的に修正
#    正) spin は交互に並ぶ==> s-up,s-down,p-up,p-down の並びになる
#    拙作、Vldos.pl とほぼ同じアルゴリズムに変更
#
# 2015.01.13
#    get_ldos_ion(self,oname,l,spin) Method 追加
#    oname='OUTCAR' を読んでパラメーターをゲットして
#    原子の種類ごとの ldos を取る
#
# 2015.01.13
#
#    dos = ReadDoscar(name)
#    dos.get_LDOS()
#    --> このMethod呼び出し処理がとてつもなく遅いのに気がつく
#        おそらく私のコーディングがアホな（python OOP の理解が足りない）せい
#        多数の原子で毎回呼び出すと信じられないくらい遅い
#        暫定的にプロットの方のルーチンで全原子の描画をしないように変更
#
#    メッソッド名に get_ を追加(変数名との住み分けの容易化のため)
#
#    get_ldos_all メッソッドを追加(メッソド名と戻り値が異なるだけ)
#
#
# 2015.01.11 (sun)
#    細かい修正,まったりと作成
#    全種類の ATOM に対応
#
# 2015.01.10 (sat)
#    基本機能はほぼ完成,まったりと作成
#    ATOM =1 のみ対応
#
# 2015.01.09 1st
#    テスト用テストプログラム(所信表明+ひな形作り始め)
#
##########################################################################
from __future__ import print_function
try:
    from ...copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.1.00"
##########################################################################

import sys
#import os
#import gzip
import re
import numpy as np

#from copy import deepcopy

try:
    sys.path.append('../../')
    import StructureAnalysisEnvironment as SAEnv
    from StructureAnalysisEnvironment.Method import *
except ImportError:
    import StructureAnalysisEnvironment as SAEnv
    from StructureAnalysisEnvironment.Method import *
#import SpaceGroupEnvironment as SGE

##########################################################################


class ReadVaspDoscar(object):

    def __init__(self, name='DOSCAR'):

        self.datlines, self.num = SAEnv.read_dataline(name)

        self.natom = int(self.datlines[0].split()[0])  # VASP正式では NSIONS
        self.title = re.sub(' *$', '', str(self.datlines[4]))  # SYSTEM

        self.emax = float(self.datlines[5].split()[0])  # EMAX
        self.emin = float(self.datlines[5].split()[1])  # EMIN
        self.nedos = int(self.datlines[5].split()[2])  # NEDOS
        self.efermi = float(self.datlines[5].split()[3])  # EFERMI (for TDOS)

        # DOSCAR のTOTAL-DOS 情報列からspin情報を推測する
        if len(self.datlines[7].split()) >= 4:  # 4列以上だと SPIN ありは確実
            self.nspin = 2
        else:
            self.nspin = 1
        self.ispin = self.nspin

        # l 分解 or lm 分解のチェック(一番最後の行でチェックする)
        if len(self.datlines[6 + self.nedos + 1].split()) >= 10:
            self.lorbit = 11  # or 1
        else:
            self.lorbit = 10  # or 0

        # lmax の取得 (atom 毎でチェックして、最大の値が全体に適応される)
        #
        #  5 = 1(ene) +  4 ( s1 + p3 )             --> l_max = 1, nonmag
        # 10 = 1(ene) +  9 ( s1 + p3 + d5 )        --> l_max = 2, nonmag
        # 17 = 1(ene) + 16 ( s1 + p3 + d5 + f7 )   --> l_max = 3, nonmag
        #
        #  9 = 1(ene) +  8 ( s1 + p3 )*2           --> l_max = 1, spin
        # 19 = 1(ene) + 18 ( s1 + p3 + d5 )*2      --> l_max = 2, spin
        # 33 = 1(ene) + 32 ( s1 + p3 + d5 + f7 )*2 --> l_max = 3, spin
        #
        lm_num = 0
        for atom0 in range(self.natom):
            _lm_num  = len(self.datlines
                         [6 + self.nedos * (atom0+ 1 ) + 1 +atom0].split())
            if lm_num < _lm_num:
                lm_num = _lm_num

        # l_max と spin の見積もり
        if lm_num == 5:
            self.lmax = 1
            _spin = 1
        elif lm_num == 10:
            self.lmax = 2
            _spin = 1
        elif lm_num == 17:
            self.lmax = 3
            _spin = 1
        elif lm_num == 9:
            self.lmax = 1
            _spin = 2
        elif lm_num == 19:
            self.lmax = 2
            _spin = 2
        elif lm_num == 33:
            self.lmax = 3
            _spin = 2
        if not _spin == self.nspin:
            sys.exit("STOP: inconsistency  spin")

        lm_max = 0
        for l in range(self.lmax+1):
            lm_max += ( 2*l +1 )*self.nspin
       #print 'l_max', self.lmax
       #print 'lm_max', lm_max

        #######################################################################
        # for DOS , atom と spin は 0 から始める(spin=0 --> up-spin)
        #
       #l_max = 3
       #if self.lorbit >= 11:
       #    lm_max = 9
       #else:
       #    lm_max = 3

        self.eng = np.zeros((self.nedos))

        self.tdos_all = np.zeros((self.nedos, self.nspin))
        self.inttdos_all = np.zeros((self.nedos, self.nspin))

        self.pdos_all = np.zeros((self.nedos, lm_max, self.natom, self.nspin))
        self.ldos_all = np.zeros((self.nedos, self.lmax+1, self.natom, self.nspin))

        for i in range(self.nedos):
            self.eng[i] = float(self.datlines[6 + i].split()[0])  # from TDOS

            dos_line = self.datlines[6 + i].split()

            if self.nspin >= 2:
                self.tdos_all[i, 0] = float(dos_line[1])  # up-sin
                self.tdos_all[i, 1] = float(dos_line[2])  # down-spin
                self.inttdos_all[i, 0] = float(dos_line[3])
                self.inttdos_all[i, 1] = float(dos_line[4])
            else:
                self.tdos_all[i, 0] = float(dos_line[1])
                self.inttdos_all[i, 0] = float(dos_line[2])


            for atom0 in range(self.natom):

                tmp = self.datlines[6 + self.nedos *
                                    (atom0 + 1) + 1 + i + atom0].split()

                if self.lorbit >= 11:
                    f = 1

                    if self.lmax >= 0:
                        # 0:s
                        for lm in range(0, 1):
                            for ispin in range(self.nspin):
                                self.pdos_all[i, lm, atom0, ispin] = float(tmp[f])
                                self.ldos_all[i, 0, atom0, ispin] = \
                                    self.ldos_all[i, 0, atom0, ispin] \
                                    + float(tmp[f])
                                f += 1

                    if self.lmax >= 1:
                        # 1:p_y,2:p_z,3:p_x
                        for lm in range(1, 4):
                            for ispin in range(self.nspin):
                                self.pdos_all[i, lm, atom0, ispin] = float(tmp[f])
                                self.ldos_all[i, 1, atom0, ispin] = \
                                    self.ldos_all[i, 1, atom0, ispin] \
                                    + float(tmp[f])
                                f += 1

                    if self.lmax >= 2:
                        # 4:d_xy,5:d_yz,6:d_3z2-r2,7:d_xz,8:d_x2-y2
                        for lm in range(4, 9):
                            for ispin in range(self.nspin):
                                self.pdos_all[i, lm, atom0, ispin] = float(tmp[f])
                                self.ldos_all[i, 2, atom0, ispin] = \
                                    self.ldos_all[i, 2, atom0, ispin] \
                                    + float(tmp[f])
                                f += 1

                    if self.lmax >= 3:
                        # 5: f-orbitals
                        for lm in range(9, 16):
                            for ispin in range(self.nspin):
                                self.pdos_all[i, lm, atom0, ispin] = float(tmp[f])
                                self.ldos_all[i, 3, atom0, ispin] = \
                                    self.ldos_all[i, 3, atom0, ispin] \
                                    + float(tmp[f])
                                f += 1

                else:
                    f = 1
                    for lm in range(self.lmax+1):
                        # 0:eng
                        # 1:lm=0: s
                        # 2:lm=1: p
                        # 3:lm=2: d
                        # 5:lm=4: f
                        for ispin in range(self.nspin):
                            self.pdos_all[i, lm, atom0, ispin] = float(tmp[f])
                            f += 1

                    self.ldos_all = self.pdos_all

            # default
            self.tdos = self.tdos_all[:, 0] # default spin=0
            self.inttdos = self.inttdos_all[:, 0] # default spin=0

    ##########################################################################
    ## EF 近傍の0.2 eV で VBM を探す
    def get_vbm(self,spin=0):
        METAL = True
        EPS = 0.00001

        for i in range(self.nedos):
            if abs(self.eng[i] - self.efermi) <= 0.2:

                if self.tdos_all[i,spin] < EPS:
                    METAL = False
                    self.e_vbm = float(self.eng[i-1])
                    break
                   #vbm_tdos = self.tdos_all[i-1,spin]

       #print "METAL=",METAL
        if not METAL:
            pass
           #print "E(VBM) = ",self.e_vbm
           #print "E(VBM) - EF = ",self.e_vbm -self.efermi
        else:
            self.e_vbm = 0.0

        return self.e_vbm

    ##########################################################################
    def get_lmax(self):
        return self.lmax

    def get_ispin(self):
        return self.nspin

    def get_natom(self):
        return self.natom

    def get_title(self):
        return self.title

    def get_system(self):
        return self.title

    def get_emax(self):
        return self.emax

    def get_emin(self):
        return self.emin

    def get_nedos(self):
        return self.nedos

    def get_efermi(self):
        return self.efermi

    def get_lorbit(self):
        return self.lorbit

    def get_eng(self):
        return self.eng

    ##########################################################################
    def get_ldos_all(self):
        return self.ldos_all

    def get_pdos_all(self):
        return self.pdos_all

    def get_tdos(self, spin=0):
        if isinstance(spin, str):
            if spin == 'nonmag':
                spin = 0
            if spin == 'non':
                spin = 0
            if spin == 'up':
                spin = 0
            if spin == 'dn':
                spin = 1
            if spin == 'down':
                spin = 1
        self.tdos = self.tdos_all[:, spin]
        return self.tdos

    def get_inttdos(self, spin=0):
        if isinstance(spin, str):
            if spin == 'nonmag':
                spin = 0
            if spin == 'non':
                spin = 0
            if spin == 'up':
                spin = 0
            if spin == 'dn':
                spin = 1
            if spin == 'down':
                spin = 1
        self.inttdos = self.inttdos_all[:, spin]
        return self.inttdos

    def get_pdos(self, lm=0, atom=0, spin=0):
        if isinstance(spin, str):
            if spin == 'nonmag':
                spin = 0
            if spin == 'non':
                spin = 0
            if spin == 'up':
                spin = 0
            if spin == 'dn':
                spin = 1
            if spin == 'down':
                spin = 1
        self.pdos = self.pdos_all[:, lm, atom, spin]
        return self.pdos

    def get_ldos(self, l=0, atom=0, spin=0):
        if isinstance(l, str):
            if l == 's':
                l = 0
            if l == 'p':
                l = 1
            if l == 'd':
                l = 2
            if l == 'f':
                l = 3
        if isinstance(spin, str):
            if spin == 'nonmag':
                spin = 0
            if spin == 'non':
                spin = 0
            if spin == 'up':
                spin = 0
            if spin == 'dn':
                spin = 1
            if spin == 'down':
                spin = 1
        self.ldos = self.ldos_all[:, l, atom, spin]
        return self.ldos

    ##########################################################################
    # TDOS_spd, (すべての原子種のs,p,d を足し合わせる,物理的にはほとんど意味が無い解析)
    def get_tdos_spd(self, l=0, spin=0):

        if isinstance(l, str):
            if l.upper() == 'S':
                l = 0
            if l.upper() == 'P':
                l = 1
            if l.upper() == 'D':
                l = 2
            if l.upper() == 'F':
                l = 3

       #l_max = 3
        tdos_spd = np.zeros((self.nedos, self.lmax+1, self.nspin))

        for atom0 in range(self.natom):
            if self.lorbit >= 11:
                if self.lmax >= 0:
                    for lm in range(0, 1):
                        for ispin in range(self.nspin):
                            tdos_spd[:, 0, ispin] = \
                                tdos_spd[:, 0, ispin] + \
                                self.pdos_all[:, lm, atom0, ispin]
                if self.lmax >= 1:
                    for lm in range(1, 4):
                        for ispin in range(self.nspin):
                            tdos_spd[:, 1, ispin] = \
                                tdos_spd[:, 1, ispin] + \
                                self.pdos_all[:, lm, atom0, ispin]
                if self.lmax >= 2:
                    for lm in range(4, 9):
                        for ispin in range(self.nspin):
                            tdos_spd[:, 2, ispin] = \
                                tdos_spd[:, 2, ispin] + \
                                self.pdos_all[:, lm, atom0, ispin]
                if self.lmax >= 3:
                    for lm in range(9, 16):
                        for ispin in range(self.nspin):
                            tdos_spd[:, 3, ispin] = \
                                tdos_spd[:, 3, ispin] + \
                                self.pdos_all[:, lm, atom0, ispin]

            else:
                for l in range(self.lmax+1):
                    for ispin in range(self.nspin):
                        tdos_spd[:, l, ispin] = \
                            tdos_spd[:, l, ispin] + \
                            self.pdos_all[:, l, atom0, ispin]

        self.tdos_spd = tdos_spd[:, l, spin]
        return self.tdos_spd

    ##########################################################################
    # LDOS_ion (サイトごとのLDOSを取る), ReadOutcar.py を読む
    # atom の情報を ion の情報へ落としているので atom の loop は必須
    # 注意) ion は 0,1,2,,,,n
    #       spin は 0 から始める (spin=0 --> up-spin)
    def get_ldos_ion(self, l=0, ion=0, spin=0):

        if isinstance(spin, str):
            if spin == 'nonmag':
                spin = 0
            if spin == 'non':
                spin = 0
            if spin == 'up':
                spin = 0
            if spin == 'dn':
                spin = 1
            if spin == 'down':
                spin = 1

        oname = 'OUTCAR'

        import StructureAnalysisEnvironment as SAEnv
        outcar = SAEnv.ReadVaspOutcar(oname)
        NATOM = outcar.get_natom()
        NION = outcar.get_nion()
        ATOMS_J = outcar.get_atoms_j()

       #l_max = 3
        ldos_ion = np.zeros((self.nedos, self.lmax+1 , NION, self.nspin))

        for atom in range(NATOM):
            ion1 = ATOMS_J[atom]
            if self.lorbit >= 11:
                if self.lmax >= 0:
                    for lm in range(0, 1):
                        for ispin in range(self.nspin):
                            ldos_ion[:, 0, ion1, ispin] = \
                                ldos_ion[:, 0, ion1, ispin] + \
                                self.pdos_all[:, lm, atom, ispin]
                if self.lmax >= 1:
                    for lm in range(1, 4):
                        for ispin in range(self.nspin):
                            ldos_ion[:, 1, ion1, ispin] = \
                                ldos_ion[:, 1, ion1, ispin] + \
                                self.pdos_all[:, lm, atom, ispin]
                if self.lmax >= 2:
                    for lm in range(4, 9):
                        for ispin in range(self.nspin):
                            ldos_ion[:, 2, ion1, ispin] = \
                                ldos_ion[:, 2, ion1, ispin] + \
                                self.pdos_all[:, lm, atom, ispin]
                if self.lmax >= 3:
                    for lm in range(9, 16):
                        for ispin in range(self.nspin):
                            ldos_ion[:, 3, ion1, ispin] = \
                                ldos_ion[:, 3, ion1, ispin] + \
                                self.pdos_all[:, lm, atom, ispin]
            else:
                for l in range(self.lmax+1):
                    for ispin in range(self.nspin):
                        ldos_ion[:, l, ion1, ispin] = \
                            ldos_ion[:, l, ion1, ispin] + \
                            self.pdos_all[:, l, atom, ispin]

        self.ldos_ion = ldos_ion[:, l, ion, spin]
        return self.ldos_ion

    ##########################################################################
    # LDOS_ion (サイトごとのLDOSを取る), ReadOutcar.py を読む
    # LDOS_ion とくらべて method 名と、戻り値だけが異なる
    # atom の情報を ion の情報へ落としているので atom の loop は必須
    # 注意) ion は 0,1,2,,,,n
    #       spin は 0 から始める (spin=0 --> up-spin)
    def get_ldos_ion_all(self):

        oname = 'OUTCAR'

        import StructureAnalysisEnvironment as SAEnv
        outcar = SAEnv.ReadVaspOutcar(oname)
        NATOM = outcar.get_natom()
        NION = outcar.get_nion()
        ATOMS_J = outcar.get_atoms_j()

       #l_max = 3
        ldos_ion = np.zeros((self.nedos, self.lmax+1, NION, self.nspin))

        for atom in range(NATOM):
            ion1 = ATOMS_J[atom]
            for i in range(self.nedos):
                if self.lorbit >= 11:
                    if self.lmax >= 0:
                        for lm in range(0, 1):
                            for ispin in range(self.nspin):
                                ldos_ion[:, 0, ion1, ispin] = \
                                    ldos_ion[:, 0, ion1, ispin] + \
                                    self.pdos_all[:, lm, atom, ispin]
                    if self.lmax >= 1:
                        for lm in range(1, 4):
                            for ispin in range(self.nspin):
                                ldos_ion[:, 1, ion1, ispin] = \
                                    ldos_ion[:, 1, ion1, ispin] + \
                                    self.pdos_all[:, lm, atom, ispin]
                    if self.lmax >= 2:
                        for lm in range(4, 9):
                            for ispin in range(self.nspin):
                                ldos_ion[:, 2, ion1, ispin] = \
                                    ldos_ion[i, 2, ion1, ispin] + \
                                    self.pdos_all[:, lm, atom, ispin]
                    if self.lmax >= 3:
                        for lm in range(9, 16):
                            for ispin in range(self.nspin):
                                ldos_ion[:, 3, ion1, ispin] = \
                                    ldos_ion[i, 3, ion1, ispin] + \
                                    self.pdos_all[:, lm, atom, ispin]
                else:
                    for l in range(self.lmax+1):
                        for ispin in range(self.nspin):
                            ldos_ion[:, l, ion1, ispin] = \
                                ldos_ion[:, l, ion1, ispin] + \
                                self.pdos_all[:, lm, atom, ispin]

        self.ldos_ion_all = ldos_ion
        return self.ldos_ion_all


##########################################################################
if __name__ == '__main__':

    import optparse
    name = 'DOSCAR'

    parser = optparse.OptionParser()
    parser.add_option('-i', '--input',
                      dest='INPUT',
                      default=name,
                      )
    options,  args = parser.parse_args()

    if options.INPUT:
        name = options.INPUT

    if len(args) > 0:
        name = args[0]

    dos = ReadVaspDoscar(name)

    NSPIN = dos.get_ispin()
    LORBIT = dos.get_lorbit()
    NATOM = dos.get_natom()
    TITLE = dos.get_title()
    EMAX = dos.get_emax()
    EMIN = dos.get_emin()
    NEDOS = dos.get_nedos()
    EFERMI = dos.get_efermi()

    print("ISPIN  = %s %s" % (str(dos.nspin), str(NSPIN)))
    print("LORBIT = %s %s" % (str(dos.lorbit), str(LORBIT)))
    print("NATOM  = %s %s" % (str(dos.natom), str(NATOM)))
    print("TITLE  = %s %s" % (str(dos.title), str(TITLE)))
    print("EMAX   = %s %s" % (str(dos.emax), str(EMAX)))
    print("EMIN   = %s %s" % (str(dos.emin), str(EMIN)))
    print("NEDOS  = %s %s" % (str(dos.nedos), str(NEDOS)))
    print("EFERMI = %s %s" % (str(dos.efermi), str(EFERMI)))

    dos.get_vbm()

    ENG = dos.get_eng()
   # TDOS = dos.get_tdos(0)                   # spin=0 (up-spin)
    TDOS = dos.get_tdos(spin=0)              # spin=0 (up-spin)

   # INTTDOS = dos.get_inttdos(0)             # spin=0 (up-spin)
    INTTDOS = dos.get_inttdos(spin=0)        # spin=0 (up-spin)


#   LDOS_ION = dos.get_ldos_ion(l=0,ion=4,spin=1)
#   for i in range(NEDOS):
#       print "%12.8f %12.8f" %( ENG[i],LDOS_ION[i] )

#   lm=0
#   atom=0
#   spin=0
#  #spin=1
#   PDOS = dos.get_pdos(lm=lm,atom=atom,spin=spin)
#   for i in range(NEDOS):
#       print "%12.8f %12.8f" %( ENG[i]-EFERMI,PDOS[i] )


##########################################################################
