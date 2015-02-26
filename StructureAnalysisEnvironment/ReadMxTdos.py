#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OpenMX 3.7
# ReadMxDos.py ==> ReadMxTdos.py (名前変更) 2015.02.25 09:46
#
#  *.Dos.Tetrahedron
#
# 構造と設計の基本方針
#
#    1) OpenMX は計算後の事後処理で DOS/PDOS が生成される
#    2) 完全に DOS(totalDOS) のファイルと PDOS(LDOS,PDOS)のファイルは別ファイル
#       別のプログラム生成手順で作られる
#
#    (1)と(2)のために、ReadMxDos クラスと ReadMxPdos クラスを分離したほうが
#    結果的に便利であると判断する
#
#    考えられる使い方は
#      A) DOS の計算だけして TDOS(本気でTDOSのみ) プロット
#      B)  DOS/PDOS の計算をして詳細にプロット (いつもの TDOS, LDOS, PDOS プロット)
#
#     ===> ２つの使い方に別れる (データーファイル/構造も別)
#          ２つ以上に大きく別れたデーター構造体
#
#     ===> ２つ別のクラスにするべき(ただし、Method の多くは継承することを前提)
#          ReadMxDosMethod.py (superclass)
#                                       ---> ReadMxTdos.py
#                                       ---> ReadMxPdos.py
#
################################################################################
#
# 2015.02.25
#  get_tdos(), get_inttdos() method を ReadMxDosMethod class から
#  ReadMxTdos class へ移動、整理
#
# 2015.02.25
#  共通する Class を ReadMxDosMethod に superclass として放り投げ
#  現存する ReadMxDos クラスは ReadMxTdos に変更した
#
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
__version__    = "0.0.1"
################################################################################

import sys
import os
import gzip
#import re
import optparse
import numpy as np

#from copy import deepcopy

import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE  

################################################################################
class ReadMxTdos(SAE.ReadMxDosMethod):

    ###################################
    # インスタンス作成
    def __init__(self,name,suffix):

        dosname = name+suffix
        if os.path.exists(dosname):
            GZIP=False
        elif os.path.exists(dosname+".gz"):
            GZIP=True
        else:
            sys.exit("STOP: "+dosname+" or "+dosname+".gz file not found")
    
        try:
            if GZIP:
                tmp = gzip.open(dosname+".gz")
            else:
                tmp = open(dosname)
            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: "+dosname+" or "+dosname+".gz does'nt open")
        finally:
            tmp.close()

        self.suffix = suffix
        self.name = name
        self.datlines = datfile.split('\n')
        self.num = len(self.datlines) -1


    ###################################
    # TDOS ( *.DOS.Tetrahedron ) 読み込み
    def get_tdos(self,spin=0):

        NSPIN = self.get_ispin()
        NEDOS = self.get_nedos()

        eng = np.zeros((NEDOS))
        dos = np.zeros((NEDOS,NSPIN))
        intdos = np.zeros((NEDOS,NSPIN))

        for i in range(NEDOS):
            eng[i] = float(self.datlines[i].split()[0])
            if NSPIN >= 2:
                dos[i,0] = float(self.datlines[i].split()[1])
                dos[i,1] = float(self.datlines[i].split()[2])
                intdos[i,0] = float(self.datlines[i].split()[3])
                intdos[i,1] = float(self.datlines[i].split()[4])
            else:
                dos[i,0] = float(self.datlines[i].split()[1])
                intdos[i,0] = float(self.datlines[i].split()[2])

        self.TDOS = dos[:,spin]
        return self.TDOS



    ###################################
    # INTTDOS ( *.DOS.Tetrahedron ) 読み込み
    def get_inttdos(self,spin=0):

        NSPIN = self.get_ispin()
        NEDOS = self.get_nedos()

        eng = np.zeros((NEDOS))
        dos = np.zeros((NEDOS,NSPIN))
        intdos = np.zeros((NEDOS,NSPIN))

        for i in range(NEDOS):
            eng[i] = float(self.datlines[i].split()[0])
            if NSPIN >= 2:
                dos[i,0] = float(self.datlines[i].split()[1])
                dos[i,1] = float(self.datlines[i].split()[2])
                intdos[i,0] = float(self.datlines[i].split()[3])
                intdos[i,1] = float(self.datlines[i].split()[4])
            else:
                dos[i,0] = float(self.datlines[i].split()[1])
                intdos[i,0] = float(self.datlines[i].split()[2])

        self.INTTDOS = intdos[:,spin]
        return self.INTTDOS

################################################################################
if __name__ == '__main__':

    name = 'Cu'
    suffix = '.DOS.Tetrahedron'
                                                                                
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

    tdos = ReadMxTdos(name,suffix)

    ispin = tdos.get_ispin()
    natom = tdos.get_natom()
    title = tdos.get_title()

    print ispin
    print natom
    print title

    ispin=0
    tdos = tdos.get_tdos(ispin)
    inttdos = tdos.get_inttdos(ispin)

    eng = tdos.get_eng()
    nedos = tdos.get_nedos()

    emax = tdos.get_emax()
    emin = tdos.get_emin()
#   print emin,emax

#   for i in range(nedos):
#       print i,eng[i],tdos[i],inttdos[i]

################################################################################
