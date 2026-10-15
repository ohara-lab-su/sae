#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.hilapw.sets_fields import SetsFields
from sae.hilapw.sets_writer import SetsWriter

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# sets.in (HiLPAW) 読み込みルーチンの基本
#
# ただ読んで同じものを吐き出すだけ
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import numpy as np


#
################################################################################
#import sys
#import os
#import re
#import optparse
################################################################################
def options():
    cname = "sets.in"
    return cname


################################################################################
# sets.in 読み込みの準備&前段階
#   for i in range(nion):
#       print lattices0[3][i]
# sets.in 読み込み
#   for i in range(sg_natom):
#       print " %8.6f %8.6f %8.6f " % (sg_position[i,0],
#                                      sg_position[i,1],
#                                      sg_position[i,2])
# sets.in 書き込み
#cname='sets.in_out'
#STD=False
if __name__ == "__main__":
    cname = options()
    lattices0 = []
    lattices0.extend(SetsFields().read_sets_param())
    sgn_index = lattices0[0]
    nion = lattices0[1]
    sg_natom = lattices0[2]
    lattices = np.zeros(6, dtype=float)
    sg_atoms = np.zeros(nion, dtype=int)
    sg_atoms_index = []
    sg_position = np.zeros((sg_natom, 3), dtype=float)
    kpoints = np.zeros(3, dtype=int)
    title, nspin, kinfo = SetsFields().read_sets(
        cname, lattices, nion, sg_atoms, sg_atoms_index, sg_position, kpoints
    )
    STD = True
    SetsWriter().print_sets(
        cname,
        STD,
        title,
        nspin,
        sgn_index,
        lattices,
        nion,
        sg_atoms,
        sg_atoms_index,
        sg_position,
        kinfo,
        kpoints,
    )
