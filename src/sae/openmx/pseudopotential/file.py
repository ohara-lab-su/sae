#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OpenMX 3.7
#    DAT_DATA13/VPSファイルを読み込む
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.02.09 1st
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

# import optparse
# import numpy as np

# import re
# from copy import deepcopy

# import StructureAnalysisEnvironment as SAE
# import SpaceGroupEnvironment as SGE


################################################################################
#
#   data = '../DFT_DATA13'
#   atom = 'C'
#   pot  = 'PBE'
#   ver  = '13'
#   name = 'C_PBE13'
#
################################################################################
class Pseudopotential(object):

    #   def __init__(self,opts):
    def __init__(self, fullname):

        #       data,\
        #       atom,\
        #       pot,\
        #       ver,\
        #       name = opts
        #       fullname = data+'/VPS/'+name+'.vps'

        if not os.path.exists(fullname):
            _legacy_error(fullname + " file not found")

        try:
            tmp = open(fullname)
            datfile = tmp.read()
        except:
            _legacy_error("STOP: " + fullname + " does'nt open")
        finally:
            tmp.close()

        self.datlines = datfile.split("\n")
        self.num = len(self.datlines) - 1

    # valence.electron を返す
    def get_valence_electron(self):
        valence_reg = re.compile("^.*valence.electron.*", re.IGNORECASE)
        for i in range(self.num):
            if bool(valence_reg.match(self.datlines[i])):
                electron = float(self.datlines[i].split()[1])
                break

        return electron


################################################################################
if __name__ == "__main__":
    data = "../DFT_DATA13"
    atom = "C"
    pot = "PBE"
    ver = "13"

    name = atom + "_" + pot + ver
    fullname = data + "/VPS/" + name + ".vps"
    #   opts = data, atom, pot, ver, name

    vps = ReadMxVps(fullname)
    electron = vps.get_valence_electron()

    print(electron)

################################################################################


ReadMxVps = Pseudopotential  # historical spelling
