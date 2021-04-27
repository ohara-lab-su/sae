#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
# *_conv.txt plot program
#
# Athena のデーターと一緒に比較する
#
################################################################################
#
# 2015.06.30
#  == None --> is None
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
import os
#import re
import optparse
#import numpy as np

import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE

import matplotlib.pyplot as plt


################################################################################
def options():

    name = 'POSCAR_conv.txt'

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT',)
    options,args = parser.parse_args()

    if not os.path.exists(name):
        name0 = SAEnv.find_datfile1('_conv.txt')
        if name0 is None:
            name0 = name
    name = name0

    if options.INPUT: name=options.INPUT
    if len(args) > 0: name=args[0]

    return name

################################################################################
if __name__ == '__main__':

#   name = options()

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


    #######################################################
#   conv = SAEnv.ReadFdmConv('Au_conv_Fermi.txt')
    #######################################################

#   E_edge = 0.0

#   times = 35
#   times = 1.0
    ###########################################################################
    conv = SAEnv.io.ReadFdmConv('Au', suffix='_conv.txt')
    txt = SAEnv.io.ReadFdmTxt('Au', suffix='.txt')
    plt.plot(conv.eng + txt.E_edge, conv.xas, color='red', linewidth=1, label='FDM Green R3')

    ###########################################################################
    nor = SAEnv.io.ReadAthenaNor('Q14B_Au001_Aufoil.txt.nor')
    plt.plot(nor.eng, nor.nor, color='blue', linewidth=1, label='exp.')
#   plt.plot(nor.eng - nor.e0 ,nor.nor,color='blue',linewidth=1,label='exp.')

#   timesP = 1.0
#   ###########################################################################
#   pw = SAEnv.ReadPwXanes('xanes.dat')
#   plt.plot(pw.eng+E_edge,pw.xas*timesP,color='green',linewidth=1,label='PWSCF fch')


#   plt.xlabel("Energy above Fermi [eV]")
    plt.xlabel("Photon Energy [eV]")
    plt.ylabel("Absorption [arb. unit]")

#   plt.axvline(x=0,color='black',linewidth=1)

    leg = plt.legend(fontsize=12,loc='lower right')
    leg.get_frame().set_alpha(0.5)

    plt.xlim( xmax=12100 )
    plt.xlim( xmin=11900 )

#   plt.xlim( xmax=200 )
#   plt.xlim( xmin=-10 )

    plt.ylim( ymin=0 )

#   plt.savefig("XAS.eps")
    plt.savefig("XAS.pdf")
#   plt.savefig("XAS.png")

    plt.show()

    plt.close('all')

#   print "NAME",name


