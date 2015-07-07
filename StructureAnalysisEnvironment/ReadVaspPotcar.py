#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# POTCAR
#
################################################################################
#
# 2015.07.07 startup
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015 Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"
################################################################################

import sys
#import os
import re
#import gzip
import numpy as np

import optparse

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
class ReadVaspPotcar(object):

    def __init__(self,POTCAR='POTCAR'):

        self.datlines, self.num = SAE.read_dataline(POTCAR)

        vrhfin_reg = re.compile('.*VRHFIN')
        zval_reg = re.compile('.*ZVAL')

        self.nion = 0
        self.atoms_index = []
        self.atoms_zval = []

        for i in range(self.num):
            if bool(vrhfin_reg.match(self.datlines[i])):
                atom0 = re.sub('.*VRHFIN =','',self.datlines[i])
                self.atoms_index.append(re.sub(':.*','',atom0).strip())
                self.nion += 1
            if bool(zval_reg.match(self.datlines[i])):
                zval0 = re.sub('.*ZVAL','',self.datlines[i])
                self.atoms_zval.append(float(re.sub('^.*=','',zval0).split()[0]))

        if len(self.atoms_index) != len(self.atoms_zval):
            sys.exit("STOP: atoms_index != atoms_zval")

    def get_nion(self):
        return self.nion

    def get_atoms_index(self):
        return self.atoms_index

    def get_atoms_zval(self):
        return self.atoms_zval

################################################################################
def options():

    name = 'POTCAR'
    parser = optparse.OptionParser()
    parser.add_option( '-i','--input', dest='INPUT',)
    options, args = parser.parse_args()
    if options.INPUT: name = options.INPUT

    return name

################################################################################
if __name__ == '__main__':

    name = options()
    potcar = ReadVaspPotcar(name)

    print potcar.nion
    print potcar.atoms_index
    print potcar.atoms_zval
