# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# VASPの LORBIT 11 で動かした時の lm 番号から軌道名を取り出すだけの関数
#
# [in]  lm
# [return] orbital
#
################################################################################
from __future__ import print_function

try:
    from .copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"


################################################################################
#
# 2015.01.15 startup
#
################################################################################

# import sys
# import os
# import re
# from numpy import *

#
# s py pz px dxy dyz dz2 dxz dx2
#
def get_vasp_orbital_info(lm):
    orbital_list = [
        's',
        'p_y',
        'p_z',
        'p_x',
        'd_xy',
        'd_yz',
        'd_3z3-r2',
        'd_xz',
        'd_x2-y2',
    ]

    orbital = orbital_list[lm]

    return orbital
