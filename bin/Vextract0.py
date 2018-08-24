#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# セル内の特定領域の原子のみを吸い出す
#   (*) 一応 Force 情報もまとめて POSCAR.vasp に吸い出すはず(未テスト14.11.13)
#
# 入力(1)  POSCAR
# 入力(2)  セル内の選択範囲（ソース中に記述, 2014.11.13 c軸の範囲を直指定)
#
# 出力(1)  POSCAR.vasp  (指定した範囲のみ出力した POSCAR)
# 出力(2)  LIST.ext     (Rmove や VmodifyAtomPosition などで使えるような形式)
#
################################################################################
#
# 2018.08.15, 08.23
#  Python2/3 両対応
#
# 2014.11.13 1st
#
################################################################################
from __future__ import print_function
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"
################################################################################

import sys
import os
import optparse
import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

#import re
#from copy import deepcopy

################################################################################
def options():

    ###############################################
    ## default parameter
    ##
    cname  = "POSCAR" # OUTPUT BASE filename
    POSCAR = "POSCAR" # INPUT (BASE) filename

    ###############################################
    ## optparse
    ##
    parser = optparse.OptionParser()

    parser.add_option(  '-i','--input',
                        dest='INPUT',
                        default=POSCAR,
    )
    parser.add_option(  '-o','--output',
                        dest='OUTPUT',
                        default=cname,
    )
    options,  args = parser.parse_args()

    if options.INPUT:
        POSCAR=options.INPUT

    if options.OUTPUT:
        cname=options.OUTPUT

    #print args,options
    if len(args) > 0:
        #print "script name:",argvs[0]
        #POSCAR=argv[0]
        #distance = float(args[0])
        cname=args[0]

    if not os.path.exists(POSCAR):
        if os.path.exists(POSCAR+".vasp"):
            POSCAR="POSCAR.vasp"
        else:
            sys.exit(POSCAR+" file not found")

    print("INPUT file name    : %s" % str(POSCAR))
    print("OUTPUT file name   : %s" % str(cname+".vasp"))
    print("")

    return [POSCAR,cname]


################################################################################
if __name__ == '__main__':

    # Default & OptionParser
    POSCAR,cname = options()

    # POSCAR の事前読み込み
    nion,natom,VASP = SAE.read_poscar_param(POSCAR)

    # POSCAR 読み込みのための準備
    t           = np.zeros((3,3))
    atoms       = []
    atoms_index = []
    ion         = np.zeros(natom)
    ion_local   = np.zeros(natom)
    position    = np.zeros((natom,3))
    fix         = np.zeros((natom,3),dtype='S')

    # POSCAR の読み込み
    title,scale,selective,direct = \
       SAE.read_poscar(POSCAR,VASP,t,atoms,atoms_index,ion,ion_local,position,fix)

    direct0 = direct

    # POSCAR からの範囲指定での抽出(c軸のみ指定)
    c0 = np.zeros(3)
    c1 = np.zeros(3)


#####################################################################
#####################################################################
    # all layer
#   c1[2] = 1.0
#   c0[2] = 0.0

    # top layer
    c1[2] = 0.90732
    c0[2] = 0.59268

    # bottom layer
#   c1[2] = 0.40732
#   c0[2] = 0.09268
#####################################################################
#####################################################################


    # 事前準備 ( if direct: direct to car and scale =1.0 )
    scale,direct,ex_natom = SAE.extract_struct_param(scale,t,natom,\
                                                     direct,position,c0,c1)

    ex_atoms       = []
    ex_atoms_index = []
    ex_position    = np.zeros((ex_natom,3))
    ex_fix         = np.zeros((ex_natom,3),dtype='S')
    ex_j           = np.zeros(ex_natom)

   ## 特定原子の抽出(フォース情報未対応)
   #ex_nion = extract_struct0(scale,t,natom,direct,position,c0,c1,\
   #                          atoms,atoms_index,ion,ion_local,\
   #                          ex_j,ex_natom,ex_atoms,ex_atoms_index,ex_position)

    # 特定原子の抽出 (フォース情報(VASP)対応版)
    ex_nion = SAE.extract_struct1(scale,t,natom,direct,position,fix,c0,c1,\
                                  atoms,atoms_index,ion,ion_local,\
                                  ex_j,ex_natom,ex_atoms,ex_atoms_index,\
                                  ex_position,ex_fix)

    # Cartesian to Direct
    if direct0:
        scale,direct = SAE.conv_car2directa(scale,t,ex_natom,direct,ex_position)


    # 抽出した原子の一覧出力
    try:
       #out = sys.stdout
        out = open('LIST.ext','w',)
    except:
        sys.exit("LIST.ext not open")

    if direct:
        mode="Direct"
    else:
        mode="Cartesian"

    print("# ", file=out)
    print("# "+mode+" Mode", file=out)
    print("# num,   positon(x,y,z),                          atomtype, atom", file=out)
    for i in range(ex_natom):
        print("%3i    %13.9f %13.9f %13.9f %3i %2s"
                      % ( ex_j[i],
                          ex_position[i,0], ex_position[i,1], ex_position[i,2],
                          ion[ex_j[i]]+1, atoms_index[int(ion[ex_j[i]])] ), file=out)
    out.close


    # POSCAR の標準出力(特定原子のみの POSCAR)
    STD=False
   #STD=True
    SAE.print_poscar(cname,STD,title,scale,ex_natom,ex_nion,selective,direct,VASP,
                     t,ex_atoms,ex_atoms_index,ex_position,ex_fix)

################################################################################

