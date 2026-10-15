#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Rread* 共通Method のボス
#
#  Method --- ReadVaspPoscar
#  Method --- ReadFdmInp
#  Method --- ReaMxDatMethod -- ReadMxDat
#                            -- ReadMxDftscf
#                            -- ReadMxOut
#                            -- ReadMxPdos
#                            -- ReadMxTdos
#  Method --- ReadRmcpotCfg
#  Method --- ReadPwIn
#
###############################################################################
# History
#
# 2015.08.25
#  startup (ReadMxDatMethod.py から抽出)
#
###############################################################################
###############################################################################
# import sys
# import os
# import re
# import gzip
# import optparse
###############################################################################
###############################################################################
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import numpy as np


####################################
# position の(x,y,z) 毎の最大を返す
#
####################################
# position の(x,y,z) 毎の最小値を返す
#
class Method(object):

    def get_title(self):
        return self.system

    def get_system(self):
        return self.system

    def get_scale(self):
        return self.scale

    def get_t(self):
        return self.t

    def get_vasp_version(self):
        return self.vasp_version

    def get_atoms(self):
        return self.atoms

    def get_atoms_j(self):
        return self.atoms_j

    def get_atoms_index(self):
        return self.atoms_index

    def get_atoms_number(self):
        return self.atoms_number

    def get_atoms_index_j(self):
        return self.atoms_index_j

    def get_atoms_number_j(self):
        return self.atoms_number_j

    def get_nion(self):
        return self.nion

    def get_natom(self):
        return self.natom

    def get_ion(self):
        return self.ion

    def get_ion_local(self):
        return self.ion_local

    def get_selective(self):
        return self.selective

    def get_direct(self):
        return self.direct

    def get_position(self):
        return self.position

    def get_fix(self):
        return self.fix

    def get_position_max(self):
        position = self.position
        self.position_max_xyz = np.zeros(3)
        for xyz in range(0, 3):
            self.position_max_xyz[xyz] = max(position[:, xyz])
        return self.position_max_xyz

    def get_position_min(self):
        position = self.position
        self.position_min_xyz = np.zeros(3)
        for xyz in range(0, 3):
            self.position_min_xyz[xyz] = min(position[:, xyz])
        return self.position_min_xyz
