#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OpenMX 3.7 *.dat 形式ファイル 読み込み class
#
#  ReadDatMx
#    *.dat 名の重複があるので DatMx とする( 例 RMC_POT の *.dat 形式 )
#
################################################################################
#
#  get_title()
#  get_ispin()
#  get_natom()
#  get_nion()
#  get_atoms_index()
#  get_atoms()
#  get_scale()
#  get_t()
#  get_selective()
#  get_direct()
#  get_position()
#  get_position_max()
#  get_position_min()
#  get_fix()
#
################################################################################
# RedMxDatMethod.py
#
# 2015.02.25
#   get_atoms_j() 作成 ReadOutcar.get_atoms_j() 相当
#
# 2015.02.24
#   OpenMX の out 形式はその情報を *.dat 読み込みをそのまま貼り付ける形
#   なので、*.out と *.dat で完全に共通の Method を使用することが出来る。
#   そのため Method の共通化がたぶんかなり意味がある。
#
#   Method のスーパークラスを作成
#   ReadMxDat.py ReadMxOut.py から分離
#   method の実装についての changeLog はそちらを参照
#
# -----------------------------------------------------------------------------
# ReadMxDat.py (旧) 2015.02.24
#
#  注意)
#     get_fix() は必ず get_position() の後に実行する
#
# 2015.02.24
#  *.dat / *.out 共通method (主に *.dat 部分) を ReadMxDatMethod.py へ
#  分離し、そちらをスーパークラスとする。class ReadMxDat ではsuperclass
#  を継承してそれら method を実装する形にする。
#
# 2015.02.24
#   spin チェックmethod
#
# 2015.02.17
#  get_position_max(), get_position_min 追加
#   position[atom,3] のそれぞれ x,y,z の最大値を返す
#
# 2015.02.17
#  get_t() を初めいくつかの method で *.dat のコメントアウト処理に正しく
#  対応してなかったため意図しない動作になっていたのを修正
#
# 2015.02.17
#  Al-Si111-ESM.dat が正しく読めないエラー
#  ReadDatMx class, get_t, get_position のバグ(仕様)を修正
#
# 2015.02.17
#  get_fix() も get_position() と同様に atoms_index の順番に合わせる
#
# 2015.02.17
#  get_atom() の新方式に合わせて get_position() の順番もソートしなおして
#  atoms_index に矛盾なく並べ直した情報を返すように変更
#
#  オリジナルの順番とatoms_indexに合わせてソートしなおした配列の対応は
#  get_position() 後の self.position_index にてアクセス可能
#
# 2015.02.16
#  get_atom() の分類方法を変更
#   古: 連続して並んでいる元素記号のみを一つのサイトとしてひとくくりにした
#   新: atoms_index (Atomic.Species タグ) の情報のみでサイトのグルーピング
#
# 2015.02.12 1st
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014,2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"
################################################################################

import sys
#import os
import re
#import gzip
import numpy as np

#import optparse 


