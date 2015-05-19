#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vband.py
#
#  calss ReadEigenval を用いた Vband.pl の同等品
#
################################################################################
#
# 2015.01.27 startup 
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

    name = 'EIGENVAL'
    out1 = 'band1.dat'
    out2 = 'band2.dat'
                                                                                
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

    return [name,out1,out2]

################################################################################
if __name__ == '__main__':

    name,out1,out2 = options()

    band = SAE.ReadEigenval(name)

    NATOM = band.get_natom()
    TITLE = band.get_title()
    NKPTS = band.get_nkpts()
    NBANDS = band.get_nbands()
    NSPIN = band.get_ispin()

    eigenval = band.get_eigenval()

    for ispin in range(NSPIN):
        if ispin == 0:
            outfile = out1
        else:
            outfile = out2

        try:
            out = open(outfile,'w')
        except:
            out.cloase()
            sys.exit("STOP:"+outfile+" can't open")

        for j in range(NBANDS):
            print >> out, ""
            print >> out, ""
            print >> out, ""
            print >> out, "## ISPIN = ",NSPIN
            print >> out, "## SPIN  = ",ispin
            print >> out, "## NBAND = ",NBANDS
            print >> out, "## BAND  = ",j
            print >> out, "## EF    = "
            print >> out, ""
            print >> out, ""
            print >> out, ""
            for k in range(NKPTS):
                print >> out, "%5d %14.8f" %( k+1, eigenval[j,k,ispin] )

        out.close()

################################################################################
     
