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
class ReadLobCohp(object):

    def __init__(self,name='COHPCAR.lobster'):

        self.datlines,self.num = SAE.read_dataline(name)
        self.nedos = int(self.datlines[1].split()[2])

        self.eng = np.zeros(self.nedos)
        self.ave = np.zeros(self.nedos)
        j=0
        for i in range(4,self.num+1):
            self.eng[j] = float(self.datlines[i].split()[0])
            self.ave[j] = float(self.datlines[i].split()[1])
            j += 1

    def get_nedos(self):
        return self.nedos

    def get_eng(self):
        return self.eng

    def get_ave(self,spin=0):
        return self.ave

################################################################################
if __name__ == '__main__':


    cohp = ReadLobCohp()

    nedos = cohp.get_nedos()
    eng = cohp.get_eng()
    ave = cohp.get_ave()

    for i in range(nedos):
        print eng[i],ave[i]


################################################################################

