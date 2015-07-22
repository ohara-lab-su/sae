#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# VASP
#  vasprun.xml 読み込み用の class ファイル
#  関数 read_vasprun2.py がベース
#
################################################################################
#
# 2015.06.15
#  追加実装
#  get_atoms()
#  get_atoms_index()
#  get_atoms_j()
#  get_atoms_index_j()
#
# 2015.01.20
#  gzip 対応
#
# 2015.01.11 (sun) startup
#  read_vasprun2.py --> ReadVasprun.py (クラス化)
#  まったりと作業
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
__version__    = "0.0.2"
################################################################################

import os
import sys
import gzip
import xml.etree.ElementTree as ET

import numpy as np
#import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

#import re
#from copy import deepcopy


################################################################################
class ReadVaspVasprun(object):

    def __init__(self,name='vasprun.xml'):

        if os.path.exists(name):
            f = name
            ZIP_FLAG = False
        elif os.path.exists(name+".gz"):
            f = gzip.open(name+".gz")
            ZIP_FLAG = True
        else:
            sys.exit("STOP: "+name+" or "+name+".gz file not found")

        try:
            tree = ET.parse(f)
        except:
            if ZIP_FLAG:
                sys.exit("can't parse "+XMLFILE+".gz")
            else:
                sys.exit("can't parse "+XMLFILE)
        finally:
            if ZIP_FLAG:
                f.close()

        self.root = tree.getroot()

        self.n_ion_loop = len(self.root.findall('calculation'))

    def get_n_ion_loop(self):
        return self.n_ion_loop

    ###################################################
    # from generator
    def generator(self):
        program = self.root.findtext("generator/i[@name='program']")
        version = self.root.findtext("generator/i[@name='version']")
        subversion = self.root.findtext("generator/i[@name='subversion']")

        GENERATOR = [program,version,subversion]
        return [GENERATOR]

    ###################################################
    # from incar
    def get_incar(self):
        SYSTEM = self.root.findtext("incar/i[@name='SYSTEM']")
        INCAR_TAG = []
        INCAR_TEXT = []
        for i in self.root.find('incar'):
               INCAR_TAG.append(i.attrib.get("name"))
               INCAR_TEXT.append(i.text)

        INCAR = [INCAR_TAG,INCAR_TEXT]
        return [INCAR]


    ###################################################
    # from kpoints
    def get_kpoints(self):
        generation = self.root.find('kpoints/generation').get('param')
        divition =  self.root.find("kpoints/generation/v[@name='divisions']").text

        KPOINTS = []
        KPOINTS.append("K-POINTS")
        KPOINTS.append("0")
        KPOINTS.append(generation)
        KPOINTS.append(divition)
        for es in self.root.find("kpoints/varray[@name='kpointlist']"):
            KPOINTS.append(es.text)

        return [KPOINTS]


    ###################################################
    # Get Number of atom
    def get_natom(self):
        self.natom = int(self.root.findtext("atominfo/atoms"))  # atoms
        return self.natom

    def get_nion(self):
        self.nion = int(self.root.findtext("atominfo/types"))   # types
        return self.nion


    ###################################################
    # atoms[i]       : 原子の種類番号(max=nion)を与えると、原子種の数を返す
    # atoms_index[i] : 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
    def get_types(self):
#       NION = self.nion()
        NION = self.get_nion()
        atoms = np.zeros(NION,dtype=int)
        atoms_index = np.zeros(NION,dtype='S2')
        number = 0
        local_nion = 1
        for es in self.root.findall("atominfo/array[@name='atoms']/set/rc"):
            index_FLAG=True
            for rc in es:
                if index_FLAG:
                    name = str(rc.text).strip()
                    index_FLAG=False
                else:
                    number_tmp = int(rc.text)
                    if number_tmp == number:
                        local_nion += 1
                    else:
                        local_nion = 1
                        number = number_tmp
            atoms[number-1] = local_nion
            atoms_index[number-1] = name

        TYPES = atoms,atoms_index
        return TYPES

    def get_atoms(self):
        atoms, atoms_index = self.get_types()
        return atoms

    def get_atoms_index(self):
        atoms, atoms_index = self.get_types()
        return atoms_index

    def get_atoms_j(self):
        natom = self.get_natom()
        nion = self.get_nion()
        atoms = self.get_atoms()
        j = 0
        atoms_j = np.zeros(natom,dtype=int)
        for ion in range(nion):
            for atom in range(atoms[ion]):
                atoms_j[j] = ion
                j += 1
        return atoms_j

    def get_atoms_index_j(self):
        natom = self.get_natom()
        nion = self.get_nion()
        atoms,atoms_index = self.get_types()
        j = 0
        atoms_index_j = np.zeros(natom,dtype='S2')
        for ion in range(nion):
            for atom in range(atoms[ion]):
                atoms_index_j[j] = atoms_index[ion]
                j += 1
        return atoms_index_j

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
    def get_t_initial(self):
        t_initial = np.zeros((3,3))
        j=0
        for e in self.root.find(\
                "structure[@name='initialpos']/crystal/varray[@name='basis']"):
            tmp = e.text.split()
            t_initial[0,j] = tmp[0]
            t_initial[1,j] = tmp[1]
            t_initial[2,j] = tmp[2]
           #print t_initial[0,j],t_initial[1,j],t_initial[2,j]
            j += 1

        return [t_initial]

    ###################################################
    # [initial] [position]
    def get_position_initial(self):
