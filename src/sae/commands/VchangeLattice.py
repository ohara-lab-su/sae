#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
#   print atoms
#   print atoms[0] # cell
#   print atoms[1] # lattice
#   print atoms[2] # pos
#   print atoms[3] # atomtype
#   print atoms[4] # rmt
#   atoms.center()
#   atoms.write(poscarname,format='vasp',direct=True,vasp5=True)
#   atoms.write(poscarname,format='vasp',vasp5=True,sort=True)
#   atoms.write(structname,format='struct')
from __future__ import print_function
from sae.structure.document import Read
import sys
import re
import os
import optparse
from ase.io import read, write
from ase.io.vasp import *
from ase.io.xyz import *
from ase.io.wien2k import *


#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#  using ASE
#
# POSCAR を読み込んで、conventional な cell パラメーターの倍数で
# 格子を変形(伸び縮み)させる
#  --> そのときの基本並進ベクトルの見積もりに ASE のルーチンをとりあえず借用する
#      (暫定:突貫工事, 2016.01.18)
#
# 基本並進ベクトル以外のVASP の情報は自前の SAE ルーチンを用いる
#  POSCAR の読み込みで二度手間ではある。つぎはぎバージョン
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2016.01.18
#   ASE and SAE のやっつけつぎはぎバージョン
#
################################################################################
################################################################################
#import numpy as np
################################ ASE
## using cellconst
#from ase.lattice import bulk
#from ase.dft.kpoints import ibz_points, get_bandpath
###############################
#from gpaw import GPAW, PW, FermiDirac, setup_paths
#from gpaw import GPAW, PW
#setup_paths.insert(0,'.')
################################################################################
def options():
    POSCAR = "POSCAR"
    times = 1.0
    parser = optparse.OptionParser(os.getcwd())
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-o", "--output", dest="OUTPUT")
    parser.add_option("-r", "--ration", dest="RATIO")
    options, args = parser.parse_args()
    if options.INPUT:
        POSCAR = options.INPUT
    if options.OUTPUT:
        OUTPUT = options.OUTPUT
    else:
        OUTPUT = POSCAR
    if options.RATIO:
        times = options.RATIO
    if len(args) > 0:
        times = float(args[0])
    return (POSCAR, OUTPUT, times)


################################################################################
# latconst[0] = a
#         [1] = b
#         [2] = c
#         [3] = alpha
#         [4] = beta
#         [5] = gamma
#
# (GPL code): for ASE io/wien2k.py
def coorsys(latconst):
    a = latconst[0]
    b = latconst[1]
    c = latconst[2]
    cal = np.cos(latconst[3] * np.pi / 180.0)
    cbe = np.cos(latconst[4] * np.pi / 180.0)
    cga = np.cos(latconst[5] * np.pi / 180.0)
    sga = np.sin(latconst[5] * np.pi / 180.0)
    return np.array(
        [
            [a, b * cga, c * cbe],
            [0, b * sga, c * (cal - cbe * cga) / sga],
            [
                0,
                0,
                c * np.sqrt(1 - cal**2 - cbe**2 - cga**2 + 2 * cal * cbe * cga) / sga,
            ],
        ]
    ).transpose()


################################################################################
# read POSCAR ( using ASE )
# cell parameter を抽出する
#   原子数
#   nat = len(atoms.get_positions())
# 格子定数の倍率
#   times = 1.0
# 等方的なときはすべて times
## NEW lattice
## NEW cell parameter
############ read VASP-POSCAR using SAE
#   print atoms2.t
#   t = np.zeros((3,3))
#   print ""
#   print atoms2.t
############ write VASP-POSCAR using SAE
if __name__ == "__main__":
    POSCAR, OUTPUT, times = options()
    print("INPUT POSCAR file  = %s" % str(POSCAR))
    print("OUTPUT(base) POSCAR file = %s" % str(OUTPUT))
    atoms = read(POSCAR, format="vasp")
    cell = atoms.cell
    metT = np.dot(cell, np.transpose(cell))
    # from ASE module
    cell2 = cellconst(metT)
    a = cell2[0]
    b = cell2[1]
    c = cell2[2]
    alpha = cell2[3]
    beta = cell2[4]
    gamma = cell2[5]
    print("-------- original ----------")
    print(cell)
    print("")
    print(a, b, c, alpha, beta)
    print("----------------------------")
    a_times = times
    b_times = times
    c_times = times
    latconst2 = [a * a_times, b * b_times, c * c_times, alpha, beta, gamma]
    cell2 = coorsys(latconst2)
    print("")
    print("------------- new ----------")
    print(cell2)
    print("")
    print(latconst2)
    print("----------------------------")
    atoms2 = Read(filename=POSCAR, code="VASP")
    # t1_x
    atoms2.t[0, 0] = cell2[0][0]
    # t1_y
    atoms2.t[1, 0] = cell2[0][1]
    # t1_z
    atoms2.t[2, 0] = cell2[0][2]
    # t2_x
    atoms2.t[0, 1] = cell2[1][0]
    # t2_y
    atoms2.t[1, 1] = cell2[1][1]
    # t2_z
    atoms2.t[2, 1] = cell2[1][2]
    # t3_x
    atoms2.t[0, 2] = cell2[2][0]
    # t3_y
    atoms2.t[1, 2] = cell2[2][1]
    # t3_z
    atoms2.t[2, 2] = cell2[2][2]
    atoms2.write(outname=OUTPUT, code="VASP", suffix=".vasp")
