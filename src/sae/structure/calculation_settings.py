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
################################################################################
# import optparse
# import sys
# import re
# import numpy as np
# import glob
# import SpaceGroupEnvironment as SGE
################################################################################
# OpenMX 用の入力ファイルのデフォルト設定項目を
# VASP の場合は VASP のファイルからコンバートする
#
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import os


class CalculationSettings:

    def get_calinfo(self, code="VASP"):
        from sae.vasp.kpoints import ReadVaspKpoints

        NSW = None
        NELM = None
        IBRION = None
        EDIFF = None
        EDIFFG = None
        KP = None
        ## for VASP
        ## INCAR 読み込み or OUTCAR 読み込み
        ## VASP の情報読み込み、KPOINTS
        if code == "VASP" or code == "vasp":
            # elif os.path.exists('OUTCAR'):
            #    print "Read VASP INCAR  = OUTCAR"
            #    file_name = 'OUTCAR'
            #    class_name = 'ReadOutcar'
            # elif os.path.exists('vasprun.xml'):
            #    print "Read VASP INCAR  = vasprun.xml"
            #    file_name = 'vasprun.xml'
            #    class_name = 'ReadVasprun'
            if os.path.exists("INCAR"):
                module_name = "sae._class_registry"
                if os.path.exists("INCAR"):
                    print("Read VASP INCAR  = INCAR")
                    file_name = "INCAR"
                    class_name = "ReadVaspIncar"
                module = __import__(module_name, globals(), locals(), [class_name], 0)
                klass = getattr(module, class_name)
                incar = klass(file_name)
                NSW = incar.get_nsw()
                NELM = incar.get_nelm()
                IBRION = incar.get_ibrion()
                # about 1 Hartree = 10 eV
                EDIFF = incar.get_ediff() / 10.0
                #
                EDIFFG = incar.get_ediffg() / 10.0
            if os.path.exists("KPOINTS"):
                kpoints = ReadVaspKpoints("KPOINTS")
                KP = kpoints.get_kpoints_array()
                kx = KP[0:0]
                ky = KP[0:1]
                kz = KP[0:2]
        return (NSW, NELM, IBRION, EDIFF, EDIFFG, KP)
