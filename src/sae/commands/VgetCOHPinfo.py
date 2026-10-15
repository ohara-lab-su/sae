#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
#   # 結合してる距離が一番長いペアを表示
#   cohp = SAE.ReadLobCohp()
#   print "Number of bond:",cohp.nbond-1
#   print "No"+str(cohp.bond_max)+",",\
#           cohp.bond_index[cohp.bond_max],":",\
#           cohp.bond_ave[cohp.bond_max]
##########################################################################
from __future__ import print_function
from sae.lobster.cohpcar import ReadLobCohp
from sae.lobster.doscar import ReadLobDos
from sae.lobster.out import ReadLobOut

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
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import optparse


#
##########################################################################
#import sys
#import os
#import gzip
#import re
#import numpy as np
#from copy import deepcopy
#import SpaceGroupEnvironment as SGE
def options():
    parser = optparse.OptionParser()
    parser.add_option("-v", action="store_true", default=False)
    parser.add_option("-d", "--dos", action="store_true", default=False)
    parser.add_option("-b", "--bond", action="store_true", default=False)
    options, args = parser.parse_args()
    return (options.v, options.dos, options.bond)


##########################################################################
# 軌道情報をサイトごとに表示
if __name__ == "__main__":
    V_FLAG, DOS_FLAG, BOND_FLAG = options()
    COHP_FLAG = False
    out = ReadLobOut()
    for i in range(out.nion):
        print(out.atoms_index[i], ":[" + str(len(out.orbit_index[i])) + "]", end="")
        for j in range(out.orbit[i]):
            print(out.orbit_index[i][j], end="")
        print("")
    # COHP 解析をした原子のペアを表示( 0番は Average)
    if V_FLAG:
        if not COHP_FLAG:
            cohp = ReadLobCohp()
            COHP_FLAG = True
        print("")
        for i in range(len(cohp.bond_index)):
            print(i, cohp.bond_index[i])
    # 原子ごとの軌道リスト
    if DOS_FLAG:
        dos = ReadLobDos()
        print("")
        for i in range(len(dos.orbit_index_j)):
            norbit = len(dos.orbit_index_j[i])
            print(dos.atoms_index_j[i], "[" + str(norbit) + "]", end="")
            for orb in range(norbit):
                print(dos.orbit_index_j[i][orb], end="")
            print("")
