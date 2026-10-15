#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# vLDOSmulti.py
#
# Vplot_LDOSm.py (2015.04.22 ベース)
# 超 Simple 化 nonmag版
# ---> subplot 版
#
# Mac OS X 上で Vldos.py と名前の重複注意
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.06.15
#    startup
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
__version__    = "0.0.5"
################################################################################

#import sys
#import os
#import gzip
import optparse
import numpy as np

#import re
#from copy import deepcopy

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

import matplotlib.pyplot as plt
import matplotlib.cm as cm
#import matplotlib.mlab as mlab

################################################################################
def options():

    parser = optparse.OptionParser()
    parser.add_option( '--emax', dest='EMAX',)
    parser.add_option( '--emin', dest='EMIN',)
    options,  args = parser.parse_args()

    return options.EMAX,options.EMIN

################################################################################
if __name__ == '__main__':


    #####################################################
    OPT_EMAX,OPT_EMIN = options()
    #####################################################
    plt.rcParams['font.size']         = 16
    plt.rcParams['legend.fontsize']   = 12
    plt.rcParams['axes.linewidth']    = 1.5
    #####################################################

    # multiplot 設定
    fig = plt.figure(figsize=(7.00, 9.89))  # for portrait
    f1 = fig.add_subplot(211)
    f2 = fig.add_subplot(212, sharex=f1)

    #####################################################
    dos = SAE.ReadVaspDoscar('DOSCAR')
    eng = dos.eng - dos.efermi
    tdos = dos.get_tdos(spin='nonmag')
    ldos = dos.get_ldos(l='p',atom=0,spin='nonmag')


    ################################################## 一段目
    f1.plot(eng,ldos, linewidth=1, label='ldos')

    f1.axvline(x=0,color="black",linewidth=1)
    f1.set_ylabel("DOS/eV", fontsize=20 )
    f1.set_ylim( ymin=0 )
    l1 = f1.legend(fontsize=12,loc='upper left')
    l1.get_frame().set_alpha(0.5)

    ################################################## 二段目
    f2.plot(eng,tdos, linewidth=1, label='tdos')

    f2.axvline(x=0,color="black",linewidth=1)
    f2.set_xlabel("$E -  E_{\mathrm{F}}$ [eV]", fontsize=20 )
    f2.set_ylabel("DOS/eV", fontsize=20 )
    f2.set_ylim( ymin=0 )
    l2 = f2.legend(fontsize=12,loc='upper left')
    l2.get_frame().set_alpha(0.5)


    if OPT_EMAX:
        plt.xlim( xmax=float(OPT_EMAX) )
    if OPT_EMIN:
        plt.xlim( xmin=float(OPT_EMIN) )

    plt.savefig('LDOSm'+".eps")
    plt.savefig('LDOSm'+".pdf")
    plt.savefig('LDOSm'+".png")

    plt.show()
    plt.close('all')

################################################################################
