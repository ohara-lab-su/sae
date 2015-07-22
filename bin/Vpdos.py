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
# 2015.01.14 strtup
#   Vldos.py からコピー, method 名, 変数名を変更しただけのもの
#   動作確認は IGZO にて
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
    parser.add_option(  '-i','--input',
                        dest='INPUT',
                        default=name,
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
    EFERMI = dos.get_efermi()

    ENG = dos.get_eng()

# 最初からごつい構造体を返すMethodを作っておく(超高速) --> おすすめ
# perl 版とほぼ同じ速度
    PDOS_ALL = dos.get_pdos_all()

    for spin in range(NSPIN):
        print >> out, ""
        print >> out, ""
        print >> out, ""
        print >> out, "##"
        print >> out, "## INFILE=",name
        print >> out, "## ISPIN =",NSPIN
        print >> out, "##  SPIN =",spin+1
        print >> out, "## NATOM =",NATOM
        print >> out, "## EMAX  =",EMAX
        print >> out, "## EMIN  =",EMIN
        print >> out, "## NLINE =",NEDOS
        print >> out, "## FERMI =",EFERMI
        print >> out, "##"
        print >> out, "##"
        print >> out, "##        total"
        print >> out, "##        eng tdos tidos"
        print >> out, "##"
        print >> out, ""
        print >> out, ""
        print >> out, ""

        TDOS = dos.get_tdos(spin)
        INTTDOS = dos.get_inttdos(spin)

        for i in range(NEDOS):
            print "%13.8f %13.8f %13.8f " %( ENG[i]-EFERMI,TDOS[i],INTTDOS[i] )

        print >> out, ""
        print >> out, ""
        print >> out, ""

        for atom in range(NATOM):
            print >> out, ""
            print >> out, ""
            print >> out, ""
            print >> out, "##"
            print >> out, "## INFILE=",name
            print >> out, "## ISPIN =",NSPIN
            print >> out, "##  SPIN =",spin+1
            print >> out, "## NATOM =",NATOM
            print >> out, "## EMAX  =",EMAX
            print >> out, "## EMIN  =",EMIN
            print >> out, "## NLINE =",NEDOS
            print >> out, "## FERMI =",EFERMI
            print >> out, "##"
            print >> out, "##"
            print >> out, "##      ATOM=",atom+1
            print >> out, "##      eng s p-y p-z p-x d-xy d-yz d-z2-r2 d-xz d-x2-y2"
            print >> out, "##"
            print >> out, ""
            print >> out, ""
            print >> out, ""

            for i in range(NEDOS):
                print >> out, "%13.8f " %( ENG[i]-EFERMI ),
                for l in range(0,9):
                    print >> out, "%13.8f " \
                            % ( PDOS_ALL[i,l,atom,spin] ),
                print ""

#   print "LORBIT = ",LORBIT
#   print "TITLE  = ",TITLE



################################################################################
