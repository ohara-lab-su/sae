#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# PDB file CRYST1 flag checker
#
#  PDB ファイル中の CRYST1 フラグ(コメント中にある)
#  を探して、PDB ファイルなのに何故か結晶モードであるかどうかの判断が出来る
#
################################################################################
#
# 2015.08.20
#  分離
#
# 2015.05.18
#  startup
#
################################################################################
from __future__ import print_function

from sae.errors import legacy_error as _legacy_error
try:
    from .copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################
#
# import os
import sys


# import optparse
# import numpy as np

# import StructureAnalysisEnvironment as SAE

################################################################################
def chk_pdb_cryst1(filename):
    try:
        pdbfile = open(filename)
    except:
        pdbfile.close()
        _legacy_error("STOP(chk_cryst1):" + filename + "file can'nt open")

    cryst1 = False
    for line in pdbfile.readlines():
        if line.startswith('CRYST1'):
            cryst1 = True

    pdbfile.close()

    return cryst1
