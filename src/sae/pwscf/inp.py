#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#  Method --- ReadVaspPoscar
#  Method --- ReadFdmInp
#  Method --- ReaMxDatMethod -- ReadMxDat
#                            -- ReadMxDftscf
#                            -- ReadMxOut
#                            -- ReadMxPdos
#                            -- ReadMxTdos
#  Method --- ReadRmcpotCfg
#  Method --- ReadPwIn
#
################################################################################
#
# PWScf (Quantum ESPRESSO 5..x )
# scf.in ファイル( pw.x 入力ファイル 読み込み)
#
# 1) pw.x 入力ファイル名の第一候補を scf.in とする
# 2) ibrav = 0 のみ対応 (2015.05.12)
# 3) タグ名と値の間の区切りの = (イコール) には必ずスペースが入る事が前提
#
# 4) CELL_PARAMETERS は {alat} が前提
# 5) ATOMIC_POSITIONS は {crystal} が前提
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.08.24
#  統合化のためのすりあわせ (4)と(5) の注意事項に注意
#
# 2015.08.24
#  統合化の前に、インスタンス重視に切りかえる
#
# 2015.05.12 startup
#
################################################################################
################################################################################
# import gzip
# import SpaceGroupEnvironment as SGE
# sys.path.append('../..')
################################################################################
################################################################################
################################################################################
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.structure.base import Method
import sys
import os
import re
import optparse
import numpy as np

try:
    Method = Method
except ImportError:
    Method = Method


