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
###############################################################################
#
# *.cfg ファイル読み込み
#
################################################################################
# [in/out] atoms[i]  : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
# [in/out] atoms_j[i]: 原子の通し番号を与えると、原子のサイト番号を与える
#                      [注意] *.cfg形式は種類を与えないので 0 番から違う種類毎
#                             に(仮に)無理やりナンバリングする
#
# [in/out] t[3,3]         :  基本並進ベクトル(注意:配列内indexは0から)
#                                  x   y   z
#                            t1 = a11 a21 a31
#                            t2 = a12 a22 a32
#                            t3 = a13 a23 a33
#
# [in/out] position[j,3]  : 通し番号(max=natom)とx,y,z 指定で内部座標
#
################################################################################
#
# 2015.08.24
#  統合化を前提として、基本並進ベクトルおよび内部座標の保存をRMC_POT形式
#  ではなく、デフォルトで VASP 形式とする
#
# 2015.07.16 startup
#
################################################################################
from __future__ import print_function
###############################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"
################################################################################

#import sys
#import os
import numpy as np
import StructureAnalysisEnvironment as SAEnv

################################################################################
class ReadRmcpotCfg(SAEnv.Method):

    def __init__(self,cname='POSCAR.cfg',suffix='.cfg',sort=False,atoms_index=None):

#       if suffix is not None: cname = cname+suffix
        self.datlines, self.num = SAEnv.read_dataline(cname)

        ###############################################
        # Read Parameter
        self.header = str(self.datlines[0])
        self.comment = str(self.datlines[1])
        self.title = self.comment
        self.system = self.title
        self.moves = self.datlines[4] # RMC
        self.saved = self.datlines[5] # RMC
        self.natom = int(self.datlines[7].split()[0])
        self.nion = int(self.datlines[8].split()[0])
        self.nmoles = self.datlines[9] # RMC
        self.angles = self.datlines[10] # RMC

        # dummy parameter
        self.vasp_version = 5
        self.direct = True # cfg は in/out 共に direct を想定
        self.selective = False
        self.scale = 1.0   # cfg は scale 1.0 を想定

        ###############################################
        ## Read Lattice Vector
        ##
        t1_x = float(self.datlines[14].split()[0]) # lattice constant/2
        t1_y = float(self.datlines[14].split()[1])
        t1_z = float(self.datlines[14].split()[2])

        t2_x = float(self.datlines[15].split()[0])
        t2_y = float(self.datlines[15].split()[1])
        t2_z = float(self.datlines[15].split()[2])

        t3_x = float(self.datlines[16].split()[0])
        t3_y = float(self.datlines[16].split()[1])
        t3_z = float(self.datlines[16].split()[2])

        self.t = np.zeros((3,3))
        self.t[0,0] = float(t1_x)
        self.t[1,0] = float(t1_y)
        self.t[2,0] = float(t1_z)

        self.t[0,1] = float(t2_x)
        self.t[1,1] = float(t2_y)
        self.t[2,1] = float(t2_z)

        self.t[0,2] = float(t3_x)
        self.t[1,2] = float(t3_y)
        self.t[2,2] = float(t3_z)

        ###############################################
        ## 原子の種類ごとの読み込み
        ##
        lines=17
        self.atoms = np.zeros(self.nion,dtype=int)
        for i in range(self.nion):
            lines += 1
            self.atoms[i] =  int(self.datlines[lines].split()[0])
            lines += 1
            tmp = self.datlines[lines]
            lines += 1
            tmp = self.datlines[lines]
            lines += 1
            tmp = self.datlines[lines]

        ###############################################
        ## 原子種の (仮) Index を作成する
        ##
        index = 0
        self.atoms_j = np.zeros(self.natom,dtype=int)
        for j in range(self.nion):
            for k in range(self.atoms[j]):
                self.atoms_j[index] = j # イオン種別の通し番号を与えておく
               #print atoms_j[index],index
                index += 1

        # 入力の原子情報基づく基本情報マトリックスの作成
        if atoms_index:
            # 入力原子情報に基づいて atoms_index を作成する
            self.atoms_index = [''] * self.nion
            if self.nion == len(atoms_index):
                for i in range(self.nion):
                    self.atoms_index[i] = atoms_index[i]

            # 入力原子情報に基づいて atoms_index_j を作成する
            self.atoms_index_j = []
            for k in range(self.nion):
                for l in range(int(self.atoms[k])):
                    self.atoms_index_j.append(str(self.atoms_index[k]))

            # 入力原子情報に基づいて atoms_number を作成する
            self.atoms_number = np.zeros(self.nion,dtype=int)
            for i in range(self.nion):
                self.atoms_number[i] = SAEnv.get_atomic_number1(str(self.atoms_index[i]))

            # 入力原子情報に基づいて atoms_number_j を作成する
            self.atoms_number_j = []
            for k in range(self.nion):
                for l in range(int(self.atoms[k])):
                    num0 = SAEnv.get_atomic_number1(str(self.atoms_index[k]))
                    self.atoms_number_j.append(num0)

            ## ion_local[j] & ion[j]
            self.ion = np.zeros(self.natom,dtype=int)
            self.ion_local = np.zeros(self.natom,dtype=int)
            tmp = -1
            for j in range(self.nion):
                local = -1
                for k in range(int(self.atoms[j])):
                    tmp += 1
                    local += 1
                    self.ion[tmp]= int(j)
                    self.ion_local[tmp] = int(local)

           ### natom までの通し番号で原子の種類番号を返す
           #self.atoms_j = np.zeros(self.natom,dtype=int)
           #j = 0
           #for ion in range(self.nion):
           #    for atom in range(self.atoms[ion]):
           #        self.atoms_j[j] = int(ion)
           #        j += 1

        else:
            self.vasp_version = 4
            self.atoms_index = []
            self.atoms_index_j = []
            self.atoms_number = []
            self.atoms_number_j = []
            self.ion = []
            self.ion_local = []


        ###############################################
        ## Read Internal Coordinate
        ##
        self.position = np.zeros((self.natom,3))
        for i in range(self.natom):
            lines += 1
            self.position[i,0] = float(self.datlines[lines].split()[0])
            self.position[i,1] = float(self.datlines[lines].split()[1])
            self.position[i,2] = float(self.datlines[lines].split()[2])
           #print position[i,0], position[i,1], position[i,2]


        # dummy parameter
        self.fix = ['T'] * self.natom

        # conver to VASP 形式(VASP形式を標準フォーマットとする)
        self.scale, self.direct = SAEnv.conv_cfg2vaspa(\
                self.scale,\
                self.t,\
                self.natom,\
                self.direct,\
                self.position)

    ############################################################################

    def get_comment(self):
        return self.comment

    def conv_cfg2vasp(self):
        self.scale, self.direct = SAEnv.conv_cfg2vasp(self.t,\
                self.natom,\
                self.direct,\
                self.position)
        return self.scale,self.direct

    ############################################################################
    #
    # RMC_POT 形式の座標系からVASP形式の座標系へ変換
    #   VASP 以外でも同じ、cartesian 系の並進＆内部座標系
    #   基本並進ベクトル＆内部座標
    #   scale factor は自動的に 1.0 になる( 1.0 としている)
    #
    # [in/out] t[3,3]         : 基本並進ベクトル(注意:配列内indexは0から)
    #                                  x   y   z
    #                            t1 = a11 a21 a31
    #                            t2 = a12 a22 a32
    #                            t3 = a13 a23 a33
    #
    # [in/out] position[j,3]  : 通し番号(max=natom)とx,y,z 指定で内部座標
    #
    ############################################################################
