#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import re
import os
import optparse
from ase.io import read, write
from ase.io.vasp import *
from ase.io.xyz import *
from ase.lattice.surface import *

if __name__ == "__main__":
    poscarname = "POSCAR"
    outname = "POSCAR.surface.vasp"
    print("INPUT POSCAR file  = ", poscarname)
    print("OUTPUT POSCAR file = ", outname)
    atoms = read(poscarname, format="vasp")
    s = surface(atoms, (1, 1, 1), 5, vacuum=10.0)
    s.write(outname, format="vasp", direct=True, vasp5=True)
