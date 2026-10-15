#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# MD(x,yz) のそれぞれの x,y,z の最大値を取得
#
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.01.08 startup
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

# import sys
import optparse
# import os
# import re
# from numpy import *
import numpy as np

import StructureAnalysisEnvironment as SAE


# import SpaceGroupEnvironment as SGE


################################################################################
def get_max_md(nloop, natom, position_loop):
    # 原子毎,xyz の最大値を取得
    position_max_atom_xyz = np.zeros((natom, 3))
    position_min_atom_xyz = np.zeros((natom, 3))
    for xyz in range(0, 3):
        for j in range(natom):
            position_max_atom_xyz[j, xyz] = max(position_loop[:, j, xyz])
            position_min_atom_xyz[j, xyz] = min(position_loop[:, j, xyz])

    # 原子毎の最大値を取得
    position_max_xyz = np.zeros(3)
    position_min_xyz = np.zeros(3)
    for xyz in range(0, 3):
        position_max_xyz[xyz] = max(position_max_atom_xyz[:, xyz])
        position_min_xyz[xyz] = min(position_min_atom_xyz[:, xyz])

    # 最大値を取得
    position_max = max(position_max_xyz[:])
    position_min = min(position_max_xyz[:])

    #   print position_max, position_min

    return [position_max, position_min]


################################################################################
if __name__ == '__main__':

    MD = 'co.md'

    parser = optparse.OptionParser()
    parser.add_option('-i', '--input',
                      dest='INPUT',
                      default=MD,
                      )
    options, args = parser.parse_args()

    if options.INPUT:
        MD = options.INPUT

    if len(args) > 0:
        MD = args[0]

    title = MD

    # MX(xyz) ファイルの事前読み込み
    nloop, natom = SAE.read_md_param(MD)

    # MD(xyz) ファイルの事前準備
    atoms_index_j = np.zeros((natom), dtype='S2')
    position_loop = np.zeros((nloop, natom, 3))
    force_loop = np.zeros((nloop, natom, 3))

    # MD(xyz) ファイル読み込み + Force 対応
    natom, nlist, elist, nion, atoms, atoms_index, energy_loop = \
        SAE.read_md3(MD, nloop, atoms_index_j, position_loop, force_loop)

    # MD(x,y,z) のそれぞれの x,y,z の最大値を取得
    position_max, position_min = get_max_md(nloop, natom, position_loop)

    print("%s %s" % (str(position_min), str(position_max)))
