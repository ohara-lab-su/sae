#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#  MD(xyz) 形式の読み込み class
#
#   read_md.py
#     def read_md3(): 座標(x,y,z) + フォース(x,y,z) + Energy 形式に対応
#   をベースとして作成
#
#   エネルギーの取得に関しては OpenMX の *.md 形式が念頭
#   ただし、それ以外は基本的には *.xyz (*.md) 形式に準じているので、
#   ReadMd.py の名前のままにしておく ( ゆえに ReadMxMd.py とはしない)
#
################################################################################
#
# get_natom()
# get_nloop()
# get_n_ion_loop()
# get_atoms_index_j()
# get_atoms_index()
# get_nion()
# get_atoms()
# get_energy_loop()
# get_position_loop()
# get_selective()
# get_force_loop()
#
# get_temp_loop()
# get_temp_given_loop()
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.06.30
#   == None --> is None
#
# 2015.06.26
#  get_position() 追加: get_position_loop の loop=0 のみ対応
#
# 2015.03.03
#  get_temp(), get_temp_given()
#
#     OpenMX *.md 形式: Temperature, Given Temp 吸い出し対応
#
# 2015.02.13 1st
#
################################################################################
from __future__ import print_function
###############################################################################
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
import os
import gzip
import re
#from numpy import *
import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
class ReadMd(object):

    ###############################################
    # MD ファイル読み込み
    def __init__(self,cname):

        if os.path.exists(cname):
            GZIP=False
        elif os.path.exists(cname+".gz"):
            GZIP=True
        else:
            sys.exit("STOP: "+cname+" or "+cname+".gz file not found")

        try:
            if GZIP:
                tmp = gzip.open(cname+".gz")
            else:
                tmp = open(cname)
            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: "+cname+" does'nt open")
        finally:
            tmp.close()

        self.datlines = datfile.split('\n')
        self.num =len(self.datlines)-1   # トータルの行数

    ###############################################
    # NATOM
    def get_natom(self):
        self.natom=int(self.datlines[0])  # 総原子数
        return self.natom

    ###############################################
    # LOOP 数 (IONループ数)
    def get_nloop(self):
        natom = self.get_natom()
        j = 0
        step = natom+2
        for i in range(0,self.num,step):
            j += 1
        self.nloop = j

        return self.nloop

    # 互換
    def get_n_ion_loop(self):
        self.nloop = self.get_nloop()
        return self.nloop

    ###############################################
    # atoms_index_j
    def get_atoms_index_j(self):
        natom = self.get_natom()

        self.atoms_index_j = []
        i = 2
        for j in range(natom):
            self.atoms_index_j.append(str(self.datlines[i+j].split()[0]))

        return self.atoms_index_j

    ###############################################
    # atoms_index(擬似)作成
    #    連続して同種の元素記号が並んでいるときは同じion-typeとする
    def get_atoms_index(self):
        natom = self.get_natom()
        atoms_index_j = self.get_atoms_index_j()

        i=0
        self.atoms_index = []
        for a in range(natom):

            i = i+2
            atoms_tmp = ''
            for j in range(natom):
               #atoms_index_j[j] = str(self.datlines[i].split()[0])
                if atoms_index_j[j] != atoms_tmp:
                    atoms_tmp = atoms_index_j[j]
                    self.atoms_index.append(atoms_index_j[j])
                i += 1

        return self.atoms_index

    ###############################################
    # nion(擬似)作成
    #    連続して同種の元素記号が並んでいるときは同じion-typeとする
    def get_nion(self):
        natom = self.get_natom()
        nloop = self.get_nloop()
        atoms_index_j = self.get_atoms_index_j()

        i=0
        for l in range(nloop):

            i = i+2
            atoms_tmp = ''
            self.nion = 0
            for j in range(natom):
                if atoms_index_j[j] != atoms_tmp:
                    self.nion += 1
                    atoms_tmp = atoms_index_j[j]
                i += 1

        return self.nion

    ###############################################
    # atoms(擬似)作成
    #    連続して同種の元素記号が並んでいるときは同じion-typeとする
    def get_atoms(self):
        nion = self.get_nion()
        nloop = self.get_nloop()
        natom = self.get_natom()
        atoms_index_j = self.get_atoms_index_j()

        i=0
        self.atoms = np.zeros(nion,dtype=int)
        for l in range(nloop):

            i = i+2
            atoms_tmp = ''
            nion = 0
            local =0
            for j in range(natom):

                # makes atoms[ion]
                if atoms_index_j[j] != atoms_tmp:
                    local =0
                    nion += 1
                    atoms_tmp = atoms_index_j[j]
                if atoms_index_j[j] == atoms_tmp:
                    local += 1
                    self.atoms[nion-1] = local
                i += 1

        return self.atoms

    ###############################################
    # データー読み込み
    def get_energy_loop(self):
        natom = self.get_natom()
        nloop = self.get_nloop()

        i=0
        self.energy_loop = np.zeros(nloop)
        for l in range(nloop):

            # get Energy
            tmp = self.datlines[i+1].split()
            if len(tmp) >= 5:
                self.energy_loop[l] =tmp[4]
               #print energy_loop[l]

            i = i+2
            for j in range(natom):
                i += 1

        return self.energy_loop

    ###############################################
    # position_loop データー読み込み
    def get_position_loop(self):
        natom = self.get_natom()
        nloop = self.get_nloop()

        i=0
        self.position_loop = np.zeros((nloop,natom,3))
        energy_loop = np.zeros(nloop)

        for l in range(nloop):

            # get Energy
            tmp = self.datlines[i+1].split()
            if len(tmp) >= 5:
                energy_loop[l] =tmp[4]
               #print energy_loop[l]

            i = i+2

            for j in range(natom):

                self.position_loop[l,j,0]  = float(self.datlines[i].split()[1])
                self.position_loop[l,j,1]  = float(self.datlines[i].split()[2])
                self.position_loop[l,j,2]  = float(self.datlines[i].split()[3])

