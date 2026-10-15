#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 統合テスト
#  入力系(ファイル読み込み系)クラスをラップするボス
#
###############################################################################
# History
#
# 2018.08.15
#  python2/3 共通化テスト
#
# 2015.08.18
#  startup
#
###############################################################################
###############################################################################
# import re
# import gzip
# import numpy as np
# import SpaceGroupEnvironment as SGE
# try:
#     # sys.path.append('../..')
#     sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
#     import StructureAnalysisEnvironment as SAE
# except ImportError:
#     import StructureAnalysisEnvironment as SAE
###############################################################################
# RMC_POT や VASP4 などでは atoms_index 情報が存在しないので自分で
# その情報を手動で入力するときに atoms_index=['In','Ga','Zn','O'] などとする
#
###############################################################################
# for TEST
#   for i in range(natom):
#       print i, atoms_index_j[i]
#   ###########################################################################
# for VASP5
###########################################################################
#   print ion
#   print ion_local
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os


###########################################################################
###########################################################################
class Read(object):

    # module_name = 'StructureAnalysisEnvironment'
    # for Default
    # class_name = 'ReadVaspPoscar'
    # for debug
    # module の動的ロード
    # class の動的ロード
    # self.cell = SAE.ReadVaspPoscar(suffix=suffix, atoms_index=atoms_index)
    # どのような計算コードでもおそらく出力される(ダミー可能な)構造情報
    def __init__(
        self, filename=None, suffix=None, code="VASP", sort=False, atoms_index=None
    ):
        module_name = "sae._class_registry"
        class_name = "ReadVaspPoscar"
        suffix = ".vasp"
        if filename is None:
            filename = "POSCAR"
        if code.upper() == "VASP":
            class_name = "ReadVaspPoscar"
            suffix = ".vasp"
            if filename is None:
                filename = "POSCAR"
        if code.upper() == "FDMNES" or code.upper() == "FDM":
            class_name = "ReadFdmInp"
            suffix = ".inp"
            if filename is None:
                filename = "read_pdb.inp"
        if code.upper() == "OPENMX" or code.upper() == "MX":
            class_name = "ReadMxDat"
            suffix = ".dat"
            if filename is None:
                filename = "openmx.dat"
        if code.upper() == "RMC_POT" or code.upper() == "RMC":
            class_name = "ReadRmcpotCfg"
            suffix = ".cfg"
            if filename is None:
                filename = "rmcpot.cfg"
        if (
            code.upper() == "PWSCF"
            or code.upper() == "QE"
            or code.upper() == "QUANTUMESPRESSO"
        ):
            class_name = "ReadPwIn"
            suffix = ".in"
            if filename is None:
                filename = "scf.in"
        if code.upper() == "WIEN2K" or code.upper() == "WIEN":
            suffix = ".struct"
            if filename is None:
                filename = "case.struct"
        if code.upper() == "HILAPW" or code.upper() == "HI":
            suffix = ".in"
            if filename is None:
                filename = "sets.in"
        print("class name = %s" % str(class_name))
        # for Python3
        # このリフレクションは python2 方式なので注意
        try:
            module = __import__(module_name, fromlist=[class_name])
        except:
            module = __import__(module_name, globals(), locals(), [class_name], 0)
        klass = getattr(module, class_name)
        self.cell = klass(filename, suffix=suffix, atoms_index=atoms_index)
        self.title = self.cell.title
        self.system = self.cell.system
        self.scale = self.cell.scale
        self.t = self.cell.t
        self.nion = self.cell.nion
        self.atoms = self.cell.atoms
        self.atoms_j = self.cell.atoms_j
        self.atoms_index = self.cell.atoms_index
        self.atoms_index_j = self.cell.atoms_index_j
        self.atoms_number = self.cell.atoms_number
        self.atoms_number_j = self.cell.atoms_number_j
        self.natom = self.cell.natom
        self.ion = self.cell.ion
        self.ion_local = self.cell.ion_local
        self.selective = self.cell.selective
        self.direct = self.cell.direct
        self.position = self.cell.position
        self.fix = self.cell.fix
        self.vasp_version = self.cell.vasp_version
        self.suffix = suffix
        self.code = code

    def get_title(self):
        self.title = self.cell.get_title()
        return self.title

    def get_system(self):
        self.system = self.cell.get_title()
        return self.system

    def get_scale(self):
        self.scale = self.cell.get_scale()
        return self.scale

    def get_t(self):
        self.t = self.cell.get_t()
        return self.t

    def get_vasp_version(self):
        return self.vasp_version

    def get_nion(self):
        self.nion = self.cell.get_nion()
        return self.nion

    def get_atoms(self):
        self.atoms = self.cell.get_atoms()
        return self.atoms

    def get_atoms_j(self):
        self.atoms_j = self.cell.get_atoms_j()
        return self.atoms_j

    def get_atoms_index(self):
        self.atoms_index = self.cell.get_atoms_index()
        return self.atoms_index

    def get_atoms_index_j(self):
        self.atoms_index_j = self.cell.get_atoms_index_j()
        return self.atoms_index_j

    def get_atoms_number_j(self):
        self.atoms_number_j = self.cell.get_atoms_number_j()
        return self.atoms_number_j

    def get_natom(self):
        self.natom = self.cell.get_natom()
        return self.natom

    def get_ion(self):
        self.ion = self.cell.get_ion()
        return self.nion

    def get_ion_local(self):
        self.ion_local = self.cell.get_ion()
        return self.ion_local

    def get_selective(self):
        self.selective = self.cell.get_selective()
        return self.selective

    def get_direct(self):
        self.direct = self.cell.get_direct()
        return self.direct

    def get_position(self):
        self.position = self.cell.get_position()
        return self.position

    def get_fix(self):
        self.fix = self.cell.get_fix()
        return self.fix

    def write(
        self,
        outname=None,
        suffix=None,
        code=None,
        calinfo=None,
        STD=False,
        MOL=False,
        FRAC=True,
    ):
        from sae.structure.writer import StructureWriter

        StructureWriter().write(
            self.cell,
            outname=outname,
            suffix=suffix,
            code=code,
            calinfo=calinfo,
            STD=STD,
            MOL=MOL,
            FRAC=FRAC,
        )
        return
