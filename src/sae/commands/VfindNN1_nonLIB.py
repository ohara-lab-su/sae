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
from copy import deepcopy

cname = "POSCAR"
POSCAR = "POSCAR"
distance = "2.5"
find = 1
parser = optparse.OptionParser()
parser.add_option("-i", "--input", dest="INPUT", default=POSCAR)
parser.add_option("-o", "--output", dest="OUTPUT", default=cname)
parser.add_option("-a", "--atom", dest="NN", default=find)
parser.add_option("-d", "--distance", dest="DISTANCE", default=distance)
options, args = parser.parse_args()
if options.INPUT:
    POSCAR = options.INPUT
if options.OUTPUT:
    cname = options.OUTPUT
if options.NN:
    find = int(options.NN)
if options.DISTANCE:
    distance = float(options.DISTANCE)
if len(args) > 0:
    distance = float(args[0])
if not os.path.exists(POSCAR):
    if os.path.exists(POSCAR + ".vasp"):
        POSCAR = "POSCAR.vasp"
    else:
        sys.exit(POSCAR + " file not found")
print("INPUT file name    : %s" % str(POSCAR))
print("OUTPUT file name   : %s" % str(cname + "_nn_" + str(find) + ".out"))
print("SEARCH DISTANCE    : %s" % str(distance))
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
ion_local = np.zeros(natom)
ion = np.zeros(natom)
tmp = -1
for j in range(nion):
    local = -1
    for k in range(int(atoms[j])):
        tmp += 1
        local += 1
        ion[tmp] = int(j)
        ion_local[tmp] = int(local)
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
        selective = True
    else:
        selective = False
    if bool(num_reg.match(tmp[0])):
        print(tmp[0])
        sys.exit("Format Error")
    if bool(direct_reg.match(tmp[0])):
        direct = True
    elif bool(car_reg.match(tmp[0])):
        direct = False
position = np.zeros((int(natom), 3))
i += 1
for j in range(natom):
    xyz = datlines[i + j].split()
    position[j, 0] = xyz[0]
    position[j, 1] = xyz[1]
    position[j, 2] = xyz[2]
car = np.zeros((natom, 3))
dic = deepcopy(position)
if direct:
    for j in range(natom):
        car[j, 0] = (
            t1_x * position[j, 0] + t2_x * position[j, 1] + t3_x * position[j, 2]
        )
        car[j, 1] = (
            t1_y * position[j, 0] + t2_y * position[j, 1] + t3_y * position[j, 2]
        )
        car[j, 2] = (
            t1_z * position[j, 0] + t2_z * position[j, 1] + t3_z * position[j, 2]
        )
else:
    car[j, 0] = position[j, 0]
    car[j, 1] = position[j, 1]
    car[j, 2] = position[j, 2]
for j in range(natom):
    position[j, 0] = car[j, 0] * scale
    position[j, 1] = car[j, 1] * scale
    position[j, 2] = car[j, 2] * scale
t1_x = t1_x * scale
t1_y = t1_y * scale
t1_z = t1_z * scale
t2_x = t2_x * scale
t2_y = t2_y * scale
t2_z = t2_z * scale
t3_x = t3_x * scale
t3_y = t3_y * scale
t3_z = t3_z * scale
super_x = 3
super_y = 3
super_z = 3
super = int(super_x * super_y * super_z)
sv = np.zeros((super, 3))
nsv = 0
for n in range(-1, 2):
    for l in range(-1, 2):
        for m in range(-1, 2):
            sv[nsv, 0] = t1_x * n + t2_x * l + t3_x * m
            sv[nsv, 1] = t1_y * n + t2_y * l + t3_y * m
            sv[nsv, 2] = t1_z * n + t2_z * l + t3_z * m
            nsv += 1
sp = np.zeros((natom * super, 3))
ion_sp = np.zeros(natom * super)
ion_local_sp = np.zeros(natom * super)
sp_j = np.zeros(natom * super)
j = -1
nsp = -1
for k in range(nion):
    for kk in range(int(atoms[k])):
        j += 1
        for nsv in range(super):
            nsp += 1
            nsp_ = natom * nsv + j
            sp[nsp, 0] = position[j, 0] + sv[nsv, 0]
            sp[nsp, 1] = position[j, 1] + sv[nsv, 1]
            sp[nsp, 2] = position[j, 2] + sv[nsv, 2]
            ion_sp[nsp] = ion[j]
            ion_local_sp[nsp] = ion_local[j]
            sp_j[nsp] = j
find0 = find - 1
x1 = position[find0, 0]
y1 = position[find0, 1]
z1 = position[find0, 2]
r = np.zeros(natom * super)
r_index = np.zeros(natom * super)
nsmax = 0
for j in range(natom * super):
    x2 = sp[j, 0]
    y2 = sp[j, 1]
    z2 = sp[j, 2]
    r0 = np.fabs((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) + (z2 - z1) * (z2 - z1))
    r1 = np.sqrt(r0)
    r[j] = r1
    r_index[j] = j
    if r[j] < distance:
        nsmax += 1
        ion_num = ion_sp[j]
r_count = 0
rs = np.zeros(nsmax)
rs_index = np.zeros(nsmax)
for j in range(natom * super):
    if r[j] < distance:
        rs[r_count] = r[j]
        rs_index[r_count] = r_index[j]
        r_count += 1
for num in range(nsmax):
    j = rs_index[num]
r = list(rs)
r_index = list(rs_index)
nmax = nsmax
n = nmax - 1
for j in range(n):
    for k in range(n, j, -1):
        if r[k - 1] > r[k]:
            tmp = r[k]
            r[k] = r[k - 1]
            r[k - 1] = tmp
            tmp_index = r_index[k]
            r_index[k] = r_index[k - 1]
            r_index[k - 1] = tmp_index
print("")
print(
    atoms_index[int(ion[int(find0)])],
    int(ion_local[find0]) + 1,
    "(",
    int(ion_local[find0]) + 1,
    ")",
)
print("   ", "  -------------------------------------")
print("   ", "  [original cell numter]")
print("   ", "   t-index site site-index      r")
print("   ", "  -------------------------------------")
for num in range(nmax):
    print(
        "   ",
        "     %5d  %2s %5d    %14.11f"
        % (
            sp_j[int(r_index[num])] + 1,
            atoms_index[int(ion[sp_j[r_index[num]]])],
            ion_local[sp_j[r_index[num]]] + 1,
            r[num],
        ),
    )
