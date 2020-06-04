#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# sets.in (HiLPAW) 書き出しルーチンの基本
#
################################################################################
from __future__ import print_function
from copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.02.16
#  無駄な import をコメントアウト
#
################################################################################

import sys
import os


# import re
# import optparse
# from numpy import *


def print_sets(cname, STD,
               title, nspin, spg_name, lattices, nion, sg_atoms, sg_atoms_index, sg_position, kinfo, kpoints):
    if STD:
        out = sys.stdout
    else:
        if os.path.exists(cname):
            sys.exit("STOP(print_sets.py): " + cname + " exists")
        else:
            try:
                out = open(cname, 'w')
            except:
                out.close()
                sys.exit("STOP(print_sets.py): " + cname + " does'nt open")

    print(title, file=out)
    print("-----nspin", file=out)
    print("%s" % str(nspin), file=out)
    print("-----space group", file=out)
    print("%s" % str(spg_name), file=out)
    print("  %8.4f %8.4f %8.4f" % (lattices[0], lattices[1], lattices[2]), file=out)
    print("  %8.4f %8.4f %8.4f" % (lattices[3], lattices[4], lattices[5]), file=out)
    print("-----atoms", file=out)
    print(" %s" % str(nion), file=out)

    index = 0
    for i in range(nion):
        print("%s %s" % (str(sg_atoms_index[i]), str(sg_atoms[i])), file=out)
        for j in range(sg_atoms[i]):
            print(" %13.9f %13.9f %13.9f"
                  % (sg_position[index, 0], sg_position[index, 1], sg_position[index, 2]), file=out)
            index += 1

    print("-----k points")
    print("%s" % str(kinfo))
    print("%s %s %s" % (str(kpoints[0]), str(kpoints[1]), str(kpoints[2])))

    out.close()
