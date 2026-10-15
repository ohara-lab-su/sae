#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.geometry.coordinates import CoordinateTransforms
from sae.vasp.poscar_fields import PoscarFields
from sae.vasp.poscar_writer import PoscarWriter

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# POSCAR の cartesian 変換
#
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.02.27
#  conv_direct2car の名前変更
#
# 2014.10.30/31
#   関数化 & ライブラリ化 テスト用テストプログラム
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014-2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import optparse
import numpy as np


#
################################################################################
# import re
# from copy import deepcopy
# import SpaceGroupEnvironment as SGE
################################################################################
###############################################
# default parameter
#
###############################################
# optparse
#
# print args,options
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
    # print "script name:",argvs[0]
    # POSCAR=argv[0]
    # distance = float(args[0])
    if len(args) > 0:
        cname = args[0]
        POSCAR = args[0]
    if not os.path.exists(POSCAR):
        if os.path.exists(POSCAR + ".vasp"):
            POSCAR = "POSCAR.vasp"
            cname = POSCAR
        else:
            sys.exit(POSCAR + " file not found")
    print("INPUT file name    : %s" % str(POSCAR))
    print("OUTPUT file name   : %s" % str(cname + ".vasp"))
    return [POSCAR, cname]


################################################################################
# Default & OptionParser
# POSCAR の事前読み込み
# POSCAR 読み込みのための準備
# POSCAR の読み込み
# Direct to Cartesian
# POSCAR の標準出力
# POSCAR のファイル出力
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
    print(fix[0, 0])
    # ABS=True  # for SuperCell
    if direct:
        # for VASP
        ABS = False
        scale, direct = CoordinateTransforms().conv_direct2cara(
            ABS, scale, t, natom, direct, position
        )
        src_mode = "Direct"
    else:
        src_mode = "Cartesian"
        print("CURRENT MODE       : %s" % str(src_mode))
        sys.exit("don't need to convert")
    print("CURRENT MODE       : %s" % str(src_mode))
    print("")
    STD = True
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
