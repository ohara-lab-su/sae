#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# *.cfg ファイル読み込み
#
################################################################################
# [in/out] atoms[i]       : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
# [in/out] atoms_j[i]    : 原子の通し番号を与えると、原子のサイト番号を与える
#                           [注意] *.cfg形式は種類を与えないので 0 番から違う種類毎
#                                    に(仮に)無理やりナンバリングする
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
# 2015.07.16 startup
#
################################################################################
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

import sys
#import os
import numpy as np
import StructureAnalysisEnvironment as SAE

################################################################################
class ReadRmcpotCfg(object):

    def __init__(self,cname='POSCAR.cfg'):

        self.datlines, self.num = SAE.read_dataline(cname)

        ###############################################
        # instance value
        self.direct = True # cfg は in/out 共に direct を想定
        self.scale = 1.0   # cfg は scale 1.0 を想定

        ###############################################
        # Read Parameter
        self.header = str(self.datlines[0])
        self.title = self.header
        self.comment = str(self.datlines[1])
        self.moves = self.datlines[4]
        self.saved = self.datlines[5]
        self.natom = int(self.datlines[7].split()[0])
        self.nion = int(self.datlines[8].split()[0])
        self.nmoles = self.datlines[9]
        self.angles = self.datlines[10]

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

    def get_title(self):
        return self.title

    def get_t(self):
        return self.t

    def get_natom(self):
        return self.natom

    def get_atoms(self):
        return self.atoms

    def get_atoms_j(self):
        return self.atoms_j

    def get_direct(self):
        return self.direct

    def get_position(self):
        return self.position

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
    def conv_cfg2vasp(self):

        if not self.direct:
            sys.exit("STOP: input file is not direct mode")

        t1_x = self.t[0,0]
        t1_y = self.t[1,0]
        t1_z = self.t[2,0]

        t2_x = self.t[0,1]
        t2_y = self.t[1,1]
        t2_z = self.t[2,1]

        t3_x = self.t[0,2]
        t3_y = self.t[1,2]
        t3_z = self.t[2,2]

        ###############################################
        ## DATA convert (RMC_POT to VASP )
        ##
        t1_x = t1_x*2
        t1_y = t1_y*2
        t1_z = t1_z*2

        t2_x = t2_x*2
        t2_y = t2_y*2
        t2_z = t2_z*2

        t3_x = t3_x*2
        t3_y = t3_y*2
        t3_z = t3_z*2

        x_offset=0.5
        y_offset=0.5
        z_offset=0.5

        # for Direct
        for i in range(self.natom):
            self.position[i,0] = self.position[i,0]/2 + x_offset
            self.position[i,1] = self.position[i,1]/2 + y_offset
            self.position[i,2] = self.position[i,2]/2 + z_offset

        self.t[0,0] = t1_x
        self.t[1,0] = t1_y
        self.t[2,0] = t1_z

        self.t[0,1] = t2_x
        self.t[1,1] = t2_y
        self.t[2,1] = t2_z

        self.t[0,2] = t3_x
        self.t[1,2] = t3_y
        self.t[2,2] = t3_z

        self.direct = True


################################################################################
if __name__ == '__main__':

    #import optparse
    # Default & OptionParser
    cname = 'igzo'

    cfg = SAE.ReadRmcpotCfg(cname+'.cfg')

    cfg.conv_cfg2vasp()
#   cfg.scale,cfg.direct = SAE.conv_cfg2vasp(cfg.scale,\
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
    SAE.print_poscar4(cname,STD,cfg.title,cfg.scale,cfg.natom,cfg.nion,\
                      cfg.direct,PV5FLAG,cfg.t,cfg.atoms,dummy,cfg.position)

