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
#  相当の情報をretrunする
#  
# それぞれの内容は下記
#
#   POSCAR=[title,scale,natom,nion,selective,direct,VASP,\
#      t_initial,atoms,atoms_index,position_initial,fix_initial]
#
#   CONTCAR=[title,scale,natom,nion,selective,direct,VASP,\
#      t_final,atoms,atoms_index,position_final,fix_final]
#
#   return [INCAR,KPOINTS,POSCAR,CONTCAR]
#
#  テスト用の Vxmread_nonLIB.py --> Vxmread_LIB0.py がベース
#
#  注意)
#    VASP の cartesian は scale=1.0 で基本並進で絶対座標化
#    されてないので、scale=1.0 ならば Direct=Car となる・・・はず？
#    direct は True としておく
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
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
from copyright import *

__status__ = "alpha"
__version__ = "0.0.4"

################################################################################

import sys
import os
import gzip
# import optparse
import xml.etree.ElementTree as ET

import numpy as np
import StructureAnalysisEnvironment as SAE


# import SpaceGroupEnvironment as SGE

# import os
# import re
# from copy import deepcopy


################################################################################
def read_vasprun0(XMLFILE):
    if os.path.exists(XMLFILE):
        f = XMLFILE
        ZIP_FLAG = False
    elif os.path.exists(XMLFILE + ".gz"):
        f = gzip.open(XMLFILE + ".gz")
        ZIP_FLAG = True
    else:
        sys.exit("STOP: " + XMLFILE + " or " + XMLFILE + ".gz file not found")

    try:
        tree = ET.parse(f)
    except:
        if ZIP_FLAG:
            sys.exit("can't parse " + XMLFILE + ".gz")
        else:
            sys.exit("can't parse " + XMLFILE)
    finally:
        if ZIP_FLAG:
            f.close()

    #   try:
    #       tree = ET.parse(XMLFILE)
    #   except:
    #       sys.exit("can'nt parse "+XMLFILE)

    root = tree.getroot()

    ###################################################
    # from generator
    program = root.findtext("generator/i[@name='program']")
    version = root.findtext("generator/i[@name='version']")
    subversion = root.findtext("generator/i[@name='subversion']")

    ###################################################
    # from incar
    SYSTEM = root.findtext("incar/i[@name='SYSTEM']")
    INCAR_TAG = []
    INCAR_TEXT = []
    for i in root.find('incar'):
        INCAR_TAG.append(i.attrib.get("name"))
        INCAR_TEXT.append(i.text)

    INCAR = [INCAR_TAG, INCAR_TEXT]

    #   try:
    #       out = open('INCAR.rebuild','w')
    #       print "Makes INCAR.rebuild"
    #       for i in range(len(root.find('incar'))):
    #          #print >> out, i.attrib.get("name"),"=",i.text
    #           print >> out, INCAR_TAG[i],"=",INCAR[i]
    #   except:
    #       out.close()
    #       sys.exit("STOP: INCAR.rebuild can't open")
    #   finally:
    #       out.close()

    ###################################################
    # from kpoints
    generation = root.find('kpoints/generation').get('param')
    divition = root.find("kpoints/generation/v[@name='divisions']").text

    KPOINTS = []
    KPOINTS.append("K-POINTS")
    KPOINTS.append("0")
    KPOINTS.append(generation)
    KPOINTS.append(divition)
    for es in root.find("kpoints/varray[@name='kpointlist']"):
        KPOINTS.append(es.text)

    #   try:
    #       out = open('KPOINTS.rebuild','w')
    #       print "Makes KPOINTS.rebuild"
    #       print >> out, 'K-POINTS'
    #       print >> out, '0'
    #       print >> out, generation
    #       print >> out, divition
    #       for es in root.find("kpoints/varray[@name='kpointlist']"):
    #           print >> out, es.text
    #   except:
    #       out.close()
    #       sys.exit("STOP: KPOINTS.rebuild can't open")
    #   finally:
    #       out.close()

    ###################################################
    # Number of ION-LOOP
    n_ion_loop = len(root.findall('calculation'))

    ###################################################
    # Get Number of atom
    natom = int(root.findtext("atominfo/atoms"))  # atoms
    nion = int(root.findtext("atominfo/types"))  # types

    ###################################################
    # atoms[i]       : 原子の種類番号(max=nion)を与えると、原子種の数を返す
    # atoms_index[i] : 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
    atoms = np.zeros(nion, dtype=int)
    atoms_index = np.zeros(nion, dtype='S2')
    number = 0
    local_nion = 1
    for es in root.findall("atominfo/array[@name='atoms']/set/rc"):
        index_FLAG = True
        for rc in es:
            if index_FLAG:
                name = str(rc.text)
                index_FLAG = False
            else:
                number_tmp = int(rc.text)
                if number_tmp == number:
                    local_nion += 1
                else:
                    local_nion = 1
                    number = number_tmp
        atoms[number - 1] = local_nion
        atoms_index[number - 1] = name

    #  for i in range(nion):
    #      print atoms_index[i],atoms[i]

    ###################################################
    # [initial] [lattice vector]
    #     基本並進ベクトル(注意:配列内indexは0から)          
    #     POSCAR 入力形式                                    
    #                                                        
    #           x   y   z                                    
    #     t1 = a11 a21 a31  ! lattice vector t1              
    #     t2 = a12 a22 a32  ! lattice vector t2              
    #     t3 = a13 a23 a33  ! lattice vector t3    
    #                                                        
    t_initial = np.zeros((3, 3))
    j = 0
    for e in root.find("structure[@name='initialpos']/crystal/varray[@name='basis']"):
        tmp = e.text.split()
        t_initial[0, j] = tmp[0]
        t_initial[1, j] = tmp[1]
        t_initial[2, j] = tmp[2]
        # print t_initial[0,j],t_initial[1,j],t_initial[2,j]
        j += 1

    ###################################################
    # [initial] [position]
    position_initial = np.zeros((natom, 3))
    j = 0
    for e in root.find("structure[@name='initialpos']/varray[@name='positions']"):
        tmp = e.text.split()
        position_initial[j, 0] = tmp[0]
        position_initial[j, 1] = tmp[1]
        position_initial[j, 2] = tmp[2]
        # print position_initial[j,0],position_initial[j,1],position_initial[j,2]
        j += 1

    ###################################################
    # [initial] [selective]
    fix_initial = np.zeros((natom, 3), dtype='S')
    selective = False
    if root.find("structure[@name='initialpos']").findall("varray[@name='selective']"):
        selective = True
    if selective:
        j = 0
        for e in root.find("structure[@name='initialpos']/varray[@name='selective']"):
            tmp = e.text.split()
            fix_initial[j, 0] = str(tmp[0])
            fix_initial[j, 1] = str(tmp[1])
            fix_initial[j, 2] = str(tmp[2])
            # print fix[j,0],fix[j,1],fix[j,2]
            j += 1

    ###################################################
    # [final] [lattice vector]
    t_final = np.zeros((3, 3))
    j = 0
    for e in root.find("structure[@name='finalpos']/crystal/varray[@name='basis']"):
        tmp = e.text.split()
        t_final[0, j] = tmp[0]
        t_final[1, j] = tmp[1]
        t_final[2, j] = tmp[2]
        j += 1

    ###################################################
    # [final] [position]
    position_final = np.zeros((natom, 3))
    j = 0
    for e in root.find("structure[@name='finalpos']/varray[@name='positions']"):
        tmp = e.text.split()
        position_final[j, 0] = tmp[0]
        position_final[j, 1] = tmp[1]
        position_final[j, 2] = tmp[2]
        # print position_final[j,0],position_final[j,1],position_final[j,2]
        j += 1

    ###################################################
    # [final] [selective]
    fix_final = np.zeros((natom, 3), dtype='S')
    selective = False
    if root.find("structure[@name='finalpos']").findall("varray[@name='selective']"):
        selective = True
    if selective:
        j = 0
        for e in root.find("structure[@name='finalpos']/varray[@name='selective']"):
            tmp = e.text.split()
            fix_final[j, 0] = str(tmp[0])
            fix_final[j, 1] = str(tmp[1])
            fix_final[j, 2] = str(tmp[2])
            # print fix[j,0],fix[j,1],fix[j,2]
            j += 1

    title = SYSTEM
    scale = 1.0
    VASP = 5  # VASP4 の vasprun.xml でも出力はVASP5形式にする
    direct = True

    POSCAR = [title, scale, natom, nion, selective, direct, VASP, \
              t_initial, atoms, atoms_index, position_initial, fix_initial]

    CONTCAR = [title, scale, natom, nion, selective, direct, VASP, \
               t_final, atoms, atoms_index, position_final, fix_final]

    return [INCAR, KPOINTS, POSCAR, CONTCAR]


