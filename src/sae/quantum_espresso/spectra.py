#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# PWScf (Quantum ESPRESSO 5..x )
# xanes.dat ( xspectra.x )
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.07.22 startup
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
import re
import optparse
import numpy as np

import StructureAnalysisEnvironment as SAEnv

# import SpaceGroupEnvironment as SGE


################################################################################
class XANES(object):

    def __init__(self, cname="xanes.dat"):

        self.datlines, self.num = SAEnv.read_dataline(cname)

        self.xas = np.zeros(self.num - 4)
        self.eng = np.zeros(self.num - 4)

        comment_reg = re.compile("^#.*")
        space_reg = re.compile("^$")
        broad_reg = re.compile("^#.*broadening")
        absorber_reg = re.compile("^#.*absorbing")

        j = 0
        for line in self.datlines:

            if bool(broad_reg.match(line)):
                self.broad = float(line.split()[5])

            if bool(absorber_reg.match(line)):
                self.absorber = int(line.split()[4])

            if not bool(comment_reg.match(line)):
                if not bool(space_reg.match(line)):
                    self.eng[j] = float(line.split()[0])
                    self.xas[j] = float(line.split()[1])
                    j += 1
        self.num = j

    def get_xas(self):
        return self.xas

    def get_eng(self):
        return self.eng

    def get_absorber(self):
        return self.absorber

    def get_broad(self):
        return self.broad


################################################################################
def options():
    name = "scf.out"

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
    dat = ReadPwXanes()

    for i in range(dat.num):
        print("%s %s" % (str(dat.eng[i]), str(dat.xas[i])))


ReadPwXanes = XANES  # historical spelling
