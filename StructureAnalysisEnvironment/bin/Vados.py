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
# 2018.08.15
#  Python2/3 両対応
#
# 2015.01.14
#   ReadDoscar , ReadOutcar に合わせて修正
#
# 2015.01.13 (sun) startup
#
#
################################################################################
from __future__ import print_function

################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
#
__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import sys
# import os
# import gzip
import optparse
# import numpy as np

# import re
# from copy import deepcopy

import StructureAnalysisEnvironment as SAE


# import SpaceGroupEnvironment as SGE

################################################################################
def options():
    name = 'DOSCAR'

    parser = optparse.OptionParser()
    parser.add_option('-i', '--input',
                      dest='INPUT',
                      default=name,
                      )
    options, args = parser.parse_args()

    if options.INPUT:
        name = options.INPUT

    if len(args) > 0:
        name = args[0]

    return name


################################################################################
if __name__ == '__main__':

    # set input file
    name = options()
    oname = 'OUTCAR'
    # set output device
    out = sys.stdout

    # makes instance ( Read DOSCAR )
    dos = SAE.io.ReadVaspDoscar(name)

    NSPIN = dos.get_ispin()
    LORBIT = dos.get_lorbit()
    NATOM = dos.get_natom()
    TITLE = dos.get_title()
    EMAX = dos.get_emax()
    EMIN = dos.get_emin()
    NEDOS = dos.get_nedos()
    EFERMI = dos.get_efermi()

    ENG = dos.get_eng()

    # makes instance ( Read OUTCAR )
    outcar = SAE.io.ReadVaspOutcar(oname)
    NION = outcar.get_nion()

    # 最初からごつい構造体を返すMethodを作っておく(超高速) --> おすすめ
    ADOS_ALL = dos.get_ldos_ion_all()

    for spin in range(NSPIN):
        print("", file=out)
        print("", file=out)
        print("", file=out)
        print("##", file=out)
        print("## INFILE= %s" % str(name), file=out)
        print("## ISPIN = %s" % str(NSPIN), file=out)
        print("##  SPIN = %s" % str(spin + 1), file=out)
        print("## NATOM = %s" % str(NATOM), file=out)
        print("## EMAX  = %s" % str(EMAX), file=out)
        print("## EMIN  = %s" % str(EMIN), file=out)
        print("## NLINE = %s" % str(NEDOS), file=out)
        print("## FERMI = %s" % str(EFERMI), file=out)
        print("##")
        print("##")
        print("##        total")
        print("##        eng tdos tidos")
        print("##")
        print("")
        print("")
        print("")

        TDOS = dos.get_tdos(spin)
        INTTDOS = dos.get_inttdos(spin)

        # 毎回Method を呼ぶ --> 非常に時間が掛かるのでお薦めしない
        # NATOM/NEDOS loop 前に一度行列を作っておくと少しはマシ(下記)
        #       ADOS_ALL = np.zeros((3,NION,NSPIN,NEDOS))
        #       for l in range(0,3):
        #           for ion in range(NION):
        #               ADOS_ALL[l,ion,spin] = dos.get_ldos_ion(l,ion,spin)

        for i in range(NEDOS):
            print("%13.8f %13.8f %13.8f " % (ENG[i] - EFERMI, TDOS[i], INTTDOS[i]))

        print("", file=out)
        print("", file=out)
        print("", file=out)

        for ion in range(NION):
            print("", file=out)
            print("", file=out)
            print("", file=out)
            print("##", file=out)
            print("## INFILE= %s" % str(name), file=out)
            print("## ISPIN = %s" % str(NSPIN), file=out)
            print("##  SPIN = %s" % str(spin + 1), file=out)
            print("##  NION = %s" % str(NION), file=out)
            print("## EMAX  = %s" % str(EMAX), file=out)
            print("## EMIN  = %s" % str(EMIN), file=out)
            print("## NLINE = %s" % str(NEDOS), file=out)
            print("## FERMI = %s" % str(EFERMI), file=out)
            print("##", file=out)
            print("##", file=out)
            print("##      ION= %s" % (ion + 1), file=out)
            print("##      eng s p d", file=out)
            print("##", file=out)
            print("", file=out)
            print("", file=out)
            print("", file=out)

            for i in range(NEDOS):
                print("%13.8f " % (ENG[i] - EFERMI), file=out, end="")
                for l in range(0, 3):
                    print("%13.8f "
                          % (ADOS_ALL[i, l, ion, spin]), file=out, end="")
                #                           % ( ADOS_ALL[l,ion,spin,i] ),
                print("", file=out)

#   print "LORBIT = ",LORBIT
#   print "TITLE  = ",TITLE


################################################################################