################################################################################
# テスト用
################################################################################
if __name__ == '__main__':

    # Default & OptionParser
    # XMLFILE = options()
    XMLFILE = "vasprun.xml"  # default name

    # vasprun.xml parse
    INCAR, KPOINTS, POSCAR, CONTCAR = read_vasprun0(XMLFILE)

    title, scale, natom, nion, selective, direct, VASP, \
    t_initial, atoms, atoms_index, position_initial, fix_initial = POSCAR

    title, scale, natom, nion, selective, direct, VASP, \
    t_final, atoms, atoms_index, position_final, fix_final = CONTCAR

    ###################################################
    # INCAR の出力
    INCAR_TAG, INCAR_TEXT = INCAR
    try:
        out = open('INCAR.rebuild', 'w')
        print("Makes INCAR.rebuild")
        for i in range(len(INCAR_TAG)):
            # print >> out, INCAR_TAG[i],"=",INCAR_TEXT[i]
            print("%s=%s" % (str(INCAR_TAG[i]), str(INCAR_TEXT[i])), file=out)
    except:
        out.close()
        sys.exit("STOP: INCAR.rebuild can't open")
    finally:
        out.close()

    ###################################################
    # KPOINTS の出力
    try:
        out = open('KPOINTS.rebuild', 'w')
        print("Makes KPOINTS.rebuild")
        for i in range(len(KPOINTS)):
            print("%s" % str(KPOINTS[i]))
    except:
        out.close()
        sys.exit("STOP: KPOINTS.rebuild can't open")
    finally:
        out.close()

    ###################################################
    # POSCAR の出力 (Initial をアウトプット)
    print("Makes POSCAR.rebuild")
    STD = False
    cname = 'POSCAR.rebuild'
    SAE.print_poscar(cname, STD, title, scale, natom, nion, selective, direct, VASP, \
                     t_initial, atoms, atoms_index, position_initial, fix_initial)

    ###################################################
    # CONTCAR の出力 (Final をアウトプット)
    print("Makes CONTCAR.rebuild")
    STD = False
    cname = 'CONTCAR.rebuild'
    SAE.print_poscar(cname, STD, title, scale, natom, nion, selective, direct, VASP, \
                     t_final, atoms, atoms_index, position_final, fix_final)
