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
#  get_ispin()   : *.out *.dat 読み込み (ReadMxOut, ReadMxDat, ReadMxDatMethod)
#  get_natom()   : *.out *.dat 読み込み (ReadMxOut, ReadMxDat, ReadMxDatMethod)
#  get_title()   : *.out *.dat 読み込み (ReadMxOut, ReadMxDat, ReadMxDatMethod)
#
#  get_emax()
#  get_emin()
#  get_nedos()
#
#  get_efermi() ダミー
#  get_lorbit() ダミー
#
#  get_nion()    : *.out *.dat 読み込み (ReadMxOut, ReadMxDat, ReadMxDatMethod)
#  get_atoms_j() : *.out *.dat 読み込み (ReadMxOut, ReadMxDat, ReadMxDatMethod)
#
################################################################################
#
# 2015.02.26
#  get_tdos()     ---> move ReadMxTdos
#  get_inttdos() ---> move ReadMxTdos
#
# 2015.02.26
#  get_atoms_j()  : *.out *.dat 読み込み (ReadMxOut, ReadMxDat, ReadMxDatMethod)
#  get_nion()     : *.out *.dat 読み込み (ReadMxOut, ReadMxDat, ReadMxDatMethod)
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
from __future__ import print_function
try:
    from ...copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.4"

################################################################################

import sys
import os
# import gzip
# import re
# import optparse
import numpy as np

# from copy import deepcopy
# import SpaceGroupEnvironment as SGE
try:
    # sys.path.append('../..')
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    import StructureAnalysisEnvironment as SAEnv
except ImportError:
    import StructureAnalysisEnvironment as SAEnv


################################################################################
class ReadMxDosMethod(object):

    ###################################
    # *.out or *.dat から ISPIN 情報を読み込む( out 優先 )
    def get_ispin(self):
        module_name = 'StructureAnalysisEnvironment'
        if os.path.exists(self.name + '.out') or os.path.exists(self.name + '.out' + '.gz'):
            class_name = 'ReadMxOut'
            datname = self.name + '.out'
        elif os.path.exists(self.name + '.dat') or os.path.exists(self.name + '.dat' + '.gz'):
            class_name = 'ReadMxDat'
            datname = self.name + '.dat'
        else:
            sys.exit("STOP: " + self.name + ".out or " + self.name + ".dat file not found")

        module = __import__(module_name, globals(), locals(), [class_name], -1)
        klass = getattr(module, class_name)

        dat = klass(datname)
        self.ispin = dat.get_ispin()

        return self.ispin

    ###################################
    # *.out or *.dat から NATOM 情報を読み込む( out 優先 )
    def get_natom(self):
        module_name = 'StructureAnalysisEnvironment'
        if os.path.exists(self.name + '.out') or os.path.exists(self.name + '.out' + '.gz'):
            class_name = 'ReadMxOut'
            datname = self.name + '.out'
        elif os.path.exists(self.name + '.dat') or os.path.exists(self.name + '.dat' + '.gz'):
            class_name = 'ReadMxDat'
            datname = self.name + '.dat'
        else:
            sys.exit("STOP: " + self.name + ".out or " + self.name + ".dat file not found")

        module = __import__(module_name, globals(), locals(), [class_name], -1)
        klass = getattr(module, class_name)

        dat = klass(datname)
        self.natom = dat.get_natom()

        return self.natom

    ###################################
    # *.out or *.dat から TITLE 情報を読み込む( out 優先 )
    def get_title(self):

        module_name = 'StructureAnalysisEnvironment'
        if os.path.exists(self.name + '.out') or os.path.exists(self.name + '.out' + '.gz'):
            class_name = 'ReadMxOut'
            datname = self.name + '.out'
        elif os.path.exists(self.name + '.dat') or os.path.exists(self.name + '.dat' + '.gz'):
            class_name = 'ReadMxDat'
            datname = self.name + '.dat'
        else:
            sys.exit("STOP: " + self.name + ".out or " + self.name + ".dat file not found")

        module = __import__(module_name, globals(), locals(), [class_name], -1)
        klass = getattr(module, class_name)

        dat = klass(datname)
        self.title = dat.get_title()

        return self.title

    ###################################
    # EMAX (エネルギー固有値の最大値)
    def get_emax(self):
        NEDOS = self.get_nedos()
        self.EMAX = float(self.datlines[NEDOS - 1].split()[0])
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
    # ION の数を求める ( *.out or *.dat から読み込む)
    def get_nion(self):
        module_name = 'StructureAnalysisEnvironment'
        if os.path.exists(self.name + '.out') or os.path.exists(self.name + '.out' + '.gz'):
            class_name = 'ReadMxOut'
            datname = self.name + '.out'
        elif os.path.exists(self.name + '.dat') or os.path.exists(self.name + '.dat' + '.gz'):
            class_name = 'ReadMxDat'
            datname = self.name + '.dat'
        else:
            sys.exit("STOP: " + self.name + ".out or " + self.name + ".dat file not found")

        module = __import__(module_name, globals(), locals(), [class_name], -1)
        klass = getattr(module, class_name)

        dat = klass(datname)
        self.NION = dat.get_nion()

        return self.NION

    ###################################
    # atoms_j を求める ( *.out or *.dat から読み込む)
    def get_atoms_j(self):
        module_name = 'StructureAnalysisEnvironment'
        if os.path.exists(self.name + '.out') or os.path.exists(self.name + '.out' + '.gz'):
            class_name = 'ReadMxOut'
            datname = self.name + '.out'
        elif os.path.exists(self.name + '.dat') or os.path.exists(self.name + '.dat' + '.gz'):
            class_name = 'ReadMxDat'
            datname = self.name + '.dat'
        else:
            sys.exit("STOP: " + self.name + ".out or " + self.name + ".dat file not found")

        module = __import__(module_name, globals(), locals(), [class_name], -1)
        klass = getattr(module, class_name)

        dat = klass(datname)
        self.atoms_j = dat.get_atoms_j()

        return self.atoms_j

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
