#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#  read POSCAR  using ASE
#
#  一般化していない（する必要も無い)
#  (111)面作成 サンプル
#
# surface(lattice, indices, layers, vacuum=0.0, )
#
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
if __name__ == '__main__':

    poscarname = 'POSCAR'
    outname = 'POSCAR.surface.vasp'

    print "INPUT POSCAR file  = ",poscarname
    print "OUTPUT POSCAR file = ",outname

    atoms = read(poscarname,format='vasp')

    s = surface(atoms, (1,1,1), 5, vacuum=10.0)
#   s.center(vacuum=10, axis=2)

    s.write(outname,format='vasp',direct=True,vasp5=True)
#   atoms.write(structname,format='struct')


