#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.vasp.poscar_writer import PoscarWriter
from sae.vasp.vasprun_fields import VasprunFields

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#  読み込んだ vasprun.xml の initial の情報を元に
#  INCAR
#  KPOINTS
#  POSCAR
#  CONTCAR
#  相当の情報を出力する
#  
#
#  vasprun.xml 読み込みプログラムの基礎
#
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.01.07
#   完全分離版
#    [ライブラリ] read_vasprun.py (<-- Vxmlread_LIB0.py ベース)  
#    [本体] Vxmlread.py
#
#   名前変更(&カスタマイズ)
#      Vxml2POSCAR.py (Vxlmread.py から名前変更 &  ~/vasp1/bin へ移行)
#   
# 2015.01.07
#   rebuild 系の出力を追加
#   関数化(引数でのやりとりではなく、戻り値をすべて一つのリストで返す方向性で)
#
#   旧バージョン(非関数) Vxmlread_nonLIB.py                                     
#   新バージョン(関数)   Vxmlread_LIB0.py
#
# 2015.01.06 1st edtion
#   Vxmlread.py
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
#import xml.etree.ElementTree as ET
#import numpy as np
#import SpaceGroupEnvironment as SGE  
#import os
#import re
#from copy import deepcopy
################################################################################
def options():
    # default name
    XMLFILE = "vasprun.xml"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT", default=XMLFILE)
    options, args = parser.parse_args()
    if options.INPUT:
        XMLFILE = options.INPUT
    if len(args) > 0:
        XMLFILE = args[0]
    return XMLFILE


################################################################################
# Default & OptionParser
# vasprun.xml parse
###################################################
# INCAR の出力
###################################################
# KPOINTS の出力
###################################################
# POSCAR の出力 (Initial をアウトプット)
#   SAE.print_poscar(cname,STD,POSCAR)
###################################################
# CONTCAR の出力 (Final をアウトプット)
#   SAE.print_poscar(cname,STD,CONTCAR)
if __name__ == "__main__":
    XMLFILE = options()
    INCAR, KPOINTS, POSCAR, CONTCAR = VasprunFields().read_vasprun0(XMLFILE)
    (
        title,
        scale,
        natom,
        nion,
        selective,
        direct,
        VASP,
        t_initial,
        atoms,
        atoms_index,
        position_initial,
        fix_initial,
    ) = POSCAR
    (
        title,
        scale,
        natom,
        nion,
        selective,
        direct,
        VASP,
        t_final,
        atoms,
        atoms_index,
        position_final,
        fix_final,
    ) = CONTCAR
    INCAR_TAG, INCAR_TEXT = INCAR
    try:
        out = open("INCAR.rebuild", "w")
        print("Makes INCAR.rebuild")
        for i in range(len(INCAR_TAG)):
            print(INCAR_TAG[i], "=", INCAR_TEXT[i], file=out)
    except:
        out.close()
        sys.exit("STOP: INCAR.rebuild can't open")
    finally:
        out.close()
    try:
        out = open("KPOINTS.rebuild", "w")
        print("Makes KPOINTS.rebuild")
        for i in range(len(KPOINTS)):
            print(KPOINTS[i], file=out)
    except:
        out.close()
        sys.exit("STOP: KPOINTS.rebuild can't open")
    finally:
        out.close()
    print("Makes POSCAR.rebuild")
    STD = False
    cname = "POSCAR.rebuild"
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
        t_initial,
        atoms,
        atoms_index,
        position_initial,
        fix_initial,
    )
    print("Makes CONTCAR.rebuild")
    STD = False
    cname = "CONTCAR.rebuild"
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
        t_final,
        atoms,
        atoms_index,
        position_final,
        fix_final,
    )
