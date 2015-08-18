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
import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
def write(cell,outname=None,code='VASP',STD=True):

    if code == 'VASP':
        if outname is None: outname ='POSCAR'
        SAE.print_poscar(outname,STD,\
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


