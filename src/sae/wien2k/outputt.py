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
################################################################################
# import gzip
# import numpy as np
# import optparse
# sys.path.append('../..')
# import SpaceGroupEnvironment as SGE
################################################################################
################################################################################
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re


###############################################
## init and Read POSCAR
class ReadWienOutputt(object):

    def __init__(self, name):
        from sae.common.text import TextFiles

        self.datlines, self.num = TextFiles().read_dataline(name)
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
