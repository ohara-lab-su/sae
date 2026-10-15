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
