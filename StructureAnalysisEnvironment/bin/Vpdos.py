#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vpdos.py
#
#   Vpdos.pl 完全互換(のはず)
#   ReadDoscar Class (ReadDoscar.py) 利用
#
#   デフォルトで  E - EF
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.01.14 strtup
#   Vldos.py からコピー, method 名, 変数名を変更しただけのもの
#   動作確認は IGZO にて
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
    parser.add_option('-i','--input', dest='INPUT', default=name,
    )
    options,  args = parser.parse_args()

    if options.INPUT:
        name=options.INPUT

    if len(args) > 0:
        name=args[0]

    return name

################################################################################
if __name__ == '__main__':

    # set input file
    name = options()

    # makes instance ( Read DOSCAR )
    dos = SAE.io.ReadVaspDoscar(name)

    # set output device
    out = sys.stdout

    NSPIN = dos.get_ispin()
    LORBIT = dos.get_lorbit()
    NATOM = dos.get_natom()
    TITLE =  dos.get_title()
    EMAX = dos.get_emax()
    EMIN = dos.get_emin()
    NEDOS = dos.get_nedos()
    EFERMI = dos.get_efermi()

    ENG = dos.get_eng()

# 最初からごつい構造体を返すMethodを作っておく(超高速) --> おすすめ
# perl 版とほぼ同じ速度
    PDOS_ALL = dos.get_pdos_all()

    for spin in range(NSPIN):
        print("", file=out)
        print("", file=out)
        print("", file=out)
        print("##", file=out)
        print("## INFILE= %s" % str(name), file=out)
        print("## ISPIN = %s" % str(NSPIN), file=out)
        print("##  SPIN = %s" % str(spin+1), file=out)
        print("## NATOM = %s" % str(NATOM), file=out)
        print("## EMAX  = %s" % str(EMAX), file=out)
        print("## EMIN  = %s" % str(EMIN), file=out)
        print("## NLINE = %s" % str(NEDOS), file=out)
        print("## FERMI = %s" % str(EFERMI), file=out)
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

        for atom in range(NATOM):
            print("", file=out)
            print("", file=out)
            print("", file=out)
            print("##", file=out)
            print("## INFILE= %s" % str(name), file=out)
            print("## ISPIN = %s" % str(NSPIN), file=out)
            print("##  SPIN = %s" % str(spin+1), file=out)
            print("## NATOM = %s" % str(NATOM), file=out)
            print("## EMAX  = %s" % str(EMAX), file=out)
            print("## EMIN  = %s" % str(EMIN), file=out)
            print("## NLINE = %s" % str(NEDOS), file=out)
            print("## FERMI = %s" % str(EFERMI), file=out)
            print("##", file=out)
            print("##", file=out)
            print("##      ATOM= %s" % str(atom+1), file=out)
            print("##      eng s p-y p-z p-x d-xy d-yz d-z2-r2 d-xz d-x2-y2", file=out)
            print("##", file=out)
            print("", file=out)
            print("", file=out)
            print("", file=out)

            for i in range(NEDOS):
                print("%13.8f " %( ENG[i]-EFERMI ), file=out, end="")
                for l in range(0,9):
                    print("%13.8f "
                            % ( PDOS_ALL[i,l,atom,spin] ), file=out, end="")
                print("", file=out)

#   print "LORBIT = ",LORBIT
#   print "TITLE  = ",TITLE


################################################################################
