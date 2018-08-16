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
# 2015.08.24
#  startup
#  統合化用にこれまでの PWvasp2in から分離
#
# 2015.03.20
#  PWvasp2in startup
#
################################################################################
from __future__ import print_function
###############################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.1.0"
################################################################################

#import optparse
import sys
#import os
#import re
#import numpy as np

#import glob
import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE


################################################################################
def print_pwscf_scf(cname,STD,\
        title,scale,natom,nion,selective,direct,vasp_version,\
        t,atoms,atoms_index,position,fix,\
        atoms_index_j):

    ############################################################################
    # mode
    title       = 'input'
    calculation = 'scf'
    title       = 'input'
    pseudo_dir  = './'
    outdir      = './work/'
    ecutwfc     = 25.0
    ecutrho     = 100.0  # ecutwfc*4.0
    occupations = 'tetrahedra'
    mixing_beta = 0.7
    conv_thr    = 0.01
    mag         = 0.6  # starting_magnetization(1)

    ############################################################################
    # output system.inp
    if STD:
        out = sys.stdout
    else:
        try:
            out = open(cname,'w')
        except:
            out.close()
            sys.exit("STOP: "+cname+" can't open")

    print >> out, "&control"
    print >> out, "                calculation = "+"'"+calculation+"'"+","
    print >> out, "                     prefix = "+"'"+title+"'"+","
    print >> out, "                 pseudo_dir = "+"'"+pseudo_dir+"'"+","
    print >> out, "                     outdir = "+"'"+outdir+"'"+","
    print >> out, "!                   tstress = .true.,"
    print >> out, "!                   tprnfor = .true.,"
    print >> out, "!             etot_conv_thr = 1.d-5,"
    print >> out, "!             forc_conv_thr = 1.d-4,"

    print >> out, "/"

    print >> out, "&system"
    print >> out, "                      ibrav = 0,"
    print >> out, "                          a = "+str(scale)+","
    print >> out, "                        nat = "+str(natom)+","
    print >> out, "                       ntyp = "+str(nion)+","
    print >> out, "                    ecutwfc = "+str(ecutwfc)+","
    print >> out, "!                   ecutrho = "+str(ecutrho)+","
    print >> out, "                occupations = "+str(occupations)+","
    print >> out, "!               occupations = 'smearing'"+","
    print >> out, "!                  smearing = 'mp'"+","
    print >> out, "!                  smearing = 'gaussian'"+","
    print >> out, "!                   degauss = 0.01"+","
    print >> out, "!                     nspin = "+"2"+","
    print >> out, "! starting_magnetization(1) = "+str(mag)+","
    print >> out, "/"

    print >> out, "&electrons"
    print >> out, "                mixing_beta = "+str(mixing_beta)+","
    print >> out, "                   conv_thr = "+str(conv_thr)+","
    print >> out, "!                  conv_thr = 1.0d-8,"
    print >> out, "/"

#   print >> out, "CELL_PARAMETERS {angstrom}"
    print >> out, "CELL_PARAMETERS {alat}"
    print >> out, " %18.15f %18.15f %18.15f" %(t[0,0], t[1,0], t[2,0])
    print >> out, " %18.15f %18.15f %18.15f" %(t[0,1], t[1,1], t[2,1])
    print >> out, " %18.15f %18.15f %18.15f" %(t[0,2], t[1,2], t[2,2])

    print >> out, "ATOMIC_SPECIES"
    for ion in range(nion):
        atomic_weight = SAE.get_atomic_weight1(atoms_index[ion])
       #print >> out, " %s %9.5f" %(atoms_index[ion], atomic_weight)
        print >> out, " %s %9.5f %s%s" \
                %(atoms_index[ion], atomic_weight,atoms_index[ion],"_PSEUDO")

    print >> out, "ATOMIC_POSITIONS {crystal}"
    for j in range(natom):
        print >> out, " %s  %18.15f %18.15f %18.15f" \
                %( atoms_index_j[j], position[j,0], position[j,1], position[j,2] )

    print >> out, "K_POINTS {automatic}"
    print >> out, "6 6 6 0 0 0"

    if not STD:
        out.close()

