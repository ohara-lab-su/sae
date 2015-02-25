#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OpenMX 3.7
# ReadMxDosMethod.py
#
#  TDOS と PDOS でのクラス分離のため共通するMethod関係を superclass として
#  分離・再設計した
#
#    ReadMxDosMethod.py (superclass)
#                                 ---> ReadMxTdos.py
#                                 ---> ReadMxPdos.py
#
################################################################################
#
# 2015.02.25
#  Method の多くを SuperClass 化
#  ReadMxDosMethod.py --(継承)--- ReadMxDos.py -(名前変更)-> ReadMxTdos.py
#                     --(継承)-----------------------------> ReadMxPdos.py
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
__version__    = "0.0.4"
################################################################################

import sys
import os
#import gzip
#import re
#import optparse
import numpy as np

#from copy import deepcopy

#import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE  

################################################################################
class ReadMxDosMethod(object):


    ###################################
    # *.out or *.dat から ISPIN 情報を読み込む( out 優先 )
    def get_ispin(self):
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
        self.ispin = dat.get_ispin()

        return self.ispin
    
    ###################################
    # *.out or *.dat から NATOM 情報を読み込む( out 優先 )
    def get_natom(self):
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
        self.natom = dat.get_natom()

        return self.natom

    ###################################
    # *.out or *.dat から TITLE 情報を読み込む( out 優先 )
    def get_title(self):

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
        self.title = dat.get_title()

        return self.title


    ###################################
    # EMAX (エネルギー固有値の最大値)
    def get_emax(self):
        NEDOS = self.get_nedos()
        self.EMAX = float(self.datlines[NEDOS-1].split()[0])
        return self.EMAX

    ###################################
    # EMAX (エネルギー固有値の最小値)
    def get_emin(self):
        self.EMIN = float(self.datlines[0].split()[0])
        return self.EMIN

    ###################################
    # NEDOS (DOSの分割数, OpenMXの*.DOS.Tetrahedron ではファイルの行数に相当)
    def get_nedos(self):
        return self.num

    ###################################
    def get_efermi(self):
        pass

    ###################################
    def get_lorbit(self):
        pass

    ###################################
    # Energy 固有値(この場合はDOSの分割値)
    def get_eng(self):
        NEDOS = self.get_nedos()
        eng = np.zeros((NEDOS))
        for i in range(NEDOS):
            eng[i] = float(self.datlines[i].split()[0])
        self.ENG = eng[:]
        return self.ENG

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

#   ReadMxPdos.py で実装
#   def get_pdos(self,lm=0,atom=0,spin=0):
#       pass

#   ReadMxPdos.py で実装
#   def get_pdos_all(self):
#       pass

#   ReadMxPdos.py で実装
#   def get_ldos(self,l=0,atom=0,spin=0):
#       pass

#   ReadMxPdos.py で実装
#   def get_ldos_all(self):
#       pass

# ReadMxPdos() にて実装
#   def get_tdos_spd(self,l=0,spin=0):
#       pass

# ReadMxPdos() にて実装
#   def get_ldos_ion(self,l=0,ion=0,spin=0):
#       pass

# ReadMxPdos() にて実装
#   def get_ldos_ion_all(self):
#       pass

###############################################################################
