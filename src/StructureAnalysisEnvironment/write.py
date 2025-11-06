#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 統合テスト
#  出力系関数をラップするボス
#
################################################################################
# History
#
# 2015.08.19
#  startup
#
################################################################################
try:
    from .copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.5"

################################################################################

import sys
import os
# import re
# import gzip
# import numpy as np

try:
    # sys.path.append('..')
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    import StructureAnalysisEnvironment as SAEnv
except ImportError:
    import StructureAnalysisEnvironment as SAEnv


# import SpaceGroupEnvironment as SGE

################################################################################
## VASP
## FDMNES
## OpenMX
## RMC_POT
## PWscf
##
def write(cell, \
          outname=None, \
          suffix=None, \
          code='VASP', \
          calinfo=None, \
          sort=False, \
          STD=False, \
          MOL=False, \
          FRAC=True):
    ### VASP ###
    ### 出力ファイル名は outname+".vasp" と自動で内部的に ".vasp" が加わる
    if code.upper() == 'VASP':
        if outname is None: outname = 'POSCAR'
        if cell.vasp_version is None: cell.vasp_version = 5
        SAEnv.print_poscar(outname, STD, \
                           cell.title, \
                           cell.scale, \
                           cell.natom, \
                           cell.nion, \
                           cell.selective, \
                           cell.direct, \
                           cell.vasp_version, \
                           cell.t, \
                           cell.atoms, \
                           cell.atoms_index, \
                           cell.position, \
                           cell.fix)

    ### FDMNES ###
    if code.upper() == 'FDMNES' or code.upper() == 'FDM':
        if outname is None: outname = 'read_pdb.inp'
        SAEnv.print_fdmnes1(outname=outname, cell=cell, STD=STD, MOL=MOL)
        if not STD:
            SAEnv.print_fdmnes_inp1(outname=outname, cell=cell, MOL=MOL)

    ### OpenMX ###
    ### 出力ファイル名は outname+".dat" と自動で内部的に ".dat" が加わる
    if code.upper() == 'OPENMX' or code.upper() == 'MX':

        if outname is None: outname = 'openemx'
        if calinfo is not None:
            NSW, NELM, IBRION, EDIFF, EDIFFG, KP = SAEnv.get_calinfo(code=calinfo)
        else:
            NSW = None
            NELM = None
            IBRION = None
            EDIFF = None
            EDIFFG = None
            KP = None

        SAEnv.print_mx_dat(outname, STD, \
                           cell.title, \
                           cell.scale, \
                           cell.natom, \
                           cell.nion, \
                           cell.selective, \
                           cell.direct, \
                           cell.vasp_version, \
                           cell.t, \
                           cell.atoms, \
                           cell.atoms_index, \
                           cell.position, \
                           cell.fix, \
                           cell.atoms_index_j, \
                           NSW=NSW, \
                           NELM=NELM, \
                           IBRION=IBRION, \
                           EDIFF=EDIFF, \
                           EDIFFG=EDIFFG, \
                           KP=KP, \
                           FRAC=FRAC)

    ### RMC_POT ###
    ### 出力ファイル名は outname+".cfg" と自動で内部的に ".cfg" が加わる
    if code.upper() == 'RMC_POT' or code.upper() == 'RMC' or code.upper() == 'RMCPOT':
        if outname is None: outname = 'rmcpot'
        SAEnv.print_rmcpot_cfg(outname, STD, \
                               cell.title, \
                               cell.scale, \
                               cell.natom, \
                               cell.nion, \
                               cell.selective, \
                               cell.direct, \
                               cell.vasp_version, \
                               cell.t, \
                               cell.atoms, \
                               cell.atoms_index, \
                               cell.position, \
                               cell.fix)

    ### PWScf ###
    if code.upper() == 'PWSCF' or code.upper() == 'QE' or code.upper() == 'QUANTUMESPRESSO':
        if outname is None: outname = 'scf.in'
        SAEnv.print_pwscf_scf(outname, STD, \
                              cell.title, \
                              cell.scale, \
                              cell.natom, \
                              cell.nion, \
                              cell.selective, \
                              cell.direct, \
                              cell.vasp_version, \
                              cell.t, \
                              cell.atoms, \
                              cell.atoms_index, \
                              cell.position, \
                              cell.fix, \
                              cell.atoms_index_j)
