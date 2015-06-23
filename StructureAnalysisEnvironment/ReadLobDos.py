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
# 2015.06.05 startup
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
#import re
#import optparse
import numpy as np

#from copy import deepcopy

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
class ReadLobDos(object):

    def __init__(self,name='DOSCAR.lobster'):

        self.datlines,self.num = SAE.read_dataline(name)
        self.natom = int(self.datlines[0].split()[0])
        self.ispin = int(self.datlines[0].split()[3])
        self.nedos = int(self.datlines[5].split()[2])

        self.eng = np.zeros(self.nedos)
        self.tdos = np.zeros((self.nedos,self.ispin))
        for i in range(self.nedos):
            self.eng[i] = float(self.datlines[6+i].split()[0])
            for spin in range(self.ispin):
                self.tdos[i,spin] = float(self.datlines[6+i].split()[1+spin*2])

    def get_nedos(self):
        return self.nedos

    def get_ispin(self):
        return self.ispin

    def get_natom(self):
        return self.natom

    def get_eng(self):
        return self.eng

    def get_tdos(self,spin=0):
        return self.tdos[:,spin]

################################################################################
if __name__ == '__main__':

    dos = ReadLobDos()

    print "ISPIN:",dos.get_ispin()
    print "NATOM:",dos.get_natom()
    print "NEDOS:",dos.get_nedos()



################################################################################

