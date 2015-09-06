#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# ReadLobDos.py
#
#  ROBSTER の DOS 計算の出力である DOSCAR.lobster のパースするクラス
#  基本構造は DOSCAR と同じなのだが、
#
#    1) 原子ごと(natom)に射影している軌道成分の数が異なる
#    2) SPIN 情報が列挙されている
#
#  などの点が本来の DOSCAR と異なり、拡張されている。
#
##########################################################################
#
# 2015.09.07
#  get_pdos() メッソッドの大規模な修正（lm引数モードの大規模修正)
#
# 2015.09.01
#  TDOS パート down-spin にバグ(INT-DOSを読んでいた) を発見、修正
#
# 2015.08.26
#   PDOS パートに対応
#
# 2015.06.05 startup
#   TDOS パートのみ対応
#
##########################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
#
__status__ = "alpha"
__version__ = "0.0.1"
##########################################################################

#import sys
#import os
#import gzip
import re
#import optparse
import numpy as np

#from copy import deepcopy

import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE

##########################################################################


class ReadLobDos(object):

    def __init__(self, name='DOSCAR.lobster'):

        self.datlines, self.num = SAEnv.read_dataline(name)

        self.natom = int(self.datlines[0].split()[0])
        self.title = self.datlines[4]

        self.nspin = int(self.datlines[0].split()[3])
        self.ispin = self.nspin
        self.emax = float(self.datlines[5].split()[0])
        self.emin = float(self.datlines[5].split()[1])
        self.nedos = int(self.datlines[5].split()[2])
        self.efermi = float(self.datlines[5].split()[3])

        self.lorbit = 11 # DOSCAR.lobster は LORBIT11 のみ(変則的)

        # total DOS part
        #  energy  DOS(up) DOS(dwn)  integrated DOS(up) integrated DOS(dwn)
        self.eng = np.zeros(self.nedos)
        self.tdos_all = np.zeros((self.nedos, self.nspin))
        self.inttdos_all = np.zeros((self.nedos, self.nspin))

        for i in range(self.nedos):
            self.eng[i] = float(self.datlines[6 + i].split()[0])
            for spin in range(self.nspin):
                self.tdos_all[i, spin] = \
                             float(self.datlines[6 + i].split()\
                             [1 + spin * (self.nspin - 1)])
                self.inttdos_all[i, spin] = \
                             float(self.datlines[6 + i].split()\
                             [1 + spin * (self.nspin - 1) + self.nspin])

        j0 = 6 + i + 1

        # partial DOS part
        # energy s-DOS(up) s-DOS(down) p-DOS(up) p-DOS(dwn) d-DOS(up) d-DOS(dwn)
        #    _pv などの擬ポテンシャルの時は軌道の数が9を超えるので注意)
        lm_max = 9  # 最大(s, px, py, pz, dxy, dyz, dzx, dx2-y2, d3z2-r2)

        # _pv などの擬ポテンシャル対応
        #    最大のnorbit (lm_max) を求める --> pdos の最大サイズ見積もり
        lm_max = 0
        i = 0
        for atom in range(self.natom):
            for j in range(self.nedos + 1):
                line = self.datlines[j0 + i]
                if j == 0:
                    orbit = re.sub('.*Z=.*;', '', line).split()
                    lm_max0 = len(orbit)
                    if lm_max0 > lm_max:
                        lm_max = lm_max0
                i += 1

        self.pdos_all = np.zeros((self.nedos, lm_max, self.natom, self.nspin))

        self.orbit_index_j = []
        self.atoms_index_j = []
        self.atoms_number_j = np.zeros(self.natom, dtype=int)

        i = 0
        for atom in range(self.natom):
            for j in range(self.nedos + 1):
                line = self.datlines[j0 + i]
                if j == 0:
                    orbit = re.sub('.*Z=.*;', '', line).split()
                    atomn = int(re.sub(';.*', '', re.sub('.*Z=', '', line)))
                    symb = SAEnv.get_atomic_symbol0(atomn)

                    norbit = len(orbit)
                    self.atoms_number_j[atom] = atomn
                    self.atoms_index_j.append(symb)
                    self.orbit_index_j.append(orbit)
                else:
                    pdos = line.split()
                    for orb in range(1, norbit + 1):
                        for spin in range(self.nspin):
                            row = \
                                int(orb + (orb - 1 + spin) * (self.nspin - 1))
                            self.pdos_all[j - 1, orb - 1, atom, spin] \
                                    = float(pdos[row])
                i += 1

        # 中身はMethodで計算される(引数で選択して PDOS を部分的に足し合わせる)
        self.pdos_sum = np.zeros(self.nedos)
        self.ldos = np.zeros(self.nedos)
        self.ldos_all = np.zeros((self.nedos, 3, self.natom, self.nspin))

    ##########################################################################
    def get_nedos(self):
        return self.nedos

    def get_nspin(self):
        return self.nspin

    def get_ispin(self):
        return self.ispin

    def get_natom(self):
        return self.natom

    # 原子ごとの原子種記号リスト
    def get_atoms_index_j(self):
        return self.atoms_index_j

    def get_atoms_number_j(self):
        return self.atoms_number_j

    # 原子ごとの射影軌道リスト
    def get_orbit_index_j(self):
        return self.orbit_index_j

    def get_eng(self):
        return self.eng

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
        return self.tdos_all[:, spin]

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
        return self.inttdos_all[:, spin]

    def get_pdos_all(self):
        return self.pdos_all

    ################################################################
    # 2015.09.07
    #   lm=数字、以外にも軌道成分の記号で指定できるように変更した
    #   主量子数の異なるものは通常は足し合わせる
    #   s 軌道を指定したら 4s と 5s 軌道あったら足し合わせる
    #   もしくは lm の記号に主量子数を付けたとき（ 4s と指定したら）
    #   軌道は主量子数も含めて選択的になる
    #
    def get_pdos(self, lm=0, atom=0, spin=0):

        pdos = np.zeros(self.nedos)

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

        if isinstance(lm, str):

            orbit_name = lm
            lml = lm.lower()

            if lml == 'py':
                orbit_name = 'p_y'
            if lml == 'pz':
                orbit_name = 'p_z'
            if lml == 'px':
                orbit_name = 'p_x'
            if lml == 'dxy' or \
                    lml == 'xy' or \
                    lml == 'yx' or \
                    lml == 'dyx' or \
                    lml == 'd_yx':
                orbit_name = 'd_xy'
            if lml == 'dyz' or \
                    lml == 'yz' or \
                    lml == 'zy' or \
                    lml == 'dzy' or \
                    lml == 'd_zy':
                orbit_name = 'd_yz'
            if lml == 'dz2' or \
                    lml == 'd_z2' or \
                    lml == 'dz^2' or \
                    lml == 'z2' or \
                    lml == 'z^2' or \
                    lml == 'd_3z2' or \
                    lml == 'd3z^2' or \
                    lml == '3z2' or \
                    lml == '3z^2' or \
                    lml == 'r2' or \
                    lml == 'r^2' or \
                    lml == 'dr^2' or \
                    lml == 'd_r^2' or \
                    lml == 'd_r2' or \
                    lml == '3z2-r2' or \
                    lml == '3z^2-r^2' or \
                    lml == 'd_3z2-r2' or \
                    lml == 'd_3z^2-r^2':
                orbit_name = 'd_z^2'
            if lml == 'dxz' or \
                    lml == 'xz' or \
                    lml == 'dzx' or \
                    lml == 'zx' or \
                    lml == 'd_zx':
                orbit_name = 'd_xz'
            if lml == 'x^2-y^2' or \
                    lml == 'd_x2-y2' or \
                    lml == 'x2-y2' or \
                    lml == 'dx2' or \
                    lml == 'x2' or \
                    lml == 'x^2' or \
                    lml == 'dx^2' or \
                    lml == 'dy2' or \
                    lml == 'y2' or \
                    lml == 'y^2' or \
                    lml == 'dy^2':
                orbit_name = 'd_x^2-y^2'

            lm = -1
            for orbit in self.orbit_index_j[atom]:
                lm += 1
                if re.match('^\d'+orbit_name, orbit):
                    pdos[:] = self.pdos_all[:, lm, atom, spin]