############################################################################
class ReadPwIn(Method):

    # 1bhor = 0.529177249 angstrom
    # 1Rydberg = 13.6056981 eV
    # set default
    ########## END of loop ############################
    ## natom までの通し番号で原子の種類番号を返す
    ## atoms_number
    ## atoms_number_j
    ###############################################
    ## ion[j] : 通し番号(max=natom)を与えると原子の種類番号を返す
    ## ion_local[j]  : 通し番号(max=natom)を与えるとサイト内のローカル通し番号を返す
    ## dummy
    def __init__(self, cname, suffix=".in", sort=False, atoms_index=None):
        from sae.common.text import TextFiles
        from sae.structure.elements import ElementTable

        self.datlines, self.num = TextFiles().read_dataline(cname)
        ibrav_reg = re.compile(".*ibrav.*", re.IGNORECASE)
        lattice_a_reg = re.compile(".* a *=", re.IGNORECASE)
        nion_reg = re.compile(".*ntyp.*", re.IGNORECASE)
        natom_reg = re.compile(".*nat.*", re.IGNORECASE)
        spin_reg = re.compile(".*nspin.*")
        prefix_reg = re.compile(".*prefix.*")
        cell_reg = re.compile(".*CELL_PARAMETERS.*", re.IGNORECASE)
        species_reg = re.compile(".*ATOMIC_SPECIES.*", re.IGNORECASE)
        position_reg = re.compile(".*ATOMIC_POSITIONS.*", re.IGNORECASE)
        self.ispin = 1
        self.prefix = "input"
        self.title = self.prefix
        self.system = self.title
        self.vasp_version = 5
        self.t = np.zeros((3, 3))
        self.atoms_index = []
        self.atoms_index_j = []
        NION_FLAG = False
        NATOM_FLAG = False
        i = 0
        for line in self.datlines:
            if bool(ibrav_reg.match(line)):
                tmp = re.sub(".*ibrav *=", "", line.lower())
                tmp = re.sub(",.*", "", tmp)
                self.ibrav = int(tmp)
                if self.ibrav != 0:
                    sys.exit("STOP: ibrav != 0")
            #               self.scale = float(tmp)*0.529177249
            if bool(lattice_a_reg.match(line)):
                tmp = re.sub(".*a *=", "", line.lower())
                tmp = re.sub(",.*", "", tmp)
                self.scale = float(tmp)
            if bool(natom_reg.match(line)):
                tmp = re.sub(".*nat *=", "", line.lower())
                tmp = re.sub(",.*", "", tmp)
                self.natom = int(tmp)
                if self.natom and (not NATOM_FLAG):
                    NATOM_FLAG = True
                    self.position = np.zeros((self.natom, 3))
            if bool(nion_reg.match(line)):
                tmp = re.sub(".*ntyp *=", "", line.lower())
                tmp = re.sub(",.*", "", tmp)
                self.nion = int(tmp)
                if self.nion and (not NION_FLAG):
                    NION_FLAG = True
                    self.atoms = np.zeros(self.nion, dtype=int)
            if bool(spin_reg.match(line)):
                tmp = re.sub(".*nspin *=", "", line.lower())
                tmp = re.sub(",.*", "", tmp)
                self.ispin = int(tmp)
            if bool(prefix_reg.match(line)):
                tmp = re.sub(".*prefix *=", "", line.lower())
                tmp = re.sub("'", "", tmp)
                tmp = re.sub(",.*", "", tmp)
                self.prefix = str(tmp.strip())
                self.title = self.prefix
                self.system = self.title
            if bool(cell_reg.match(line)):
                t1_x = self.datlines[i + 1].split()[0]
                t1_y = self.datlines[i + 1].split()[1]
                t1_z = self.datlines[i + 1].split()[2]
                t2_x = self.datlines[i + 2].split()[0]
                t2_y = self.datlines[i + 2].split()[1]
                t2_z = self.datlines[i + 2].split()[2]
                t3_x = self.datlines[i + 3].split()[0]
                t3_y = self.datlines[i + 3].split()[1]
                t3_z = self.datlines[i + 3].split()[2]
                self.t[0, 0] = t1_x
                self.t[1, 0] = t1_y
                self.t[2, 0] = t1_z
                self.t[0, 1] = t2_x
                self.t[1, 1] = t2_y
                self.t[2, 1] = t2_z
                self.t[0, 2] = t3_x
                self.t[1, 2] = t3_y
                self.t[2, 2] = t3_z
            if bool(species_reg.match(self.datlines[i])):
                for j in range(self.nion):
                    atom_name = self.datlines[i + j + 1].split()[0]
                    self.atoms_index.append(atom_name)
            if bool(position_reg.match(line)):
                for j in range(self.natom):
                    atom_name = str(self.datlines[i + j + 1].split()[0])
                    self.atoms_index_j.append(atom_name)
                    self.position[j, 0] = self.datlines[i + j + 1].split()[1]
                    self.position[j, 1] = self.datlines[i + j + 1].split()[2]
                    self.position[j, 2] = self.datlines[i + j + 1].split()[3]
                    for k in range(self.nion):
                        if self.atoms_index[k] == atom_name:
                            self.atoms[k] += 1
            i += 1
        self.atoms_j = np.zeros(self.natom, dtype=int)
        j = 0
        for ion in range(self.nion):
            for atom in range(self.atoms[ion]):
                self.atoms_j[j] = int(ion)
                j += 1
        self.atoms_number = np.zeros(self.nion, dtype=int)
        for i in range(self.nion):
            self.atoms_number[i] = ElementTable().get_atomic_number1(
                str(self.atoms_index[i])
            )
        self.atoms_number_j = []
        for k in range(self.nion):
            for l in range(int(self.atoms[k])):
                self.atoms_number_j.append(str(self.atoms_number[k]))
        self.ion = np.zeros(self.natom, dtype=int)
        self.ion_local = np.zeros(self.natom, dtype=int)
        tmp = -1
        for j in range(self.nion):
            local = -1
            for k in range(int(self.atoms[j])):
                tmp += 1
                local += 1
                self.ion[tmp] = int(j)
                self.ion_local[tmp] = int(local)
        self.direct = True
        self.selective = False
        self.fix = [""] * self.natom

    def get_ispin(self):
        return self.ispin

    def get_ibrav(self):
        return self.ibrav
