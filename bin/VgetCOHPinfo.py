#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# pCOHP に関する解析をする前に必要な情報をゲットする
#
##########################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.08.25
#   startup
#
##########################################################################
from __future__ import print_function
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
#
__status__ = "alpha"
__version__ = "0.0.1"
##########################################################################

#import sys
#import os
#import gzip
#import re
#import numpy as np
import optparse
#from copy import deepcopy

import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE


def options():
    parser = optparse.OptionParser()
    parser.add_option('-v', action='store_true', default=False,)
    parser.add_option('-d', '--dos', action='store_true', default=False,)
    parser.add_option('-b', '--bond', action='store_true', default=False,)
    options, args = parser.parse_args()

    return options.v, options.dos, options.bond

##########################################################################
if __name__ == '__main__':

    V_FLAG, DOS_FLAG, BOND_FLAG = options()

    COHP_FLAG = False

    # 軌道情報をサイトごとに表示
    out = SAEnv.ReadLobOut()
    for i in range(out.nion):
        print out.atoms_index[i], ":[" + str(len(out.orbit_index[i])) + "]",
        for j in range(out.orbit[i]):
            print out.orbit_index[i][j],
        print ""

    if V_FLAG:
        # COHP 解析をした原子のペアを表示( 0番は Average)
        if not COHP_FLAG:
            cohp = SAEnv.ReadLobCohp()
            COHP_FLAG = True
        print ""
        for i in range(len(cohp.bond_index)):
            print i, cohp.bond_index[i]

    if DOS_FLAG:
        # 原子ごとの軌道リスト
        dos = SAEnv.ReadLobDos()
        print ""
        for i in range(len(dos.orbit_index_j)):
            norbit = len(dos.orbit_index_j[i])
            print dos.atoms_index_j[i],"["+str(norbit)+"]",
            for orb in range(norbit):
                print dos.orbit_index_j[i][orb],
            print ""


#   # 結合してる距離が一番長いペアを表示
#   cohp = SAEnv.ReadLobCohp()
#   print "Number of bond:",cohp.nbond-1
#   print "No"+str(cohp.bond_max)+",",\
#           cohp.bond_index[cohp.bond_max],":",\
#           cohp.bond_ave[cohp.bond_max]


##########################################################################
