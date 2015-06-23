#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vldos.py
#
#   Vldos.pl 完全互換(のはず)
#   python 版は OUTCAR or vasprun.xml のみ利用
#
#  ReadDoscar Class (ReadDoscar.py) 利用
#
#  [Method]
#
#   ISPIN = dos.ispin()
#   LORBIT = dos.lorbit()
#   NATOM = dos.natom()
#   TITLE =  dos.title()
#   EMAX = dos.emax()
#   EMIN = dos.emin()
#   NEDOS = dos.nedos()
#   EFERMI = dos.efermi()
#
#   ENG = dos.eng()
#   TDOS = dos.tdos(spin=1)
#   INTTDOS = dos.inttdos(spin=1)
#   PDOS = dos.pdos(lm=0,spin=1)
#   LDOS = dos.ldos(l=0,spin=1)   # LORIBT=11 の時は自動で要素をsumする
#
#
################################################################################
#
# 2015.01.14
#    ReadDoscar , ReadOutar に合わせて修正
#
# 2015.01.11 (sun) startup
#    基本機能はほぼ完成,まったりと作成
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
    dos = SAE.ReadDoscar(name)

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
    LDOS_ALL = dos.get_ldos_all()

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

# 毎回Method を呼ぶ --> 非常に時間が掛かるのでお薦めしない
# NATOM/NEDOS loop 前に一度行列を作っておくと少しはマシ(下記)
#       LDOS_ALL = np.zeros((3,NATOM,NSPIN,NEDOS))
#       for l in range(0,3):
#           for atom in range(NATOM):
#               LDOS_ALL[l,atom,spin] = dos.ldos(l,atom,spin)

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
            print >> out, "##      eng s p d"
            print >> out, "##"
            print >> out, ""
            print >> out, ""
            print >> out, ""

            for i in range(NEDOS):
                print >> out, "%13.8f " %( ENG[i]-EFERMI ),
                for l in range(0,3):
                    print >> out, "%13.8f " \
                            % ( LDOS_ALL[i,l,atom,spin] ),
#                           % ( LDOS_ALL[l,atom,spin,i] ),
                print ""


#   print "LORBIT = ",LORBIT
#   print "TITLE  = ",TITLE



################################################################################