#       NATOM = self.natom()
        NATOM = self.get_natom()
        position_initial = np.zeros((NATOM,3))
        j=0
        for e in self.root.find(\
                "structure[@name='initialpos']/varray[@name='positions']"):
            tmp = e.text.split()
            position_initial[j,0] = tmp[0]
            position_initial[j,1] = tmp[1]
            position_initial[j,2] = tmp[2]
           #print position_initial[j,0],position_initial[j,1],position_initial[j,2]
            j += 1

        return [position_initial]

    ###################################################
    # [initial] [selective]
    def get_selective_initial(self):
#       NATOM = self.natom()
        NATOM = self.get_natom()
        fix_initial = np.zeros((NATOM,3),dtype='S')
        selective=False
        if self.root.find(\
                "structure[@name='initialpos']").findall("varray[@name='selective']"):
            selective=True
        if selective:
            j=0
            for e in self.root.find("structure[@name='initialpos']/varray[@name='selective']"):
                tmp = e.text.split()
                fix_initial[j,0] = str(tmp[0])
                fix_initial[j,1] = str(tmp[1])
                fix_initial[j,2] = str(tmp[2])
               #print fix[j,0],fix[j,1],fix[j,2]
                j +=1

        return [fix_initial]

    ###################################################
    # [final] [lattice vector]
    def get_t_final(self):
        t_final = np.zeros((3,3))
        j=0
        for e in self.root.find(\
                "structure[@name='finalpos']/crystal/varray[@name='basis']"):
            tmp = e.text.split()
            t_final[0,j] = tmp[0]
            t_final[1,j] = tmp[1]
            t_final[2,j] = tmp[2]
            j += 1

        return [t_final]

    ###################################################
    # [final] [position]
    def get_position_final(self):
        natom = self.get_natom()
        position_final = np.zeros((natom,3))
        j=0
        for e in self.root.find(\
                "structure[@name='finalpos']/varray[@name='positions']"):
            tmp = e.text.split()
            position_final[j,0] = tmp[0]
            position_final[j,1] = tmp[1]
            position_final[j,2] = tmp[2]
           #print position_final[j,0],position_final[j,1],position_final[j,2]
            j += 1

        return [position_final]

    ###################################################
    # [final] [selective]
    def get_fix_final(self):
        natom = self.get_natom()
        fix_final = np.zeros((natom,3),dtype='S')
        selective=False
        if self.root.find(\
                "structure[@name='finalpos']").findall("varray[@name='selective']"):
            selective=True
        if selective:
            j=0
            for e in self.root.find(\
                    "structure[@name='finalpos']/varray[@name='selective']"):
                tmp = e.text.split()
                fix_final[j,0] = str(tmp[0])
                fix_final[j,1] = str(tmp[1])
                fix_final[j,2] = str(tmp[2])
               #print fix[j,0],fix[j,1],fix[j,2]
                j +=1

        return [fix_final]

    ###################################################
    # [ion_loop] [lattice vector]
    def get_t_loop(self):
        t_loop = np.zeros((3,3,self.n_ion_loop))
        ion_loop=0
        for cal in self.root.findall(\
                "calculation/structure/crystal/varray[@name='basis']"):
            j=0
            for e in cal:
                tmp = e.text.split()
                t_loop[0,j,ion_loop] = tmp[0]
                t_loop[1,j,ion_loop] = tmp[1]
                t_loop[2,j,ion_loop] = tmp[2]
               #print t_loop[0,j,ion_loop],\
               #      t_loop[1,j,ion_loop],\
               #      t_loop[2,j,ion_loop]
                j += 1
            ion_loop +=1

        return [t_loop]

    ###################################################
    # [ion_loop] [position]
