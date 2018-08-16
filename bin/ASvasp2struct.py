#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#  using ASE
#
################################################################################
from __future__ import print_function
################################################################################
import sys
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


################################################################################

poscarname = 'POSCAR'
wien_suffix = '.struct'

parser = optparse.OptionParser(os.getcwd())
parser = optparse.OptionParser()
parser.add_option( '-i','--input',dest='INPUT')
options,args = parser.parse_args()

if options.INPUT: poscarname=options.INPUT
if len(args) > 0: poscarname=args[0]

if not os.path.exists(poscarname):
    poscarname0 = poscarname
    poscarname = 'CONTCAR'
    if not os.path.exists(poscarname):
        sys.exit("STOP: "+poscarname+" and "+poscarname0+" file not found")

print "INPUT POSCAR file  = ",poscarname
print "OUTPUT struct file = ",poscarname+wien_suffix

atoms = read_vasp(poscarname)
atoms.write(poscarname+wien_suffix,format='struct')


