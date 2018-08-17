#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#  using ASE
#
#  read: format='cif'
#  write: format='vasp'
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
#from ase.lattice import bulk
#from ase.dft.kpoints import ibz_points, get_bandpath
###############################

#from gpaw import GPAW, PW, FermiDirac, setup_paths
#from gpaw import GPAW, PW
#setup_paths.insert(0,'.')

import StructureAnalysisEnvironment as SAE

################################################################################
def options():

    base = 'POSCAR'
    ##############################################
    in_suffix = '.cif'
    ##############################################

    out_suffix = '.vasp'

    name = base+in_suffix

    if not os.path.exists(name):
        try:
            base0 = SAE.find_datfile('cif')
            if not base0 is None:
                base = base0
                name = base+in_suffix
        except:
            pass

    parser = optparse.OptionParser(os.getcwd())
    parser = optparse.OptionParser()
    parser.add_option( '-i','--input',dest='INPUT')
    options,args = parser.parse_args()

    if options.INPUT:
        name = options.INPUT
        base = re.sub(in_suffix,'',name)

    if len(args) > 0:
        name = args[0]
        base = re.sub(in_suffix,'',name)

    if not os.path.exists(name):
        sys.exit("STOP: "+name+" file not found")

    return name,base,in_suffix,out_suffix

################################################################################
if __name__ == '__main__':

    cifname,base,in_suffix,out_suffix = options()

    cifname = cifname                # inputname
    poscarname = cifname+out_suffix  # outputname

    print("INPUT CIF file  = ",cifname)
    print("OUTPUT POSCAR file = ",poscarname)

    atoms = read(cifname,format='cif')
    atoms.center()

    atoms.write(poscarname,format='vasp',direct=True,vasp5=True)


