#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# *_bav.txt to xyz format
#
#
################################################################################
#
# 2018.08.21
#  Python2/3 両対応
#
# 2015.06.24 startup
#
################################################################################
from __future__ import print_function
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

import sys
import os
#import gzip
#import re
import optparse
#import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
def options():

#   name = 'POSCAR.txt'
    name = 'Cu'
    suffix = '_bav.txt'

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT',)
    parser.add_option(  '-s','--std', action='store_true',)
    options,args = parser.parse_args()

    if not os.path.exists(name+suffix):
        name0 = SAE.find_datfile1(suffix)
        name = name0.replace(suffix,'')

    if options.INPUT: name=options.INPUT
    if len(args) > 0: name=args[0]

    return name,suffix,options.std


################################################################################
if __name__ == '__main__':

    name,suffix,STD_FLAG = options()
    bav = SAE.ReadFdmBav(name,suffix)

    natom = bav.get_natom()
    lmax = bav.get_lmax()
    edge = bav.get_edge()
    t = bav.get_t()
    position = bav.get_position()
    atoms_index_j = bav.get_atoms_index_j()

#   print "natom =",natom
#   print "lmax = ",lmax
#   print "edge = ",edge
#   print "t    = "
#   print t

    if STD_FLAG:
        xyz = sys.stdout
    else:
        try:
            xyz = open(name+'.xyz','w')
        except:
            xyz.close()

    print(natom, file=xyz)
    print("", file=xyz)
    for i in range(natom):
        print(" %s %14.10f %14.10f %14.10f"
                %(atoms_index_j[i],position[i,0],position[i,1],position[i,2]), file=xyz)

    xyz.close()
