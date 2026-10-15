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
FNClist = "FNC.list"
EPS = 0.0001
distance = "2.5"
find = 1
parser = optparse.OptionParser()
parser.add_option("-i", "--input", dest="INPUT", default=POSCAR)
parser.add_option("-o", "--output", dest="OUTPUT", default=cname)
options, args = parser.parse_args()
if options.INPUT:
    POSCAR = options.INPUT
if options.OUTPUT:
    cname = options.OUTPUT
distance = float(distance)
if not os.path.exists(POSCAR):
    if os.path.exists(POSCAR + ".vasp"):
        POSCAR = "POSCAR.vasp"
    else:
        sys.exit(POSCAR + " file not found")
if not os.path.exists(FNClist):
    sys.path.exit(FNClist + "file not found")
print("INPUT file name    : %s" % str(POSCAR))
print("OUTPUT file name   : %s" % str(cname + "_nn_" + str(find) + ".out"))
print("SEARCH DISTANCE    : %s" % str(distance))
tmp = open(FNClist)
datfile = tmp.read()
tmp.close
datlines = datfile.split("\n")
nfnc = int(len(datlines)) - 1
dist = np.zeros(nfnc)
atom_fnc = np.zeros(nfnc)
for i in range(nfnc):
    tmp = datlines[i].split()
    atom_fnc[i] = tmp[0]
    dist[i] = tmp[1]
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
r = np.zeros((natom * super, nfnc))
r_index = np.zeros((natom * super, nfnc))
nsmax = np.zeros(nfnc)
for fnc in range(nfnc):
    find0 = atom_fnc[fnc] - 1
    distance = float(dist[fnc])
    x1 = position[find0, 0]
    y1 = position[find0, 1]
    z1 = position[find0, 2]
    for j in range(natom * super):
        x2 = sp[j, 0]
        y2 = sp[j, 1]
        z2 = sp[j, 2]
        r0 = np.fabs(
            (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) + (z2 - z1) * (z2 - z1)
        )
        r1 = np.sqrt(r0)
        r[j, fnc] = r1
        r_index[j, fnc] = j
        if r[j, fnc] < distance:
            nsmax[fnc] += 1
            ion_num = ion_sp[j]
nsmax_tmp = 0
for fnc in range(nfnc):
    if nsmax[fnc] >= nsmax_tmp:
        nsmax_max = nsmax[fnc]
rs = np.zeros((int(nsmax_max), nfnc))
rs_index = np.zeros((int(nsmax_max), nfnc))
for fnc in range(nfnc):
    r_count = 0
    for j in range(natom * super):
        if r[j, fnc] < distance:
            rs[r_count, fnc] = r[j, fnc]
            rs_index[r_count, fnc] = r_index[j, fnc]
            r_count += 1
    for num in range(int(nsmax_max)):
        j = rs_index[num, fnc]
nmax = int(nsmax_max)
for fnc in range(nfnc):
    n = nmax - 1
    for j in range(n):
        for k in range(n, j, -1):
            if rs[k - 1, fnc] > rs[k, fnc]:
                tmp = rs[k, fnc]
                rs[k, fnc] = rs[k - 1, fnc]
                rs[k - 1, fnc] = tmp
                tmp_index = rs_index[k, fnc]
                rs_index[k, fnc] = rs_index[k - 1, fnc]
                rs_index[k - 1, fnc] = tmp_index
print("")
fnc_max = np.zeros(nfnc)
fnc_min = np.zeros(nfnc)
for fnc in range(nfnc):
    fnc_max[fnc] = rs[int(int(nsmax[fnc])) - 1, fnc]
    fnc_min[fnc] = rs[1, fnc]
print("")
nbond = 2
fnc_bond_max = np.zeros(nbond)
fnc_bond_min = np.zeros(nbond)
fnc_bond_max[0] = fnc_max[0]
fnc_bond_min[0] = fnc_min[0]
fnc_bond_max[1] = fnc_max[1]
fnc_bond_min[1] = fnc_min[1]
for fnc in range(nfnc):
    find0 = int(atom_fnc[fnc]) - 1
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
                sp_j[int(rs_index[num, fnc])] + 1,
                atoms_index[int(ion[sp_j[rs_index[num, fnc]]])],
                ion_local[sp_j[rs_index[num, fnc]]] + 1,
                rs[num, fnc],
            ),
        )
index_bond = np.zeros(natom)
fnc_atom = np.zeros(natom)
for j in range(natom):
    index_bond[j] = 0
    for fnc in range(nfnc):
        find0 = int(atom_fnc[fnc]) - 1
        if j == find0:
            fnc_atom[atom_fnc[fnc] - 1] = fnc
            index_bond[j] = 1
outfnc = open(cname + ".fnc", "w")
print("     ", title, file=outfnc)
print("")
print("     ", "No. of possible rmin-rmax pairs:", file=outfnc)
print("     ", nbond, file=outfnc)
print("     ", file=outfnc, end="")
for ib in range(nbond):
    print("%2.3f " % fnc_bond_min[ib], file=outfnc, end="")
print("", file=outfnc)
print("     ", file=outfnc, end="")
for ib in range(nbond):
    print("%2.3f " % fnc_bond_max[ib], file=outfnc, end="")
print("", file=outfnc)
print("", file=outfnc)
print("     %3d" % natom, file=outfnc)
print("", file=outfnc)
for j in range(natom):
    if index_bond[j] == 1:
        find0 = j
        fnc0 = fnc_atom[find0]
        print("     %3d %3d" % (find0 + 1, nmax - 1), file=outfnc)
        for num in range(1, nmax):
            print(
                "    ",
                int(sp_j[int(rs_index[num, int(fnc0)])] + 1),
                file=outfnc,
                end="",
            )
        print("", file=outfnc)
        print("      ", file=outfnc, end="")
        for num in range(1, nmax):
            print("1", file=outfnc, end="")
        print("", file=outfnc)
    else:
        print("     %3d %3d" % (j + 1, 0), file=outfnc)
outfnc.close()
