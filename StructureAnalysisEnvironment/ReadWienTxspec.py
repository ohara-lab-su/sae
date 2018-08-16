#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# WIEK2k case.txspec
#
#
################################################################################
#
# 2015.06.30
#   == None --> is None
#
# 2015.04.06
#  suffix を変更可能にした(以前のままでも使える)
#
# 2015.03.28(sat)
#  startup
#
################################################################################
from __future__ import print_function
###############################################################################
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

import sys
import os
import re
#import gzip
import numpy as np

#import optparse

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
class ReadWienTxspec(object):

    ############################################################################
    ## init
    def __init__(self,case='case',spin=None,suffix='.txspec'):

#       suffix = '.txspec'
        if spin is None:
            spin = ''
        self.datlines,self.num = SAE.read_dataline(case+suffix+spin)

        s_reg = re.compile(' #S=.*')
        g_reg = re.compile(' #GAMMA=.*')

        self.eng = []
        self.unbroad_xas  = []

        for i in range(self.num):
            line = self.datlines[i]

           #if bool(s_reg.match(line)):
           #    self.s = float(line.split()[1])
           #if bool(g_reg.match(line)):
           #    self.g = float(line.split()[1])

            if not bool(s_reg.match(line)) and not bool(g_reg.match(line)):
                self.eng.append(float(line.split()[0]))
                self.unbroad_xas.append(float(line.split()[1]))

    def get_eng(self):
        self.eng = np.array(self.eng)
        return self.eng

    def get_emin(self):
        self.emin = min(self.eng)
        return self.emin

    def get_emax(self):
        self.emax = max(self.eng)
        return self.emax

    def get_unbroad_xas(self):
        self.unbroad_xas = np.array(self.unbroad_xas)
        return self.unbroad_xas

#   def get_s(self):
#       return self.s

#   def get_gamma(self):
#       return self.g

    def write(self,outputname=None):
        if outputname is None:
            out = sys.stdout
        else:
            try:
                out = open(outputname,'w')
            except:
                out.close()
                sys.exit(outputname+" can't not open")

        nxas = len(self.xas)
        for i in range(nxas):
            print >> out, "%9.5f %14.8f" % (self.eng[i], self.xas[i])

        if not outputname is None:
            out.close()

################################################################################
if __name__ == '__main__':

    import optparse

    case = re.sub('.*/','',os.getcwd())
   #case = 'Cu'

    suffix = '.txspec'

    unit = 'ev'

    parser = optparse.OptionParser(os.getcwd())
    parser.add_option( '-i','--input', dest='INPUT', )
    options, args = parser.parse_args()

    if options.INPUT: case = options.INPUT

    xspec = ReadWienTxspec(case+suffix)
    xspec.write()

