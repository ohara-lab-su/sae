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
#import optparse
import argparse
#import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

import matplotlib.pyplot as plt


################################################################################
def options():

    name = 'read_pdb.inp'

#   parser = optparse.OptionParser()
    parser = argparse.ArgumentParser()
    parser.add_argument(  '-i','--input', dest='INPUT',)
    parser.add_argument(  '--emax',)
    parser.add_argument(  '--emin',)
    parser.add_argument(  '--dmax',)
#   options,args = parser.parse_args()
    options = parser.parse_args()

    if options.INPUT: name=options.INPUT

#   if len(args) > 0: name=args[0]

    return name,options.emax,options.emin,options.dmax

################################################################################
if __name__ == '__main__':

    inpname,OPT_EMAX,OPT_EMIN,OPT_DMAX = options()

    if OPT_EMAX:
        OPT_EMAX=float(OPT_EMAX)
        print "Emax     =",OPT_EMAX
    if OPT_EMIN:
        OPT_EMIN=float(OPT_EMIN)
        print "Emin     =",OPT_EMIN
    if OPT_DMAX:
        OPT_DMAX=float(OPT_DMAX)
        print "Ymax(DOS)=",OPT_DMAX

    suffix='_sd0.txt'

    ###########################################################################
#   inp = SAE.ReadFdmInp(inpname)
#   filout = inp.get_filout()
#   ispin = inp.get_ispin()
#   txt = SAE.ReadFdmTxt(name0,'.txt')
#   bav = SAE.ReadFdmBav(name0)
    ###########################################################################

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


#   E_edge   = 24350.0
#   E_fermi  = -5.82491

    E_edge   = 0.0
    E_fermi  = 0.0
    EF0 = E_edge + E_fermi

    ###########################################################################
    sd = SAE.ReadFdmSd('Pd6/Pd6',inpname='Pd6/read_pdb.inp',\
                        absorber=(1,2,3,4,5),weight=6.0)
    dos = sd.get_ldos(l='p')
    plt.plot(sd.eng+E_edge,dos,linewidth=2,label='absorber LDOS (p)')
    ###########################################################################
#   sd = SAE.ReadFdmSd('Pd19/R5_fdm/allsite/Pd19',absorber=(1,2,3),weight=3.0)
#   dos = sd.get_ldos(l='p')
#   plt.plot(sd.eng,dos,linewidth=1,label='Pd19:absorber LDOS (p)')
    ###########################################################################

#   plt.xlabel("Energy above Fermi [eV]")
#   plt.ylabel("Absorption [arb. unit]")
    plt.ylabel("LDOS [stat/eV]")
#   plt.axvline(x=0,color='black',linewidth=1)
    plt.axvline(x=EF0,color='black',linewidth=1)

    plt.ticklabel_format(axis='x',useOffset=False)
#   leg = plt.legend(fontsize=12,loc='lower right')
#   leg = plt.legend(loc='lower right')
    leg = plt.legend(loc='upper right')
    leg.get_frame().set_alpha(0.5)

    if OPT_EMAX:
        plt.xlim( xmax=float(OPT_EMAX))
    if OPT_EMIN:
        plt.xlim( xmin=float(OPT_EMIN))
    if OPT_DMAX:
        plt.ylim( ymax=float(OPT_DMAX))

    plt.savefig("LDOS.eps")
    plt.savefig("LDOS.pdf")
    plt.savefig("LDOS.png")

    plt.show()

    plt.close('all')

#   print "NAME",name


