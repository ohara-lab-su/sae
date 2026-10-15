#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from ase.io import read, write
from ase.io.vasp import *
from ase.io.xyz import *

#!/usr/bin/env python                                                           
################################################################################
################################################################################
#import numpy as np                                                             
################################ ASE
#from ase.lattice import bulk
#from ase.dft.kpoints import ibz_points, get_bandpath
###############################
#from gpaw import GPAW, PW, FermiDirac, setup_paths
#from gpaw import GPAW, PW
#setup_paths.insert(0,'.')
atoms = read_vasp("POSCAR")
atoms.write("POSCAR.cif", format="cif")
