#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# WIEK2k case.outputt を読み込む class  ( for tetra )
#
#
################################################################################
#
# 2015.03.24
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
#import os
import re
#import gzip
#import numpy as np

#import optparse

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
class ReadWienOutputt(object):

    ###############################################
    ## init and Read POSCAR
    def __init__(self,name):
        self.datlines,self.num = SAE.read_dataline(name)

        jatom_txt = '.*JATOM'
        jatom_reg = re.compile(jatom_txt)

        self.isplits = []
        for i in range(self.num):
            if bool(jatom_reg.match(self.datlines[i])):

                jatom = re.sub(jatom_txt,'',self.datlines[i])
                jatom = int(re.sub(' *MULT=.*$','',jatom))

                isplit = re.sub('.*ISPLIT=','',self.datlines[i]).split()[1].split(',')
                self.isplits.append(isplit)

        self.nion = jatom

    def get_nion(self):
        return self.nion

    def get_wien_orbital(self):
        return self.isplits

################################################################################
if __name__ == '__main__':

    name = 'Cu.outputt'
    tetra = ReadWienOutputt(name)

    print tetra.nion
    print tetra.isplits[0]

