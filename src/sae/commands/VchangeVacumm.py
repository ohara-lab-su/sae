#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.geometry.coordinates import CoordinateTransforms
from sae.vasp.poscar import ReadVaspPoscar
from sae.vasp.poscar_writer import PoscarWriter

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# VchangeVacuum.py
#
#  POSCAR の真空層だけ増やしたり減らしたりする
#
#  c軸がa-b面に垂直なケースのみを想定している
#  *) vacuum の長さをc軸の長さとすればどのようなケースでも一応は動く
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.06.16 startup
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


#
################################################################################
#import numpy as np
#import re
#from copy import deepcopy
#import SpaceGroupEnvironment as SGE
################################################################################
###############################################
## default parameter
##
###############################################
## optparse
##
#print args,options
def options():
    # OUTPUT "BASE" filename
    outname = "POSCAR"
    # INPUT (BASE) filename
    inpname = "POSCAR"
    vacuum = None
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-o", "--output", dest="OUTPUT")
    parser.add_option("-v", "--vacuum")
    options, args = parser.parse_args()
    if options.INPUT:
        inpname = options.INPUT
    if options.OUTPUT:
        outname = options.OUTPUT
    if options.vacuum:
        vacuum = float(options.vacuum)
    else:
        sys.exit("STOP: plase input vacuum size")
    #print "script name:",argvs[0]
    #POSCAR=argv[0]
    #distance = float(args[0])
    if len(args) > 0:
        inpname = args[0]
    if not os.path.exists(inpname):
        if not os.path.exists(inpname + ".gz"):
            if os.path.exists(inpname + ".vasp"):
                POSCAR = "POSCAR.vasp"
            else:
                sys.exit(POSCAR + " file not found")
    return [inpname, outname, vacuum]


################################################################################
# Default & OptionParser
# Read POSCAR file
# convert to Cartesian Corrdinate
# check c-axis
# shift position
# makes new translation vector of c-axis
# conver to original coordinate mode
# POSCAR の標準出力
#STD=True
if __name__ == "__main__":
    inpname, outname, vacuum = options()
    outsuffix = "_v" + str(int(vacuum))
    outname = outname + outsuffix
    print("INPUT file name    : %s" % str(inpname))
    print("OUTPUT file name   : %s" % str(outname + ".vasp"))
    print("Vacuum SIZE        : %s" % str(str(int(vacuum))))
    poscar = ReadVaspPoscar(inpname)
    title = poscar.get_title()
    scale = poscar.get_scale()
    t = poscar.get_t()
    vasp = poscar.get_vasp_version()
    atoms = poscar.get_atoms()
    atoms_index = poscar.get_atoms_index()
    natom = poscar.get_natom()
    nion = poscar.get_nion()
    selective = poscar.get_selective()
    direct = poscar.get_direct()
    position = poscar.get_position()
    fix = poscar.get_fix()
    direct0 = direct
    if direct:
        scale, t, natom, direct, position = CoordinateTransforms().conv_direct2carABS(
            scale, t, natom, direct, position
        )
    else:
        scale, t, natom, direct, position = CoordinateTransforms().conv_car2carABS(
            scale, t, natom, direct, position
        )
    cmax = max(position[:, 2])
    cmin = min(position[:, 2])
    bulk_size = cmax - cmin
    position[:, 2] = position[:, 2] - cmin + vacuum
    t[2, 2] = bulk_size + vacuum * 2.0
    if direct0:
        scale, t, natom, direct, position = CoordinateTransforms().conv_car2direct(
            scale, t, natom, direct, position
        )
    STD = False
    PoscarWriter().print_poscar(
        outname,
        STD,
        title,
        scale,
        natom,
        nion,
        selective,
        direct,
        vasp,
        t,
        atoms,
        atoms_index,
        position,
        fix,
    )