################################################################################
class ReadMxDatMethod(object):

    ###################################
    # title (System.Name)
    def get_title(self):
        comment_reg = re.compile('^#.*',re.IGNORECASE)
        title_reg = re.compile('.*System\.Name')
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(title_reg.match(self.datlines[i])):
                    src = self.datlines[i].split()[1]
                    self.SYSTEM = re.sub(' *$','',src) 
                    break
        return self.SYSTEM

    ###################################
    # spin の有無( SpinPolarization on = 2, off = 1 )
    # scf.SpinPolarization        on
    def get_ispin(self):
        comment_reg = re.compile('^#.*',re.IGNORECASE)
        reg_spin =  re.compile('.*scf\.SpinPolarization',re.IGNORECASE)
        reg_switch_off = re.compile('Off',re.IGNORECASE)
        reg_switch_on = re.compile('On',re.IGNORECASE)
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg_spin.match(self.datlines[i])):
                    if bool(reg_switch_off.match(self.datlines[i].split()[1])):
                        self.ispin = 1
                    elif bool(reg_switch_on.match(self.datlines[i].split()[1])):
                        self.ispin = 2
                    else:
                        sys.exit("STOP: unknown SpinPolarization switch")

        return self.ispin

    ###################################
    # natom
    def get_natom(self):
        comment_reg = re.compile('^#.*',re.IGNORECASE)
        reg = re.compile('.*Atoms\.Number')
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg.match(self.datlines[i])):
                    self.natom = int(self.datlines[i].split()[1])
                    break 
        return self.natom


    ###################################
    # NION
    def get_nion(self):
        comment_reg = re.compile('^#.*',re.IGNORECASE)
        reg = re.compile('.*Species\.Number')
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg.match(self.datlines[i])):
                    self.NION = int(self.datlines[i].split()[1])
                    break
        return self.NION


    ###################################
    # atoms_index
    def get_atoms_index(self):
        nion = self.get_nion()

        comment_reg = re.compile('^#.*',re.IGNORECASE)
        reg0 = re.compile('.*\<Definition\.of\.Atomic\.Species')
        reg1 = re.compile('.*Definition\.of\.Atomic\.Species\>')

        self.atoms_index = []
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg0.match(self.datlines[i])):
                    j = 1
                    while not bool(reg1.match(self.datlines[i+j])):
                        self.atoms_index.append(self.datlines[i+j].split()[0])
                        j += 1
                    if nion != j -1 :
                        sys.exit("STOP: Atomic.Species Tag Error")
                    break
        return self.atoms_index


    ###################################
    # atoms (get_atoms version1) 正しく動作します
    #  連続する原子を同種原子と考えて、連続してない同一元素記号の元は
    #  別種類とする考え方での分類。に基づく Method
   #def get_atoms(self):
   #    nion = self.get_nion()
   #    natom = self.get_natom()
   #    reg0 = re.compile('.*\<Atoms\.SpeciesAndCoordinates')
   #    reg1 = re.compile('.*Atoms\.SpeciesAndCoordinates\>')
   #    self.atoms = np.zeros(nion,dtype=int)
   #    for i in range(self.num):
   #        if bool(reg0.match(self.datlines[i])):
   #            j = 1
   #            species0 = ''
   #            types = -1
   #            while not bool(reg1.match(self.datlines[i+j])):
   #                species = self.datlines[i+j].split()[1]
   #                if species != species0:
   #                    types += 1
   #                self.atoms[types] += 1
   #                species0 = species
   #                j += 1
   #            if natom != j -1 :
   #                sys.exit("STOP: Atomic.Number and Atoms.SpeciesAndCoordinates Tag Error")
   #            break
   #    return self.atoms


   ####################################
   ## atoms (get_atoms version2) 正しく動作します
   ##  OpenMX 的には Species.Number で区分される PAO/VPS は同一記号ならば
   ##  かならず同一サイトとして分類してもよい感じなので、そのように分類し直す
   ##  この分類変更にともなって position と fix の行列も整理し直す必要あるので注意
   ##  むしろ、VASP の PP の並び(atoms_index と atoms)を直したほうが早い？
    def get_atoms(self):
        nion = self.get_nion()
        natom = self.get_natom()
        atoms_index = self.get_atoms_index()

        comment_reg = re.compile('^#.*',re.IGNORECASE)
        reg0 = re.compile('.*\<Atoms\.SpeciesAndCoordinates')
        reg1 = re.compile('.*Atoms\.SpeciesAndCoordinates\>')

        self.atoms = np.zeros(nion,dtype=int)
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg0.match(self.datlines[i])):
                    i += 1
                    for j in range(natom):
                        for k in range(nion):
                            if self.datlines[i+j].split()[1] == atoms_index[k]:
                                self.atoms[k] += 1
                    if not bool(reg1.match(self.datlines[i+j+1])):
                        sys.exit("STOP: Atomic.Number and Atoms.SpeciesAndCoordinates Tag Error")

        return self.atoms


    ###################################
    # atoms_j (My配列),natomまでの通し番号で原子の種類を返すMethod
    #    ReadMxDatMethod.get_atoms version2 に対応する get_atoms_j
    #   atoms_index (ReadOutcar.get_atoms_index_j に準じる)
    def get_atoms_j(self):
        nion = self.get_nion()
        natom = self.get_natom()
        atoms = self.get_atoms()
        j = 0
        atoms_j = np.zeros(natom,dtype=int)
        for ion in range(nion):
            for atom in range(atoms[ion]):
                atoms_j[j] = ion
                j += 1

        return atoms_j


    ###################################
    ## scale factor
    def get_scale(self):
        return 1.0


    ###################################
    ## Read Translation Vector                                                  
    ##         x   y   z                                                        
    ##   t1 = t11 t21 t31                                                       
    ##   t2 = t12 t22 t32                                                       
    ##   t3 = t13 t23 t33                                                       
    ##
    ##   Unit を調べて AU のときは Ang にして返す
    ##
    def get_t(self):
        BOHR= 0.529177   # Bohr radius in Angstrom

        comment_reg = re.compile('^#.*',re.IGNORECASE)
        reg_unit0 = re.compile('AU',re.IGNORECASE)
        reg_unit1 = re.compile('Ang',re.IGNORECASE)
        reg2 = re.compile('.*Atoms\.UnitVectors\.Unit')
        reg3 = re.compile('.*\<Atoms\.UnitVectors')
        reg4 = re.compile('.*Atoms\.UnitVectors\>')

        # get UNIT
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg2.match(self.datlines[i])):
                    if bool(reg_unit0.match(self.datlines[i].split()[1])):
                       #FLAG_UNIT = True   # 'Atomic Unit'
                       UNIT = BOHR
                    elif bool(reg_unit1.match(self.datlines[i].split()[1])):
                       #FLAG_UNIT = False  # 'Ang'
                       UNIT = 1.0
                    else:
                        sys.exit("STOP: Unknown Atoms.UnitVectors.Unit")
                    break

        # get translation vector
        self.t = np.zeros((3,3))
        self.FLAG_t = False
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg3.match(self.datlines[i])):
                    self.FLAG_t = True

                    self.t[0,0] = float(self.datlines[i+1+0].split()[0])*UNIT
                    self.t[1,0] = float(self.datlines[i+1+0].split()[1])*UNIT
                    self.t[2,0] = float(self.datlines[i+1+0].split()[2])*UNIT

                    self.t[0,1] = float(self.datlines[i+1+1].split()[0])*UNIT
                    self.t[1,1] = float(self.datlines[i+1+1].split()[1])*UNIT
                    self.t[2,1] = float(self.datlines[i+1+1].split()[2])*UNIT

                    self.t[0,2] = float(self.datlines[i+1+2].split()[0])*UNIT
                    self.t[1,2] = float(self.datlines[i+1+2].split()[1])*UNIT
                    self.t[2,2] = float(self.datlines[i+1+2].split()[2])*UNIT

                    if not bool(reg4.match(self.datlines[i+1+3])):
                        sys.exit("STOP: Atoms.UnitVectors Error")
                    break

        return self.t


    ###################################
    ## selective モードの取得
    def get_selective(self):
        comment_reg = re.compile('^#.*',re.IGNORECASE)
        reg_md0 = re.compile('.*\<MD\.Fixed\.XYZ')

        self.selective =False
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg_md0.match(self.datlines[i])):
                    self.selective=True
                    break

        return self.selective


    ###################################
    # 内部座標のDirect Mode の取得
    def get_direct(self):

        comment_reg = re.compile('^#.*',re.IGNORECASE)
        reg_unit0 = re.compile('AU',re.IGNORECASE)
        reg_unit1 = re.compile('Ang',re.IGNORECASE)
        reg_unit2 = re.compile('FRAC',re.IGNORECASE)
        reg3 = re.compile('.*Atoms\.SpeciesAndCoordinates\.Unit')

        # get UNIT
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg3.match(self.datlines[i])):
                    if bool(reg_unit0.match(self.datlines[i].split()[1])):
                       direct = False
                    elif bool(reg_unit1.match(self.datlines[i].split()[1])):
                       direct = False
                    elif bool(reg_unit2.match(self.datlines[i].split()[1])):
                       direct = True
                    else:
                        sys.exit("STOP: Unknown Atoms.SpeciesAndCoordinates.Unit")
                    break

        return direct


    ###################################
    ##  position (正しく動作する)
    ##    内部座標の順番を表記された順番でそのまま取得する
    ##
    ##    内部座標の取得 AU --> Ang 変換だけはここでやる
    ##    (カーテシアンとダイレクトの変換はここでは行わない)
    ##    並んでいる順番通りに並べる
    ##
   #def get_position(self):
   #    BOHR= 0.529177   # Bohr radius in Angstrom

   #    comment_reg = re.compile('^#.*',re.IGNORECASE)
   #    reg_unit0 = re.compile('AU',re.IGNORECASE)
   #    reg_unit1 = re.compile('Ang',re.IGNORECASE)
   #    reg_unit2 = re.compile('FRAC',re.IGNORECASE)
   #    reg_position0 = re.compile('.*Atoms\.SpeciesAndCoordinates\.Unit')
   #    reg_position1 = re.compile('.*\<Atoms\.SpeciesAndCoordinates ')
   #    reg_position2 = re.compile('.*Atoms\.SpeciesAndCoordinates\>')

   #    natom = self.get_natom()

   #    # get UNIT
   #    for i in range(self.num):
   #        if bool(reg_position0.match(self.datlines[i])):
   #            if bool(reg_unit0.match(self.datlines[i].split()[1])):
   #              #direct = False
   #               UNIT = BOHR        # 'Atomic Unit'
   #            elif bool(reg_unit1.match(self.datlines[i].split()[1])):
   #              #direct = False
   #               UNIT = 1.0 # 'Ang'
   #            elif bool(reg_unit2.match(self.datlines[i].split()[1])):
   #              #direct = True
   #               UNIT = 1.0
   #            else:
   #                sys.exit("STOP: Unknown Atoms.SpeciesAndCoordinates.Unit")
   #            break

   #    self.p = np.zeros((natom,3))
   #    for i in range(self.num):
   #        if not bool(comment_reg.match(self.datlines[i])):
   #            if bool(reg_position1.match(self.datlines[i])):
   #                j = 1
   #                while not bool(reg_position2.match(self.datlines[i+j])):
   #                    self.p[j-1,0] = float(self.datlines[i+j].split()[2])*UNIT
   #                    self.p[j-1,1] = float(self.datlines[i+j].split()[3])*UNIT
   #                    self.p[j-1,2] = float(self.datlines[i+j].split()[4])*UNIT
   #                    j += 1
   #                if natom != j -1 :
   #                    sys.exit("STOP: Atomic.Number and Atoms.SpeciesAndCoordinates Tag Error")

   #    return self.p


    ###################################
    ##  position (正しく動作する)
    ##    内部座標の順番を atoms_index (および atoms) と同じくするために
    ##    元素記号ごと(atom_indexの順番で)ソートする
    ##
    ##    内部座標の取得 AU --> Ang 変換だけはここでやる
    ##    (カーテシアンとダイレクトの変換はここでは行わない)
    ##    並んでいる順番通りに並べる
    ##
    def get_position(self):
        BOHR= 0.529177   # Bohr radius in Angstrom

        comment_reg = re.compile('^#.*',re.IGNORECASE)
        reg_unit0 = re.compile('AU',re.IGNORECASE)
        reg_unit1 = re.compile('Ang',re.IGNORECASE)
        reg_unit2 = re.compile('FRAC',re.IGNORECASE)
        reg_position0 = re.compile('.*Atoms\.SpeciesAndCoordinates\.Unit')
        reg_position1 = re.compile('.*\<Atoms\.SpeciesAndCoordinates')
       #reg_position2 = re.compile('.*Atoms\.SpeciesAndCoordinates\>')

        natom = self.get_natom()
        nion = self.get_nion()
        atoms_index = self.get_atoms_index()

        # get UNIT
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg_position0.match(self.datlines[i])):
                    if bool(reg_unit0.match(self.datlines[i].split()[1])):
                      #direct = False
                       UNIT = BOHR        # 'Atomic Unit'
                    elif bool(reg_unit1.match(self.datlines[i].split()[1])):
                      #direct = False
                       UNIT = 1.0 # 'Ang'
                    elif bool(reg_unit2.match(self.datlines[i].split()[1])):
                      #direct = True
                       UNIT = 1.0
                    else:
                        sys.exit("STOP: Unknown Atoms.SpeciesAndCoordinates.Unit")
                    break

        self.position = np.zeros((natom,3))
        self.position_index = np.zeros(natom,dtype=int)   # sort_index --> original_index
        self.position_index_r = np.zeros(natom,dtype=int) # original_index --> sort_index
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg_position1.match(self.datlines[i])):
                    l = 0 # sort_index
                    for k in range(nion):
                        for j in range(1,natom+1): # original_index
                            if atoms_index[k] == self.datlines[i+j].split()[1]:
                                self.position_index[l] = \
                                      int(self.datlines[i+j].split()[0]) -1
                                self.position_index_r[j-1] = l
                                self.position[l,0] = \
                                      float(self.datlines[i+j].split()[2])*UNIT
                                self.position[l,1] = \
                                      float(self.datlines[i+j].split()[3])*UNIT
                                self.position[l,2] = \
                                      float(self.datlines[i+j].split()[4])*UNIT
                                l += 1
                    break
        return self.position


    ###################################
    ## position の(x,y,z) 毎の最大を返す
    ##
    def get_position_max(self):
        position = self.get_position()

        self.position_max_xyz = np.zeros((3))
        for xyz in range(0,3):
            self.position_max_xyz[xyz] = max(position[:,xyz])

        return self.position_max_xyz


    ###################################
    ## position の(x,y,z) 毎の最小値を返す
    ##
    def get_position_min(self):
        position = self.get_position()

        self.position_min_xyz = np.zeros((3))
        for xyz in range(0,3):
            self.position_min_xyz[xyz] = min(position[:,xyz])

        return self.position_min_xyz


    ###################################
    ## fixed
    ##  fix の情報は VASP 相当に変更する(F=Fix, T=moving True)
    ##  position の取得と別のmethodにする
    ##
    ##  内部座標を atoms_index と合わせるためにソートする
    ##
    ##  注意)
    ##  ソート用のindexは get_position() で生成される self.position_index
    ##  が必要。get_fix 中では get_position() は読まずに self.get_position()
    ##  実行後に get_fix が実行されると仮定して self.position_index および
    ##  self.position_index_r を用いる
    ##
    def get_fix(self):
        natom = self.get_natom()
        selective = self.get_selective()
       #self.fix = []
        self.fix = np.zeros((natom,3),dtype='S')
        if selective:
            comment_reg = re.compile('^#.*',re.IGNORECASE)
            reg_md0 = re.compile('.*\<MD\.Fixed\.XYZ')
            reg_md1 = re.compile('.*MD\.Fixed\.XYZ\>')

            self.selective =False
            for i in range(self.num):
                if not bool(comment_reg.match(self.datlines[i])):
                    if bool(reg_md0.match(self.datlines[i])):
                        self.selective=True
                        j = 1
                        while not bool(reg_md1.match(self.datlines[i+j])):
                            fix_x = int(self.datlines[i+j].split()[1])
                            fix_y = int(self.datlines[i+j].split()[2])
                            fix_z = int(self.datlines[i+j].split()[3])

                            if fix_x == 1:
                                fix_x = 'F'  # Moving False ( Fixed )
                            elif fix_x == 0:
                                fix_x = 'T'  # Moving True  ( non Fixed )
                            else:
                                sys.exit("STOP: unknown Fixed Parameter")

                            if fix_y == 1:
                                fix_y = 'F'  # Moving False ( Fixed )
                            elif fix_y == 0:
                                fix_y = 'T'  # Moving True  ( non Fixed )
                            else:
                                sys.exit("STOP: unknown Fixed Parameter")

                            if fix_z == 1:
                                fix_z = 'F'  # Moving False ( Fixed )
                            elif fix_z == 0:
                                fix_z = 'T'  # Moving True  ( non Fixed )
                            else:
                                sys.exit("STOP: unknown Fixed Parameter")

                           #self.fix.append([fix_x, fix_y, fix_z])

                           ### original の index で fix を作るのではなく
                           ### atoms_index の並びで sort した index で fix を作る
                           #self.fix[j-1,0] = fix_x
                           #self.fix[j-1,1] = fix_y
                           #self.fix[j-1,2] = fix_z
                            self.fix[self.position_index_r[j-1],0] = fix_x
                            self.fix[self.position_index_r[j-1],1] = fix_y
                            self.fix[self.position_index_r[j-1],2] = fix_z
                           #########################
                            j += 1
                        if natom != j -1 :
                            sys.exit("STOP: Atomic.Number and Atoms.SpeciesAndCoordinates Tag Error")
                        break
        return self.fix

################################################################################

