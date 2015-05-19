#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vados.py
#
#   Vldos.py (LDOS)
#   Vados.py (ADOS)
#
#  ADOS モードのテスト用
#  原子種ごとの s,p,d 軌道を gnuplot 形式で出力
#
################################################################################
#
# 2015.01.14
#   ReadDoscar , ReadOutcar に合わせて修正
#
# 2015.01.13 (sun) startup
#
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
    oname = 'OUTCAR'
    # set output device
    out = sys.stdout

    # makes instance ( Read DOSCAR )
    dos = SAE.ReadDoscar(name)

    NSPIN = dos.get_ispin()
    LORBIT = dos.get_lorbit()
    NATOM = dos.get_natom()
    TITLE =  dos.get_title()
    EMAX = dos.get_emax()
    EMIN = dos.get_emin()
    NEDOS = dos.get_nedos()
    EFERMI = dos.get_efermi()

    ENG = dos.get_eng()

    # makes instance ( Read OUTCAR )                                            
    outcar = SAE.ReadOutcar(oname)                                              
    NION = outcar.get_nion()             

# 最初からごつい構造体を返すMethodを作っておく(超高速) --> おすすめ
    ADOS_ALL = dos.get_ldos_ion_all()

    for spin in range(NSPIN):
        print >> out, ""
        print >> out, ""
        print >> out, ""
        print >> out, "##"
        print >> out, "## INFILE= ",name
        print >> out, "## ISPIN = ",NSPIN
        print >> out, "##  SPIN = ",spin+1
        print >> out, "## NATOM = ",NATOM
        print >> out, "## EMAX  = ",EMAX
        print >> out, "## EMIN  = ",EMIN
        print >> out, "## NLINE = ",NEDOS
        print >> out, "## FERMI = ",EFERMI
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
#       ADOS_ALL = np.zeros((3,NION,NSPIN,NEDOS))
#       for l in range(0,3):
#           for ion in range(NION):
#               ADOS_ALL[l,ion,spin] = dos.get_ldos_ion(l,ion,spin)

        for i in range(NEDOS):
            print "%13.8f %13.8f %13.8f " %( ENG[i]-EFERMI,TDOS[i],INTTDOS[i] )

        print >> out, ""
        print >> out, ""
        print >> out, ""

        for ion in range(NION):
            print >> out, ""
            print >> out, ""
            print >> out, ""
            print >> out, "##"
            print >> out, "## INFILE= ",name
            print >> out, "## ISPIN = ",NSPIN
            print >> out, "##  SPIN = ",spin+1
            print >> out, "##  NION = ",NION
            print >> out, "## EMAX  = ",EMAX
            print >> out, "## EMIN  = ",EMIN
            print >> out, "## NLINE = ",NEDOS
            print >> out, "## FERMI = ",EFERMI
            print >> out, "##"
            print >> out, "##"
            print >> out, "##      ION=",ion+1
            print >> out, "##      eng s p d"
            print >> out, "##"
            print >> out, ""
            print >> out, ""
            print >> out, ""

            for i in range(NEDOS):
                print >> out, "%13.8f " %( ENG[i]-EFERMI ),
                for l in range(0,3):
                    print >> out, "%13.8f " \
                            % ( ADOS_ALL[i,l,ion,spin] ),
#                           % ( ADOS_ALL[l,ion,spin,i] ),
                print ""


#   print "LORBIT = ",LORBIT
#   print "TITLE  = ",TITLE



################################################################################
