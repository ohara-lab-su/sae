#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 構造情報以外の情報を変換するボスっぽい関数
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
#
# 2015.08.20
#  startup
#
################################################################################
from __future__ import print_function
###############################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014,2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.1.0"
################################################################################

#import optparse
#import sys
import os
#import re
#import numpy as np

#import glob
import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE

################################################################################
# OpenMX 用の入力ファイルのデフォルト設定項目を
# VASP の場合は VASP のファイルからコンバートする
#
def get_calinfo(code='VASP'):

    NSW=None
    NELM=None
    IBRION=None
    EDIFF=None
    EDIFFG=None
    KP=None

    ## for VASP
    if code == 'VASP' or code == 'vasp':
        ## INCAR 読み込み or OUTCAR 読み込み
        if os.path.exists('INCAR'):

            module_name = 'StructureAnalysisEnvironment'
            if os.path.exists('INCAR'):
                print("Read VASP INCAR  = INCAR")
                file_name = 'INCAR'
                class_name = 'ReadIncar'
           #elif os.path.exists('OUTCAR'):
           #    print "Read VASP INCAR  = OUTCAR"
           #    file_name = 'OUTCAR'
           #    class_name = 'ReadOutcar'
           #elif os.path.exists('vasprun.xml'):
           #    print "Read VASP INCAR  = vasprun.xml"
           #    file_name = 'vasprun.xml'
           #    class_name = 'ReadVasprun'

            module = __import__(module_name,globals(),locals(),[class_name],-1)
            klass = getattr(module,class_name)

            incar = klass(file_name)
            NSW = incar.get_nsw()
            NELM = incar.get_nelm()
            IBRION = incar.get_ibrion()

            EDIFF = incar.get_ediff()/10.   # about 1 Hartree = 10 eV
            EDIFFG = incar.get_ediffg()/10. #

        ## VASP の情報読み込み、KPOINTS
        if os.path.exists('KPOINTS'):
            kpoints = SAEnv.ReadVaspKpoints('KPOINTS')
            KP = kpoints.get_kpoints_array()
            kx = KP[0:0]
            ky = KP[0:1]
            kz = KP[0:2]

    return NSW,NELM,IBRION,EDIFF,EDIFFG,KP


