#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#  読み込んだ vasprun.xml の情報を元に
#  CONTCAR
#  相当の情報を loop 毎に出力する
#
#  ほぼ　read_vasprun1.py の __main__ ルーチンのみ抜粋
#  単独コードとして微妙に修正のみ
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.01.07
#  ION ループごとの CONTCAR 出力プログラムへ改変
#  Vxml2CONTCAR_ALL.py
#
# 2015.01.07
#  ION ループごとの出力ルーチンを別関数へ分離
#     read_vasprn0.py  (INCAR,KPOINTS,POSCAR,CONTCAR)
#     read_vasprn1.py  (CONTCAR_ALL)
#
# 2015.01.07
#   完全分離版 read_vasprun.py (<-- Vxmlread_LIB0.py ベース)
#
# 2015.01.07
#   rebuild 系の出力を追加
#   関数化(引数でのやりとりではなく、戻り値をすべて一つのリストで返す方向性で)
#   INCAR と KPOINTS 出力は暫定処置
#
#   旧バージョン(非関数) Vxmlread_nonLIB.py
#   新バージョン(関数)   Vxmlread_LIB0.py
#
# 2015.01.06 1st edtion
#   Vxmlread.py
#
################################################################################
from __future__ import print_function
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"                                                           
__credits__    = ["Kengo NAKADA"]                                                         
__email__      = "kengo.nakada@gmail.com"                                                 
__copyright__  = "Copyright 2015, Kengo NAKADA"                                           
__license__    = "MIT"                                                                    
#                                                                                         
__status__     = "alpha"                                                                  
__version__    = "0.0.5"                                                                  
################################################################################

#import sys
import optparse
#import xml.etree.ElementTree as ET

#import numpy as np
import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE  

#import os
#import re
#from copy import deepcopy


################################################################################
def options():                                                                  
                                                                                
    XMLFILE = "vasprun.xml"  # default name
                                                                                
    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input',
                        dest='INPUT',
                        default=XMLFILE,
    )
    options,  args = parser.parse_args()
                                                                                
    if options.INPUT:
        XMLFILE=options.INPUT
                                                                                
    if len(args) > 0:
        XMLFILE=args[0]
                                                                                
    return XMLFILE


################################################################################
if __name__ == '__main__':

    # Default & OptionParser
    XMLFILE = options()
   #XMLFILE = "vasprun.xml"  # default name

    # vasprun.xml parse
    n_ion_loop,CONTCAR_ALL =  SAE.read_vasprun1(XMLFILE)

    title,scale,natom,nion,selective,direct,VASP,\
       t_loop,atoms,atoms_index,position_loop,fix_final = CONTCAR_ALL

    print("Numver of ION-LOOP:", n_ion_loop)

    ###################################################
    # loop 毎のCONTCAR の出力
    for ion_loop in range(n_ion_loop):
        print("Makes CONTCAR."+str(ion_loop+1)+".rebuild")

        t =  t_loop[:,:,ion_loop]
        position = position_loop[:,:,ion_loop]
        fix = fix_final

        STD=False
        cname='CONTCAR.'+str(ion_loop+1)+'.rebuild'
        SAE.print_poscar(cname,STD,\
                title,scale,natom,nion,selective,direct,VASP,\
                t,atoms,atoms_index,position,fix)

   
