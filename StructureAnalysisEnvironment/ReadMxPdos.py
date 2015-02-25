#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OpenMX 3.7
#   ReadMxPdos.py 目盛バカ食いバージョン(動作は割と速いはず)
#  
#    *.Dos.Tetrahedron.atom*
#    ReadMxDosMethod.py (superclass)
#                                 ---> ReadMxTdos.py
#                                 ---> ReadMxPdos.py
#  
################################################################################
#
# 2015.02.25
#  get_ldos_ion()
#  get_ldos_ion_all()
#  実装初め (MXplot_ADOS.py 用)
#
# 2015.02.25
#  ReadMxDosMethod から継承している Method において
#  入力のデーターファイルの都合 self.datlines を取るインスタンス変数は
#  ReadMxPdos ではうまく使えない
#     ---> ReadMxPdos 内で self.datlines をうまく定義できないので
#          本質的には無理、無理やり何処かの原子のPDOSファイルを置くことは
#          出来るが誤解が生じる可能性がある。
#
#  とりあえず現状では
#  get_emax()
#  get_emin()
#  get_eng()
#  get_tdos()
#  get_inttdos()
#
#  method は ReadMxPdos 内でオーバーライトしておく
#   ---> ReadMxTdos を呼び出して使う形
#
# 2015.02.25
#  ReadDoscar.py とほぼ同等の動作をする Method をほぼ実装
#
# 2015.02.25
#  共通する Class を ReadMxDosMethod に superclass として放り投げ
#  現存する ReadMxDos クラスは ReadMxTdos に変更し、同様に ReadMxPdos 作成
#
#  基本方針でコンストラクタで全てデーター読み込みなので、動作は割と速いはず
#  目盛はバカバカ食う。
#
#
# ------------------------- ReadMxDosMethod 分離前
# 2015.02.25
#  OpenMX 用の DOS/PDOS 用の superclass に作成した method を分離、継承化
#
# 2015.02.25
#  get_tdos, get_inttdos, get_ispin, get_natom, get_titile  の実装等
#
# 2015.02.24
#    startup
#    主に ReadMxDat, ReadMxDatMethod の整備
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
__version__    = "0.1.4"
################################################################################

import sys
import os
#import gzip
import re
import glob
import optparse
import numpy as np

#from copy import deepcopy

import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE  


