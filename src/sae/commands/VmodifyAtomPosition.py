#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
#   # POSCAR の標準出力
#   print ""
#   STD=True
#   print_poscar(cname,STD,title,scale,natom,nion,selective,direct,VASP,t,atoms,atoms_index,position,fix)
################################################################################
from __future__ import print_function
from sae.common.text import TextFiles
from sae.geometry.coordinates import CoordinateTransforms
from sae.geometry.positions import PositionOperations
from sae.vasp.poscar_fields import PoscarFields
from sae.vasp.poscar_writer import PoscarWriter

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 移動原子リスト (通しの原子番号, x, y, z(ang))
# に従い POSCAR 構造の原子を一部(全部)移動する
# リストに記述する単位は ang 単位
#
# POSCAR ベース入力、POSCAR 形式での出力
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.02.27
#  conv_direct2car --> conv_direct2car0
#
# 2014.11.05 1st
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import optparse
import numpy as np


#
################################################################################
#import SpaceGroupEnvironment as SGE
#import re
#from copy import deepcopy
################################################################################
###############################################
## default parameter
##
###############################################
## optparse
##
#print args,options
def options():
    # OUTPUT BASE filename
    cname = "POSCAR"
    # INPUT (BASE) filename
    POSCAR = "POSCAR"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT", default=POSCAR)
    parser.add_option("-o", "--output", dest="OUTPUT", default=cname)
    options, args = parser.parse_args()
    if options.INPUT:
        POSCAR = options.INPUT
    if options.OUTPUT:
        cname = options.OUTPUT
    #print "script name:",argvs[0]
    #POSCAR=argv[0]
    #distance = float(args[0])
    if len(args) > 0:
        cname = args[0]
    if not os.path.exists(POSCAR):
        if os.path.exists(POSCAR + ".vasp"):
            POSCAR = "POSCAR.vasp"
        else:
            sys.exit(POSCAR + " file not found")
    print("INPUT file name    :", POSCAR)
    print("OUTPUT file name   :", cname + ".vasp")
    return [POSCAR, cname]


################################################################################
# Default & OptionParser
# POSCAR の事前読み込み
# POSCAR 読み込みのための準備
# POSCAR の読み込み
# 移動原子リスト読み込み (data,x,y,z)
# Direct to Cartesian
# 原子移動(ang) 必要:カーテシアンmode
# Cartesian to Direct
# POSCAR のファイル標準出力
if __name__ == "__main__":
    POSCAR, cname = options()
    nion, natom, VASP = PoscarFields().read_poscar_param(POSCAR)
    t = np.zeros((3, 3))
    atoms = []
    atoms_index = []
    ion = np.zeros(natom)
    ion_local = np.zeros(natom)
    position = np.zeros((natom, 3))
    fix = np.zeros((natom, 3), dtype="S")
    title, scale, selective, direct = PoscarFields().read_poscar(
        POSCAR, VASP, t, atoms, atoms_index, ion, ion_local, position, fix
    )
    direct0 = direct
    name = "LIST"
    nlist = TextFiles().read_list_param(name)
    list_atoms = np.zeros((nlist, 4))
    nlist = TextFiles().read_list4(name, list_atoms)
    #ABS=True  # for SuperCell
    if direct0:
        # for VASP
        ABS = False
        scale, direct = CoordinateTransforms().conv_direct2cara(
            ABS, scale, t, natom, direct, position
        )
    PositionOperations().move_atoms0(scale, t, direct, position, nlist, list_atoms)
    if direct0:
        scale, direct = CoordinateTransforms().conv_car2directa(
            scale, t, natom, direct, position
        )
    STD = False
    PoscarWriter().print_poscar(
        cname,
        STD,
        title,
        scale,
        natom,
        nion,
        selective,
        direct,
        VASP,
        t,
        atoms,
        atoms_index,
        position,
        fix,
    )
