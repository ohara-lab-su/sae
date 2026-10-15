#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.common.paths import FileDiscovery
import sys
import os
from ase.io import read, write
from ase.io.vasp import *
from ase.io.xyz import *
from ase.lattice.surface import *

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
#
# 2018.08.17
#  Python2/3 両対応
#
################################################################################
################################################################################
#import re
#import optparse
#import numpy as np
################################ ASE
#from ase.lattice import bulk
#from ase.dft.kpoints import ibz_points, get_bandpath
###############################
#from gpaw import GPAW, PW, FermiDirac, setup_paths
#from gpaw import GPAW, PW
#setup_paths.insert(0,'.')
################################################################################
#
#
if __name__ == "__main__":
    cifname = "case.cif"
    if not os.path.exists(cifname):
        cifname = FileDiscovery().find_datfile("cif")
        if cifname is None:
            sys.exit("STOP: cif file not found")
        cifname = cifname + ".cif"
    outname1 = cifname + ".POSCAR.vasp"
    outname2 = cifname + ".POSCAR.surface.vasp"
    print("INPUT CIF file             = ", cifname)
    print("OUTPUT POSCAR crystal file = ", outname1)
    print("OUTPUT POSCAR surface file = ", outname2)
    cel = read(cifname, format="cif")
    sur = surface(cel, (1, 1, 1), 5, vacuum=15.0)
    sur.center(vacuum=15, axis=2)
    cel.write(outname1, format="vasp", direct=True, vasp5=True)
    sur.write(outname2, format="vasp", direct=True, vasp5=True, sort=True)
