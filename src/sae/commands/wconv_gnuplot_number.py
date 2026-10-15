#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import glob
import optparse
import copy
from numpy import *
import re

cname = os.path.basename(os.getcwd())
parser = optparse.OptionParser()
parser.add_option("-a", "--atom", action="store", type="int", default="1")
parser.add_option("-o", "--orbital", action="store", type="string", default="d")
parser.add_option("-f", "--ef", action="store_true", dest="FLAG_EF")
parser.add_option("-e", "--unit", action="store_true", dest="FLAG_UNIT")
parser.add_option("-v", "--debug", action="store_true")
parser.add_option("-t", "--test", action="store_true")
parser.add_option("-d", "--deep", action="store_true")
options, args = parser.parse_args()
if len(args) > 0:
    cname = args[0]
if options.debug:
    print("")
    print("BASE NAME     =", cname)
unit = ""
if options.FLAG_UNIT:
    unit = "ev"
    unit_tmp = "eV"
else:
    unit_tmp = "Ry"
if not os.path.exists(cname + ".int"):
    print(cname + ".int file not found")
    print("EXIT")
    sys.exit()
if options.debug:
    print("UNIT          =", unit_tmp)
    print("EF0 MODE      =", options.FLAG_EF)
TOTALDOS_FLAG = False
tmp = open(cname + ".int")
intfile = tmp.read()
tmp.close
intlines = intfile.split("\n")
n = intlines[2].split()
n_total_orbit = int(n[0])
max_orbit_number = 1
for line in range(1, 1 + n_total_orbit):
    orbital = intlines[line + 2].split()
    tmp = int(orbital[1])
    if tmp > max_orbit_number:
        max_orbit_number = tmp
if options.debug:
    print("")
    print("MAXORBIT NUM  =", max_orbit_number)
atom = 0
l = 0
for num in range(1, 1 + n_total_orbit):
    orbital = intlines[num + 2].split()
    atom_tmp = int(orbital[0])
    if atom_tmp == 0:
        TOTALDOS_FLAG = True
    if atom_tmp < atom:
        print("STOP: READ", cname + ".int Files, atom_tmp < atom ", atom_tmp, atom)
        sys.exit()
    if atom_tmp > atom:
        atom = int(orbital[0])
natom = atom
if options.debug:
    print("NATOM         =", natom)
    print("TOTAL ORBITAL =", n_total_orbit)
    if TOTALDOS_FLAG:
        print("TOTLDOS       =", TOTALDOS_FLAG)
indexatom = zeros(n_total_orbit + 1)
indexorbit = zeros(n_total_orbit + 1)
indexname = ["list0"]
l = 0
atom = 0
for num in range(1, 1 + n_total_orbit):
    l += 1
    orbital = intlines[num + 2].split()
    atom_tmp = int(orbital[0])
    orbit_tmp = int(orbital[1])
    indexatom[num] = atom_tmp
    indexorbit[num] = orbit_tmp
    indexname.append(orbital[2])
if options.test:
    print("")
    print("num, indexatom[num], indexorbit[num], indexname[num]")
    for num in range(1, n_total_orbit + 1):
        print(num, int(indexatom[num]), int(indexorbit[num]), indexname[num])
    print("")
if TOTALDOS_FLAG:
    norbit = zeros(natom + 1 + 1)
    local_index_orbit = zeros((natom + 1 + 1, max_orbit_number + 1))
else:
    norbit = zeros(natom + 1)
    local_index_orbit = zeros((natom + 1, max_orbit_number + 1))
i = 1
atom0 = 0
for num in range(3, 3 + n_total_orbit):
    orbital = intlines[num].split()
    atom = int(orbital[0])
    norbit[atom] = i
    if atom > atom0:
        i = 1
        norbit[atom] = i
        atom0 = atom
    i += 1
    if options.test:
        print(
            "num,atom, norbit[atom], orbital",
            num - 2,
            atom,
            int(norbit[atom]),
            int(orbital[1]),
        )
if TOTALDOS_FLAG:
    norbit[0] = 1
    start = 0
else:
    start = 1
if options.debug:
    print("")
    for atom in range(start, natom + 1):
        if atom == 0:
            print("ATOM=", atom, "NUM ORBIT", int(norbit[atom]), "(TOTAL-DOS)")
        else:
            print("ATOM=", atom, "NUM ORBIT", int(norbit[atom]))
    print("")
num = 1
for atom in range(0, natom + 1):
    for num_local_orbit in range(1, int(norbit[atom]) + 1):
        index_local_orbit = zeros((natom + 1, norbit[atom] + 1))
for atom in range(0, natom + 1):
    for num_local_orbit in range(1, int(norbit[atom]) + 1):
        index_local_orbit[atom, num_local_orbit] = int(indexorbit[num])
        num += 1
if options.test:
    print("")
    print("num, atom, norbit[atom], num_local_orbit,", end="")
    print("indexorbit[num], index_local_orbit[atom,num_local_orbit, indexname[num]")
    num = 1
    for atom in range(0, natom + 1):
        for num_local_orbit in range(1, int(norbit[atom]) + 1):
            print(
                num,
                atom,
                int(norbit[atom]),
                num_local_orbit,
                int(indexorbit[num]),
                int(index_local_orbit[atom, num_local_orbit]),
                indexname[num],
            )
            num += 1
if max_orbit_number > n_total_orbit:
    indexnum = zeros((natom + 1, max_orbit_number + 1))
else:
    indexnum = zeros((natom + 1, n_total_orbit + 1))
for num in range(1, 1 + n_total_orbit):
    indexnum[int(indexatom[num]), int(indexorbit[num])] = num
if options.test:
    print("")
    print(
        "num, indexnum[indexatom[num],indexorbit[num]], indexatom[num], indexorbit[num] = "
    )
    for num in range(1, 1 + n_total_orbit):
        print(num, int(indexnum[int(indexatom[num]), int(indexorbit[num])]), end="")
        print(int(indexatom[num]), int(indexorbit[num]))
if options.test:
    print("")
i = 1
atom0 = 0
for num in range(1, 1 + n_total_orbit):
    orbital = intlines[num + 2].split()
    atom = int(orbital[0])
    if atom > atom0:
        i = 1
        norbit[atom] = i
        atom0 = atom
    if atom == options.atom:
        if not atom == 0:
            orbital_name = orbital[2].lower()
            match = re.match("tot\\-.*", orbital_name)
            if match:
                site = re.sub("tot-", "", orbital_name)
            dst = options.orbital + "-" + site
            if orbital_name == dst:
                if options.debug:
                    print(dst, i)
                else:
                    print(i + 1)
        else:
            orbital_name = orbital[2].lower()
            if options.debug:
                print(orbial_name, atom)
            else:
                print(atom + 2)
    i += 1
