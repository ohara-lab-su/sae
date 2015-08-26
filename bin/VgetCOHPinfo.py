#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# pCOHP に関する解析をする前に必要な情報をゲットする
#
################################################################################
#
# 2015.08.25
#   startup
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
#import numpy as np

#from copy import deepcopy

import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE

################################################################################
if __name__ == '__main__':


    # 軌道情報をサイトごとに表示
    out = SAEnv.ReadLobOut()
    for i in range(out.nion):
        print out.atoms_index[i],":["+str(len(out.orbit_index[i]))+"]",
        for j in range(out.orbit[i]):
            print out.orbit_index[i][j],
        print ""

#   # 結合してる距離が一番長いペアを表示
#   cohp = SAEnv.ReadLobCohp()
#   print "Number of bond:",cohp.nbond-1
#   print "No"+str(cohp.bond_max)+",",\
#           cohp.bond_index[cohp.bond_max],":",\
#           cohp.bond_ave[cohp.bond_max]


################################################################################

