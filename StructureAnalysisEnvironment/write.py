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
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015 Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.5"
################################################################################

#import sys
#import os
#import re
#import gzip
#import numpy as np
import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE

################################################################################
def write(cell,outname=None,code='VASP',calinfo=None,STD=False,MOL=False,FRAC=True):

    ### VASP
    if code.upper() == 'VASP':
        if outname is None: outname = 'POSCAR'
        if cell.vasp_version is None: cell.vasp_version = 5
        SAEnv.print_poscar(outname,STD,\
                           cell.title,\
                           cell.scale,\
                           cell.natom,\
                           cell.nion,\
                           cell.selective,\
                           cell.direct,\
                           cell.vasp_version,\
                           cell.t,\
                           cell.atoms,\
                           cell.atoms_index,\
                           cell.position,\
                           cell.fix)

    ### FDMNES
    if code.upper() == 'FDMNES' or code.upper() == 'FDM':

        if outname is None: outname = 'read_pdb.inp'
        SAEnv.print_fdmnes1(outname=outname,cell=cell,STD=STD,MOL=MOL)
        if not STD:
            SAEnv.print_fdmnes_inp1(outname=outname,cell=cell,MOL=MOL)

    ## OpenMX
    if code.upper() == 'OPENMX' or code.upper() == 'MX':

        if outname is None: outname = 'openemx'
        if calinfo is not None:
            NSW,NELM,IBRION,EDIFF,EDIFFG,KP = SAEnv.get_calinfo(code=calinfo)
        else:
            NSW=None
            NELM=None
            IBRION=None
            EDIFF=None
            EDIFFG=None
            KP=None

        SAEnv.print_mx_dat(outname,STD,\
                           cell.title,\
                           cell.scale,\
                           cell.natom,\
                           cell.nion,\
                           cell.selective,\
                           cell.direct,\
                           cell.vasp_version,\
                           cell.t,\
                           cell.atoms,\
                           cell.atoms_index,\
                           cell.position,\
                           cell.fix,\
                           cell.atoms_index_j,\
                           NSW=NSW,\
                           NELM=NELM,\
                           IBRION=IBRION,\
                           EDIFF=EDIFF,\
                           EDIFFG=EDIFFG,\
                           KP=KP,\
                           FRAC=FRAC)

    ## RMC_POT
    if code.upper() == 'RMC_POT' or code.upper() == 'RMC':

        # scale factor to 1.0
        cell.scale = SAEnv.conv_scale21(cell.scale,cell.t)

        # Cartesian to Direct
        if not cell.direct:
            cell.scale,cell.direct = SAEnv.conv_car2direct(cell.scale,\
                    cell.t,cell.natom,cell.direct,cell.position)
            src_mode="Cartesian"
        else:
            src_mode="Direct"

