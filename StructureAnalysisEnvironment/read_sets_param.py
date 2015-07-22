#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# sets.in (HiLAPW) 読み込みの事前準備
#
################################################################################
#
# 2014.11.25/26 1st version
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"
################################################################################

import sys
import os
#import re
#import optparse
#import numpy as np

################################################################################
#
# [return] sgn_index   : 空間群の名前
# [return] nion        : サイト数
# [return] sg_natom    : 全原子数(空間群を用いた時の独立サイト内の全原子数)
#
# [return] sg_atoms[]  : サイト毎の原子数(matrix)
#
################################################################################
def read_sets_param(cname='sets.in'):

    if not os.path.exists(cname):
        sys.exit("STOP: "+cname+" file not found")

    try:
        tmp = open(cname)
    except:
        tmp.close()
        sys.exit("STOP: "+cname+" does'nt open")

    setsfile = tmp.read()
    tmp.close()
    setslines = setsfile.split('\n')

    sgn_index  = str(setslines[4])
    nion       = int(setslines[8])

    sg_natom       = 0
    sg_atoms       = []
    sg_atoms_index = []

    index = 8
    for i in range(nion):
        index += 1
        tmp = setslines[index].split()

        sg_atoms_index.extend(tmp[0])
        sg_atoms.extend(tmp[1])
        sg_natom = sg_natom + int(tmp[1])
        for j in range(int(tmp[1])):
            index += 1

#   for j in range(len(sg_atoms_index)):
#       print sg_atoms_index[j], sg_atoms[j]

    return sgn_index,nion,sg_natom,sg_atoms



################################################################################
if __name__ == '__main__':

    # sets.in 読み込みの準備&前段階
    lattices0 = []
    lattices0.extend(read_sets_param())

    sgn_index  = lattices0[0]
    nion       = lattices0[1]
    sg_natom   = lattices0[2]

#   for i in range(nion):
#       print lattices0[3][i]


