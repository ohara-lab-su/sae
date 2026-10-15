#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import optparse
from ase.io import read, write
from ase.io.vasp import *
from ase.io.xyz import *

poscarname = "POSCAR"
wien_suffix = ".struct"
parser = optparse.OptionParser(os.getcwd())
parser = optparse.OptionParser()
parser.add_option("-i", "--input", dest="INPUT")
options, args = parser.parse_args()
if options.INPUT:
    poscarname = options.INPUT
if len(args) > 0:
    poscarname = args[0]
if not os.path.exists(poscarname):
    poscarname0 = poscarname
    poscarname = "CONTCAR"
    if not os.path.exists(poscarname):
        sys.exit("STOP: " + poscarname + " and " + poscarname0 + " file not found")
print("INPUT POSCAR file  = ", poscarname)
print("OUTPUT struct file = ", poscarname + wien_suffix)
atoms = read_vasp(poscarname)
atoms.write(poscarname + wien_suffix, format="struct")
