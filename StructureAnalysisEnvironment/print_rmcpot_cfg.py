#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# RMC_POT (cfg) 出力 まとめ(ラップ)ルーチン
#
################################################################################
# History
#
# 2015.08.24
#  startup
#
################################################################################
from __future__ import print_function

try:
    from copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

# import sys
# import os
# import re
# import gzip
# import numpy as np
import StructureAnalysisEnvironment as SAEnv


# import SpaceGroupEnvironment as SGE

def print_rmcpot_cfg(cname, STD, \
                     title, scale, natom, nion, selective, direct, vasp_version, \
                     t, atoms, atoms_index, position, fix):
    # scale factor to 1.0
    scale, t, natom, direct, position = SAEnv.conv_scale21( \
        scale, \
        t, \
        natom, \
        direct, \
        position)

    # Cartesian to Direct
    if not direct:
        scale, t, natom, direct, position = SAEnv.conv_car2direct( \
            scale, \
            t, \
            natom, \
            direct, \
            position)

    # RMC_POT(cfg) へ変換
    scale, t, natom, direct, position = SAEnv.conv_vasp2cfg( \
        scale, \
        t, \
        natom, \
        direct, \
        position)

    # print cfg (RMC_POT) style
    SAEnv.print_rmcpot_cfg_raw( \
        cname, \
        STD, \
        title, \
        t, \
        natom, \
        nion, \
        atoms, \
        position)
