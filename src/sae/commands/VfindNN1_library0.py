#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.geometry.coordinates import CoordinateTransforms
from sae.vasp.poscar_fields import PoscarFields
from sae.vasp.poscar_writer import PoscarWriter

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


def read_param_poscar():
    tmp = open(POSCAR)
    datfile = tmp.read()
    tmp.close
    datlines = datfile.split("\n")
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
    return [nion, natom, VASP]


def read_poscar(VASP, t, atoms, atoms_index, ion, ion_local, position, fix):
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
    t[0, 0] = t1_x
    t[1, 0] = t1_y
    t[2, 0] = t1_z
    t[0, 1] = t2_x
    t[1, 1] = t2_y
    t[2, 1] = t2_z
    t[0, 2] = t3_x
    t[1, 2] = t3_y
    t[2, 2] = t3_z
    i = 5
    if VASP == 4:
        atoms.extend(datlines[i].split())
    elif VASP == 5:
        atoms_index.extend(datlines[i].split())
        i += 1
        atoms.extend(datlines[i].split())
    else:
        sys.exit("Error: unknown VASP format")
    nion = int(len(atoms))
    natom = 0
    for j in range(nion):
        sum = int(atoms[j])
        natom = natom + sum
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
    i += 1
    for j in range(natom):
        xyz = datlines[i + j].split()
        position[j, 0] = xyz[0]
        position[j, 1] = xyz[1]
        position[j, 2] = xyz[2]
        if selective:
            fix[j, 0] = str(xyz[3])
            fix[j, 1] = str(xyz[4])
            fix[j, 2] = str(xyz[5])
    return [title, scale, selective, direct]


def print_poscar(
    title, scale, selective, direct, VASP, t, atoms, atoms_index, position, fix
):
    print("%s" % str(title))
    print(" %s" % str(scale))
    print("  %13.9f %13.9f %13.9f" % (t[0, 0], t[1, 0], t[2, 0]))
    print("  %13.9f %13.9f %13.9f" % (t[0, 1], t[1, 1], t[2, 1]))
    print("  %13.9f %13.9f %13.9f" % (t[0, 2], t[1, 2], t[2, 2]))
    if VASP == 5:
        print(" ", end="")
        for i in range(nion):
            print("%s" % atoms_index[i], end="")
        print(" ")
    print(" ", end="")
    for i in range(nion):
        print("%s" % atoms[i], end="")
    print(" ")
    if selective:
        print("Selective Dynamics")
    if direct:
        print("Direct")
    else:
        print("Cartesian")
    for i in range(int(natom)):
        print(
            " %13.9f %13.9f %13.9f" % (position[i, 0], position[i, 1], position[i, 2]),
            end="",
        )
        if selective:
            print("", end="")
            print("%s %s %s" % (str(fix[i, 0]), str(fix[i, 1]), str(fix[i, 2])), end="")
        print("")


def conv_direct2car(scale, natom, t, position):
    t1_x = t[0, 0]
    t1_y = t[1, 0]
    t1_z = t[2, 0]
    t2_x = t[0, 1]
    t2_y = t[1, 1]
    t2_z = t[2, 1]
    t3_x = t[0, 2]
    t3_y = t[1, 2]
    t3_z = t[2, 2]
    for j in range(natom):
        position[j, 0] = (
            t1_x * position[j, 0] + t2_x * position[j, 1] + t3_x * position[j, 2]
        )
        position[j, 1] = (
            t1_y * position[j, 0] + t2_y * position[j, 1] + t3_y * position[j, 2]
        )
        position[j, 2] = (
            t1_z * position[j, 0] + t2_z * position[j, 1] + t3_z * position[j, 2]
        )
    for j in range(natom):
        position[j, 0] = position[j, 0] * scale
        position[j, 1] = position[j, 1] * scale
        position[j, 2] = position[j, 2] * scale
    t1_x = t1_x * scale
    t1_y = t1_y * scale
    t1_z = t1_z * scale
    t2_x = t2_x * scale
    t2_y = t2_y * scale
    t2_z = t2_z * scale
    t3_x = t3_x * scale
    t3_y = t3_y * scale
    t3_z = t3_z * scale
    t[0, 0] = t1_x
    t[1, 0] = t1_y
    t[2, 0] = t1_z
    t[0, 1] = t2_x
    t[1, 1] = t2_y
    t[2, 1] = t2_z
    t[0, 2] = t3_x
    t[1, 2] = t3_y
    t[2, 2] = t3_z


if __name__ == "__main__":
    nion, natom, VASP = read_param_poscar()
    t = np.zeros((3, 3))
    atoms = []
    atoms_index = []
    ion = np.zeros(natom)
    ion_local = np.zeros(natom)
    position = np.zeros((natom, 3))
    fix = np.zeros((natom, 3), dtype="S")
    title, scale, selective, direct = PoscarFields().read_poscar(
        VASP, t, atoms, atoms_index, ion, ion_local, position, fix
    )
    if direct:
        CoordinateTransforms().conv_direct2car(scale, natom, t, position)
        scale = 1.0
    PoscarWriter().print_poscar(
        title, scale, selective, direct, VASP, t, atoms, atoms_index, position, fix
    )
