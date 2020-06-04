#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# ReadLobOut.py
#  ROBSTER の pCOHP 計算の出力 lobsterout をパースするクラス
#  軌道成分の吸い出し用
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.06.05 startup
#
################################################################################
from __future__ import print_function

try:
    from ...copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import sys
import os
# import gzip
import re
# import optparse
import numpy as np

# from copy import deepcopy

try:
    # sys.path.append('../..')
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    import StructureAnalysisEnvironment as SAEnv
except ImportError:
    import StructureAnalysisEnvironment as SAEnv


# import SpaceGroupEnvironment as SGE

################################################################################
class ReadLobOut(object):

    def __init__(self, name='lobsterout'):

        self.datlines, self.num = SAEnv.read_dataline(name)
        orbital_reg = re.compile('.*\(Bunge\)', re.IGNORECASE)

        self.atoms_index = []
        self.orbit_index = []  # ion ごとにプロジェクションされた軌道
        self.orbit = []  # ion ごとの軌道の数
        ion = 0
        for i in range(self.num):
            if bool(orbital_reg.match(self.datlines[i])):
                self.atoms_index.append(self.datlines[i].split()[0])
                orbit = re.sub('.*\(Bunge\)', '', self.datlines[i]).split()
                self.orbit_index.append(orbit)
                self.orbit.append(len(orbit))
                ion += 1

        self.nion = ion
        self.orbit = np.array(self.orbit)

    ############################################################################
    def get_nion(self):
        return self.nion

    def get_atoms_index(self):
        return self.atoms_index

    def get_orbit_index(self):
        return self.orbit_index

    def get_orbit(self):
        return self.orbit


################################################################################
if __name__ == '__main__':

    out = ReadLobOut()

    #######################################################
    # exsample)
    #    nion, atoms_index, orbit, orbit_index の関係
    #    orbit_index  # ion ごとにプロジェクションされた軌道
    #    orbit        # ion ごとの軌道の数
    #
    #   print out.nion
    #   print out.atoms_index
    #   print out.orbit
    #   print out.orbit_index
    #   print ""
    for i in range(out.nion):
        print("%s:" % str(out.atoms_index[i]), end="")
        for j in range(out.orbit[i]):
            print("%s" % str(out.orbit_index[i][j]), end="")
        print("")

################################################################################
