#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# WIEK2k case.outputt を読み込む class  ( for tetra )
#
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.03.24
#  startup
#
################################################################################
from __future__ import print_function

from sae.errors import legacy_error as _legacy_error

from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import sys
import os
import re

# import gzip
# import numpy as np

# import optparse

import StructureAnalysisEnvironment as SAEnv

# import SpaceGroupEnvironment as SGE


################################################################################
class BandOutput(object):

    ###############################################
    ## init and Read POSCAR
    def __init__(self, name):
        self.datlines, self.num = SAEnv.read_dataline(name)

        jatom_txt = ".*JATOM"
        jatom_reg = re.compile(jatom_txt)

        self.isplits = []
        for i in range(self.num):
            if bool(jatom_reg.match(self.datlines[i])):
                jatom = re.sub(jatom_txt, "", self.datlines[i])
                jatom = int(re.sub(" *MULT=.*$", "", jatom))

                isplit = re.sub(".*ISPLIT=", "", self.datlines[i]).split()[1].split(",")
                self.isplits.append(isplit)

        self.nion = jatom

    def get_nion(self):
        return self.nion

    def get_wien_orbital(self):
        return self.isplits


################################################################################
if __name__ == "__main__":
    name = "Cu.outputt"
    tetra = ReadWienOutputt(name)

    print(tetra.nion)
    print(tetra.isplits[0])


ReadWienOutputt = BandOutput  # historical spelling
