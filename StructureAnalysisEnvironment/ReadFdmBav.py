#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
# *_bav.txt ファイル
#
###############################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.09.11
#  scf ループ関係の情報吸い出しを追加
#
# 2015.06.25
#  R2 bases に対応した cluster: atom positions 吸い出しに対応
#
# 2015.06.23 startup
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
__version__ = "0.0.1"
###############################################################################

import sys
#import gzip
import os
import re
import optparse
import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

###############################################################################


class ReadFdmBav(object):

    def __init__(self, cname, suffix='_bav.txt'):

        self.datlines, self.num = SAE.read_dataline(cname + suffix)

        ngroup_reg = re.compile('.*ngroup =.*')
        excited_atom_reg = re.compile('.*Excited atom.*')
        atom_type_reg = re.compile('.*Atom type.*')
        threshold_reg = re.compile('.*Threshold:.*')
        r2_reg = re.compile('.*Transformation Crystal Bases.*Bases R2.*')
        positions_reg = re.compile('.*Cluster: atom positions in order.*')
        scf_flag_reg = re.compile('.*Self consistent calculation')
        scf_max_reg = re.compile('.*Maximum number of iteration')
        scf_end_reg = re.compile('.*Begining of cycle.*')
        scf_toten_reg = re.compile('.*Unit cell energy.*')

        nspin_reg = re.compile('.*Magnetic calculation')

        self.t = np.zeros((3, 3))
#       self.position = []

        self.nspin = 1  # default nonmag
        self.SCF = False
        self.n_scf_loop = 0
        self.scf_toten = []

        for i in range(self.num):

            # SCF 計算のチェック
            if bool(scf_flag_reg.match(self.datlines[i])):
                self.SCF = True

            # scf ループの最大値
            if bool(scf_max_reg.match(self.datlines[i])):
                self.nsw = int(self.datlines[i].split()[5])

            # scf ループ数のカウント
            if bool(scf_end_reg.match(self.datlines[i])):
                self.n_scf_loop = int(self.datlines[i].split()[3])

            # scf ループ毎の unit cell の全エネルギー
            if bool(scf_toten_reg.match(self.datlines[i])):
                self.scf_toten.append(self.datlines[i])

            # 全原子数の検索
            if bool(ngroup_reg.match(self.datlines[i])):
                if self.datlines[i].split()[0] == 'ngroup':
                    self.ngroup = \
                            int(self.datlines[i].split()[2].replace(',', ''))
                else:
                    sys.exit("STOP(ReadFdmBav): ngroup tag not found.")

            # 吸収原子の最大のlを探す
            if bool(excited_atom_reg.match(self.datlines[i])):
                j = 2
                l = 0
                while 1:
                    _l = self.datlines[i+j].split()[1]
                    if l < _l:
                        l = _l
                    j += 1
                    if bool(atom_type_reg.match(self.datlines[i+j+1])):
                        break
                self.lmax = l

            # Magnetic? or Nonmag
            if bool(nspin_reg.match(self.datlines[i])):
                self.nspin = 2

            # 吸収端
            if bool(threshold_reg.match(self.datlines[i])):
                self.edge = self.datlines[i].split()[2]

            # absorber を原点とした時の基本並進ベクトル
            if bool(r2_reg.match(self.datlines[i])):
                t1_x = float(self.datlines[i + 1].split()[0])
                t1_y = float(self.datlines[i + 1].split()[1])
                t1_z = float(self.datlines[i + 1].split()[2])

                t2_x = float(self.datlines[i + 2].split()[0])
                t2_y = float(self.datlines[i + 2].split()[1])
                t2_z = float(self.datlines[i + 2].split()[2])

                t3_x = float(self.datlines[i + 3].split()[0])
                t3_y = float(self.datlines[i + 3].split()[1])
                t3_z = float(self.datlines[i + 3].split()[2])

                self.t[0, 0] = t1_x
                self.t[1, 0] = t1_y
                self.t[2, 0] = t1_z

                self.t[0, 1] = t2_x
                self.t[1, 1] = t2_y
                self.t[2, 1] = t2_z

                self.t[0, 2] = t3_x
                self.t[1, 2] = t3_y
                self.t[2, 2] = t3_z

            # positon (絶対座標系)
            if bool(positions_reg.match(self.datlines[i])):

                self.position = []
                self.atoms_index_j = []

                j = 0
                while 1:
                    zz = int(self.datlines[2 + i + j].split()[0])
                    self.atoms_index_j.append(SAE.get_atomic_symbol0(zz))
                    px = float(self.datlines[2 + i + j].split()[1])
                    py = float(self.datlines[2 + i + j].split()[2])
                    pz = float(self.datlines[2 + i + j].split()[3])
                    self.position.append([px, py, pz])
                    j += 1
                    if len(self.datlines[2 + i + j].split()) <= 0:
                        break
                self.natom = j
                self.position = np.array(self.position)

        self.ispin = self.nspin
        self.scf_toten = np.array(self.scf_toten)

    def get_nspin(self):
        return self.nspin

    def get_natom(self):
        self.natom = self.natom if hasattr(self, 'natom') else 0
        return self.natom

    def get_ngroup(self):
        self.ngroup = self.ngroup if hasattr(self, 'ngroup') else 0
        return self.ngroup

    def get_t(self):
        return self.t

    def get_edge(self):
        self.edge = self.edge if hasattr(self, 'edge') else None
        return self.edge

    def get_lmax(self):
        self.lmax = self.lmax if hasattr(self, 'lmax') else None
        return self.lmax

    def get_position(self):
        return self.position

    def get_atoms_index_j(self):
        return self.atoms_index_j

###############################################################################


def options():

    #   name = 'POSCAR.txt'
    name = 'Cu'
    suffix = '_bav.txt'

    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest='INPUT',)
    options, args = parser.parse_args()

    if not os.path.exists(name + suffix):
        name0 = SAE.find_datfile1(suffix)
        name = name0.replace(suffix, '')

    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]

    return name, suffix

###############################################################################
if __name__ == '__main__':

    name, suffix = options()
    bav = ReadFdmBav(name, suffix)

    natom = bav.get_natom()
    lmax = bav.get_lmax()
    edge = bav.get_edge()
    t = bav.get_t()
    position = bav.get_position()
    atoms_index_j = bav.get_atoms_index_j()

    print("n_ion_loop %s" % str(bav.n_scf_loop))
    for i in range(bav.n_scf_loop):
        print("%s" % str(bav.scf_toten[i]))

    print("natom = %s" % str(natom))
    print("lmax  = %s" % str(lmax))
    print("edge  = %s" % str(edge))
    print("t     = %s" % str(t))

#   for i in range(natom):
#       print "%s %10.6f %10.6f %10.6f" \
#         % (atoms_index_j[i], position[i, 0], position[i, 1], position[i, 2])
#       print position[i][0],position[i][1],position[i][2]
