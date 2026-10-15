#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.pwscf.out import ReadPwOut
from sae.vasp.vasprun_writer import VasprunWriter

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# PWscf *.out --> CONTCAR(POSCAR) 変換出力
#
# 構造緩和の final だけを抜き出す
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.05.13 startup
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import optparse


#
################################################################################
#import gzip
#import os
#import re
#import numpy as np
#import SpaceGroupEnvironment as SGE
################################################################################
def write_poscar(cname, title, scale, t, natom, nion, atoms, atoms_index, position):
    try:
        out = open(cname + ".vasp", "w")
    except:
        out.close()
        sys.exit("STOP:" + cname + ".vasp can't open")
    print(title, file=out)
    print(" ", scale, file=out)
    print("  %13.9f %13.9f %13.9f" % (t[0, 0], t[1, 0], t[2, 0]), file=out)
    print("  %13.9f %13.9f %13.9f" % (t[0, 1], t[1, 1], t[2, 1]), file=out)
    print("  %13.9f %13.9f %13.9f" % (t[0, 2], t[1, 2], t[2, 2]), file=out)
    print(" ", file=out, end="")
    for i in range(nion):
        print(atoms_index[i], file=out, end="")
    print(" ", file=out)
    print(" ", file=out, end="")
    for i in range(nion):
        print(atoms[i], file=out, end="")
    print(" ", file=out)
    print("Direct", file=out)
    for i in range(int(natom)):
        print(
            " %13.9f %13.9f %13.9f" % (position[i, 0], position[i, 1], position[i, 2]),
            file=out,
            end="",
        )
        print("", file=out)
    out.close()


################################################################################
def options():
    name = "scf.out"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT", default=name)
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]
    return name


################################################################################
# 重要) vasprun 用に基本並進ベクトルをすけーるする
if __name__ == "__main__":
    OUTPUT = "vasprun.xml"
    output_name = options()
    pwout = ReadPwOut(output_name)
    cname = output_name + ".CONTCAR"
    title = pwout.get_title()
    scale = pwout.get_scale()
    t = pwout.get_t()
    natom = pwout.get_natom()
    nion = pwout.get_nion()
    atoms = pwout.get_atoms()
    atoms_index = pwout.get_atoms_index()
    atoms_index_j = pwout.get_atoms_index_j()
    # final
    position = pwout.get_position()
    n_ion_loop = pwout.get_n_ion_loop()
    force_loop = pwout.get_force_loop()
    position_loop = pwout.get_position_loop()
    energy_loop = pwout.get_energy_loop()
    write_poscar(cname, title, scale, t, natom, nion, atoms, atoms_index, position)
    print("INPUT  :", output_name)
    print("OUTPUT :", output_name + ".CONTCAR" + ".vasp")
    t = t * scale
    VasprunWriter().print_vasprun0(
        OUTPUT,
        title,
        n_ion_loop,
        natom,
        nion,
        atoms,
        atoms_index,
        atoms_index_j,
        t,
        position_loop,
        force_loop,
        energy_loop,
    )
