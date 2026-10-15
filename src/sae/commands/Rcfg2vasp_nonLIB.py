#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import optparse
import numpy as np

cname = "igzo"
parser = optparse.OptionParser()
parser.add_option("-i", "--input", dest="INPUT", default=cname)
options, args = parser.parse_args()
if options.INPUT:
    cname = options.INPUT
if len(args) > 0:
    cname = args[0]
if cname:
    print("INPUT file name :", cname + ".cfg")
    print("OUTPUT file name:", cname + ".vasp")
if not os.path.exists(cname + ".cfg"):
    sys.exit(cname + ".cfg file not found")
tmp = open(cname + ".cfg")
datfile = tmp.read()
tmp.close
datlines = datfile.split("\n")
header = datlines[0]
comment = datlines[1]
tmp = datlines[2]
tmp = datlines[3]
moves = datlines[4]
saved = datlines[5]
tmp = datlines[6]
t = datlines[7].split()
natom = t[0]
t = datlines[8].split()
ntype = t[0]
nmoles = datlines[9]
angles = datlines[10]
tmp = datlines[11]
tmp = datlines[12]
tmp = datlines[13]
v = datlines[14].split()
t1_x = float(v[0])
t1_y = float(v[1])
t1_z = float(v[2])
v = datlines[15].split()
t2_x = float(v[0])
t2_y = float(v[1])
t2_z = float(v[2])
v = datlines[16].split()
t3_x = float(v[0])
t3_y = float(v[1])
t3_z = float(v[2])
tmp = datlines[17]
lines = 17
type = np.zeros(int(ntype) + 1)
for i in range(int(ntype)):
    lines += 1
    n = datlines[lines].split()
    type[i] = n[0]
    lines += 1
    tmp = datlines[lines]
    lines += 1
    tmp = datlines[lines]
    lines += 1
    tmp = datlines[lines]
position = np.zeros((int(natom) + 1, 3))
for i in range(int(natom)):
    lines += 1
    xyz = datlines[lines].split()
    position[i, 0] = xyz[0]
    position[i, 1] = xyz[1]
    position[i, 2] = xyz[2]
t1_x = t1_x * 2
t1_y = t1_y * 2
t1_z = t1_z * 2
t2_x = t2_x * 2
t2_y = t2_y * 2
t2_z = t2_z * 2
t3_x = t3_x * 2
t3_y = t3_y * 2
t3_z = t3_z * 2
x_offset = 0.5
y_offset = 0.5
z_offset = 0.5
for i in range(int(natom)):
    position[i, 0] = position[i, 0] / 2 + x_offset
    position[i, 1] = position[i, 1] / 2 + y_offset
    position[i, 2] = position[i, 2] / 2 + z_offset
vasp = open(cname + ".vasp", "w")
print(comment, file=vasp)
print("1.0", file=vasp)
print("  %13.9f %13.9f %13.9f" % (t1_x, t1_y, t1_z), file=vasp)
print("  %13.9f %13.9f %13.9f" % (t2_x, t2_y, t2_z), file=vasp)
print("  %13.9f %13.9f %13.9f" % (t3_x, t3_y, t3_z), file=vasp)
print(" atoms", file=vasp)
for i in range(int(ntype)):
    print(int(type[i]), file=vasp, end=" ")
print("", file=vasp)
print("Direct", file=vasp)
for i in range(int(natom)):
    print(
        " %13.9f %13.9f %13.9f" % (position[i, 0], position[i, 1], position[i, 2]),
        file=vasp,
    )
vasp.close()
