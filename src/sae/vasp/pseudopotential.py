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

from sae.errors import legacy_error as _legacy_error

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
    pass  # package imports do not alter sys.path
    import StructureAnalysisEnvironment as SAEnv
    from StructureAnalysisEnvironment.Method import *

    pass  # dependencies are explicit below
except ImportError:
    import StructureAnalysisEnvironment as SAEnv

    pass  # dependencies are explicit below
try:
    from sae._logging import XLogger
except ImportError:
    pass

# import SpaceGroupEnvironment as SGE


################################################################################
class Potcar(object):

    def __init__(
        self,
        POTCAR="POTCAR",
        logger: XLogger = None,
    ):
        try:
            logger = XLogger(log_level="debug")
        except:
            import logging

            logger = logging.getLogger("dummy")
            logger.addHandler(logging.NullHandler())

        self.logger = logger
        self.logger.info("== ReadVaspPotcar() ==")

        self.datlines, self.num = SAEnv.read_dataline(POTCAR)

        vrhfin_reg = re.compile(".*VRHFIN")
        zval_reg = re.compile(".*ZVAL")

        self.nion = 0
        self.atoms_index = []
        self.atoms_zval = []

        for i in range(self.num):
            if bool(vrhfin_reg.match(self.datlines[i])):
                atom0 = re.sub(".*VRHFIN =", "", self.datlines[i])
                self.atoms_index.append(re.sub(":.*", "", atom0).strip())
                self.nion += 1
            if bool(zval_reg.match(self.datlines[i])):
                zval0 = re.sub(".*ZVAL", "", self.datlines[i])
                self.atoms_zval.append(float(re.sub("^.*=", "", zval0).split()[0]))

        if len(self.atoms_index) != len(self.atoms_zval):
            _legacy_error("STOP: atoms_index != atoms_zval")

    def get_nion(self):
        return self.nion

    def get_atoms_index(self):
        return self.atoms_index

    def get_atoms_zval(self):
        return self.atoms_zval


################################################################################
def options():
    name = "POTCAR"
    parser = optparse.OptionParser()
    parser.add_option(
        "-i",
        "--input",
        dest="INPUT",
    )
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT

    return name


################################################################################
if __name__ == "__main__":
    name = options()
    potcar = ReadVaspPotcar(name)

    print("%s" % str(potcar.nion))
    print("%s" % str(potcar.atoms_index))
    print("%s" % str(potcar.atoms_zval))


ReadVaspPotcar = Potcar  # historical spelling
