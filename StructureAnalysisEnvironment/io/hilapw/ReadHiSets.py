#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# sets.in (HiLAPW) 読み込み用のclass
#  群論の扱いに ASE を用いるバージョン
#
###############################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.05.14
#  startup
#
###############################################################################
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
###############################################################################

import sys
import os
#import re
import optparse
import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

#from ase.lattice.spacegroup import Spacegroup
from  ase.lattice.spacegroup import crystal

###############################################################################
class ReadHiSets(object):

    def __init__(self,cname='sets.in'):

        self.datlines,self.num = SAE.read_dataline(cname)

        self.title = str(self.datlines[0])
        self.nspin = int(self.datlines[2])
        self.sgn   = str(self.datlines[4])

        # for a,b,c,alpha,beta,gamma
        self.lattices = np.zeros(6)

        self.lattices[0] = self.datlines[5].split()[0] # a
        self.lattices[1] = self.datlines[5].split()[1] # b
        self.lattices[2] = self.datlines[5].split()[2] # c

        self.lattices[3] = self.datlines[6].split()[0] # alpha
        self.lattices[4] = self.datlines[6].split()[1] # beta
        self.lattices[5] = self.datlines[6].split()[2] # gamma

        self.nion = int(self.datlines[8])

        self.position = []
        self.atoms_index = np.zeros(self.nion,dtype='S2')
        self.atoms = np.zeros(self.nion,dtype=int)
        self.kpoints = np.zeros(3,dtype=int)
        self.natom = 0

        off = 9
        for i in range(self.nion):
            line = self.datlines[off].split()

            self.atoms_index[i] = str(line[0])
            self.atoms[i] = int(self.datlines[off].split()[1])

            for j in range(int(line[1])):
                x = float(self.datlines[off+1].split()[0])
                y = float(self.datlines[off+1].split()[1])
                z = float(self.datlines[off+1].split()[2])
                self.position.append([x,y,z])
               #print x,y,z
                self.natom += 1
                off += 1

            off += 1

        self.kinfo = int(self.datlines[off+1])

        self.kpoints[0] = int(self.datlines[off+2].split()[0])
        self.kpoints[1] = int(self.datlines[off+2].split()[1])
        self.kpoints[2] = int(self.datlines[off+2].split()[2])

    ###########################################################################
    def get_title(self):
        return self.title

    def get_position(self):
        return self.position


###############################################################################
def options():
    name = 'sets.in'

    parser = optparse.OptionParser()

    parser.add_option( '-i','--input', dest='INPUT',)
    options,args = parser.parse_args()

    if options.INPUT:
        name=options.INPUT

    if len(args) > 0:
        name=args[0]

    return name


###############################################################################
if __name__ == '__main__':

    name = options()
    sets = ReadHiSets(name)

    print("INPUT: %s" % str(name))

    print("")
    print(sets.get_title())