#                   print lm,orbit_name
        else:
            pdos[:] = self.pdos_all[:, lm, atom, spin]

        return pdos

    ################################################################
    #   0 からスタート
    #   特定原子の特定軌道から特定の軌道までのPDOS成分を足し合わせる
    def get_pdos_sum(self, start, end, atom=0, spin=0):

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

        for i in range(start, end + 1):
            self.pdos_sum[:] = \
                    self.pdos_all[:, i, atom, spin] + self.pdos_sum[:]

        return self.pdos_sum

    ################################################################
    #   l軌道に対応するlm軌道成分のリストをorbit_index_jから作成する
    #   PDOS成分の足し合わせ
    #   原子ごと(atomごと) に実際に射影しているlm成分が異なるので
    #   l軌道ごとに毎回調査する必要があるためにこのルーチンを動かす
    def get_ldos(self, l=0, atom=0, spin=0):

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

        if isinstance(l, int):
            if l == 0:
                l = 's'
            if l == 1:
                l = 'p'
            if l == 2:
                l = 'd'
            if l == 3:
                l = 'f'

        ldos = np.zeros(self.nedos)
        norbit = len(self.orbit_index_j[atom])  # 計算した lm 成分の数
        orbit_list = []
        for orb in range(norbit):
            orbit = self.orbit_index_j[atom][orb]
            pattern = '.*' + str(l).lower() + '.*'
            if re.match(pattern, orbit):
                orbit_list.append(orb)

        for orb in orbit_list:
            ldos[:] = self.pdos_all[:, orb, atom, spin] + ldos[:]

        self.ldos = ldos
        del ldos

        return self.ldos

    # get_ldos を原子種、スピンごとにすべて行う
    def get_ldos_all(self):

        ldos_all = np.zeros((self.nedos, 3, self.natom, self.nspin))

        for atom in range(self.natom):
            norbit = len(self.orbit_index_j[atom])
