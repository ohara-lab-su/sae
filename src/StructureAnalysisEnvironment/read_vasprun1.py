#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#  読み込んだ vasprun.xml の initial の情報を元に
#  CONTCAR
#  相当の情報を loop 毎にretrunする
#  
# それぞれの内容は下記
#
#   CONTCAR_ALL=[title,scale,natom,nion,selective,direct,VASP,\
#      t_loop,atoms,atoms_index,position_loop,fix_final]
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
#  Python2/3 両対応暫定
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

from sae.errors import legacy_error as _legacy_error

try:
    from .copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *


__status__ = "alpha"
__version__ = "0.0.4"

################################################################################

import sys
import os
import gzip
# import optparse
import xml.etree.ElementTree as ET

import numpy as np

try:
    import StructureAnalysisEnvironment as SAE
except:
    import StructureAnalysisEnvironment as SAE

# import SpaceGroupEnvironment as SGE

# import os
# import re
# from copy import deepcopy


################################################################################
def read_vasprun1(XMLFILE):
    if os.path.exists(XMLFILE):
        f = XMLFILE
        ZIP_FLAG = False
    elif os.path.exists(XMLFILE + ".gz"):
        f = gzip.open(XMLFILE + ".gz")
        ZIP_FLAG = True
    else:
        _legacy_error("STOP: " + XMLFILE + " or " + XMLFILE + ".gz file not found")

    try:
        tree = ET.parse(f)
    except:
        if ZIP_FLAG:
            _legacy_error("can't parse " + XMLFILE + ".gz")
        else:
            _legacy_error("can't parse " + XMLFILE)
    finally:
        if ZIP_FLAG:
            f.close()

    #   try:
    #       tree = ET.parse(XMLFILE)
    #   except:
    #       _legacy_error("can'nt parse "+XMLFILE)

    root = tree.getroot()

    ###################################################
    # from generator
    program = root.findtext("generator/i[@name='program']")
    version = root.findtext("generator/i[@name='version']")
    subversion = root.findtext("generator/i[@name='subversion']")

    ###################################################
    # from incar
    SYSTEM = root.findtext("incar/i[@name='SYSTEM']")

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

    ###################################################
    # [ion_loop] [lattice vector]
    t_loop = np.zeros((3, 3, n_ion_loop))
    ion_loop = 0
    for cal in root.findall("calculation/structure/crystal/varray[@name='basis']"):
        j = 0
        for e in cal:
            tmp = e.text.split()
            t_loop[0, j, ion_loop] = tmp[0]
            t_loop[1, j, ion_loop] = tmp[1]
            t_loop[2, j, ion_loop] = tmp[2]
            # print t_loop[0,j,ion_loop],\
            #      t_loop[1,j,ion_loop],\
            #      t_loop[2,j,ion_loop]
            j += 1
        ion_loop += 1

    ###################################################
    # [ion_loop] [position]
    #   for cal in root.findall("calculation/structure/varray[@name='positions']/v"):
    ion_loop = 0
    position_loop = np.zeros((natom, 3, n_ion_loop))
    for cal in root.findall("calculation/structure/varray[@name='positions']"):
        j = 0
        for e in cal:
            tmp = e.text.split()
            position_loop[j, 0, ion_loop] = tmp[0]
            position_loop[j, 1, ion_loop] = tmp[1]
            position_loop[j, 2, ion_loop] = tmp[2]
            # print position_loop[j,0,ion_loop],\
            #      position_loop[j,1,ion_loop],\
            #      position_loop[j,2,ion_loop]
            j += 1
        ion_loop += 1

    title = SYSTEM
    scale = 1.0
    VASP = 5  # VASP4 の vasprun.xml でも出力はVASP5形式にする
    direct = True

    CONTCAR_ALL = [title, scale, natom, nion, selective, direct, VASP, \
                   t_loop, atoms, atoms_index, position_loop, fix_final]

    return [n_ion_loop, CONTCAR_ALL]


################################################################################
# テスト用
################################################################################
if __name__ == '__main__':

    # Default & OptionParser
    # XMLFILE = options()
    XMLFILE = "vasprun.xml"  # default name

    # vasprun.xml parse
    n_ion_loop, CONTCAR_ALL = read_vasprun1(XMLFILE)

    title, scale, natom, nion, selective, direct, VASP, \
    t_loop, atoms, atoms_index, position_loop, fix_final = CONTCAR_ALL

    print("Numver of ION-LOOP:%s" % str(n_ion_loop))

    ###################################################
    # loop 毎のCONTCAR の出力
    for ion_loop in range(n_ion_loop):
        # print "Makes CONTCAR."+str(ion_loop+1)+".rebuild"
        print("Makes CONTCAR.%s.rebuild" % str(ion_loop + 1))

        t = t_loop[:, :, ion_loop]
        position = position_loop[:, :, ion_loop]
        fix = fix_final

        STD = False
        cname = 'CONTCAR.' + str(ion_loop + 1) + '.rebuild'
        SAE.print_poscar(cname, STD, \
                         title, scale, natom, nion, selective, direct, VASP, \
                         t, atoms, atoms_index, position, fix)
