#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
#   特定原子の LDOS 多段組
#
################################################################################
#
# 2015.09.07
#  startup
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
import optparse
#import numpy as np

import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE

import matplotlib.pyplot as plt
import matplotlib.cm as cm


################################################################################
def options():

    inpname = 'read_pdb.inp'

    parser = optparse.OptionParser()
    parser.add_option('-i','--inpname', dest='INPUT',)
    parser.add_option('-f','--filout')
    parser.add_option('-a','--atom',)
    parser.add_option('-l','--orbit',)
    parser.add_option('--fermi', action='store_true', default=False)
    options,args = parser.parse_args()

    if options.INPUT: inpname=options.INPUT
    if len(args) > 0: inpname=args[0]

    return [inpname,options.filout,
            options.atom,options.orbit,
            options.fermi]

################################################################################
if __name__ == '__main__':

    inpname,filout,atom,orbit,FLAG_fermi = options()

    if not atom:
        atom=0
    suffix_sd = '_sd'+str(atom)+'.txt'
    suffix_conv = '_conv.txt'

    if not orbit:
        orbit=1

    inp = SAEnv.ReadFdmInp(inpname)
    ispin = inp.ispin
    if not filout:
        filout = inp.filout

    ###########################################################################
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
    ysize0 = 0.83

    ###########################################################################

    orbit_list = ['s','p','d']
    norbit = len(orbit_list)
    ysize = ysize0/(norbit)

    num = 0

    ###########################################################################

    txt = SAEnv.ReadFdm(filout,'.txt')
    conv = SAEnv.ReadFdmConv(filout, suffix_conv)
    sd0 = SAEnv.ReadFdmSd(filout, '_sd0.txt')

    ################################################ convert Energy
    # PhotoEnegy モードで計算した時と同じ結果を返す
    if not inp.get_energygpho() and not FLAG_fermi:
        print "current mode is Fermi"
        print "---> convert to PhotoEnergy"
        print "     + E_edge"
        eng_off =  txt.E_edge

    # E_fermi を引く(A) : A=B
    if not inp.get_energygpho() and FLAG_fermi:
        print "current mode is Fermi"
        print "---> subtract E_fermi"
        print "     - E_fermi"
        eng_off = - txt.E_fermi

    # E_fermi を引く(B) : A=B
    if inp.get_energygpho() and FLAG_fermi:
        print "current mode is PhotoEnergy"
        print "---> convert to EF0 mode"
        print "     - E_edge - E_fermi"
        eng_off - txt.E_Fermi - txt.E_edge

    EF0 = txt.E_edge + txt.E_Fermi

    ######################################### plot LDOS
    #
    sd = SAEnv.ReadFdmSd(filout, suffix_sd)
    for orbit in orbit_list:
        plt.axes([orgx, orgy, xsize, ysize])

        dos = sd.get_ldos(l=orbit)
        eng = sd.get_eng() + eng_off

        num += 1
        label = str(atom)+'-'+orbit
        color = cm.prism((num+1)*10)

        plt.plot(eng, dos, linewidth=2, color=color, label=label)
        plt.axvline(x=EF0, color='black', linewidth=1)

        plt.xticks([])
        leg = plt.legend(loc='upper right')
        leg.get_frame().set_alpha(0.5)

        orgy = orgy + ysize + off

#   plt.xlabel("Energy above Fermi [eV]")
#   plt.ylabel("Absorption [arb. unit]")

    plt.savefig("LDOS"+str(atom)+".eps")
    plt.savefig("LDOS"+str(atom)+".pdf")
    plt.savefig("LDOS"+str(atom)+".png")

    plt.show()

    plt.close('all')

#   print "NAME",name


