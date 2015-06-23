#!/usr/bin/env python

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


cell = read_vasp('POSCAR')

write_vasp('POSCAR_444.vasp', cell*(4,4,4), label='444supercell',direct=True,sort=True,vasp5=True)

#atoms.write('POSCAR.cif',format='cif')