################################################################################
class ReadMxPdos(SAE.ReadMxDosMethod):

    ###################################
    # 0) コンストラクタで複数ファイルからまるごとデータ構造を配列に読み込む)
    # 1) 計算していない原子も含めてすべての原子の配列を用意
    # 2) LDOS までコンストラクタで作ってしまう
    #
    def __init__(self,name,suffix):

        # 読み込みファイル名の物質名部分
        self.name = name

        # NSPIN & NATOM を *.out もしくは *.dat から抽出
        NSPIN = self.get_ispin()
        NATOM = self.get_natom()

        # 読み込むPDOSファイルの確認(1)
        # 実際にPDOSを計算したatomの番号を抽出する
        dosname = name+suffix
        pdos_list = glob.glob(dosname+'.atom*')
        if len(pdos_list) < 1:
            sys.exit("STOP: "+dosname+".atom* file not found")

        # NEDOS の算出
        NEDOS = sum(1 for line in open(pdos_list[0]))

        # インスタンス変数化
        self.NATOM = NATOM
        self.NSPIN = NSPIN
        self.num = NEDOS

        ls = []
        for i in range(len(pdos_list)):
            pdos_name = pdos_list[i]
            subtract_name0 = dosname+'.atom'
            subtract_name1 = '\..*'
            dst = re.sub(subtract_name0,'',pdos_name)
            dst = int(re.sub(subtract_name1,'',dst))
            ls.append(dst)

        # リストの重複項目を削除
        atom_list = sorted(set(ls), key=ls.index)
        if atom_list < 1:
            sys.exit("STOP: Contradiction Number of atoms")

        ###################################
        # ADOS 収納に使う配列
        # *.PDOS.Tetrahedron.atom? ファイルからのデータ抽出
        self.ados = np.zeros((NEDOS,NATOM,NSPIN))
        self.intados = np.zeros((NEDOS,NATOM,NSPIN))
        for atom in atom_list:
            data,nline = SAE.read_dataline(dosname+'.atom'+str(atom))
            if nline != NEDOS:
                sys.exit("STOP: Contradiction Number of Data Line")
            for ispin in range(NSPIN):
                for j in range(nline):
                    self.ados[i,atom-1,ispin] = float(data[i].split()[1+ispin])
                    self.intados[i,atom-1,ispin] = float(data[i].split()[2+ispin])

        ###################################
        # TDOS_spd 収納に使う配列(原子種ごとの情報を潰すのであまり意味は無い)
        l_max = 4 #s,p,d,f
        self.tdos_spd = np.zeros((NEDOS,l_max,NSPIN))
        self.inttdos_spd = np.zeros((NEDOS,l_max,NSPIN))

        ###################################
        # LDOS 収納に使う配列(原子種ごと)
        l_max = 4 #s,p,d,f
        self.ldos = np.zeros((NEDOS,l_max,NATOM,NSPIN))
        self.intldos = np.zeros((NEDOS,l_max,NATOM,NSPIN))

        ###################################
        # PDOS 収納に使う配列(原子種,軌道ごと)
        # *.PDOS.Tetrahedron.atom?.* ファイルの検索,suffix抽出
        lm_max = 1+3+5+7 # s+p+d+f
        self.pdos = np.zeros((NEDOS,lm_max,NATOM,NSPIN))
        self.intpdos = np.zeros((NEDOS,lm_max,NATOM,NSPIN))
        self.eng  = np.zeros((NEDOS,NATOM))

        # 原子種のループ
        for atom in atom_list:
            base = dosname+'.atom'+str(atom)

            # s-orbital (1)
            orbit='s'
            orbit_list = glob.glob(base+'.'+orbit+'*')
            if len(orbit_list) > 0:
                for i in range(len(orbit_list)):
                    data,nline = SAE.read_dataline(orbit_list[i])
                    if nline != NEDOS:
                        sys.exit("STOP: Contradiction Number of Data Line")
                    for ispin in range(NSPIN):
                        for j in range(nline):
                            self.eng[j] = float(data[j].split()[0])

                            self.pdos[j,0,atom-1,ispin] =\
                                    float(data[j].split()[1+ispin])
                            self.intpdos[j,0,atom-1,ispin] =\
                                    float(data[j].split()[2+ispin])

                            self.ldos[j,0,atom-1,ispin] = \
                                    self.ldos[j,0,atom-1,ispin] +\
                                    float(data[j].split()[1+ispin])
                            self.intpdos[j,0,atom-1,ispin] = \
                                    self.intpdos[j,0,atom-1,ispin] +\
                                    float(data[j].split()[2+ispin])

                            self.tdos_spd[j,0,ispin] = \
                                    self.tdos_spd[j,0,ispin] +\
                                    float(data[j].split()[1+ispin])
                            self.inttdos_spd[j,0,ispin] = \
                                    self.inttdos_spd[j,0,ispin] +\
                                    float(data[j].split()[2+ispin])
    
            # p-orbital (3)
            orbit='p'
            orbit_list = glob.glob(base+'.'+orbit+'*')
            if len(orbit_list) > 0:
                for i in range(len(orbit_list)):
                    data,nline = SAE.read_dataline(orbit_list[i])
                    if nline != NEDOS:
                        sys.exit("STOP: Contradiction Number of Data Line")
                    for ispin in range(NSPIN):
                        for j in range(nline):
                            self.eng[j] = float(data[j].split()[0])

                            self.pdos[j,1+i,atom-1,ispin] =\
                                    float(data[j].split()[1+ispin])
                            self.intpdos[j,1+i,atom-1,ispin] =\
                                    float(data[j].split()[2+ispin])

                            self.ldos[j,1,atom-1,ispin] = \
                                    self.ldos[j,1,atom-1,ispin] +\
                                    float(data[j].split()[1+ispin])
                            self.intldos[j,1,atom-1,ispin] = \
                                    self.intldos[j,1,atom-1,ispin] +\
                                    float(data[j].split()[2+ispin])

                            self.tdos_spd[j,1,ispin] = \
                                    self.tdos_spd[j,1,ispin] +\
                                    float(data[j].split()[1+ispin])
                            self.inttdos_spd[j,1,ispin] =\
                                    self.inttdos_spd[j,1,ispin] +\
                                    float(data[j].split()[2+ispin])

            # d-orbital (5)
            orbit='d'
            orbit_list = glob.glob(base+'.'+orbit+'*')
            if len(orbit_list) > 0:
                for i in range(len(orbit_list)):
                    data,nline = SAE.read_dataline(orbit_list[i])
                    if nline != NEDOS:
                        sys.exit("STOP: Contradiction Number of Data Line")
                    for ispin in range(NSPIN):
                        for j in range(nline):
                            self.eng[i] = float(data[j].split()[0])

                            self.pdos[j,4+i,atom-1,ispin] =\
                                    float(data[j].split()[1+ispin])
                            self.intpdos[j,4+i,atom-1,ispin] =\
                                    float(data[j].split()[2+ispin])

                            self.ldos[j,2,atom-1,ispin] = \
                                    self.ldos[j,2,atom-1,ispin] +\
                                    float(data[j].split()[1+ispin])
                            self.intldos[j,2,atom-1,ispin] = \
                                    self.intldos[j,2,atom-1,ispin] +\
                                    float(data[j].split()[2+ispin])

                            self.tdos_spd[j,2,ispin] = \
                                    self.tdos_spd[j,2,ispin] +\
                                    float(data[j].split()[1+ispin])
                            self.inttdos_spd[j,2,ispin] = \
                                    self.inttdos_spd[j,2,ispin] +\
                                    float(data[j].split()[2+ispin])

            # f-orbital (7)
            orbit='f'
            orbit_list = glob.glob(base+'.'+orbit+'*')
            if len(orbit_list) > 0:
                for i in range(len(orbit_list)):
                    data,nline = SAE.read_dataline(orbit_list[i])
                    if nline != NEDOS:
                        sys.exit("STOP: Contradiction Number of Data Line")
                    for ispin in range(NSPIN):
                        for j in range(nline):
                            self.eng[i] = float(data[j].split()[0])

                            self.pdos[i,9+i,atom-1,ispin] =\
                                    float(data[j].split()[1+ispin])
                            self.intpdos[i,9+i,atom-1,ispin] =\
                                    float(data[j].split()[2+ispin])

                            self.ldos[j,3,atom-1,ispin] = \
                                    self.ldos[j,3,atom-1,ispin] +\
                                    float(data[j].split()[1+ispin])
                            self.intldos[j,3,atom-1,ispin] = \
                                    self.intldos[j,3,atom-1,ispin] +\
                                    float(data[j].split()[2+ispin])

                            self.tdos_spd[j,3,ispin] = \
                                    self.tdos_spd[j,3,ispin] +\
                                    float(data[j].split()[1+ispin])
                            self.inttdos_spd[j,3,ispin] =\
                                    self.inttdos_spd[j,3,ispin] +\
                                    float(data[j].split()[2+ispin])

    ###################################
    # PDOS (lm,atom,spin 指定)
    def get_pdos(self,lm=0,atom=0,spin=0):
        self.pdos0 = self.pdos[:,lm,atom,spin]
        return self.pdos0

    ###################################
    # PDOS を全部そのまま返す
    def get_pdos_all(self):
        return self.pdos

    ###################################
    # LDOS (l,atom,spin 指定)
    def get_ldos(self,l=0,atom=0,spin=0):
        self.ldos0 = self.ldos[:,l,atom,spin]
        return self.ldos0

    ###################################
    # LDOS を全部そのまま返す
    def get_ldos_all(self):
        return self.ldos

    ###################################
    # (TDOS_SPD) PDOS の spd 合計(原子情報でsum)
    def get_tdos_spd(self,l=0,spin=0):
        self.tdos_spd0 = self.tdos_spd[:,l,spin]
        return self.tdos_spd0

    ###################################
    # LDOS_ion (サイトごとのLDOSを取る), ReadDoscar.get_ldos_ion() 互換
    # *.out or *.dat から atom の ion 情報を読み取るのは必須
    def get_ldos_ion(self,l=0,ion=0,spin=0):

        module_name = 'StructureAnalysisEnvironment'
        if os.path.exists(self.name+'.out') or os.path.exists(self.name+'.out'+'.gz'):
            class_name = 'ReadMxOut'
            datname = self.name+'.out'
        elif os.path.exists(self.name+'.dat') or os.path.exists(self.name+'.dat'+'.gz'):
            class_name = 'ReadMxDat'
            datname = self.name+'.dat'
        else:
            sys.exit("STOP: "+self.name+".out or "+self.name+".dat file not found")

        module = __import__(module_name,globals(),locals(),[class_name],-1)
        klass = getattr(module,class_name)
        dat = klass(datname)

        NEDOS = self.num
        NATOM = self.NATOM
        NSPIN = self.NSPIN
        NION = dat.get_nion()
        atoms_j = dat.get_nion()
        print atoms_j

        l_max = 4
        ldos_ion = np.zeros((NEDOS,l_max,NION,NSPIN))

        for spin in range(NSPIN):
            for atom in range(NATOM):
                ion = atoms_j[atom]
                for i in range(NEDOS):
                    for lm in range(0,1):  # 0:s
                        ldos_ion[i,0,ion,spin] = \
                                ldos_ion[i,0,ion,spin] + \
                                self.pdos[i,lm,atom,spin]
                    for lm in range(1,4):  # 3:p
                        ldos_ion[i,0,ion,spin] = \
                                ldos_ion[i,0,ion,spin] + \
                                self.pdos[i,lm,atom,spin]
                    for lm in range(4,9):  # 5:d
                        ldos_ion[i,0,ion,spin] = \
                                ldos_ion[i,0,ion,spin] + \
                                self.pdos[i,lm,atom,spin]
                    for lm in range(9,16): # 7:d
                        ldos_ion[i,0,ion,spin] = \
                                ldos_ion[i,0,ion,spin] + \
                                self.pdos[i,lm,atom,spin]

        self.LDOS_ION = ldos_ion[:,l,ion,spin]
        return self.LDOS_ION
    
    def get_ldos_ion_all(self):
        pass

    def get_emax(self):
        suffix_tdos='.DOS.Tetrahedron'
        if os.path.exists(self.name+suffix_tdos) or \
                os.path.exists(self.name+suffix_tdos+'.gz'):
            dos = SAE.ReadMxTdos(name,suffix_tdos)
            self.EMAX = dos.get_emax()
        return self.EMAX

    def get_min(self):
        suffix_tdos='.DOS.Tetrahedron'
        if os.path.exists(self.name+suffix_tdos) or \
                os.path.exists(self.name+suffix_tdos+'.gz'):
            dos = SAE.ReadMxTdos(name,suffix_tdos)
            self.EMIN = dos.get_emin()
        return self.EMIN

    def get_eng(self):
        suffix_tdos='.DOS.Tetrahedron'
        if os.path.exists(self.name+suffix_tdos) or \
                os.path.exists(self.name+suffix_tdos+'.gz'):
            dos = SAE.ReadMxTdos(name,suffix_tdos)
            self.ENG = dos.get_eng()
        return self.ENG

    def get_tdos(self,spin=0):
        suffix_tdos='.DOS.Tetrahedron'
        if os.path.exists(self.name+suffix_tdos) or \
                os.path.exists(self.name+suffix_tdos+'.gz'):
            dos = SAE.ReadMxTdos(name,suffix_tdos)
            self.TDOS = dos.get_tdos(spin)
        return self.TDOS

    def get_inttdos(self,spin=0):
        suffix_tdos='.DOS.Tetrahedron'
        if os.path.exists(self.name+suffix_tdos) or \
                os.path.exists(self.name+suffix_tdos+'.gz'):
            dos = SAE.ReadMxTdos(name,suffix_tdos)
            self.INTTDOS = dos.get_inttdos(spin)
        return self.INTTDOS

################################################################################
if __name__ == '__main__':

    name = 'Cu'
    suffix = '.PDOS.Tetrahedron'
                                                                                
    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input',
                        dest='INPUT',
                        default=name,
    )
    options,  args = parser.parse_args()
                                                                                
    if options.INPUT:
        name=options.INPUT
                                                                                
    if len(args) > 0:
        name=args[0]

    pdos = ReadMxPdos(name,suffix)

    ispin = pdos.get_ispin()
    natom = pdos.get_natom()
    title = pdos.get_title()

#   print ispin
#   print natom
#   print title

#   ispin=0
#   tdos = dos.get_tdos(ispin)
#   inttdos = dos.get_inttdos(ispin)

#   eng = dos.get_eng()
#   nedos = dos.get_nedos()

#   emax = dos.get_emax()
#   emin = dos.get_emin()
#   print emin,emax

#   for i in range(nedos):
#       print i,eng[i],tdos[i],inttdos[i]

################################################################################
