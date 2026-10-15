#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.vasp.outcar_fields import OutcarFields
from sae.vasp.poscar_fields import PoscarFields

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# POSCAR および OUTCAR を読み ION-LOOP 毎の原子位置、フォースを出力する
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2014.11.17
#    Vforce.pl を python 化 (using LIB_vasp )
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import optparse
import numpy as np


#                                                                                         
################################################################################
#import sys
#import os
#import re
#import SpaceGroupEnvironment as SGE  
#from numpy import *
#from copy import deepcopy
#from LIB_vasp import read_poscar_param
#from LIB_vasp import read_poscar
#from LIB_vasp import print_poscar
#from LIB_vasp import *
#from LIB_vasp.read_poscar_param import *
#from LIB_vasp.read_poscar import *
#from LIB_vasp.read_outcar_param import *
#from LIB_vasp.read_outcar_position import *
#from LIB_vasp.print_poscar import *
################################################################################
###############################################
## default parameter
##
###############################################
## optparse
##
#print args,options
#   if len(args) > 0:
#       #print "script name:",argvs[0]
#       #POSCAR=argv[0]
#       #distance = float(args[0])
#       cname=args[0]
#print "INPUT POSCAR file name    :",POSCAR
#print "INPUT OUTCAR file name    :",OUTCAR
def options():
    # OUTPUT BASE filename
    OUTCAR = "OUTCAR"
    # INPUT (BASE) filename
    POSCAR = "POSCAR"
    parser = optparse.OptionParser()
    parser.add_option("-p", "--poscar", dest="INPUT", default=POSCAR)
    parser.add_option("-o", "--outcar", dest="OUTLOG", default=OUTCAR)
    options, args = parser.parse_args()
    if options.INPUT:
        POSCAR = options.INPUT
    if options.OUTLOG:
        OUTCAR = options.OUTLOG
    return [POSCAR, OUTCAR]


################################################################################
# Default & OptionParser
# POSCAR の事前読み込み
# POSCAR 読み込みのための準備
# POSCAR の読み込み
# OUTCAR の事前読み込み
#print "NLOOP = ",nloop
# OUTCAR 読み込みのための準備
# OUTCAR 読み込み(原子位置とフォース), 座標系はPOSCARの座標系のまま
if __name__ == "__main__":
    POSCAR, OUTCAR = options()
    nion, natom, VASP = PoscarFields().read_poscar_param(POSCAR)
    t = np.zeros((3, 3))
    atoms = []
    atoms_index = []
    ion = np.zeros(natom)
    ion_site = np.zeros(natom)
    position = np.zeros((natom, 3))
    fix = np.zeros((natom, 3), dtype="S")
    title, scale, selective, direct = PoscarFields().read_poscar(
        POSCAR, VASP, t, atoms, atoms_index, ion, ion_site, position, fix
    )
    nloop = OutcarFields().read_outcar_param(OUTCAR, natom)
    position_loop = np.zeros((nloop, natom, 3))
    force_loop = np.zeros((nloop, natom, 3))
    OutcarFields().read_outcar_position(OUTCAR, natom, nloop, position_loop, force_loop)
    print("")
    for i in range(nloop):
        for j in range(natom):
            print(
                " %11.8f %11.8f %11.8f  %19.10f %19.10f %19.10f"
                % (
                    position_loop[i, j, 0],
                    position_loop[i, j, 1],
                    position_loop[i, j, 2],
                    force_loop[i, j, 0],
                    force_loop[i, j, 1],
                    force_loop[i, j, 2],
                )
            )
        print("")
