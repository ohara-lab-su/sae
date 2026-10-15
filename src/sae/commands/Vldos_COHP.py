#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.lobster.doscar import ReadLobDos

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vldos_COHP.py
#
#  Vldos.py とほぼ同等
#  DOSCAR の代わりに DOSCAR.lobster を読み込む
#
#  original の DOSCAR より DOSCAR.lobster は三桁少ないので注意
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.09.03
#    startup
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
    name = "DOSCAR.lobster"
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
#   dos = SAE.io.ReadVaspDoscar(name)
# set output device
if __name__ == "__main__":
    name = options()
    dos = ReadLobDos(name)
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
    for spin in range(NSPIN):
        print("", file=out)
        print("", file=out)
        print("", file=out)
        print("##", file=out)
        print("## INFILE=", name, file=out)
        print("## ISPIN =", NSPIN, file=out)
        print("##  SPIN =", spin + 1, file=out)
        print("## NATOM =", NATOM, file=out)
        print("## EMAX  =", EMAX, file=out)
        print("## EMIN  =", EMIN, file=out)
        print("## NLINE =", NEDOS, file=out)
        print("## FERMI =", EFERMI, file=out)
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
            print("%9.5f %9.5f %9.5f " % (ENG[i], TDOS[i], INTTDOS[i]))
        print("", file=out)
        print("", file=out)
        print("", file=out)
        for atom in range(NATOM):
            print("", file=out)
            print("", file=out)
            print("", file=out)
            print("##", file=out)
            print("## INFILE=", name, file=out)
            print("## ISPIN =", NSPIN, file=out)
            print("##  SPIN =", spin + 1, file=out)
            print("## NATOM =", NATOM, file=out)
            print("## EMAX  =", EMAX, file=out)
            print("## EMIN  =", EMIN, file=out)
            print("## NLINE =", NEDOS, file=out)
            print("## FERMI =", EFERMI, file=out)
            print("##", file=out)
            print("##", file=out)
            print("##      ATOM=", atom + 1, file=out)
            print("##      eng s p d", file=out)
            print("##", file=out)
            print("", file=out)
            print("", file=out)
            print("", file=out)
            for i in range(NEDOS):
                print("%9.5f " % ENG[i], file=out, end="")
                for l in range(0, 3):
                    print("%9.5f " % LDOS_ALL[i, l, atom, spin], file=out, end="")
                print("")
