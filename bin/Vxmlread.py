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
# 2015.01.07                                                                    
#   完全分離版
#    [ライブラリ] read_vasprun.py (<-- Vxmlread_LIB0.py ベース)        
#    [本体] Vxmlread.py   
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
__author__     = "Kengo NAKADA"                                                           
__maintainer__ = "Kengo NAKADA"                                                           
__credits__    = ["Kengo NAKADA"]                                                         
__email__      = "kengo.nakada@gmail.com"                                                 
__copyright__  = "Copyright 2015, Kengo NAKADA"                                           
__license__    = "MIT"                                                                    
#                                                                                         
__status__     = "alpha"                                                                  
__version__    = "0.0.1"                                                                  
################################################################################

import sys
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

    # vasprun.xml parse
    INCAR,KPOINTS,POSCAR,CONTCAR =  SAE.read_vasprun0(XMLFILE)

    title,scale,natom,nion,selective,direct,VASP,\
       t_initial,atoms,atoms_index,position_initial,fix_initial = POSCAR

    title,scale,natom,nion,selective,direct,VASP,\
       t_final,atoms,atoms_index,position_final,fix_final = CONTCAR

    ###################################################
    # INCAR の出力
    INCAR_TAG,INCAR_TEXT = INCAR
    try:
        out = open('INCAR.rebuild','w')
        print "Makes INCAR.rebuild"
        for i in range(len(INCAR_TAG)):
            print >> out, INCAR_TAG[i],"=",INCAR_TEXT[i]
    except:
        out.close()
        sys.exit("STOP: INCAR.rebuild can't open")
    finally:
        out.close()

    ###################################################
    # KPOINTS の出力
    try:
        out = open('KPOINTS.rebuild','w')
        print "Makes KPOINTS.rebuild"
        for i in range(len(KPOINTS)):
            print >> out, KPOINTS[i]
    except:
        out.close()
        sys.exit("STOP: KPOINTS.rebuild can't open")
    finally:
        out.close()

    ###################################################
    # POSCAR の出力 (Initial をアウトプット)
    print "Makes POSCAR.rebuild"
    STD=False
    cname='POSCAR.rebuild'
    SAE.print_poscar(cname,STD,title,scale,natom,nion,selective,direct,VASP,\
       t_initial,atoms,atoms_index,position_initial,fix_initial)


    ###################################################
    # CONTCAR の出力 (Final をアウトプット)
    print "Makes CONTCAR.rebuild"
    STD=False
    cname='CONTCAR.rebuild'
    SAE.print_poscar(cname,STD,title,scale,natom,nion,selective,direct,VASP,\
       t_final,atoms,atoms_index,position_final,fix_final)
    
