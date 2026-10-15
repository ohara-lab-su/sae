#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import re
import optparse
import numpy as np

POSCAR = "POSCAR"
cname = "sets"
parser = optparse.OptionParser()
parser.add_option("-i", "--input", dest="INPUT", default=POSCAR)
parser.add_option("-o", "--output", dest="OUTPUT", default=cname)
options, args = parser.parse_args()
if options.INPUT:
    POSCAR = options.INPUT
if options.OUTPUT:
    cname = options.OUTPUT
if len(args) > 0:
    POSCAR = args[0]
if not os.path.exists(POSCAR):
    if os.path.exists(POSCAR + ".vasp"):
        POSCAR = "POSCAR.vasp"
    else:
        sys.exit(POSCAR + " file not found")
if POSCAR:
    print("INPUT file name :", POSCAR)
if cname:
    print("OUTPUT file name:", cname + ".in")
tmp = open(POSCAR)
datfile = tmp.read()
tmp.close
datlines = datfile.split("\n")
title = datlines[0]
scale = float(datlines[1])
v = datlines[2].split()
t1_x = float(v[0])
t1_y = float(v[1])
t1_z = float(v[2])
v = datlines[3].split()
t2_x = float(v[0])
t2_y = float(v[1])
t2_z = float(v[2])
v = datlines[4].split()
t3_x = float(v[0])
t3_y = float(v[1])
t3_z = float(v[2])
a = np.zeros((3, 3))
a[0, 0] = t1_x
a[1, 0] = t1_y
a[2, 0] = t1_z
a[0, 1] = t2_x
a[1, 1] = t2_y
a[2, 1] = t2_z
a[0, 2] = t3_x
a[1, 2] = t3_y
a[2, 2] = t3_z
i = 5
atoms = datlines[i].split()
if atoms[0].isdigit():
    VASP = 4
else:
    VASP = 5
    atoms_index = list(atoms)
    i += 1
    atoms = datlines[i].split()
nion = int(len(atoms))
natom = 0
for j in range(len(atoms)):
    sum = int(atoms[j])
    natom = natom + sum
ion_site = np.zeros(natom)
ion = np.zeros(natom)
tmp = -1
for j in range(nion):
    local = -1
    for k in range(int(atoms[j])):
        tmp += 1
        local += 1
        ion[tmp] = int(j)
        ion_site[tmp] = int(local)
        print(tmp, int(ion[tmp]), int(ion_site[tmp]))
num_reg = re.compile("^[+-]?(\\d*\\.\\d+|\\d+\\.?\\d*)([eE][+-]?\\d+|)\\Z")
selective_reg = re.compile("^S.*")
direct_reg = re.compile("^D.*")
car_reg = re.compile("^C.*")
i += 1
tmp = datlines[i].split()
if bool(num_reg.match(tmp[0])):
    print(tmp[0])
    sys.exit("Format Error")
else:
    if bool(selective_reg.match(tmp[0])):
        i += 1
        tmp = datlines[i].split()
        selective = 1
    else:
        selective = 0
    if bool(num_reg.match(tmp[0])):
        print(tmp[0])
        sys.exit("Format Error")
    if bool(direct_reg.match(tmp[0])):
        direct = 1
    elif bool(car_reg.match(tmp[0])):
        direct = 0
position = np.zeros((int(natom), 3))
i += 1
for j in range(natom):
    xyz = datlines[i + j].split()
    position[j, 0] = xyz[0]
    position[j, 1] = xyz[1]
    position[j, 2] = xyz[2]
sets = open(cname + ".in", "w")
print(title, file=sets)
print("-----nspin", file=sets)
print("1", file=sets)
print("-----space group", file=sets)
print("P1", file=sets)
print(" ", t1_x * scale, " ", t2_y * scale, " ", t3_z * scale, file=sets)
print(" 90.0 90.0 90.0", file=sets)
print("-----atoms", file=sets)
print("   ", nion, file=sets)
l = 0
for j in range(nion):
    print(" ", atoms_index[j], " ", int(atoms[j]), file=sets)
    for k in range(int(atoms[j])):
        print(
            "    %14.11f %14.11f %14.11f"
            % (position[l, 0], position[l, 1], position[l, 2]),
            file=sets,
        )
        l += 1
print("-----k points", file=sets)
print(" 0", file=sets)
print(" 8 8 8", file=sets)
sets.close()
