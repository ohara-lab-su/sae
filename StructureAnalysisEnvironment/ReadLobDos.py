#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
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
################################################################################
#
# 2015.08.26
#   PDOS パートに対応
#
# 2015.06.05 startup
#   TDOS パートのみ対応
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"
################################################################################

#import sys
#import os
#import gzip
import re
#import optparse
import numpy as np

#from copy import deepcopy

import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE

################################################################################
class ReadLobDos(object):

    def __init__(self,name='DOSCAR.lobster'):

        self.datlines,self.num = SAEnv.read_dataline(name)

        self.natom = int(self.datlines[0].split()[0])
        self.title = self.datlines[4]

        self.nspin = int(self.datlines[0].split()[3])
        self.emax = float(self.datlines[5].split()[0])
        self.emin = float(self.datlines[5].split()[1])
        self.nedos = int(self.datlines[5].split()[2])
        self.efermi = float(self.datlines[5].split()[3])

        # total DOS part
        self.eng = np.zeros(self.nedos)
        self.tdos_all = np.zeros((self.nedos, self.nspin))

        for i in range(self.nedos):
            self.eng[i] = float(self.datlines[6+i].split()[0])
            for spin in range(self.nspin):
                self.tdos_all[i,spin] = float(self.datlines[6+i].split()[1+spin*2])

        j0 = 6+i+1

        # partial DOS part
        lm_max = 9 # 最大
        self.pdos_all = np.zeros((self.nedos, lm_max, self.natom, self.nspin))

        self.orbit_index_j = []
        self.atoms_index_j = []
        self.atoms_number_j = np.zeros(self.natom,dtype=int)

        i =0
        for atom in range(self.natom):
            for j in range(self.nedos+1):
                line = self.datlines[j0+i]
                if j == 0:
                    orbit = re.sub('.*Z=.*;','',line).split()
                    atomn = int(re.sub(';.*','',re.sub('.*Z=','',line)))
                    symb = SAEnv.get_atomic_symbol0(atomn)
                    norbit = len(orbit)
                    self.atoms_number_j[atom] = atomn
                    self.atoms_index_j.append(symb)
                    self.orbit_index_j.append(orbit)
                else:
                    pdos = line.split()
                    for orb in range(1,norbit+1):
                        for spin in range(self.nspin):
                            row =  int(orb + (orb - 1 + spin)*(self.nspin -1))
                            self.pdos_all[j-1, orb-1, atom, spin] = float(pdos[row])
                i += 1

        # 中身はMethodで計算される(引数で選択して PDOS を部分的に足し合わせる)
        self.pdos_sum = np.zeros(self.nedos)
        self.ldos = np.zeros(self.nedos)

    ############################################################################
    def get_nedos(self):
        return self.nedos

    def get_nspin(self):
        return self.nspin

    def get_natom(self):
        return self.natom

    def get_atoms_index_j(self):
        return self.atoms_index_j

    def get_atoms_number_j(self):
        return self.atoms_number_j

    def get_orbit_index_j(self):
        return self.orbit_index_j

    def get_eng(self):
        return self.eng

    def get_tdos(self,spin=0):
        if isinstance(spin, str):
            if spin == 'nonmag': spin=0
            if spin == 'non': spin=0
            if spin == 'up': spin=0
            if spin == 'dn': spin=1
            if spin == 'down': spin=1
        return self.tdos_all[:,spin]

    def get_pdos_all(self):
        return self.pdos_all

    def get_pdos(self,lm=0,atom=0,spin=0):
        if isinstance(spin, str):
            if spin == 'nonmag': spin=0
            if spin == 'non': spin=0
            if spin == 'up': spin=0
            if spin == 'dn': spin=1
            if spin == 'down': spin=1
        return self.pdos_all[:,lm,atom,spin]

    ################################################################
    #   0 からスタート
    #   特定原子の特定軌道から特定の軌道までのPDOS成分を足し合わせる
    def get_pdos_sum(self,start,end,atom=0,spin=0):

        if isinstance(spin, str):
            if spin == 'nonmag': spin=0
            if spin == 'non': spin=0
            if spin == 'up': spin=0
            if spin == 'dn': spin=1
            if spin == 'down': spin=1

        for i in range(start,end+1):
            self.pdos_sum[:] = self.pdos_all[:,i,atom,spin] + self.pdos_sum[:]

        return self.pdos_sum

    ################################################################
    #   l軌道に対応するlm軌道成分のリストをorbit_index_jから作成する
    #   PDOS成分の足し合わせ
    #   原子ごと(atomごと) に実際に射影しているlm成分が異なるので
    #   l軌道ごとに毎回調査する必要があるためにこのルーチンを動かす
    def get_ldos(self,l=0,atom=0,spin=0):

        if isinstance(spin, str):
            if spin == 'nonmag': spin=0
            if spin == 'non': spin=0
            if spin == 'up': spin=0
            if spin == 'dn': spin=1
            if spin == 'down': spin=1

        if isinstance(l, int):
            if l == 0: l = 's'
            if l == 1: l = 'p'
            if l == 2: l = 'd'
            if l == 3: l = 'f'

        norbit = len(self.orbit_index_j[atom]) # 計算した lm 成分の数
        orbit_list = []
        for orb in range(norbit):
            orbit = self.orbit_index_j[atom][orb]
            pattern = '.*'+str(l).lower()+'.*'
            if re.match( pattern, orbit):
                orbit_list.append(orb)

        for orb in orbit_list:
            self.ldos[:] = self.pdos_all[:,orb,atom,spin] + self.ldos[:]

        return self.ldos

################################################################################
if __name__ == '__main__':

    dos = SAEnv.ReadLobDos()

    dos.get_ldos()

#   # atom=0, spin=0 の lm: 1 から 3 まで足し合わせた pdos を出力
#   pdos = dos.get_pdos_sum(1,3,atom=0,spin=0)
#   for i in range(dos.nedos):
#       print pdos[i]

#   print "ISPIN:",dos.get_nspin()
#   print "NATOM:",dos.get_natom()
#   print "NEDOS:",dos.get_nedos()



################################################################################