#   def conv_cfg2vasp(self):

#       if not self.direct:
#           sys.exit("STOP: input file is not direct mode")

#       t1_x = self.t[0,0]
#       t1_y = self.t[1,0]
#       t1_z = self.t[2,0]

#       t2_x = self.t[0,1]
#       t2_y = self.t[1,1]
#       t2_z = self.t[2,1]

#       t3_x = self.t[0,2]
#       t3_y = self.t[1,2]
#       t3_z = self.t[2,2]

#       ###############################################
#       ## DATA convert (RMC_POT to VASP )
#       ##
#       t1_x = t1_x*2
#       t1_y = t1_y*2
#       t1_z = t1_z*2

#       t2_x = t2_x*2
#       t2_y = t2_y*2
#       t2_z = t2_z*2

#       t3_x = t3_x*2
#       t3_y = t3_y*2
#       t3_z = t3_z*2

#       x_offset=0.5
#       y_offset=0.5
#       z_offset=0.5

#       # for Direct
#       for i in range(self.natom):
#           self.position[i,0] = self.position[i,0]/2 + x_offset
#           self.position[i,1] = self.position[i,1]/2 + y_offset
#           self.position[i,2] = self.position[i,2]/2 + z_offset

#       self.t[0,0] = t1_x
#       self.t[1,0] = t1_y
#       self.t[2,0] = t1_z

#       self.t[0,1] = t2_x
#       self.t[1,1] = t2_y
#       self.t[2,1] = t2_z

#       self.t[0,2] = t3_x
#       self.t[1,2] = t3_y
#       self.t[2,2] = t3_z

#       self.direct = True


################################################################################
if __name__ == '__main__':

    #import optparse
    # Default & OptionParser
    cname = 'igzo'

    atoms_index = ['In','Ga','Zn','O']
    cfg = SAEnv.ReadRmcpotCfg(cname+'.cfg',atoms_index=atoms_index)
#   print cfg.title
#   print cfg.atoms

#   cfg.conv_cfg2vasp()
#   cfg.scale,cfg.direct = SAEnv.conv_cfg2vasp(cfg.scale,\
#           cfg.t,\
#           cfg.natom,\
#           cfg.direct,\
#           cfg.position)

    # 擬似VASP5 設定
    dummy   = "In Ga Zn O"
    PV5FLAG = True  # 擬似VASP5 出力

    # VASP4+擬似VASP5 出力
   #print ""
    STD=False
   #STD=True
    SAEnv.print_poscar4(cname,STD,cfg.title,cfg.scale,cfg.natom,cfg.nion,\
                      cfg.direct,PV5FLAG,cfg.t,cfg.atoms,dummy,cfg.position)

