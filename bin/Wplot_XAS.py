#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Wplot_XAS.py
#
# wplot_XAS_K, wplot_XAS_L の基本アイデアを踏襲
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.04.06
#  plot 部分を分離 plot_sum_xas() と plot_xas() に分離
#
# 2015.03.27 (sat)
#  startup
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
import os
#import gzip
import re
import optparse
#import numpy as np

#from copy import deepcopy

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
def options():

    name = re.sub('.*/','',os.getcwd())

    parser = optparse.OptionParser(os.getcwd())
    parser.add_option( '-i', '--input', dest='INPUT',)
    parser.add_option( '--emax', dest='EMAX',)
    parser.add_option( '--emin', dest='EMIN',)
    parser.add_option( '--ymax', dest='YMAX',)
    options,  args = parser.parse_args()

    if options.INPUT: name = options.INPUT

    return [name,\
            options.EMAX,options.EMIN,options.YMAX]

################################################################################
if __name__ == '__main__':

    # set input file
    case,EMAX,EMIN,YMAX = options()

    ############################################
    # check SPIN
    if os.path.exists(case+'.output0'):
        output0_file = case+'.output0'
    elif os.path.exists(case+'.output0.gz'):
        output0_file = case+'.output0.gz'
    elif os.path.exists(case+'.output0000'):
        output0_file = case+'.output0000'
    elif os.path.exists(case+'.output0000.gz'):
        output0_file = case+'.output0000.gz'
    else:
        sys.exit("STOP: output0 file not found")

    output0 = SAE.ReadWienOutput0(output0_file)
    nspin = output0.get_ispin()
#   nion = output0.get_nion()
#   atoms_index = output0.get_atoms_index()

    FLAG_SPIN = False
    if nspin >= 2:
        FLAG_SPIN = True

    FLAG_SHOW=True
    dos_suffix = '.dos1ev'
    txspec_suffix = '.txspec'
    xspec_suffix = '.xspec'
    outname='XAS'

    if not FLAG_SPIN:
        SAE.plot_xas(case=case,\
                dos_suffix=dos_suffix,\
                txspec_suffix=txspec_suffix,\
                xspec_suffix=xspec_suffix,\
                outname=outname,\
                OPT_EMAX=EMAX,OPT_EMIN=EMIN,OPT_YMAX=YMAX,FLAG_SHOW=FLAG_SHOW)
    else:
        for i in [ 'up', 'dn' ]:
            print("=== "+str(i))
            FLAG_SHOW=False
            SAE.plot_xas(case=case,\
                    dos_suffix=dos_suffix+str(i),\
                    txspec_suffix=txspec_suffix+str(i),\
                    xspec_suffix=xspec_suffix+str(i),\
                    outname=outname+str(i),\
                    OPT_EMAX=EMAX,OPT_EMIN=EMIN,OPT_YMAX=YMAX,FLAG_SHOW=FLAG_SHOW)

        print("=== up+dn")
        FLAG_SHOW=True
        outname='XAS'
        SAE.plot_sum_xas(case=case,dos_suffix=dos_suffix,outname=outname,\
                    OPT_EMAX=EMAX,OPT_EMIN=EMIN,OPT_YMAX=YMAX,FLAG_SHOW=FLAG_SHOW)


