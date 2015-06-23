#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# vLDOSs.py
#
# Vplot_LDOSm.py (2015.04.22 ベース)
# 超 Simple 化 nonmag版
#
# Mac OS X 上で Vldos.py と名前の重複注意
#
################################################################################
#
# 2015.06.15
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

    atom = 1 # 0版から始まる

    parser = optparse.OptionParser()
    parser.add_option( '-a', '--atom', )
    parser.add_option( '--emax', dest='EMAX',)
    parser.add_option( '--emin', dest='EMIN',)
    options,  args = parser.parse_args()

    if options.atom:
        atom = options.atom

    if len(args) > 0:
        atom = int(args[0])

    return [atom,options.EMAX,options.EMIN]

################################################################################
if __name__ == '__main__':

    #####################################################
    #
    nspin = 1 # non-spin( nspin=1 ), spin( nspin=2 )
    spin = 0  # non-spin/up-spin( spin=0 ), dn-spin( spin=1 )

    #####################################################
    # set input file
    atom,OPT_EMAX,OPT_EMIN = options()
    atom -= 1  # 原子種の番号を0番からスタートの変換する

    #####################################################
    # オプションの確認
    title = 'ZrO2'
    output = 'LDOS'

#   orbit = 0 # s
#   orbit = 1 # p
    orbit = 2 # d

    #####################################################
    #
    plt.rcParams['font.size']         = 18
    plt.rcParams['legend.fontsize']   = 10
    plt.rcParams['axes.linewidth']    = 1.5
    plt.figure(figsize=(7.00, 9.89))  # for portrait

    orgx = 0.150
    orgy = 0.082
    xsize = 0.75
    ysize = 0.55
    off = 0.020

    plt.axes([ orgx,orgy, xsize, ysize ])

    #####################################################
    dos = SAE.ReadDoscar('05_layer/relax/DOSCAR')
    eng = dos.get_eng() - dos.get_efermi()
    tdos = dos.get_tdos()
    ldos = dos.get_ldos(orbit,atom,spin)
    plt.plot(eng,tdos, linewidth=1, label='total 05-layer')

    dos = SAE.ReadDoscar('06_layer/relax/DOSCAR')
    eng = dos.get_eng() - dos.get_efermi()
    tdos = dos.get_tdos()
    ldos = dos.get_ldos(orbit,atom,spin)
    plt.plot(eng,tdos, linewidth=1, label='total 06-layer')

    dos = SAE.ReadDoscar('07_layer/relax/DOSCAR')
    eng = dos.get_eng() - dos.get_efermi()
    tdos = dos.get_tdos()
    ldos = dos.get_ldos(orbit,atom,spin)
    plt.plot(eng,tdos, linewidth=1, label='total 07-layer')


    #####################################################
    plt.axvline(x=0,color="black",linewidth=1)
    xl = plt.xlabel("$E -  E_{\mathrm{F}}$ [eV]", fontsize=20 )
    yl = plt.ylabel("DOS/eV", fontsize=20 )
    plt.ylim( ymin=0 )
    #####################################################

#   leg = plt.legend(fontsize=12,bbox_to_anchor=(orgx,orgy+ysize*4),loc='lower left')
    leg = plt.legend(fontsize=8,loc='upper right')
    leg.get_frame().set_alpha(0.5)

    if OPT_EMAX:
        plt.xlim( xmax=float(OPT_EMAX) )
    if OPT_EMIN:
        plt.xlim( xmin=float(OPT_EMIN) )

    plt.title(title,fontsize=16)
    plt.savefig(output+str(atom+1)+".eps")
    plt.savefig(output+str(atom+1)+".pdf")
    plt.savefig(output+str(atom+1)+".png")

    plt.show()
    plt.close('all')

################################################################################
