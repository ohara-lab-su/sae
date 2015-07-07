#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# ACF.dat viewer
#
################################################################################
#
# 2015.07.07 startup
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015 Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.5"
################################################################################

import sys
import os
import re
#import gzip
import numpy as np

import optparse

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE


################################################################################
def options():

    name = 'POSCAR'
    parser = optparse.OptionParser()
    parser.add_option( '-i','--input', dest='INPUT',)
    options, args = parser.parse_args()

    if options.INPUT: name = options.INPUT

    if not os.path.exists(name):
        name0 = 'CONTCAR'
        if not os.path.exists(name0):
            sys.exit("STOP: "+name+" and "+name0+" file not found")
        else:
            name = name0

    return name

################################################################################
if __name__ == '__main__':

    name = options()

    poscar = SAE.ReadPoscar(name)
    potcar = SAE.ReadVaspPotcar()
    acfdat = SAE.ReadVaspAcf(poscar=poscar,potcar=potcar,acf='ACF.dat')
    acfdat.get_max_bader()
    acfdat.get_min_bader()

    print "#  atom  zval  charge  diff"
    for i in range(acfdat.natom):
        print "%3d %s %5.2f %7.3f %7.3f" \
                %(i+1,acfdat.atoms_index_j[i],acfdat.atoms_zval_j[i],\
                acfdat.charge[i],acfdat.bader[i])

    print "----------"
    print "MAX charge",acfdat.max_bader
    print "MIN charge",acfdat.min_bader
#   print poscar.natom


