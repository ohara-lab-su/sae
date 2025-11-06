#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Get fermi for PWSCf
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.07.17 startup
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.1.1"
################################################################################

import sys
#import gzip
#import os
import re
import optparse
import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE


################################################################################
def options():
    name = 'scf.out'

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT', default=name,)
    options,args = parser.parse_args()

    if options.INPUT: name=options.INPUT
    if len(args) > 0: name=args[0]

    return name

################################################################################
if __name__ == '__main__':

    name = options()
    out = SAE.ReadPwOut(name)

    print("NAME",name)

    print("TITLE",out.get_title())

    print("LATTICE PARAMETER %6.4f" % (out.get_scale()))

    print("NATOM",out.get_natom())
    print("NION",out.get_nion())
    print("NBANDS",out.get_nbands())
    print("NSW",out.get_nsw())
    print("ION-LOOP",out.get_n_ion_loop())
    print("")
    print("EFERMI(eV)",out.get_efermi())
    print("EFERMI(Ry)",out.get_efermi()/13.6)

#   print ""
#   print out.get_atoms_index()
#   print out.get_atoms()
#   print ""

#   print ""
#   print out.get_atoms_j()
#   print out.get_atoms_index_j()

#   print ""
#   print "TRANSLATION VECTOR"
#   print out.get_t()

#   print ""
#   print out.get_position()

#   print ""
#   position_loop = out.get_position_loop()
#   for j in range(out.get_n_ion_loop()):
#       print ""
#       print position_loop[j,:,:]

#   print "FORCE"
#   force_loop = out.get_force_loop()
#   for j in range(out.get_n_ion_loop()):
#       print ""
#       print force_loop[j,:,:]

#   print "ENERGY"
#   toten_ion = out.get_toten_ion()
#   for i in range(out.get_n_ion_loop()):
#       print toten_ion[i]


