#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vtdos.py
#
#  DOSCAR から gnuplot 形式へ変換
#  TDOS と INT-TDOS の結果のみ出力、ほぼテスト用
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.10.28
#   フェルミレベルに関してのオプションを追加
#
# 2015.01.14 startup
#    get_tdos & get_inttdos テスト用を兼ねる
#
################################################################################
from __future__ import print_function
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
#import os
#import gzip
import optparse
#import numpy as np

#import re
#from copy import deepcopy

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
def options():

    name = 'DOSCAR'

    parser = optparse.OptionParser()
    parser.add_option('-i','--input', dest='INPUT')
    # スイッチが入ると Ef = 0 のスイッチが 'off' になる
    parser.add_option('--fermi', action='store_true',default=False,)
    options,  args = parser.parse_args()

    if options.INPUT: name=options.INPUT

    if len(args) > 0: name=args[0]

    return name, options.fermi

################################################################################
if __name__ == '__main__':

    # set input file
    name, FERMI_FLAG = options()

    # makes instance ( Read DOSCAR )
    dos = SAE.ReadVaspDoscar(name)

    # set output device
    out = sys.stdout

    NSPIN = dos.get_ispin()
    LORBIT = dos.get_lorbit()
    NATOM = dos.get_natom()
    TITLE =  dos.get_title()
    EMAX = dos.get_emax()
    EMIN = dos.get_emin()
    NEDOS = dos.get_nedos()

    ENG = dos.get_eng()

    print("", file=out)
    print("", file=out)
    print("", file=out)

    if FERMI_FLAG:
        EFERMI = 0.0
        print("## EF = 0", file=out)
    else:
        EFERMI = dos.get_efermi()
        print("## EF = ", EFERMI, file=out)
    print("## Energy = E - EF", file=out)

    for spin in range(NSPIN):
        print("##", file=out)
        print("## INFILE= ",name, file=out)
        print("## ISPIN = ",NSPIN, file=out)
        print("##  SPIN = ",spin+1, file=out)
        print("## NATOM = ",NATOM, file=out)
        print("## EMAX  = ",EMAX, file=out)
        print("## EMIN  = ",EMIN, file=out)
        print("## NLINE = ",NEDOS, file=out)
        print("## FERMI = ",EFERMI, file=out)
        print("##", file=out)
        print("##", file=out)
        print("##        total", file=out)
        print("##        eng tdos tidos", file=out)
        print("##", file=out)
        print("", file=out)
        print("", file=out)
        print("", file=out)

        TDOS = dos.get_tdos(spin)
        INTTDOS = dos.get_inttdos(spin)

        for i in range(NEDOS):
            print("%13.8f %13.8f %13.8f " %( ENG[i]-EFERMI,TDOS[i],INTTDOS[i] ), file=out)

        print("", file=out)
        print("", file=out)
        print("", file=out)


################################################################################
