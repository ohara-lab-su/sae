#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# ReadLobCohp.py
#  ROBSTER の pCOHP 計算の出力である COHPCAR.lobster のパースするクラス
#
################################################################################
#
# 2015.08.25
#   あらゆるタイプのCOHPデータを読めるように変更
#   (ボンドタイプの数をカウントする)
#
# 2015.06.05
#   startup
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

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
class ReadLobCohp(object):

    def __init__(self,name='COHPCAR.lobster'):

        self.datlines,self.num = SAE.read_dataline(name)
        self.nedos = int(self.datlines[1].split()[2])

        self.nbond = int(self.datlines[1].split()[0])
        self.nspin = int(self.datlines[1].split()[1])

        self.eng = np.zeros(self.nedos)

        # nbond = 0 のときを Average とする
        self.cohp_all = np.zeros((self.nedos,self.nbond,self.nspin))
        self.icohp_all = np.zeros((self.nedos,self.nbond,self.nspin))

        self.bond_index = [''] * (self.nbond)
        self.bond_leng = np.zeros(self.nbond)

        # ボンドの各情報(ボンドしている原子のペア、平均値、最大のボンド)
        self.bond_index[0] = 'Average'
        leng0 = 0
        self.bond_max_index = 0
        for i in range(1,self.nbond):
            char0 = self.datlines[i+2].split()[0]
            char1 = re.sub('^.*:','',char0)
            self.bond_index[i] = re.sub('\(.*','',char1)
            length = float(re.sub('\)','',re.sub('^.*\(','',char0)).strip())
            if leng0 < length:
                leng0 = length
                self.bond_max_index = i
            self.bond_leng[i] = length

#       print self.bond_max_index,self.bond_index[self.bond_max_index],\
#                                  self.bond_leng[self.bond_max_index]
#       for i in range(self.nbond):
#           print self.bond_index[i],':',self.bond_leng[i]

        for i in range(self.nedos):

            line = i+2+self.nbond
            self.eng[i] = float(self.datlines[line].split()[0])

            for ispin in range(self.nspin):
                for bond in range(self.nbond):

                    row0 = 1+2*bond + ispin*(2*self.nbond)
                    row1 = 2+2*bond + ispin*(2*self.nbond)

                    self.cohp_all[i,bond,ispin] = \
                            float(self.datlines[line].split()[row0])
                    self.icohp_all[i,bond,ispin] = \
                            float(self.datlines[line].split()[row1])

    ############################################################################

    def get_nedos(self):
        return self.nedos

    def get_nspin(self):
        return self.nspin

    def get_nbond(self):
        return self.nbond

    def get_bond_index(self): # 全ボンドペアの原子種の情報(0番はAverage)
        return self.bond_index

    def get_bond_max_index(self): # 最大のボンド長を持つ原子ペアの添え字
        return self.bond_max_index

    def get_bond_leng(self): # 全ボンドペアの平均値
        return self.bond_leng

    def get_eng(self):
        return self.eng

    ###################
    # pCOHP の平均
    #
    def get_ave(self,spin=0):
        if isinstance(spin, str):
            if spin == 'nonmag': spin=0
            if spin == 'non': spin=0
            if spin == 'up': spin=0
            if spin == 'dn': spin=1
            if spin == 'down': spin=1
        self.ave = self.cohp_all[:,0,spin]
        return self.ave

    ###################
    # pCOHP 積分の平均
    #
    def get_iave(self,spin=0):
        if isinstance(spin, str):
            if spin == 'nonmag': spin=0
            if spin == 'non': spin=0
            if spin == 'up': spin=0
            if spin == 'dn': spin=1
            if spin == 'down': spin=1
        self.ave = self.icohp_all[:,0,spin]
        return self.ave

    ###################
    # pCOHP ボンドごと
    #
    def get_cohp(self,bond=0,spin=0): # bond=0 は平均
        if isinstance(spin, str):
            if spin == 'nonmag': spin=0
            if spin == 'non': spin=0
            if spin == 'up': spin=0
            if spin == 'dn': spin=1
            if spin == 'down': spin=1
        self.cohp = self.cohp_all[:,bond,spin]
        return self.cohp

    ###################
    # pCOHP 積分のボンドごと
    #
    def get_icohp(self,bond=0,spin=0):  # bond=0 は平均
        if isinstance(spin, str):
            if spin == 'nonmag': spin=0
            if spin == 'non': spin=0
            if spin == 'up': spin=0
            if spin == 'dn': spin=1
            if spin == 'down': spin=1
        self.icohp = self.icohp_all[:,bond,spin]
        return self.icohp

################################################################################
if __name__ == '__main__':


    cohp = ReadLobCohp()

    bond1 = cohp.get_cohp(bond=1,spin=0)  # bond=0 は平均値
#   nedos = cohp.get_nedos()
#   eng = cohp.get_eng()
#   ave = cohp.get_ave()

#   for i in range(nedos):
#       print eng[i],ave[i]


################################################################################

