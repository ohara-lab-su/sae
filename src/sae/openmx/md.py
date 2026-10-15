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
################################################################################
# from numpy import *
# sys.path.append('../..')
# import SpaceGroupEnvironment as SGE
################################################################################
################################################################################
#   MD = "co.md"  # default name
#   MD = "C60_position.xyz"
#   MD = "graphene_N.md"
############################################################################
############################################################################
#   for i in range(nloop):
#       print " ",i," ", energy_loop[i]
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
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import optparse
import os
import gzip
import re
import numpy as np


###############################################
# MD ファイル読み込み
###############################################
# NATOM
###############################################
# LOOP 数 (IONループ数)
# 互換
###############################################
# atoms_index_j
###############################################
# atoms_index(擬似)作成
#    連続して同種の元素記号が並んでいるときは同じion-typeとする
###############################################
# nion(擬似)作成
#    連続して同種の元素記号が並んでいるときは同じion-typeとする
###############################################
# atoms(擬似)作成
#    連続して同種の元素記号が並んでいるときは同じion-typeとする
###############################################
# データー読み込み
###############################################
# position_loop データー読み込み
###############################################
# position (initial) データー読み込み
###############################################
# position_loop データー読み込み
###############################################
# force_loop データー読み込み
###############################################
# OpenMX *.md 形式, MD モード
###############################################
# OpenMX *.md 形式, MD モード
class ReadMd(object):

    def __init__(self, cname):
        if os.path.exists(cname):
            GZIP = False
        elif os.path.exists(cname + ".gz"):
            GZIP = True
        else:
            sys.exit("STOP: " + cname + " or " + cname + ".gz file not found")
        try:
            if GZIP:
                tmp = gzip.open(cname + ".gz")
            else:
                tmp = open(cname)
            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: " + cname + " does'nt open")
        finally:
            tmp.close()
        self.datlines = datfile.split("\n")
        # トータルの行数
        self.num = len(self.datlines) - 1

    def get_natom(self):
        # 総原子数
        self.natom = int(self.datlines[0])
        return self.natom

    def get_nloop(self):
        natom = self.get_natom()
        j = 0
        step = natom + 2
        for i in range(0, self.num, step):
            j += 1
        self.nloop = j
        return self.nloop

    def get_n_ion_loop(self):
        self.nloop = self.get_nloop()
        return self.nloop

    def get_atoms_index_j(self):
        natom = self.get_natom()
        self.atoms_index_j = []
        i = 2
        for j in range(natom):
            self.atoms_index_j.append(str(self.datlines[i + j].split()[0]))
        return self.atoms_index_j

    def get_atoms_index(self):
        natom = self.get_natom()
        atoms_index_j = self.get_atoms_index_j()
        i = 0
        self.atoms_index = []
        for a in range(natom):
            i = i + 2
            atoms_tmp = ""
            # atoms_index_j[j] = str(self.datlines[i].split()[0])
            for j in range(natom):
                if atoms_index_j[j] != atoms_tmp:
                    atoms_tmp = atoms_index_j[j]
                    self.atoms_index.append(atoms_index_j[j])
                i += 1
        return self.atoms_index

    def get_nion(self):
        natom = self.get_natom()
        nloop = self.get_nloop()
        atoms_index_j = self.get_atoms_index_j()
        i = 0
        for l in range(nloop):
            i = i + 2
            atoms_tmp = ""
            self.nion = 0
            for j in range(natom):
                if atoms_index_j[j] != atoms_tmp:
                    self.nion += 1
                    atoms_tmp = atoms_index_j[j]
                i += 1
        return self.nion

    def get_atoms(self):
        nion = self.get_nion()
        nloop = self.get_nloop()
        natom = self.get_natom()
        atoms_index_j = self.get_atoms_index_j()
        i = 0
        self.atoms = np.zeros(nion, dtype=int)
        for l in range(nloop):
            i = i + 2
            atoms_tmp = ""
            nion = 0
            local = 0
            # makes atoms[ion]
            for j in range(natom):
                if atoms_index_j[j] != atoms_tmp:
                    local = 0
                    nion += 1
                    atoms_tmp = atoms_index_j[j]
                if atoms_index_j[j] == atoms_tmp:
                    local += 1
                    self.atoms[nion - 1] = local
                i += 1
        return self.atoms

    def get_energy_loop(self):
        natom = self.get_natom()
        nloop = self.get_nloop()
        i = 0
        self.energy_loop = np.zeros(nloop)
        # get Energy
        # print energy_loop[l]
        for l in range(nloop):
            tmp = self.datlines[i + 1].split()
            if len(tmp) >= 5:
                self.energy_loop[l] = tmp[4]
            i = i + 2
            for j in range(natom):
                i += 1
        return self.energy_loop

    def get_position_loop(self):
        natom = self.get_natom()
        nloop = self.get_nloop()
        i = 0
        self.position_loop = np.zeros((nloop, natom, 3))
        energy_loop = np.zeros(nloop)
        # get Energy
        # print energy_loop[l]
        for l in range(nloop):
            tmp = self.datlines[i + 1].split()
            if len(tmp) >= 5:
                energy_loop[l] = tmp[4]
            i = i + 2
            #               nlist = len(tmp)
            #               if nlist >= 7:
            #                   force_loop[l,j,0]     = float(tmp[4])
            #                   force_loop[l,j,1]     = float(tmp[5])
            #                   force_loop[l,j,2]     = float(tmp[6])
            for j in range(natom):
                self.position_loop[l, j, 0] = float(self.datlines[i].split()[1])
                self.position_loop[l, j, 1] = float(self.datlines[i].split()[2])
                self.position_loop[l, j, 2] = float(self.datlines[i].split()[3])
                i += 1
        return self.position_loop

    def get_position(self, loop=0):
        natom = self.get_natom()
        self.position = np.zeros((natom, 3))
        i = 2
        for j in range(natom):
            self.position[j, 0] = float(self.datlines[i + j].split()[1])
            self.position[j, 1] = float(self.datlines[i + j].split()[2])
            self.position[j, 2] = float(self.datlines[i + j].split()[3])
        return self.position

    def get_selective(self):
        i = 2
        tmp = self.datlines[i].split()
        nlist = len(tmp)
        if nlist >= 7:
            self.selective = True
        else:
            self.selective = False
        return self.selective

    def get_force_loop(self):
        natom = self.get_natom()
        nloop = self.get_nloop()
        i = 0
        self.force_loop = np.zeros((nloop, natom, 3))
        for l in range(nloop):
            i = i + 2
            for j in range(natom):
                tmp = self.datlines[i].split()
                nlist = len(tmp)
                if nlist >= 7:
                    self.force_loop[l, j, 0] = float(tmp[4])
                    self.force_loop[l, j, 1] = float(tmp[5])
                    self.force_loop[l, j, 2] = float(tmp[6])
                i += 1
        return self.force_loop

    def get_temp_loop(self):
        natom = self.get_natom()
        nloop = self.get_nloop()
        temp_text = ".*Temperature="
        temp_reg = re.compile(temp_text)
        given_end = "\\(Given Temp.=.*"
        i = 0
        self.temp_loop = np.zeros(nloop)
        for l in range(nloop):
            i += 1
            if bool(temp_reg.match(self.datlines[i])):
                src = re.sub(temp_text, "", self.datlines[i])
                temp = float(re.sub(given_end, "", src))
                self.temp_loop[l] = temp
            i = i + natom + 1
        return self.temp_loop

    def get_temp_given_loop(self):
        natom = self.get_natom()
        nloop = self.get_nloop()
        given_text = ".*\\(Given Temp.="
        given_reg = re.compile(given_text)
        given_end = "\\)"
        i = 0
        self.temp_given_loop = np.zeros(nloop)
        for l in range(nloop):
            i += 1
            if bool(given_reg.match(self.datlines[i])):
                src = re.sub(given_text, "", self.datlines[i])
                temp = float(re.sub(given_end, "", src))
                self.temp_given_loop[l] = temp
            i = i + natom + 1
        return self.temp_given_loop
