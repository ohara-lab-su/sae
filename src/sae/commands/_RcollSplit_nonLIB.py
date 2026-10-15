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
    print("INPUT file name :", cname + "_coll.cfg")
    print("OUTPUT file name:", cname + "_*.vasp")
if not os.path.exists(cname + "_coll.cfg"):
    sys.exit(cname + ".cfg file not found")
tmp = open(cname + "_coll.cfg")
datfile = tmp.read()
tmp.close
datlines = datfile.split("\n")
total_num = len(datlines)
page = 0
lines = int(0)
while lines < total_num - 1:
    page += 1
    print("page:", page)
    header = datlines[lines]
    comment = datlines[lines + 1]
    tmp = datlines[lines + 2]
    tmp = datlines[lines + 3]
    moves = datlines[lines + 4]
    saved = datlines[lines + 5]
    tmp = datlines[lines + 6]
    t = datlines[lines + 7].split()
    natom = t[0]
    t = datlines[lines + 8].split()
    ntype = t[0]
    nmoles = datlines[lines + 9]
    angles = datlines[lines + 10]
    tmp = datlines[lines + 11]
    tmp = datlines[lines + 12]
    tmp = datlines[lines + 13]
    v = datlines[lines + 14].split()
    t1_x = float(v[0])
    t1_y = float(v[1])
    t1_z = float(v[2])
    v = datlines[lines + 15].split()
    t2_x = float(v[0])
    t2_y = float(v[1])
    t2_z = float(v[2])
    v = datlines[lines + 16].split()
    t3_x = float(v[0])
    t3_y = float(v[1])
    t3_z = float(v[2])
    tmp = datlines[lines + 17]
    lines = 17 + lines
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
    lines += 1
    tmp = datlines[lines]
    lines += 1
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
    vasp = open(cname + "_" + str(page) + ".vasp", "w")
    (print >> vasp, comment)
    (print >> vasp, "1.0")
    (print >> vasp, "  %13.9f %13.9f %13.9f" % (t1_x, t1_y, t1_z))
    (print >> vasp, "  %13.9f %13.9f %13.9f" % (t2_x, t2_y, t2_z))
    (print >> vasp, "  %13.9f %13.9f %13.9f" % (t3_x, t3_y, t3_z))
    (print >> vasp, " In Ga Zn O")
    for i in range(int(ntype)):
        (print >> vasp, int(type[i]))
    (print >> vasp, "")
    (print >> vasp, "Direct")
    for i in range(int(natom)):
        (
            print >> vasp,
            " %13.9f %13.9f %13.9f" % (position[i, 0], position[i, 1], position[i, 2]),
        )
    vasp.close()