#               nlist = len(tmp)
#               if nlist >= 7:
#                   force_loop[l,j,0]     = float(tmp[4])
#                   force_loop[l,j,1]     = float(tmp[5])
#                   force_loop[l,j,2]     = float(tmp[6])
                i += 1

        return self.position_loop

    ###############################################
    # position (initial) データー読み込み
    def get_position(self,loop=0):

        natom = self.get_natom()
        self.position = np.zeros((natom,3))

        i = 2
        for j in range(natom):
            self.position[j,0]  = float(self.datlines[i+j].split()[1])
            self.position[j,1]  = float(self.datlines[i+j].split()[2])
            self.position[j,2]  = float(self.datlines[i+j].split()[3])

        return self.position


    ###############################################
    # position_loop データー読み込み
    def get_selective(self):

        i = 2
        tmp = self.datlines[i].split()
        nlist = len(tmp)
        if nlist >= 7:
            self.selective = True
        else:
            self.selective = False

        return self.selective

    ###############################################
    # force_loop データー読み込み
    def get_force_loop(self):
        natom = self.get_natom()
        nloop = self.get_nloop()

        i=0
        self.force_loop = np.zeros((nloop,natom,3))
        for l in range(nloop):

            i = i+2
            for j in range(natom):

                tmp = self.datlines[i].split()
                nlist = len(tmp)
                if nlist >= 7:
                    self.force_loop[l,j,0]     = float(tmp[4])
                    self.force_loop[l,j,1]     = float(tmp[5])
                    self.force_loop[l,j,2]     = float(tmp[6])
                i += 1

        return self.force_loop


    ###############################################
    # OpenMX *.md 形式, MD モード
    def get_temp_loop(self):
        natom = self.get_natom()
        nloop = self.get_nloop()

        temp_text = '.*Temperature='
        temp_reg = re.compile(temp_text)
        given_end = '\(Given Temp.=.*'

        i=0
        self.temp_loop = np.zeros((nloop))
        for l in range(nloop):
            i += 1
            if bool(temp_reg.match(self.datlines[i])):
                src = re.sub(temp_text,'',self.datlines[i])
                temp = float(re.sub(given_end,'',src))
                self.temp_loop[l] = temp
            i = i + natom + 1

        return self.temp_loop

    ###############################################
    # OpenMX *.md 形式, MD モード
    def get_temp_given_loop(self):
        natom = self.get_natom()
        nloop = self.get_nloop()

        given_text = '.*\(Given Temp.='
        given_reg = re.compile(given_text)
        given_end = '\)'

        i=0
        self.temp_given_loop = np.zeros((nloop))
        for l in range(nloop):
            i += 1
            if bool(given_reg.match(self.datlines[i])):
                src = re.sub(given_text,'',self.datlines[i])
                temp = float(re.sub(given_end,'',src))
                self.temp_given_loop[l] = temp
            i = i + natom + 1

        return self.temp_given_loop


################################################################################
if __name__ == '__main__':

#   MD = "co.md"  # default name
#   MD = "C60_position.xyz"
#   MD = "graphene_N.md"
    MD = "gly_VS.md"

    MD0 = "gly_VS"
    suffix = "md"

    MD = MD0+'.'+suffix

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT',)
    options,  args = parser.parse_args()

    if options.INPUT: MD=options.INPUT
    if len(args) > 0: MD=args[0]

    if not os.path.exists(MD):
        MD0 = SAE.find_datfile('md')
        suffix ='md'
        if MD0 is None:
            MD0 = SAE.find_datfile('xyz')
            suffix ='xyz'
            if MD0 is None:
                sys.exit("STOP: INPUT file not found.")

        if not os.path.exists(MD0+'.md'):
            MD0 = SAE.find_datfile('xyz')
            suffix ='xyz'
            if not os.path.exists(MD0+'.xyz'):
                sys.exit("STOP")

    MD = MD0+'.'+suffix

    ############################################################################
    md = ReadMd(MD)
    natom = md.get_natom()
    nion  = md.get_nion()
    nloop = md.get_nloop()
    atoms_index_j = md.get_atoms_index_j()
    atoms_index = md.get_atoms_index()
    atoms = md.get_atoms()
    energy_loop = md.get_energy_loop()
    position_loop = md.get_position_loop()
    selective = md.get_selective()
    force_loop = md.get_force_loop()

    temp_loop = md.get_temp_loop()
    temp_given_loop = md.get_temp_given_loop()
    ############################################################################

    print("NATOM = %s" % str(natom))
    print("NION  = %s" % str(nion))
    print("NLOOP = %s" % str(nloop))
    for i in range(natom):
        print(" %s" % str(atoms_index_j[i]))

    print("")
    print("", end="")
    for i in range(nion):
        print("%s" % str(atoms_index[i]), end="")
    print("")
    print("", end="")
    for i in range(nion):
        print(atoms[i], end="")
    print("")

    print("")
#   for i in range(nloop):
#       print " ",i," ", energy_loop[i]

    print("selective %s" % str(selective))
    print("")
#   for l in range(nloop):
#       print "===============loop===============",l
#       for j in range(natom):
#           print atoms_index_j[j],\
#                   position_loop[l,j,0],\
#                   position_loop[l,j,1],\
#                   position_loop[l,j,2],
#           if selective:
#                   print force_loop[l,j,0],\
#                         force_loop[l,j,1],\
#                         force_loop[l,j,2],
#           print ""

#   for l in range(nloop):
#       print temp_loop[l]

