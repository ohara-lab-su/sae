#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
#  sd*.txt plot program
#  multiplot version
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.08.18 startup
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
#import optparse
import argparse
#import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

import matplotlib.pyplot as plt


################################################################################
def options():

#   parser = optparse.OptionParser()
    parser = argparse.ArgumentParser()
    parser.add_argument(  '--emax',)
    parser.add_argument(  '--emin',)
#   options,args = parser.parse_args()
    options = parser.parse_args()

    return options.emax,options.emin

################################################################################
if __name__ == '__main__':

    ###########################################################################
    OPT_EMAX,OPT_EMIN = options()
    if OPT_EMAX:
        OPT_EMAX=float(OPT_EMAX)
        print("Emax     =",OPT_EMAX)
    if OPT_EMIN:
        OPT_EMIN=float(OPT_EMIN)
        print("Emin     =",OPT_EMIN)
    ###########################################################################
    plt.rcParams['font.family']     = 'Times New Roman'
    plt.rcParams['font.size']       = 16  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize'] = 14  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']  = 1.5 # 軸の太さを設定。目盛りは変わらない
    ###########################################################################


    ###########################################################################
    # multiplot 設定
    fig = plt.figure(figsize=(7.00, 9.89)) # for portrait
    f0 = fig.add_subplot(311)
    f1 = fig.add_subplot(312, sharex=f0)
    f2 = fig.add_subplot(313, sharex=f0)

    ###########################################################################
    # f0: sd0
    txt = SAE.ReadFdmTxt('BaTiO3_R3m')
    sd_sd0 = SAE.ReadFdmSd('BaTiO3_R3m',suffix='_sd0.txt',inpname='read_pdb.inp')

    ef = txt.E_edge + txt.E_fermi
    dos_s_sd0 = sd_sd0.get_ldos(l='s')
    dos_p_sd0 = sd_sd0.get_ldos(l='p')

    f0.plot(sd_sd0.eng+txt.E_edge,dos_p_sd0,color='red',linewidth=1,label='sd0, Ba-p')
    f0.axvline(x=ef,color='black',linewidth=1)

    f0.set_ylabel("LDOS [stat/eV]")
#   f0.set_xlabel("Photon Energy [eV]")
    l0 = f0.legend(loc='upper right')
    l0.get_frame().set_alpha(0.5)
    f0.ticklabel_format(axis='x',useOffset=False)


    ###########################################################################
    # f1: sd1
#   txt = SAE.ReadFdmTxt(BASE+'BaTiO3_R3m')
    sd_sd1 = SAE.ReadFdmSd('BaTiO3_R3m',suffix='_sd1.txt',inpname='read_pdb.inp')

#   ef = txt.E_edge + txt.E_fermi
    dos_s_sd1 = sd_sd1.get_ldos(l='s')
    dos_p_sd1 = sd_sd1.get_ldos(l='p')

    f1.plot(sd_sd1.eng+txt.E_edge,dos_p_sd1,color='red',linewidth=1,label='sd1, Ba-p')
    f1.axvline(x=ef,color='black',linewidth=1)

    f1.set_ylabel("LDOS [stat/eV]")
#   f1.set_xlabel("Photon Energy [eV]")
    l1 = f1.legend(loc='upper right')
    l1.get_frame().set_alpha(0.5)
    f1.ticklabel_format(axis='x',useOffset=False)

    ###########################################################################
    # f2: sd2
#   txt = SAE.ReadFdmTxt(BASE+'BaTiO3_R3m')
    sd_sd2 = SAE.ReadFdmSd('BaTiO3_R3m',suffix='_sd2.txt',inpname='read_pdb.inp')

#   ef = txt.E_edge + txt.E_fermi
    dos_s_sd2 = sd_sd2.get_ldos(l='s')
    dos_p_sd2 = sd_sd2.get_ldos(l='p')

    f2.plot(sd_sd2.eng+txt.E_edge,dos_p_sd2,color='red',linewidth=1,label='sd2, Ti-p')
    f2.axvline(x=ef,color='black',linewidth=1)

    f2.set_ylabel("LDOS [stat/eV]")
#   f2.set_xlabel("Photon Energy [eV]")
    l2 = f2.legend(loc='upper right')
    l2.get_frame().set_alpha(0.5)
    f2.ticklabel_format(axis='x',useOffset=False)




#   l1 = plt.legend(fontsize=12,loc='lower right')
#   l1 = plt.legend(loc='lower right')

    if OPT_EMAX:
        plt.xlim( xmax=float(OPT_EMAX))
    if OPT_EMIN:
        plt.xlim( xmin=float(OPT_EMIN))

    plt.savefig("LDOSmulti.eps")
    plt.savefig("LDOSmulti.pdf")
    plt.savefig("LDOSmulti.png")

    plt.show()

    plt.close('all')

#   print "NAME",name