#   for cal in root.findall("calculation/structure/varray[@name='positions']/v"):
    def get_position_loop(self):
        natom = self.get_natom()
        ion_loop=0
        position_loop = np.zeros((natom,3,self.n_ion_loop))
        for cal in self.root.findall(\
                "calculation/structure/varray[@name='positions']"):
            j = 0
            for e in cal:
                tmp = e.text.split()
                position_loop[j,0,ion_loop] = tmp[0]
                position_loop[j,1,ion_loop] = tmp[1]
                position_loop[j,2,ion_loop] = tmp[2]
               #print position_loop[j,0,ion_loop],\
               #      position_loop[j,1,ion_loop],\
               #      position_loop[j,2,ion_loop]
                j += 1
            ion_loop += 1

        return [position_loop]

    ###################################################
    # [ion_loop] [forces]
    def get_force_loop(self):
        natom = self.get_natom()
        ion_loop=0
        force_loop = np.zeros((natom,3,self.n_ion_loop))
        for cal in self.root.findall(\
                "calculation/varray[@name='forces']"):
            j = 0
            for e in cal:
                tmp = e.text.split()
                force_loop[j,0,ion_loop] = tmp[0]
                force_loop[j,1,ion_loop] = tmp[1]
                force_loop[j,2,ion_loop] = tmp[2]
               #print force_loop[j,0,ion_loop],\
               #      force_loop[j,1,ion_loop],\
               #      force_loop[j,2,ion_loop]
                j += 1
            ion_loop += 1

        return [force_loop]

    ###################################################
    # [ion_loop] [stress]
    def get_stress_loop(self):
        natom = self.get_natom()
        ion_loop=0
        stress_loop = np.zeros((natom,3,self.n_ion_loop))
        for cal in self.root.findall("calculation/varray[@name='stress']"):
            j = 0
            for e in cal:
                tmp = e.text.split()
                stress_loop[j,0,ion_loop] = tmp[0]
                stress_loop[j,1,ion_loop] = tmp[1]
                stress_loop[j,2,ion_loop] = tmp[2]
               #print stress_loop[j,0,ion_loop],\
               #      stress_loop[j,1,ion_loop],\
               #      stress_loop[j,2,ion_loop]
                j += 1
            ion_loop += 1

        return [stress_loop]

    ###################################################
    # [ion_loop] [energy]
    # ion loop 毎の Energy (without entropy)
    def get_energy(self):
        e_wo_entrp_loop = np.zeros((self.n_ion_loop))
        e_fr_energy_loop = np.zeros((self.n_ion_loop))
        i = 0
        for e in self.root.findall("calculation/energy/i[@name='e_wo_entrp']"):
            e_wo_entrp_loop[i] = e.text
            i += 1
        i = 0
        for e in self.root.findall("calculation/energy/i[@name='e_fr_energy']"):
            e_fr_energy_loop[i] = e.text
            i += 1

        energy = [e_fr_energy_loop,e_wo_entrp_loop]
        return [energy]

#   title=SYSTEM
#   scale=1.0
#   VASP=5 # VASP4 の vasprun.xml でも出力はVASP5形式にする
#   direct=True


#   POSCAR=[title,scale,natom,nion,selective,direct,VASP,\
#      t_initial,atoms,atoms_index,position_initial,fix_initial]

#   CONTCAR=[title,scale,natom,nion,selective,direct,VASP,\
#      t_final,atoms,atoms_index,position_final,fix_final]

#   CONTCAR_ALL=[title,scale,natom,nion,selective,direct,VASP,\
#      t_loop,atoms,atoms_index,position_loop,fix_final]

#   return [n_ion_loop,POSCAR,CONTCAR,CONTCAR_ALL,FORCE_ALL,ENERGY_ALL]



################################################################################
# テスト用
################################################################################
if __name__ == '__main__':

    import optparse
    # Default & OptionParser
   #XMLFILE = options()
    XMLFILE = "vasprun.xml"  # default name

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT',)
    options,  args = parser.parse_args()

    if options.INPUT: XMLFILE=options.INPUT
    if len(args) > 0: XMLFILE=args[0]

    # vasprun.xml parse
    vasprun = ReadVaspVasprun(XMLFILE)

    nion = vasprun.get_nion()
    natom = vasprun.get_natom()
    n_ion_loop =  vasprun.get_n_ion_loop()
    atoms = vasprun.get_atoms()
    atoms_j = vasprun.get_atoms_j()
    atoms_index = vasprun.get_atoms_index()
    atoms_index_j = vasprun.get_atoms_index_j()

    print 'NATOM   =',natom
    print 'NION    =',nion
    print 'LOOP    =',vasprun.get_n_ion_loop()

    print ""
    print "atoms_index"
    print "   ",
    for ion in range(nion):
        print atoms_index[ion],
    print ""
    print "atoms"
    print "   ",
    for ion in range(nion):
        print atoms[ion],

#   print ""
#   print "atom_j"
#   for atom in range(natom):
#       print atom,atoms_j[atom]

#   print ""
#   print "atoms_index_j"
#   for atom in range(natom):
#       print atom,atoms_index_j[atom]

