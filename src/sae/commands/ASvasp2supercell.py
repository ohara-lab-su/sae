#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from ase.io import read, write
from ase.io.vasp import *
from ase.io.xyz import *

cell = read_vasp("POSCAR")
write_vasp(
    "POSCAR_444.vasp",
    cell * (4, 4, 4),
    label="444supercell",
    direct=True,
    sort=True,
    vasp5=True,
)
