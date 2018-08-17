#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#  POSCAR の a,b,cc 軸方向の真空層を増やしたり減らしたりする
#
#  using ASE
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
################################################################################
from __future__ import print_function
################################################################################

import sys
import re
import os
import optparse
#import numpy as np

################################ ASE
from ase.io import read,write
from ase.io.vasp import *
from ase.io.xyz import *
from ase.lattice.surface import *
#from ase.lattice import bulk
#from ase.dft.kpoints import ibz_points, get_bandpath
###############################

#from gpaw import GPAW, PW, FermiDirac, setup_paths
#from gpaw import GPAW, PW
#setup_paths.insert(0,'.')

import StructureAnalysisEnvironment as SAE

################################################################################
def options():

    inpname = 'POSCAR'
    outname = 'POSCAR.vasp'
    vacuum = None

    parser = optparse.OptionParser()
    parser.add_option( '-i','--input', dest='INPUT',)
    parser.add_option( '-o','--output', dest='OUTPUT',)
    parser.add_option( '-v','--vacuum',)
    options, args = parser.parse_args()

    if options.INPUT: inpname = options.INPUT
    if options.OUTPUT: outname = options.OUTPUT

    if options.vacuum:
        vacuum = float(options.vacuum)
    else:
        sys.exit("STOP: plase input vacuum size")

    if inpname == outname:
        sys.exit("STOP: (IN)"+inpname+", (OUT)"+outputname)

    return [inpname,outname,vacuum]

################################################################################
if __name__ == '__main__':

    inpname,outname,vacuum = options()

    print("INPUT POSCAR file  = ",inpname)
    print("OUTPUT POSCAR file = ",outname)
    print("Vacuum SIZE        = ",str(vacuum))

    cell = read(inpname,format='vasp')

    if not vacuum is None:
        cell.center(vacuum=vacuum)

    cell.write(outname,format='vasp',direct=True,vasp5=True)
#   atoms.write(structname,format='struct')


