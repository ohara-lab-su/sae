#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OpenMX 3.7
# ReadMxPdos.py
#
#  *.Dos.Tetrahedron.atom*
#
#  ReadMxDosMethod.py (superclass)
#                               ---> ReadMxTdos.py
#                               ---> ReadMxPdos.py
#
################################################################################
#
# 2015.02.25
#  共通する Class を ReadMxDosMethod に superclass として放り投げ
#  現存する ReadMxDos クラスは ReadMxTdos に変更し、同様に ReadMxPdos 作成
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
class ReadMxPdos(SAE.ReadMxDosMethod):

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

    dos = ReadMxPdos(name,suffix)

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
