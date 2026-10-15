#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# PWScf (Quantum ESPRESSO 5..x )
# dos 関連出力 ファイル( dos.x projwfc.x 出力ファイル 読み込み)
#
# 正直なgnuplot形式なので、matplotlib から使うときは numpy でスライスする
# だけなのだが、今までの plot プログラムからの呼び出しとの互換のために
# Method 化する
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.05.08 startup
#
################################################################################
from __future__ import print_function

from sae.errors import legacy_error as _legacy_error

from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.1.1"

################################################################################

import sys

# import gzip
import os

# import re
import optparse
import numpy as np

import StructureAnalysisEnvironment as SAEnv

# import SpaceGroupEnvironment as SGE


################################################################################
class TotalDOS(object):

    def __init__(self, cname="input.dos"):

        self.datlines, self.num = SAEnv.read_dataline(cname)
        self.nedos = self.num - 1

        if len(self.datlines[1].split()) > 3:
            self.ispin = 2
        else:
            self.ispin = 1

        self.eng = np.zeros((self.nedos))
        self.tdos_all = np.zeros((self.nedos, self.ispin))
        self.inttdos_all = np.zeros((self.nedos, 1))

        for i in range(self.nedos):
            self.eng[i] = float(self.datlines[1 + i].split()[0])
            if self.ispin >= 2:
                self.tdos_all[i, 0] = float(self.datlines[1 + i].split()[1])
                self.tdos_all[i, 1] = float(self.datlines[1 + i].split()[2])
                self.inttdos_all[i, 0] = float(self.datlines[1 + i].split()[3])
            else:
                self.tdos_all[i, 0] = float(self.datlines[1 + i].split()[1])
                self.inttdos_all[i, 0] = float(self.datlines[1 + i].split()[2])

        # default spin=1
        self.tdos = self.tdos_all[:, 0]
        self.inttdos = self.inttdos_all[:, 0]

    def get_eng(self):
        return self.eng

    def get_tdos(self, spin=0):
        return self.tdos_all[:, spin]

    def get_inttdos(self, spin=0):
        if spin != 0:
            raise ValueError("QE integrated DOS is spin-summed; use spin=0")
        return self.inttdos_all[:, 0]

    def get_ispin(self):
        return self.ispin

    def get_nedos(self):
        return self.nedos


################################################################################
def options():
    name = "Fe.dos"

    parser = optparse.OptionParser()
    parser.add_option(
        "-i",
        "--input",
        dest="INPUT",
        default=name,
    )
    options, args = parser.parse_args()

    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]

    return name


################################################################################
if __name__ == "__main__":

    name = options()
    dos = ReadPwTdos(name)

    nedos = dos.get_nedos()
    tdos = dos.get_tdos(spin=0)
    eng = dos.get_eng()
    print("ISPIN %s" % str(dos.get_ispin()))

    for i in range(nedos):
        print(" %11.8f %11.8f " % (eng[i], tdos[i]))


ReadPwTdos = TotalDOS  # historical spelling
