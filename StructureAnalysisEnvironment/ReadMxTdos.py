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
#import numpy as np

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
   
        self.name = name
        self.datlines = datfile.split('\n')
        self.num = len(self.datlines) -1


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

    dos = ReadMxTdos(name,suffix)

    ispin = dos.get_ispin()
    natom = dos.get_natom()
    title = dos.get_title()

    print ispin
    print natom
    print title

    ispin=0
    tdos = dos.get_tdos(ispin)
    inttdos = dos.get_inttdos(ispin)

    eng = dos.get_eng()
    nedos = dos.get_nedos()

    emax = dos.get_emax()
    emin = dos.get_emin()
    print emin,emax

    for i in range(nedos):
        print i,eng[i],tdos[i],inttdos[i]

################################################################################
