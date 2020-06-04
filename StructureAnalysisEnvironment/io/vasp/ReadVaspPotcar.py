#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# POTCAR
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応暫定
#
# 2015.07.07 startup
#
################################################################################
from __future__ import print_function

try:
    from ...copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import sys
import os
import re
# import gzip
import numpy as np

import optparse

try:
    # sys.path.append('../..')
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    import StructureAnalysisEnvironment as SAEnv
    from StructureAnalysisEnvironment.Method import *
    from StructureAnalysisEnvironment.io import *
except ImportError:
    import StructureAnalysisEnvironment as SAEnv
    from StructureAnalysisEnvironment.io import *


# import SpaceGroupEnvironment as SGE


################################################################################
class ReadVaspPotcar(object):

    def __init__(self, POTCAR='POTCAR'):

        self.datlines, self.num = SAEnv.read_dataline(POTCAR)

        vrhfin_reg = re.compile('.*VRHFIN')
        zval_reg = re.compile('.*ZVAL')

        self.nion = 0
        self.atoms_index = []
        self.atoms_zval = []

        for i in range(self.num):
            if bool(vrhfin_reg.match(self.datlines[i])):
                atom0 = re.sub('.*VRHFIN =', '', self.datlines[i])
                self.atoms_index.append(re.sub(':.*', '', atom0).strip())
                self.nion += 1
            if bool(zval_reg.match(self.datlines[i])):
                zval0 = re.sub('.*ZVAL', '', self.datlines[i])
                self.atoms_zval.append(float(re.sub('^.*=', '', zval0).split()[0]))

        if len(self.atoms_index) != len(self.atoms_zval):
            sys.exit("STOP: atoms_index != atoms_zval")

    def get_nion(self):
        return self.nion

    def get_atoms_index(self):
        return self.atoms_index

    def get_atoms_zval(self):
        return self.atoms_zval


################################################################################
def options():
    name = 'POTCAR'
    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest='INPUT', )
    options, args = parser.parse_args()
    if options.INPUT: name = options.INPUT

    return name


################################################################################
if __name__ == '__main__':
    name = options()
    potcar = ReadVaspPotcar(name)

    print("%s" % str(potcar.nion))
    print("%s" % str(potcar.atoms_index))
    print("%s" % str(potcar.atoms_zval))