#           print norbit,self.orbit_index_j[atom]
            orbit_list_s = []
            orbit_list_p = []
            orbit_list_d = []
            orbit_list_f = []

            for orb in range(norbit):
                orbit = self.orbit_index_j[atom][orb]
                pattern_s = '.*s.*'
                pattern_p = '.*p.*'
                pattern_d = '.*d.*'
                pattern_f = '.*f.*'
                if re.match(pattern_s, orbit): orbit_list_s.append(orb)
                if re.match(pattern_p, orbit): orbit_list_p.append(orb)
                if re.match(pattern_d, orbit): orbit_list_d.append(orb)
                if re.match(pattern_f, orbit): orbit_list_f.append(orb)

            for orb in orbit_list_s:
                ldos_all[:, 0, atom, :] = \
                       self.pdos_all[:, orb, atom, :] + ldos_all[:, 0, atom, :]
            for orb in orbit_list_p:
                ldos_all[:, 1, atom, :] = \
                       self.pdos_all[:, orb, atom, :] + ldos_all[:, 1, atom, :]
            for orb in orbit_list_d:
                ldos_all[:, 2, atom, :] = \
                       self.pdos_all[:, orb, atom, :] + ldos_all[:, 2, atom, :]
            for orb in orbit_list_f:
                ldos_all[:, 3, atom, :] = \
                       self.pdos_all[:, orb, atom, :] + ldos_all[:, 3, atom, :]

        self.ldos_all = ldos_all
        del ldos_all

        return self.ldos_all

    def print_doscar(self):
        pass

##########################################################################
if __name__ == '__main__':

    dos = SAEnv.ReadLobDos()

#   dos.get_ldos()
#   dos.get_ldos_all()
    dos.get_pdos(lm = 'px')
#   dos.get_pdos(lm = 'r2')

#   # atom=0, spin=0 の lm: 1 から 3 まで足し合わせた pdos を出力
#   pdos = dos.get_pdos_sum(1,3,atom=0,spin=0)
#   for i in range(dos.nedos):
#       print pdos[i]

#   print "ISPIN:",dos.get_nspin()
#   print "NATOM:",dos.get_natom()
#   print "NEDOS:",dos.get_nedos()


##########################################################################
