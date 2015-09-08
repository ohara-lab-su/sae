#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
#   特定原子の PDOS 多段組
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
    parser.add_option('-i','--inpname', dest='INPUT')
    parser.add_option('-f','--filout')
    parser.add_option('-a','--atom')
    parser.add_option('--emax')
    parser.add_option('--emin')
    parser.add_option('--label')
    parser.add_option('-b', '--broad', action='store_true', default=False)
    parser.add_option('-x', '--xas', action='store_true', default=False)
    parser.add_option('--fermi', action='store_true', default=False)
    parser.add_option('--sp', action='store_true', default=False)
    parser.add_option('--spd', action='store_true', default=False)
    options,args = parser.parse_args()

    if options.INPUT: inpname=options.INPUT
    if len(args) > 0: inpname=args[0]

    return [inpname, options.filout, options.atom, options.label,
            options.emax, options.emin,
            options.broad, options.fermi, options.xas,
            options.sp, options.spd]

################################################################################
if __name__ == '__main__':

    inpname, filout, atom, LABEL,\
            OPT_EMAX, OPT_EMIN,\
            FLAG_BROAD, FLAG_FERMI, FLAG_XAS,\
            FLAG_SP, FLAG_SPD = options()

    if FLAG_BROAD: FLAG_XAS = True
    if OPT_EMAX: print "Emax=", OPT_EMAX
    if OPT_EMIN: print "Emin=", OPT_EMIN
    if atom: print "ATOM=", atom

    if not atom: atom = 0

    suffix_sd = '_sd'+str(atom)+'.txt'
    suffix_conv = '_conv.txt'

    ###########################################################################

    plt.rcParams['font.family']     = 'Times New Roman'
    plt.rcParams['font.size']       = 15  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize'] = 10  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']  = 1.4 # 軸の太さを設定。目盛りは変わらない

    plt.figure(figsize=(7.00, 9.89))  # for portrait

    orgx = 0.170
    orgy = 0.080
    off = 0.016
    xsize = 0.75
    ysize0 = 0.81

    ###########################################################################

    # for default
    list1_1=['s']
    list1_2=['p_y','p_z','p_x']
    list1_3=['d_xy','d_yz','d_3z2-r2','d_xz','d_x2-y2']
    list1 = [list1_1, list1_2, list1_3]

    # for hexagonal (s-orbital and p-orbital MODE)
    list4_1=['s']
    list4_2=['p_z']
    list4_3=['p_y','p_x']
    list4 = [list4_1, list4_2, list4_3]

    if FLAG_SPD:
        print "ORBITAL MODE: Default Orbitals"
        block_list = list1
    elif FLAG_SP:
        print "ORBITAL MODE: s-orbital and p-orbital"
        block_list = list4
    else:
        print "ORBITAL MODE: Default Orbitals"
        block_list = list1

    nblock = len(block_list)
    if FLAG_XAS:
        ysize = ysize0/(nblock+1)
    else:
        ysize = ysize0/(nblock)

    ###########################################################################

    inp = SAEnv.ReadFdmInp(inpname)
    if not filout: filout = inp.filout

#   bav = SAE.ReadFdmBav(filout)
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

    ############################################ convert Energy (set eng_off)
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

    EF0 = txt.E_edge + txt.E_Fermi

    ######################################### plot XAS
    num = 0
    if FLAG_XAS:
        plt.axes([orgx, orgy, xsize, ysize])

        xas = conv.get_xas()
        engx = conv.get_eng() + eng_off

        label = 'XAS (with broadening)'
        color = cm.prism((num+1)*10)

        plt.plot(engx, xas, linewidth=2, color='black', label=label)
        plt.ticklabel_format(axis='x', useOffset=False)
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

        plt.xlabel("Photon Energy [eV]")
#       plt.xlabel("Energy above Fermi [eV]")
        plt.ylabel("Absorption [arb. unit]")

        orgy = orgy + ysize + off

    ######################################### plot LDOS
    spin = 0
    XTICKS_FLAG = True
    for blk in range(nblock-1,-1,-1):

        plt.axes([orgx, orgy, xsize, ysize])
        lm_list = block_list[blk]

        for orbit in lm_list:

            print "orbit = ",orbit
            dos = sd.get_pdos(lm=orbit,spin=spin)
            eng = sd.get_eng() + eng_off

            num += 1
            if not LABEL:
                label = str(atom)+'-'+orbit
            else:
                label = str(LABEL)+'-'+orbit
            color = cm.prism((num+1)*10)

            plt.plot(eng, dos, linewidth=2, color=color, label=label)
            plt.ticklabel_format(axis='x', useOffset=False)
            plt.axvline(x=EF0, color='black', linewidth=1)
            if OPT_EMAX: plt.xlim(xmax=float(OPT_EMAX))
            if OPT_EMIN: plt.xlim(xmin=float(OPT_EMIN))

            if XTICKS_FLAG and not FLAG_XAS:
#               plt.xlabel("Energy above Fermi [eV]")
                plt.xlabel("Photon Energy [eV]")
                XTICKS_FLAG  = False

            leg = plt.legend(loc='upper right')
            leg.get_frame().set_alpha(0.5)

        if blk == 1: plt.ylabel("DOS [state/eV]")
        if blk == 2 and FLAG_XAS: plt.xticks([])
        if not blk == 2: plt.xticks([])

        orgy = orgy + ysize + off


#   plt.ylabel("Absorption [arb. unit]")

    plt.savefig("PDOS"+str(atom)+".eps")
    plt.savefig("PDOS"+str(atom)+".pdf")
    plt.savefig("PDOS"+str(atom)+".png")

    plt.show()

    plt.close('all')

#   print "NAME",name


