#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from ase.io import read, write
from ase.io.vasp import *
from ase.io.xyz import *

atoms = read_vasp("POSCAR")
atoms.write("POSCAR.pdb", format="pdb")
