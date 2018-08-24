#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# VrotPOSCAR
#  基本並進ベクトル（および内部座標）を回転させる
#
#  例) x-y 面内に広がる graphene ,真空層(z軸方向) のスラブモデルで構築した
#      Graphene を x軸方向真空層で、z-y 軸面に広がるグラフェン構造へ
#      変換する
#      (たとえば　openMX の ESM は x軸方向へ EMS を積む必要がある)
#
################################################################################
#
# 2018.08.15, 2018.08.23
#  Python2/3 両対応
#
# 2015.03.09
#   direct 呼び出し method を間違えていた（違うmethodを呼んでいた)のを修正
#
# 2015.03.03
#  引数処理のバグを修正
#  デバッグモードを追加
#
# 2015.03.03
#   startup
#   selective dynamic はすべて OFF
#
################################################################################
from __future__ import print_function
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014,2015 Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"
################################################################################

import sys
#import os
#import re
#import gzip
#import numpy as np

import optparse

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE


################################################################################
if __name__ == '__main__':

    poscarname = 'POSCAR'
    outputname = poscarname+'.vasp'

    alpha = 0
    beta = 0
    gamma = 0

    parser = optparse.OptionParser()
    parser.add_option( '-i','--input', dest='INPUT')
    parser.add_option( '-o','--output', dest='OUTPUT')
    parser.add_option( '-a','--alpha', dest='ALPHA')
    parser.add_option( '-b','--beta', dest='BETA')
    parser.add_option( '-g','--gamma', dest='GAMMA')
    parser.add_option( '-s','--std', action='store_true')
    parser.add_option( '-d','--debug', action='store_true')
    options, args = parser.parse_args()

    STD=False
    DEBUG=False
    if options.ALPHA:
        alpha = float(options.ALPHA)
    if options.BETA:
        beta = float(options.BETA)
    if options.GAMMA:
        gamma = float(options.GAMMA)
    if options.INPUT:
        poscarname = options.INPUT
    if options.OUTPUT:
        outputname = options.OUTPUT
    if options.std:
        STD=True
    if options.debug:
        DEBUG=True
        STD=True

    if len(args) > 2:
        alpha=float(args[0])
        beta=float(args[1])
        gamma=float(args[2])

    if not STD or DEBUG:
        print("INPUT      :",poscarname)
        print("OUTPUT     :",outputname)
        print("ALPHA(DEG) :",alpha)
        print("BETA(DEG)  :",beta)
        print("GAMMA(DEG) :",gamma)

    # makes instance
    poscar = SAE.ReadVaspPoscar(poscarname)

    title = poscar.get_title()
    scale = poscar.get_scale()
    t = poscar.get_t()
    vasp = poscar.get_vasp_version()
    nion = poscar.get_nion()
    atoms = poscar.get_atoms()
    atoms_index = poscar.get_atoms_index()
    natom = poscar.get_natom()
    selective = poscar.get_selective()
    direct = poscar.get_direct()
    position = poscar.get_position()
    fix = poscar.get_fix()

    ion = poscar.get_ion()
    ion_local = poscar.get_ion_local()
    atoms_index_j = poscar.get_atoms_index_j()

    if STD:
        out = sys.stdout
    else:
        try:
            out = open(outputname,'w')
        except:
            sys.exit("STOP: "+out+" can't open")

################################################################################
# ORIGINAL POSCAR
################################################################################
#   print >> out, title
    if DEBUG:
        print(" ",scale, file=out)
        print("  %13.9f %13.9f %13.9f" %(t[0,0],t[1,0],t[2,0]), file=out)
        print("  %13.9f %13.9f %13.9f" %(t[0,1],t[1,1],t[2,1]), file=out)
        print("  %13.9f %13.9f %13.9f" %(t[0,2],t[1,2],t[2,2]), file=out)
        print("", file=out)
#
#   if vasp >= 5:
#       print >> out, " ",
#       for i in range(nion):
#           print >> out,atoms_index[i],
#       print >> out, " "
#
#   print >> out, " ",
#   for i in range(nion):
#       print >> out, atoms[i],
#   print >> out, " "
#
#   if selective:
#       print >> out, "Selective Dynamics"
#   if direct:
#       print >> out, "Direct"
#   else:
#       print >> out, "Cartesian"
#
#   for j in range(natom):
#       print >> out, " %13.9f %13.9f %13.9f" \
#               %(position[j,0], position[j,1], position[j,2]),
#       if selective:
#           print >> out, "",
#           print >> out, fix[j,0],fix[i,1],fix[i,2],
#       print >> out, ""
################################################################################


################################################################################
# Rotated  POSCAR
################################################################################

    # オイラー角(deg)
    title0= "alpha="+str(alpha)+", beta="+str(beta)+", gamma="+str(gamma)

    # オイラー角で回した時の基本並進ベクトル
    t,position = poscar.conv_rot_euler(alpha,beta,gamma)

    print(title+": "+title0, file=out)
    print(" ",scale, file=out)
    print("  %13.9f %13.9f %13.9f" %(t[0,0],t[1,0],t[2,0]), file=out)
    print("  %13.9f %13.9f %13.9f" %(t[0,1],t[1,1],t[2,1]), file=out)
    print("  %13.9f %13.9f %13.9f" %(t[0,2],t[1,2],t[2,2]), file=out)

    if vasp >= 5:
        print(" ", file=out, end="")
        for i in range(nion):
            print(atoms_index[i], file=out, end="")
        print(" ", file=out)

    print(" ", file=out, end="")
    for i in range(nion):
        print(atoms[i], file=out, end="")
    print(" ", file=out)

    if direct:
        print("Direct", file=out)
    else:
        print("Cartesian", file=out)

    for j in range(natom):
        print(" %13.9f %13.9f %13.9f"
                %(position[j,0], position[j,1], position[j,2]), file=out, end="")
        print("")

    if not STD:
        out.close()

