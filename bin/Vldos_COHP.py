#!/usr/bin/env python
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
# 2015.09.03
#    startup
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

import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE

################################################################################
def options():

    name = 'DOSCAR.lobster'

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT')
    options,  args = parser.parse_args()

    if options.INPUT: name=options.INPUT
    if len(args) > 0: name=args[0]

    return name

################################################################################
if __name__ == '__main__':

    # set input file
    name = options()
#   dos = SAEnv.ReadVaspDoscar(name)
    dos = SAEnv.ReadLobDos(name)

    # set output device
    out = sys.stdout

    NSPIN = dos.ispin
    LORBIT = dos.lorbit
    NATOM = dos.natom
    TITLE =  dos.title
    EMAX = dos.emax
    EMIN = dos.emin
    NEDOS = dos.nedos
    EFERMI = dos.efermi
    ENG = dos.eng

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

        for i in range(NEDOS):
            print "%9.5f %9.5f %9.5f " %( ENG[i],TDOS[i],INTTDOS[i] )

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
                print >> out, "%9.5f " %( ENG[i] ),
                for l in range(0,3):
                    print >> out, "%9.5f " \
                            % ( LDOS_ALL[i,l,atom,spin] ),
                print ""


################################################################################
