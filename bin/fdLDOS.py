#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
# *_conv.txt plot program
#
################################################################################
#
# 2015.05.21 startup
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

#import sys
#import gzip
#import os
#import re
import optparse
#import numpy as np

import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE

import matplotlib.pyplot as plt


################################################################################
def options():

    name = 'read_pdb.inp'

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT',)
    parser.add_option(  '-a','--atom',)
    parser.add_option(  '-l',)
    options,args = parser.parse_args()

    if options.INPUT:
        name=options.INPUT

    if len(args) > 0:
        name=args[0]

    return name,options.atom,options.l

################################################################################
if __name__ == '__main__':

    inpname,atom,orbit = options()

    if not atom:
        atom=1
    suffix_sd = '_sd'+str(atom)+'.txt'

    if not orbit:
        orbit=1

    inp = SAEnv.ReadFdmInp(inpname)
    name0 = inp.get_filout()

    ###########################################################################
#   txt = SAEnv.ReadFdmTxt(name0,'.txt')
#   bav = SAEnv.ReadFdmBav(name0)
    sd = SAEnv.ReadFdmSd(name0, suffix_sd)
    ###########################################################################

    ispin = inp.get_ispin()

    dos = sd.get_ldos(l=orbit)
    eng = sd.get_eng()

    plt.rcParams['font.family']     = 'Times New Roman'
    plt.rcParams['font.size']       = 16  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize'] = 14  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']  = 1.5 # 軸の太さを設定。目盛りは変わらない

    plt.figure(figsize=(7.00, 9.89))  # for portrait

    orgx = 0.170
    orgy = 0.080
    off = 0.010
    xsize = 0.75
    ysize = 0.83/2.

    plt.axes([orgx,orgy,xsize,ysize])

    plt.plot(eng, dos, linewidth=2, label='DOS')

#   plt.xlabel("Energy above Fermi [eV]")
#   plt.ylabel("Absorption [arb. unit]")
    plt.axvline(x=0, color='black', linewidth=1)

#   leg = plt.legend(fontsize=12,loc='lower right')
#   leg = plt.legend(loc='lower right')
    leg = plt.legend(loc='upper right')
    leg.get_frame().set_alpha(0.5)

#   plt.savefig("XAS.eps")
#   plt.savefig("XAS.pdf")
#   plt.savefig("XAS.png")

    plt.show()

    plt.close('all')

#   print "NAME",name


