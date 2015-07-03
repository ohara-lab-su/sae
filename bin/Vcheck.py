#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vcheck.py
#
#  1) VASP に必要な入力ファイルが存在しているかのチェック。
#  2) NSW のチェック
#  3) ブロードニングのチェック
#
#  4) POSCAR の selective の有無のチェック
#
#  などを行う。
#  ジョブ投入時のケアレスミスのチェック
#
################################################################################
#
# 2015.07.033 startup
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.2"
################################################################################

import sys
import os
import optparse
#import numpy as np

#import re
#from copy import deepcopy

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
def options():

    parser = optparse.OptionParser()
    parser.add_option( '-i','--input', dest='INPUT',)
    parser.add_option( '-o','--output', dest='OUTPUT',)
    parser.add_option( '-v','--vacuum')
    options,  args = parser.parse_args()

    if options.INPUT: inpname=options.INPUT
    if len(args) > 0: inpname=args[0]


################################################################################
if __name__ == '__main__':

    # Default & OptionParser
    inpname,outname,vacuum = options()

    outsuffix = "_v"+str(int(vacuum))
    outname = outname+outsuffix

    print "INPUT file name    :",inpname
    print "OUTPUT file name   :",outname+".vasp"
    print "Vacuum SIZE        :",str(int(vacuum))

    # Read POSCAR file
    poscar = SAE.ReadPoscar(inpname)
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

    # convert to Cartesian Corrdinate
    if direct:
        scale,t,natom,direct,position = \
                SAE.conv_direct2carABS1(scale,t,natom,direct,position)
    else:
        scale,t,natom,direct,position = \
                SAE.conv_car2carABS1(scale,t,natom,direct,position)

    # check c-axis
    cmax = max(position[:,2])
    cmin = min(position[:,2])
    bulk_size = cmax - cmin

    # shift position
    position[:,2] = position[:,2] - cmin + vacuum

    # makes new translation vector of c-axis
    t[2,2] = bulk_size + vacuum*2.

    # conver to original coordinate mode
    if direct0:
        scale,t,natom,direct,position = \
                SAE.conv_car2direct1(scale,t,natom,direct,position)

    # POSCAR の標準出力
    STD=False
   #STD=True
    SAE.print_poscar(outname,STD,title,scale,natom,nion,\
                 selective,direct,vasp,t,atoms,atoms_index,position,fix)


################################################################################

