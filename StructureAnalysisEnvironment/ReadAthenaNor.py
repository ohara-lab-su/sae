#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Read Athena Normalize Data ( *.txt.nor )
#
#
################################################################################
#
# 2015.03.30
#  startup
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014,2015 Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"
################################################################################

#import sys
import os
import re
#import gzip
import numpy as np

#import optparse

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
class ReadAthenaNor(object):

    def __init__(self,name='case.txt.nor'):

        self.datlines,self.num = SAE.read_dataline(name)
        comment_reg = re.compile('^#.*')

        self.eng = []
        self.nor = []
        self.ndata = 0
        for i in range(self.num):
            line = self.datlines[i]
            if not bool(comment_reg.match(line)):
                self.eng.append(float(line.split()[0]))
                self.nor.append(float(line.split()[1]))
                self.ndata += 1

        self.nor = np.array(self.nor)
        self.eng = np.array(self.eng)

    def get_nor(self):
        return self.nor

    def get_eng(self):
        return self.eng

    def get_ndata(self):
        return self.ndata

################################################################################
if __name__ == '__main__':

    import optparse

    name = 'Cu_foil_10ms.txt.nor'

    parser = optparse.OptionParser(os.getcwd())
    parser.add_option( '-i','--input', dest='INPUT', )
    options, args = parser.parse_args()

    if options.INPUT:
        case = options.INPUT

    spec = ReadAthenaNor(name)
    eng = spec.get_eng()
    nor = spec.get_nor()
    ndata = spec.get_ndata()

    for i in range(ndata):
        print eng[i],nor[i]


