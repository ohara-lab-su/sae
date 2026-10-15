#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
##########################################################################
from __future__ import print_function
from sae.geometry.coordinates import CoordinateTransforms
from sae.rmcpot.cfg_writer import RmcConfigWriter
from sae.rmcpot.conversion import RmcConversions
from sae.vasp.poscar_fields import PoscarFields
from sae.vasp.poscar_writer import PoscarWriter

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 基本となる POSCAR ファイルから密度を求める
# (あくまで格子定数と原子数から求められる密度)
#
# 入力 POSCAR
#
# 出力(1) 標準出力
# 出力(2) POSCAR.cfg
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2014.11.13 1st
#
#  RchangeDnsity.py (2014.11.07 版)
#  Rvasp2cfg.py (2014.10.31 版)
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
import numpy as np


#
################################################################################
#import SpaceGroupEnvironment as SGE
#import re
#import optparse
#from copy import deepcopy
################################################################################
def options():
    # OUTPUT BASE filename
    cname = "POSCAR"
    # INPUT (BASE) filename
    POSCAR = "POSCAR"
    if not os.path.exists(POSCAR):
        sys.exit("STOP: " + POSCAR + " file not found")
    print("INPUT file name :", POSCAR)
    print("OUTPUT file name:", cname + ".cfg")
    return [POSCAR, cname]


################################################################################
# Default & OptionParser
# POSCAR の事前読み込み
# POSCAR 読み込みのための準備
# POSCAR の読み込み
##########################################################################
# スケールファクターを 1.0 へ変換
# Cartesian to Direct
# RMC_POT(cfg) 形式への変換 必須:direct-Mode
# RMC_POT(cfg) 形式への出力(標準出力)
#STD=True
#SAE.print_cfg(outname,STD,title,t,natom,nion,atoms,position)
############## VASP 形式の*.vasp への出力(構造確認用)
##
# RMC_POT (*.cfg) 形式から VASP 形式へ変換
# 引数版
# 擬似VASP5 設定
# VASP4+擬似VASP5 出力
#STD=True
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
    scale = CoordinateTransforms().conv_scale21a(scale, t)
    lattice = t[0, 0]
    # for RMC_POT
    cell = t[0, 0] / 2
    density = natom / lattice**3
    print("")
    print("  NATOM           = ", natom)
    print("  LATTICE         = ", lattice)
    print("  CELL (RMC.cfg)  = ", cell)
    print("")
    print("  DENSITY         = ", density)
    print("")
    if not direct:
        scale, direct = CoordinateTransforms().conv_car2directa(
            scale, t, natom, direct, position
        )
    scale, direct = RmcConversions().conv_vasp2cfg(scale, t, natom, direct, position)
    t[0, 0] = cell
    t[1, 1] = cell
    t[2, 2] = cell
    outname = cname
    print("  OUTPUT CFG-FILE = ", outname + ".cfg")
    STD = False
    RmcConfigWriter().print_rmcpot_cfg(
        outname, STD, title, t, natom, nion, atoms, position
    )
    print("  OUTPUT POSCAR   = ", outname + ".vasp")
    # conv_cfg2vasp は direce を想定(in/out)
    direct = True
    # conv_cfg2vasp は scale 1.0 を想定
    scale = 1.0
    scale, direct = RmcConversions().conv_cfg2vaspa(scale, t, natom, direct, position)
    dummy = "In Ga Zn O"
    # 擬似VASP5 出力
    PV5FLAG = True
    STD = False
    PoscarWriter().print_poscar4(
        outname,
        STD,
        title,
        scale,
        natom,
        nion,
        direct,
        PV5FLAG,
        t,
        atoms,
        dummy,
        position,
    )
    print("")
