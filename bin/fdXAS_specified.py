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
# 2015.06.30
#  == None --> is None
#
# 2015.05.21 startup
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

#import sys
#import gzip
import os
#import re
import optparse
#import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

import matplotlib.pyplot as plt


################################################################################
def options():

    name = 'POSCAR'
    suffix = '_conv.txt'

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT',)
    options,args = parser.parse_args()

    if not os.path.exists(name):
        name0 = SAE.find_datfile1('_conv.txt')
        name0 = name0.replace(suffix,'')
        if name0 is None:
            name0 = name
        name = name0

    if options.INPUT: name=options.INPUT
    if len(args) > 0: name=args[0]

    return name,suffix

################################################################################
if __name__ == '__main__':

    name,suffix = options()
#   conv = SAE.ReadFdmConv(name)
#   eng = conv.get_eng()
#   xas = conv.get_xas()

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

#   E_edge   = 8979.0
    E_edge   = 0.0
    E_fermi  = -5.41217

#   conv = SAE.ReadFdmConv(name,suffix)

    conv = SAE.ReadFdmConv('R3.0/Au',suffix)
    plt.plot(conv.eng+E_edge,conv.xas,linewidth=2,label='XAS')


    plt.ticklabel_format(axis='x',useOffset=False)
    plt.xlabel("Energy above Fermi [eV]")
#   plt.xlabel("Photon Energy [eV]")
    plt.ylabel("Absorption [arb. unit]")

#   plt.axvline(x=0,color='black',linewidth=1)

    leg = plt.legend(fontsize=12,loc='lower right')
    leg.get_frame().set_alpha(0.5)

    plt.savefig("XAS.eps")
    plt.savefig("XAS.pdf")
    plt.savefig("XAS.png")

    plt.show()

    plt.close('all')

#   print "NAME",name


