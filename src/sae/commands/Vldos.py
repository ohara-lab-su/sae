#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
#   print "LORBIT = ",LORBIT
#   print "TITLE  = ",TITLE
################################################################################
from __future__ import print_function
from sae.vasp.doscar import ReadVaspDoscar

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vldos.py
#
#   Vldos.pl 完全互換(のはず)
#   python 版は OUTCAR or vasprun.xml のみ利用
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.01.14
#    ReadDoscar , ReadOutar に合わせて修正
#
# 2015.01.11 (sun) startup
#    基本機能はほぼ完成,まったりと作成
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import optparse


#
################################################################################
#import os
#import gzip
#import numpy as np
#import re
#from copy import deepcopy
#import SpaceGroupEnvironment as SGE
################################################################################
def options():
    name = "DOSCAR"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]
    return name


################################################################################
# set input file
# makes instance ( Read DOSCAR )
# set output device
# 最初からごつい構造体を返すMethodを作っておく(超高速) --> おすすめ
# perl 版とほぼ同じ速度
if __name__ == "__main__":
    name = options()
    dos = ReadVaspDoscar(name)
    out = sys.stdout
    NSPIN = dos.ispin
    LORBIT = dos.lorbit
    NATOM = dos.natom
    TITLE = dos.title
    EMAX = dos.emax
    EMIN = dos.emin
    NEDOS = dos.nedos
    EFERMI = dos.efermi
    ENG = dos.eng
    LDOS_ALL = dos.get_ldos_all()
    # 毎回Method を呼ぶ --> 非常に時間が掛かるのでお薦めしない
    # NATOM/NEDOS loop 前に一度行列を作っておくと少しはマシ(下記)
    #       LDOS_ALL = np.zeros((3,NATOM,NSPIN,NEDOS))
    #       for l in range(0,3):
    #           for atom in range(NATOM):
    #               LDOS_ALL[l,atom,spin] = dos.ldos(l,atom,spin)
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
            print("%13.8f %13.8f %13.8f " % (ENG[i] - EFERMI, TDOS[i], INTTDOS[i]))
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
            print("##  SPIN = %s" % str(spin + 1), file=out)
            print("## NATOM = %s" % str(NATOM), file=out)
            print("## EMAX  = %s" % str(EMAX), file=out)
            print("## EMIN  = %s" % str(EMIN), file=out)
            print("## NLINE = %s" % str(NEDOS), file=out)
            print("## FERMI = %s" % str(EFERMI), file=out)
            print("##", file=out)
            print("##", file=out)
            print("##      ATOM= %s" % str(atom + 1), file=out)
            print("##      eng s p d", file=out)
            print("##", file=out)
            print("", file=out)
            print("", file=out)
            print("", file=out)
            #                           % ( LDOS_ALL[l,atom,spin,i] ),
            for i in range(NEDOS):
                print("%13.8f " % (ENG[i] - EFERMI), file=out, end="")
                for l in range(0, 3):
                    print("%13.8f " % LDOS_ALL[i, l, atom, spin], file=out, end="")
                print("")
