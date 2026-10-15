#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.common.text import TextFiles
from sae.geometry.coordinates import CoordinateTransforms
from sae.geometry.positions import PositionOperations
from sae.rmcpot.cfg_writer import RmcConfigWriter
from sae.rmcpot.conversion import RmcConversions
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
# 入力はベースとなる POSCAR ファイル
# 直接 RMC_POT 用の cfg ファイルを出力する (VmodifyAtomPosition は POSCAR 出力)
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.02.27
#  conv_direct2car --> conv_direct2car0
#
# 2014.11.05 1st
#   基本ベースは VmodifyAtomPosition.py (2014.11.05 version)
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
# default parameter
#
# cname  = "POSCAR" # OUTPUT BASE filename
###############################################
# optparse
#
#print args,options
def options():
    # OUTPUT BASE filename
    cname = "igzo"
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
    if len(args) > 0:
        cname = args[0]
        POSCAR = args[0]
    if not os.path.exists(POSCAR):
        sys.exit(POSCAR + " file not found")
    if POSCAR:
        print("INPUT file name :", POSCAR)
    if cname:
        print("OUTPUT file name:", cname + ".cfg")
    return [POSCAR, cname]


################################################################################
# Default & OptionParser
# POSCAR の事前読み込み
# POSCAR 読み込みのための準備
# POSCAR の読み込み
##########################################################################
# 移動原子リスト読み込み (data,x,y,z)
# Direct to Cartesian
# スケールファクターを 1.0 へ変換
# 原子移動(ang) 必要:cartesian-mode
#    入力list_atom: cartesian-実座標系(ang)
#    入力position : cartesian-内部座標系(scale)
#    内部でスケールし直すのでスケールファクターは実はなんでも良い
##########################################################################
# Cartesian to Direct
#   # POSCAR のファイル標準出力
#   STD=False
#   print_poscar(POSCAR,STD,title,scale,natom,nion,selective,direct,VASP,t,atoms,atoms_index,position,fix)
# RMC_POT(cfg) 形式への変換 必須:direct-Mode
# RMC_POT(cfg) 形式への出力(標準出力)
#STD=True
# SAE.print_cfg(cname,STD,title,t,natom,nion,atoms,position)
##########################################################################
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
    name = "LIST"
    nlist = TextFiles().read_list_param(name)
    list_atoms = np.zeros((nlist, 4))
    nlist = TextFiles().read_list4(name, list_atoms)
    if direct:
        # for VASP
        ABS = False
        scale, direct = CoordinateTransforms().conv_direct2cara(
            ABS, scale, t, natom, direct, position
        )
    for i in range(nlist):
        print(
            i,
            int(list_atoms[i, 0]),
            list_atoms[i, 1],
            list_atoms[i, 2],
            list_atoms[i, 3],
        )
    scale = CoordinateTransforms().conv_scale21a(scale, t)
    PositionOperations().move_atoms0(scale, t, direct, position, nlist, list_atoms)
    if not direct:
        scale, direct = CoordinateTransforms().conv_car2directa(
            scale, t, natom, direct, position
        )
    scale, direct = RmcConversions().conv_vasp2cfg(scale, t, natom, direct, position)
    STD = False
    RmcConfigWriter().print_rmcpot_cfg(
        cname, STD, title, t, natom, nion, atoms, position
    )
    # conv_cfg2vasp は direce を想定(in/out)
    direct = True
    # conv_cfg2vasp は scale 1.0 を想定
    scale = 1.0
    scale, direct = RmcConversions().conv_cfg2vaspa(scale, natom, t, direct, position)
    dummy = "In Ga Zn O"
    # 擬似VASP5 出力
    PV5FLAG = True
    STD = False
    PoscarWriter().print_poscar4(
        cname,
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
