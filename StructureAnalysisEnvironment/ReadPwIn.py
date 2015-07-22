#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# PWScf (Quantum ESPRESSO 5..x )
# scf.in ファイル( pw.x 入力ファイル 読み込み)
#
# 1) pw.x 入力ファイル名の第一候補を scf.in とする
# 2) ibrav = 0 のみ対応 (2015.05.12)
# 3) タグ名と値の間の区切りの = (イコール) には必ずスペースが入る事が前提
# 4) CELL_PARAMETERS は {alat} が前提
# 5) ATOMIC_POSITIONS は {crystal} が前提
#
################################################################################
#
# 2015.05.12 startup
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
__version__    = "0.1.1"
################################################################################

import sys
#import gzip
#import os
import re
import optparse
import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
class ReadPwIn(object):

    def __init__(self,cname):

        self.datlines,self.num = SAE.read_dataline(cname)

        ibrav_reg = re.compile('.*ibrav.*',re.IGNORECASE)
        lattice_a_reg = re.compile('.* a *=',re.IGNORECASE)
        nion_reg = re.compile('.*ntyp.*',re.IGNORECASE)
        natom_reg = re.compile('.*nat.*',re.IGNORECASE)
        spin_reg = re.compile('.*nspin.*')
        prefix_reg = re.compile('.*prefix.*')

        # 1bhor = 0.529177249 angstrom
        # 1Rydberg = 13.6056981 eV

        # set default
        self.ispin = 1
        self.prefix = 'input'

        for line in self.datlines:

            if bool(ibrav_reg.match(line)):
                tmp = re.sub('.*ibrav *=','',line.lower())
                tmp = re.sub(',.*','',tmp)
                self.ibrav = int(tmp)
                if self.ibrav != 0:
                    sys.exit("STOP: ibrav != 0")

            if bool(lattice_a_reg.match(line)):
                tmp = re.sub('.*a *=','',line.lower())
                tmp = re.sub(',.*','',tmp)
#               self.scale = float(tmp)*0.529177249
                self.scale = float(tmp)

            if bool(natom_reg.match(line)):
                tmp = re.sub('.*nat *=','',line.lower())
                tmp = re.sub(',.*','',tmp)
                self.natom = int(tmp)

            if bool(nion_reg.match(line)):
                tmp = re.sub('.*ntyp *=','',line.lower())
                tmp = re.sub(',.*','',tmp)
                self.nion = int(tmp)

            if bool(spin_reg.match(line)):
                tmp = re.sub('.*nspin *=','',line.lower())
                tmp = re.sub(',.*','',tmp)
                self.ispin = int(tmp)

            if bool(prefix_reg.match(line)):
                tmp = re.sub('.*prefix *=','',line.lower())
                tmp = re.sub('\'','',tmp)
                tmp = re.sub(',.*','',tmp)
                self.prefix = str(tmp.strip())

    ############################################################################
    # ReadPoscar.py での t に準ずる構造
    def get_t(self):
        self.t = np.zeros((3,3))
        cell_reg = re.compile('.*CELL_PARAMETERS.*',re.IGNORECASE)
        for i in range(self.num):
            line = self.datlines[i]
            if bool(cell_reg.match(line)):

                t1_x = self.datlines[i+1].split()[0]
                t1_y = self.datlines[i+1].split()[1]
                t1_z = self.datlines[i+1].split()[2]

                t2_x = self.datlines[i+2].split()[0]
                t2_y = self.datlines[i+2].split()[1]
                t2_z = self.datlines[i+2].split()[2]

                t3_x = self.datlines[i+3].split()[0]
                t3_y = self.datlines[i+3].split()[1]
                t3_z = self.datlines[i+3].split()[2]

                self.t[0,0] = t1_x
                self.t[1,0] = t1_y
                self.t[2,0] = t1_z

                self.t[0,1] = t2_x
                self.t[1,1] = t2_y
                self.t[2,1] = t2_z

                self.t[0,2] = t3_x
                self.t[1,2] = t3_y
                self.t[2,2] = t3_z

        return self.t

    ############################################################################
    def get_atoms_index(self):

        species_reg = re.compile('.*ATOMIC_SPECIES.*',re.IGNORECASE)
        self.atoms_index = []
        for i in range(self.num):
            if bool(species_reg.match(self.datlines[i])):
                for j in range(self.nion):
                    atom_name = self.datlines[i+j+1].split()[0]
                    self.atoms_index.append(atom_name)
        return self.atoms_index

    ############################################################################
    def get_atoms(self):

        self.get_atoms_index()
        self.atoms = np.zeros(self.nion,dtype=int)
        position_reg = re.compile('.*ATOMIC_POSITIONS.*',re.IGNORECASE)
        for i in range(self.num):
            line = self.datlines[i]
            if bool(position_reg.match(line)):
                for j in range(self.natom):
                    tmp = str(self.datlines[i+j+1].split()[0])
                    for k in range(self.nion):
                        if self.atoms_index[k] == tmp:
                            self.atoms[k] += 1
        return self.atoms

    ############################################################################
    # natom までの通し番号で原子種を返す(元素記号ではなくて原子の種類番号を返す)
    def get_atoms_j(self):  # ReadOutcar.py 互換, ReadMxDatMethod.py 互換

        self.get_atoms()
        self.atoms_j = np.zeros(self.natom,dtype=int)
        j = 0
        for ion in range(self.nion):
            for atom in range(self.atoms[ion]):
                self.atoms_j[j] = int(ion)
                j += 1

        return self.atoms_j

    ############################################################################
    # natom までの通し番号で原子種の記号を返す
    def get_atoms_index_j(self): # ReadMd, ReadPoscar, 互換

        position_reg = re.compile('.*ATOMIC_POSITIONS.*',re.IGNORECASE)
        self.atoms_index_j = []
        for i in range(self.num):
            if bool(position_reg.match(self.datlines[i])):
                for j in range(self.natom):
                    atom_name = self.datlines[i+j+1].split()[0]
                    self.atoms_index_j.append(atom_name)

        return self.atoms_index_j

    ############################################################################
    def get_position(self):

        position_reg = re.compile('.*ATOMIC_POSITIONS.*',re.IGNORECASE)
        self.position = np.zeros((self.natom,3))
        for i in range(self.num):
            line = self.datlines[i]
            if bool(position_reg.match(line)):
                for j in range(self.natom):
                    self.position[j,0] = self.datlines[i+j+1].split()[1]
                    self.position[j,1] = self.datlines[i+j+1].split()[2]
                    self.position[j,2] = self.datlines[i+j+1].split()[3]

        return self.position

    ############################################################################
    def get_ispin(self):
        return self.ispin

    def get_ibrav(self):
        return self.ibrav

    def get_scale(self):
        return self.scale

    def get_nion(self):
        return self.nion

    def get_natom(self):
        return self.natom

    def get_title(self):
        return self.prefix

################################################################################
def options():
    name = 'scf.in'

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT', default=name,)
    options,args = parser.parse_args()

    if options.INPUT: name=options.INPUT
    if len(args) > 0: name=args[0]

    return name

################################################################################
if __name__ == '__main__':

    name = options()
    out = ReadPwIn(name)

    print "NAME",name

    print "TITLE      :",out.get_title()

    print "IBRAV      :",out.get_ibrav()
    print "SCALE(ang) :",out.get_scale()
    print "NATOM      :",out.get_natom()
    print "NION       :",out.get_nion()

    print "T"
    print out.get_t()

    print ""
    print out.get_atoms_index()
    print out.get_atoms()

    print ""
    print out.get_atoms_j()
    print out.get_atoms_index_j()

    print ""
    print out.get_position()

