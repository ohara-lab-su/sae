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
#   スピン非対応
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
    parser.add_option('--emax')
    parser.add_option('--emin')
    parser.add_option('--label')
    parser.add_option('-b', '--broad', action='store_true', default=False)
    parser.add_option('-x', '--xas', action='store_true', default=False)
    # atom におけるl成分をすべて足す(total)
    parser.add_option('-t','--total', action='store_true', default=False)
    # total の積分
    parser.add_option('--inttotal', action='store_true', default=False)
    parser.add_option('--fermi', action='store_true', default=False)
    options,args = parser.parse_args()

    if options.INPUT: inpname = options.INPUT
    if len(args) > 0: inpname = args[0]

    return [inpname, options.filout,
            options.atom,  options.label,
            options.emax, options.emin,
            options.broad, options.fermi, options.xas,
            options.total, options.inttotal]

################################################################################
if __name__ == '__main__':

    inpname, filout, atom, LABEL,\
            OPT_EMAX, OPT_EMIN,\
            FLAG_BROAD, \
            FLAG_FERMI, FLAG_XAS, FLAG_TOTAL, FLAG_INTTOTAL = options()

    if FLAG_BROAD: FLAG_XAS = True
    if OPT_EMAX: print "Emax=", OPT_EMAX
    if OPT_EMIN: print "Emin=", OPT_EMIN

    if not atom: atom = 0
    spin = 0

    suffix_sd = '_sd'+str(atom)+'.txt'
    suffix_conv = '_conv.txt'

    ###########################################################################
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

    if FLAG_TOTAL:
        norbit = len(orbit_list)+1
    else:
        norbit = len(orbit_list)

    if FLAG_XAS:
        ysize = ysize0/(norbit+1)
    else:
        ysize = ysize0/(norbit)

    ###########################################################################

    inp = SAEnv.ReadFdmInp(inpname)
    if not filout: filout = inp.filout

#   bav = SAE.ReadFdmBav(name0)
    txt = SAEnv.ReadFdm(filout,'.txt')
    conv = SAEnv.ReadFdmConv(filout, suffix_conv)
    sd0 = SAEnv.ReadFdmSd(filout, '_sd0.txt')
    sd = SAEnv.ReadFdmSd(filout, suffix_sd)

    ispin = inp.ispin

    if not OPT_EMAX:
        emax = sd.emax
        emax0 = sd0.emax
        if emax0 > emax: emax = emax0
        print "EMAX = ",emax

    if not OPT_EMIN:
        emin = sd.emin
        emin0 = sd0.emin
        if emin0 < emin: emin = emin0
        print "EMIN = ",emin

    ################################################ convert Energy
    # PhotoEnegy モードで計算した時と同じ結果を返す
    if not inp.get_energygpho() and not FLAG_FERMI:
        print "current mode is Fermi"
        print "---> convert to PhotoEnergy"
        print "     + E_edge"
        eng_off =  txt.E_edge

    # E_fermi を引く(A) : A=B
    if not inp.get_energygpho() and FLAG_FERMI:
        print "current mode is Fermi"
        print "---> subtract E_fermi"
        print "     - E_fermi"
        eng_off = - txt.E_fermi

    # E_fermi を引く(B) : A=B
    if inp.get_energygpho() and FLAG_FERMI:
        print "current mode is PhotoEnergy"
        print "---> convert to EF0 mode"
        print "     - E_edge - E_fermi"
        eng_off - txt.E_Fermi - txt.E_edge

    if FLAG_FERMI:
        EF0 = 0.0
        label_fermi = "Energy above Fermi [eV]"
    else:
        EF0 = txt.E_edge + txt.E_Fermi
        label_fermi = "Photon Energy [eV]"

    ######################################### plot XAS
    num = 0
    XTICKS_FLAG = False
    if FLAG_XAS:
        plt.axes([orgx, orgy, xsize, ysize])

        xas = conv.get_xas()
        engx = conv.get_eng() + eng_off

        label = 'XAS (with broadening)'
        color = cm.prism((num+1)*10)

        plt.plot(engx, xas, linewidth=2, color='black', label=label)
        plt.axvline(x=EF0, color='black', linewidth=1)
        xmin_XAS, xmax_XAS, ymin_XAS, ymax_XAS = plt.axis()
        if OPT_EMAX: plt.xlim(xmax=float(OPT_EMAX))
        if OPT_EMIN: plt.xlim(xmin=float(OPT_EMIN))

        if FLAG_BROAD:
            dos_p = txt.xas
            eng_p = txt.eng + eng_off
            plt.plot(eng_p, dos_p, linewidth=1, color=color, label='XAS')
            plt.ylim(ymax=ymax_XAS)

        leg = plt.legend(loc='lower right')
        leg.get_frame().set_alpha(0.5)

        # label & xticks
        plt.ylabel("Absorption [arb. unit]")
        if not XTICKS_FLAG:
            plt.xlabel(label_fermi)
            XTICKS_FLAG = True

        orgy = orgy + ysize + off

    ######################################### plot TDOS / atom
    #
    eng = sd.get_eng() + eng_off
    if FLAG_TOTAL:
        plt.axes([orgx, orgy, xsize, ysize])

        tdos = sd.get_tdos(spin=spin)

        num += 1
        color = cm.prism((num+1)*10)

        plt.plot(eng, tdos, linewidth=2, color=color, label='total')
        plt.axvline(x=EF0, color='black', linewidth=1)
        if OPT_EMAX: plt.xlim(xmax=float(OPT_EMAX))
        if OPT_EMIN: plt.xlim(xmin=float(OPT_EMIN))

        # label & xticks
        if not XTICKS_FLAG:
            plt.xlabel(label_fermi)
            XTICKS_FLAG = True
        else:
            plt.xticks([])

        orgy = orgy + ysize + off

    ######################################### plot LDOS / atom
    #
    orb = 0
    for orbit in orbit_list:
        plt.axes([orgx, orgy, xsize, ysize])

        dos = sd.get_ldos(l=orbit, spin=spin)

        num += 1
        if LABEL:
            label = LABEL+'-'+orbit
        else:
            label = str(atom)+'-'+orbit
        color = cm.prism((num+1)*10)

        plt.plot(eng, dos, linewidth=2, color=color, label=label)
        plt.axvline(x=EF0, color='black', linewidth=1)
        if OPT_EMAX: plt.xlim(xmax=float(OPT_EMAX))
        if OPT_EMIN: plt.xlim(xmin=float(OPT_EMIN))

        # label & xticks
        if orb == 0: plt.ylabel("DOS [state/eV]")
        if not XTICKS_FLAG:
            plt.xlabel(label_fermi)
            XTICKS_FLAG = True
        else:
            plt.xticks([])

        leg = plt.legend(loc='upper right')
        leg.get_frame().set_alpha(0.5)

        orb += 1
        orgy = orgy + ysize + off

    #########################################

    if FLAG_FERMI:
        fermi='_fermi'
    else:
        fermi=''

    plt.savefig("LDOS"+str(atom)+fermi+".eps")
    plt.savefig("LDOS"+str(atom)+fermi+".pdf")
    plt.savefig("LDOS"+str(atom)+fermi+".png")

    plt.show()

    plt.close('all')

#   print "NAME",name


