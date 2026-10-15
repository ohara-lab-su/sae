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
################################################################################
# import gzip
# import optparse
# from copy import deepcopy
# sys.path.append('../..')
# import SpaceGroupEnvironment as SGE
################################################################################
################################################################################
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
################################################################################
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import numpy as np


############################################################################
class ReadLobOut(object):

    def __init__(self, name="lobsterout"):
        from sae.common.text import TextFiles

        self.datlines, self.num = TextFiles().read_dataline(name)
        orbital_reg = re.compile(".*\\(Bunge\\)", re.IGNORECASE)
        self.atoms_index = []
        # ion ごとにプロジェクションされた軌道
        self.orbit_index = []
        # ion ごとの軌道の数
        self.orbit = []
        ion = 0
        for i in range(self.num):
            if bool(orbital_reg.match(self.datlines[i])):
                self.atoms_index.append(self.datlines[i].split()[0])
                orbit = re.sub(".*\\(Bunge\\)", "", self.datlines[i]).split()
                self.orbit_index.append(orbit)
                self.orbit.append(len(orbit))
                ion += 1
        self.nion = ion
        self.orbit = np.array(self.orbit)

    def get_nion(self):
        return self.nion

    def get_atoms_index(self):
        return self.atoms_index

    def get_orbit_index(self):
        return self.orbit_index

    def get_orbit(self):
        return self.orbit
