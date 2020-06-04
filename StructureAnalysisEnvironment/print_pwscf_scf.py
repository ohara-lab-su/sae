#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# print
#   PWScf (Quantum ESPRESSO ) to *.in
#
################################################################################
#
# 2018.08.21
#  Python2/3 両対応
#
# 2015.08.24
#  startup
#  統合化用にこれまでの PWvasp2in から分離
#
# 2015.03.20
#  PWvasp2in startup
#
################################################################################
from __future__ import print_function

try:
    from copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.1.0"

################################################################################

# import optparse
import sys
# import os
# import re
# import numpy as np

# import glob
import StructureAnalysisEnvironment as SAE


# import SpaceGroupEnvironment as SGE


################################################################################
def print_pwscf_scf(cname, STD,
                    title, scale, natom, nion, selective, direct, vasp_version,
                    t, atoms, atoms_index, position, fix,
                    atoms_index_j):
    ############################################################################
    # mode
    title = 'input'
    calculation = 'scf'
    title = 'input'
    pseudo_dir = './'
    outdir = './work/'
    ecutwfc = 25.0
    ecutrho = 100.0  # ecutwfc*4.0
    occupations = 'tetrahedra'
    mixing_beta = 0.7
    conv_thr = 0.01
    mag = 0.6  # starting_magnetization(1)

    ############################################################################
    # output system.inp
    if STD:
        out = sys.stdout
    else:
        try:
            out = open(cname, 'w')
        except:
            out.close()
            sys.exit("STOP: " + cname + " can't open")

    print("&control", file=out)
    print("                calculation = " + "'" + calculation + "'" + ",", file=out)
    print("                     prefix = " + "'" + title + "'" + ",", file=out)
    print("                 pseudo_dir = " + "'" + pseudo_dir + "'" + ",", file=out)
    print("                     outdir = " + "'" + outdir + "'" + ",", file=out)
    print("!                   tstress = .true.,", file=out)
    print("!                   tprnfor = .true.,", file=out)
    print("!             etot_conv_thr = 1.d-5,", file=out)
    print("!             forc_conv_thr = 1.d-4,", file=out)

    print("/", file=out)

    print("&system", file=out)
    print("                      ibrav = 0,", file=out)
    print("                          a = " + str(scale) + ",", file=out)
    print("                        nat = " + str(natom) + ",", file=out)
    print("                       ntyp = " + str(nion) + ",", file=out)
    print("                    ecutwfc = " + str(ecutwfc) + ",", file=out)
    print("!                   ecutrho = " + str(ecutrho) + ",", file=out)
    print("                occupations = " + str(occupations) + ",", file=out)
    print("!               occupations = 'smearing'" + ",", file=out)
    print("!                  smearing = 'mp'" + ",", file=out)
    print("!                  smearing = 'gaussian'" + ",", file=out)
    print("!                   degauss = 0.01" + ",", file=out)
    print("!                     nspin = " + "2" + ",", file=out)
    print("! starting_magnetization(1) = " + str(mag) + ",", file=out)
    print("/", file=out)

    print("&electrons", file=out)
    print("                mixing_beta = " + str(mixing_beta) + ",", file=out)
    print("                   conv_thr = " + str(conv_thr) + ",", file=out)
    print("!                  conv_thr = 1.0d-8,", file=out)
    print("/", file=out)

    #   print("CELL_PARAMETERS {angstrom}", file=out)
    print("CELL_PARAMETERS {alat}", file=out)
    print(" %18.15f %18.15f %18.15f" % (t[0, 0], t[1, 0], t[2, 0]), file=out)
    print(" %18.15f %18.15f %18.15f" % (t[0, 1], t[1, 1], t[2, 1]), file=out)
    print(" %18.15f %18.15f %18.15f" % (t[0, 2], t[1, 2], t[2, 2]), file=out)

    print("ATOMIC_SPECIES", file=out)
    for ion in range(nion):
        atomic_weight = SAE.get_atomic_weight1(atoms_index[ion])
        # print(" %s %9.5f" %(atoms_index[ion], atomic_weight), file=out)
        print(" %s %9.5f %s%s"
              % (atoms_index[ion], atomic_weight, atoms_index[ion], "_PSEUDO"), file=out)

    print("ATOMIC_POSITIONS {crystal}", file=out)
    for j in range(natom):
        print(" %s  %18.15f %18.15f %18.15f"
              % (atoms_index_j[j], position[j, 0], position[j, 1], position[j, 2]), file=out)

    print("K_POINTS {automatic}", file=out)
    print("6 6 6 0 0 0", file=out)

    if not STD:
        out.close()
