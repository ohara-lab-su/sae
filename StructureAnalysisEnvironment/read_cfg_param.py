# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# *.cfg ファイル読み込みのための準備関数
#
# [in/out] cname    : *.cfg filename
#
# [return] natom    : number of atom
# [return] nion    : number of ion
#
################################################################################
#
# 2014.10.30 1st
#
################################################################################
try:
    from .copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import sys
import os
import optparse
from numpy import *


def read_cfg_param(cname):
    ###############################################
    ## Open RMC_POT cfg file
    ##
    try:
        tmp = open(cname + '.cfg')
    except:
        tmp.close()
        sys.exit("Error(read_cfg_param.py): " + cname + ".cfg not open")

    datfile = tmp.read()
    tmp.close()
    datlines = datfile.split('\n')

    ###############################################
    ## Read Header
    ##
    a = datlines[7].split()
    natom = int(a[0])

    a = datlines[8].split()
    nion = int(a[0])

    return [natom, nion]
