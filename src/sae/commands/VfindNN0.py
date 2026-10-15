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

cname = "POSCAR"
POSCAR = "POSCAR"
find = 1
parser = optparse.OptionParser()
parser.add_option("-i", "--input", dest="INPUT", default=POSCAR)
parser.add_option("-o", "--output", dest="OUTPUT", default=cname)
parser.add_option("-a", "--atom", dest="NN", default=find)
options, args = parser.parse_args()
if options.INPUT:
    POSCAR = options.INPUT
if options.OUTPUT:
    cname = options.OUTPUT
if options.NN:
    find = int(options.NN)
if len(args) > 0:
    find = int(args[0])
if not os.path.exists(POSCAR):
    if os.path.exists(POSCAR + ".vasp"):
        POSCAR = "POSCAR.vasp"
    else:
        sys.exit(POSCAR + " file not found")
if POSCAR:
    print("INPUT file name : %s" % str(POSCAR))
if cname:
    print("OUTPUT file name: %s_nn_%s.out" % (cname, str(find)))
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
for j in range(nion):
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
num_reg = re.compile("^[+-]?(\\d*\\.\\d+|\\d+\\.?\\d*)([eE][+-]?\\d+|)\\Z")
selective_reg = re.compile("^S.*", re.IGNORECASE)
direct_reg = re.compile("^D.*", re.IGNORECASE)
car_reg = re.compile("^C.*", re.IGNORECASE)
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
car = np.zeros((natom, 3))
for j in range(natom):
    car[j, 0] = t1_x * position[j, 0] + t2_x * position[j, 1] + t3_x * position[j, 2]
    car[j, 1] = t1_y * position[j, 0] + t2_y * position[j, 1] + t3_y * position[j, 2]
    car[j, 2] = t1_z * position[j, 0] + t2_z * position[j, 1] + t3_z * position[j, 2]
for j in range(natom):
    position[j, 0] = car[j, 0] * scale
    position[j, 1] = car[j, 1] * scale
    position[j, 2] = car[j, 2] * scale
find0 = find - 1
r = np.zeros(natom)
r_index = np.zeros(natom)
for j in range(natom):
    x1 = float(position[find0, 0])
    y1 = float(position[find0, 1])
    z1 = float(position[find0, 2])
    x2 = float(position[j, 0])
    y2 = float(position[j, 1])
    z2 = float(position[j, 2])
    r0 = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) + (z2 - z1) * (z2 - z1)
    r1 = np.sqrt(r0)
    r[j] = r1
    r_index[j] = j
n = natom - 1
for j in range(n):
    for k in range(n, j, -1):
        if r[k - 1] > r[k]:
            tmp = r[k]
            r[k] = r[k - 1]
            r[k - 1] = tmp
            tmp_index = r_index[k]
            r_index[k] = r_index[k - 1]
            r_index[k - 1] = tmp_index
print("scale              : %s" % str(scale))
print("translation vector : %11.9f %11.9f %11.9f" % (t1_x, t1_y, t1_z))
print("                     %11.9f %11.9f %11.9f" % (t2_x, t2_y, t2_z))
print("                     %11.9f %11.9f %11.9f" % (t3_x, t3_y, t3_z))
nn = open(cname + "_nn_" + str(find) + ".out", "w")
print(
    "%s %d (%d)"
    % (
        atoms_index[int(ion[int(find0)])],
        int(ion_site[find0]) + 1,
        int(ion_site[find0]) + 1,
    ),
    file=nn,
)
print("      t-index site site-index      r", file=nn)
print("     -------------------------------------", file=nn)
for j in range(natom):
    print(
        "   ",
        "     %5d  %2s %5d    %14.11f"
        % (
            int(r_index[j]) + 1,
            atoms_index[int(ion[int(r_index[j])])],
            int(ion_site[int(r_index[j])]) + 1,
            r[j],
        ),
        file=nn,
    )
nn.close
