#!/usr/bin/env python
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
# *_bav.txt ファイル
#
################################################################################
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

#import sys
#import gzip
#import os
import re
import optparse
#import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
class ReadFdmBav(object):

    def __init__(self,cname,suffix='_bav.txt'):

        self.datlines,self.num = SAE.read_dataline(cname+suffix)

        excited_atom_reg = re.compile('.*Excited atom.*')
        threshold_reg = re.compile('.*Threshold:.*')

        for i in range(self.num):
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

    def get_edge(self):
        return self.edge

    def get_lmax(self):
        self.lmax = self.lmax if hasattr(self,'lmax') else None
        return self.lmax

################################################################################
def options():

#   name = 'POSCAR.txt'
    name = 'Cu'
    suffix = '_bav.txt'

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT',)
    options,args = parser.parse_args()

    if options.INPUT: name=options.INPUT
    if len(args) > 0: name=args[0]

    return name,suffix

################################################################################
if __name__ == '__main__':

    name,suffix = options()
    bav = ReadFdmBav(name,suffix)

    print "lmax = ",bav.get_lmax()
    print "edge = ",bav.get_edge()

