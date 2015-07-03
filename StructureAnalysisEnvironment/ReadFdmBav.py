#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
# *_bav.txt ファイル
#
################################################################################
#
# 2015.06.25
#  R2 bases に対応した cluster: atom positions 吸い出しに対応
#
# 2015.06.23 startup
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

import sys
#import gzip
import os
import re
import optparse
import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
class ReadFdmBav(object):

    def __init__(self,cname,suffix='_bav.txt'):

        self.datlines,self.num = SAE.read_dataline(cname+suffix)

        ngroup_reg = re.compile('.*ngroup =.*')
        excited_atom_reg = re.compile('.*Excited atom.*')
        threshold_reg = re.compile('.*Threshold:.*')
        r2_reg = re.compile('.*Transformation Crystal Bases.*Bases R2.*')
        positions_reg = re.compile('.*Cluster: atom positions in order.*')

        self.t = np.zeros((3,3))
#       self.position = []

        for i in range(self.num):

            # 全原子数の検索
            if bool(ngroup_reg.match(self.datlines[i])):
                if self.datlines[i].split()[0] == 'ngroup':
                    self.ngroup = int(self.datlines[i].split()[2].replace(',',''))
                else:
                    sys.exit("STOP: ngroup tag not found.")

            # 吸収原子の最大のlを探す
            if bool(excited_atom_reg.match(self.datlines[i])):
                i += 2
                l = 0
                while 1:
                    l0 = self.datlines[i].split()[1]
                    if l < l0:
                        l = l0
                    i += 1
                    if not len(self.datlines[i]):
                        break
                self.lmax = l

            # 吸収端
            if bool(threshold_reg.match(self.datlines[i])):
                self.edge = self.datlines[i].split()[2]

            # absorber を原点とした時の基本並進ベクトル
            if bool(r2_reg.match(self.datlines[i])):
                t1_x = float(self.datlines[i+1].split()[0])
                t1_y = float(self.datlines[i+1].split()[1])
                t1_z = float(self.datlines[i+1].split()[2])

                t2_x = float(self.datlines[i+2].split()[0])
                t2_y = float(self.datlines[i+2].split()[1])
                t2_z = float(self.datlines[i+2].split()[2])

                t3_x = float(self.datlines[i+3].split()[0])
                t3_y = float(self.datlines[i+3].split()[1])
                t3_z = float(self.datlines[i+3].split()[2])

                self.t[0,0] = t1_x
                self.t[1,0] = t1_y
                self.t[2,0] = t1_z

                self.t[0,1] = t2_x
                self.t[1,1] = t2_y
                self.t[2,1] = t2_z

                self.t[0,2] = t3_x
                self.t[1,2] = t3_y
                self.t[2,2] = t3_z

            # positon (絶対座標系)
            if bool(positions_reg.match(self.datlines[i])):

                self.position = []
                self.atoms_index_j = []

                j = 0
                while 1:
                    zz = int(self.datlines[2+i+j].split()[0])
                    self.atoms_index_j.append(SAE.get_atomic_symbol0(zz))
                    px = float(self.datlines[2+i+j].split()[1])
                    py = float(self.datlines[2+i+j].split()[2])
                    pz = float(self.datlines[2+i+j].split()[3])
                    self.position.append([px,py,pz])
                    j += 1
                    if len(self.datlines[2+i+j].split()) <= 0:
                        break
                self.natom = j
                self.position = np.array(self.position)

    def get_natom(self):
        self.natom = self.natom if hasattr(self,'natom') else 0
        return self.natom

    def get_ngroup(self):
        self.ngroup = self.ngroup if hasattr(self,'ngroup') else 0
        return self.ngroup

    def get_t(self):
        return self.t

    def get_edge(self):
        self.edge = self.edge if hasattr(self,'edge') else None
        return self.edge

    def get_lmax(self):
        self.lmax = self.lmax if hasattr(self,'lmax') else None
        return self.lmax

    def get_position(self):
        return self.position

    def get_atoms_index_j(self):
        return self.atoms_index_j

################################################################################
def options():

#   name = 'POSCAR.txt'
    name = 'Cu'
    suffix = '_bav.txt'

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT',)
    options,args = parser.parse_args()

    if not os.path.exists(name+suffix):
        name0 = SAE.find_datfile1(suffix)
        name = name0.replace(suffix,'')

    if options.INPUT: name=options.INPUT
    if len(args) > 0: name=args[0]

    return name,suffix

################################################################################
if __name__ == '__main__':

    name,suffix = options()
    bav = ReadFdmBav(name,suffix)

    natom = bav.get_natom()
    lmax = bav.get_lmax()
    edge = bav.get_edge()
    t = bav.get_t()
    position = bav.get_position()
    atoms_index_j = bav.get_atoms_index_j()

    print "natom =",natom
    print "lmax = ",lmax
    print "edge = ",edge
    print "t    = "
    print t

    for i in range(natom):
        print "%s %10.6f %10.6f %10.6f" \
                %(atoms_index_j[i],position[i,0],position[i,1],position[i,2])
#       print position[i][0],position[i][1],position[i][2]

