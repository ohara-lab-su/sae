#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#  読み込んだ vasprun.xml の情報を元に
#  CONTCAR
#  相当の情報を loop 毎に MD 形式で出力する
#
#
################################################################################
#
# 2015.01.08
#  フォースおよびエネルギーの出力対応
#  読み込みルーチンを read_vasprun2.py へ変更
#
# 2015.01.07
#  Vxml2MD.py へコードを改変(Vxml2CONTCAR_ALL.py がベース
#  MD(x,y,z)形式へ出力,フォースは未対応
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
__author__     = "Kengo NAKADA"                                                           
__maintainer__ = "Kengo NAKADA"                                                           
__credits__    = ["Kengo NAKADA"]                                                         
__email__      = "kengo.nakada@gmail.com"                                                 
__copyright__  = "Copyright 2015, Kengo NAKADA"                                           
__license__    = "MIT"                                                                    
#                                                                                         
__status__     = "alpha"                                                                  
__version__    = "0.0.7"                                                                  
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
    vasprun =  SAE.read_vasprun2(XMLFILE)

    n_ion_loop,POSCAR,CONTCAR,CONTCAR_ALL,FORCE_ALL,ENERGY_ALL = vasprun

    title,scale,natom,nion,selective,direct,VASP,\
       t_loop,atoms,atoms_index,position_loop,fix_final = CONTCAR_ALL

    e_wo_entrp_loop,e_fr_energy_loop = ENERGY_ALL
    force_loop,stress_loop = FORCE_ALL

#   print "Numver of ION-LOOP:", n_ion_loop
#   print "Number of ION :", nion

    t =  t_loop[:,:,n_ion_loop-1]
    position = position_loop[:,:,n_ion_loop-1]

    ###################################################
    # loop 毎のCONTCAR の出力
    for ion_loop in range(n_ion_loop):
        pass
#       print "Makes CONTCAR."+str(ion_loop+1)+".rebuild"

        t =  t_loop[:,:,ion_loop]
        position = position_loop[:,:,ion_loop]
        force = force_loop[:,:,ion_loop]
        e_wo_entrp = e_wo_entrp_loop[ion_loop]

#       # 絶対座標化 (セル内の描画になるので絶対化にはあまり意味が無い)
#       #             一応はこのルーチン部分を挟むことで、抜けた後は
#       #             普通に座標系が絶対座標化される
#       ABS=True
#       SAE.conv_direct2car(ABS,scale,t,natom,direct,position)

        j=0
        print natom
        print "   setp=     ",ion_loop+1,"     ","  Energy=",e_wo_entrp
        for ion in range(nion):
            for atom in range(atoms[ion]):
                print "   %2s %12.8f %12.8f %12.8f  %12.8f %12.8f %12.8f" \
                        % ( atoms_index[ion],\
                        position[j,0],position[j,1],position[j,2],\
                        force[j,0], force[j,1], force[j,2] )
                j+=1


