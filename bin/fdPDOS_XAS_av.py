#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
#   特定原子の PDOS 多段組(FDplot_PDOS.py) をベースとした特化型スクリプト
#   複数のデータを読み込んで平均化して DOS と XAS をプロット
#   その都度編集せよ
#
################################################################################
#
# 2015.09.09
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

    parser = optparse.OptionParser()
    parser.add_option('-a', '--atom')
    parser.add_option('--emax')
    parser.add_option('--emin')
    parser.add_option('--ymax')
    parser.add_option('--dmax')
    parser.add_option('--label')
    parser.add_option('-o', '--outsuffix')
    parser.add_option('-b', '--broad', action='store_true', default=False)
    parser.add_option('-x', '--xas', action='store_true', default=False)
    parser.add_option('--fermi', action='store_true', default=False)
    parser.add_option('--sp', action='store_true', default=False)
    parser.add_option('--spd', action='store_true', default=False)
    parser.add_option('--dosweight',)  # for LDOS
    parser.add_option('--nw', action='store_true', default=False)
    options,args = parser.parse_args()

    return [options.atom, options.label, options.outsuffix,
            options.emax, options.emin, options.ymax, options.dmax,
            options.broad, options.fermi, options.xas,
            options.sp, options.spd, options.dosweight, options.nw]

################################################################################
if __name__ == '__main__':

    atom, LABEL, OUTSUFFIX,\
       OPT_EMAX, OPT_EMIN, OPT_YMAX, OPT_DMAX,\
       FLAG_BROAD, FLAG_FERMI, FLAG_XAS,\
       FLAG_SP, FLAG_SPD, WEDOS, FLAG_NW = options()

    if FLAG_BROAD: FLAG_XAS = True
    if OPT_EMAX: print "Emax=", OPT_EMAX
    if OPT_EMIN: print "Emin=", OPT_EMIN
    if FLAG_XAS and OPT_YMAX: print "Ymax(XAS)=", OPT_YMAX
    if OPT_DMAX: print "Ymax(DOS)=", OPT_DMAX
    if atom: print "ATOM=", atom

    if not atom: atom = 0

    if WEDOS:
        print "DOS Weight =",WEDOS
    else:
#       WEDOS = 1.0
        WEDOS = None

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

    fil_1 = 'R5_fdm_ad_on_67/ZrO2Pd'
    fil_2 = 'R5_fdm_ad_on_68/ZrO2Pd'
    fil_3 = 'R5_fdm_ad_on_72/ZrO2Pd'

    inp_1 = 'R5_fdm_ad_on_67/read_pdb.inp'
    inp_2 = 'R5_fdm_ad_on_68/read_pdb.inp'
    inp_3 = 'R5_fdm_ad_on_72/read_pdb.inp'

    inp = SAEnv.ReadFdmInp(inp_1)

    conv = SAEnv.ReadFdmConv(fil_1, suffix='_conv.txt')
    conv_2 = SAEnv.ReadFdmConv(fil_2, suffix='_conv.txt')
    conv_3 = SAEnv.ReadFdmConv(fil_3, suffix='_conv.txt')
    conv_1 = conv

    txt = SAEnv.ReadFdmTxt(fil_1, suffix='.txt')
    txt_2 = SAEnv.ReadFdmTxt(fil_2, suffix='.txt')
    txt_3 = SAEnv.ReadFdmTxt(fil_3, suffix='.txt')
    txt_1 = txt

    s_sd0 = '_sd0.txt'
    sd0_1 = SAEnv.ReadFdmSd(fil_1, inpname=inp_1, suffix=s_sd0, weight=WEDOS)
    sd0_2 = SAEnv.ReadFdmSd(fil_2, inpname=inp_2, suffix=s_sd0, weight=WEDOS)
    sd0_3 = SAEnv.ReadFdmSd(fil_3, inpname=inp_3, suffix=s_sd0, weight=WEDOS)

    s_sd = '_sd'+str(atom)+'.txt'
    sd_1 = SAEnv.ReadFdmSd(fil_1, inpname=inp_1, suffix=s_sd, weight=WEDOS)
    sd_2 = SAEnv.ReadFdmSd(fil_2, inpname=inp_2, suffix=s_sd, weight=WEDOS)
    sd_3 = SAEnv.ReadFdmSd(fil_3, inpname=inp_3, suffix=s_sd, weight=WEDOS)

    txt_xas_av = (txt_1.xas + txt_2.xas + txt_3.xas)/3.
    conv_xas_av = (conv_1.xas + conv_2.xas + conv_3.xas)/3.

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

        ##### average
        xas = conv_xas_av
        engx = conv.eng + eng_off
        #####

        label = 'XAS (with broadening)'
        color = cm.prism((num+1)*10)

        plt.plot(engx, xas, linewidth=2, color='black', label=label)
        plt.ticklabel_format(axis='x', useOffset=False)
        plt.axvline(x=EF0, color='black', linewidth=1)
        xmin_XAS, xmax_XAS, ymin_XAS, ymax_XAS = plt.axis()
        plt.ylim(ymin=0.0)
        if OPT_EMAX: plt.xlim(xmax=float(OPT_EMAX))
        if OPT_EMIN: plt.xlim(xmin=float(OPT_EMIN))
        if OPT_YMAX: plt.ylim(ymax=float(OPT_YMAX))

        if FLAG_BROAD:

            ##### average
            dos_p = txt_xas_av
            eng_p = txt.eng + eng_off
            #####

            plt.plot(eng_p, dos_p, linewidth=1, color=color, label='XAS')
            plt.ylim(ymax=ymax_XAS)
            plt.ylim(ymin=0.0)
            if OPT_EMAX: plt.xlim(xmax=float(OPT_EMAX))
            if OPT_EMIN: plt.xlim(xmin=float(OPT_EMIN))
            if OPT_YMAX: plt.ylim(ymax=float(OPT_YMAX))

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

        dmax0 = 0.0
        for orbit in lm_list:

            ####### average
            dos_1 = sd_1.get_pdos(lm=orbit, spin=spin)
            dos_2 = sd_2.get_pdos(lm=orbit, spin=spin)
            dos_3 = sd_3.get_pdos(lm=orbit, spin=spin)
            dos = ( dos_1 + dos_2 + dos_3 )/3.
            eng = sd_1.get_eng() + eng_off

            dmax_1 = sd_1.ymax
            dmax_2 = sd_2.ymax
            dmax_3 = sd_3.ymax
            dmax = max([dmax_1,dmax_2,dmax_3])
            #############

            if dmax0 < dmax:
                dmax0 = dmax

            num += 1
            if not LABEL:
                label = str(atom)+'-'+orbit
            else:
                label = str(LABEL)+'-'+orbit
            color = cm.prism((num+1)*10)

            plt.plot(eng, dos, linewidth=2, color=color, label=label)
            plt.ticklabel_format(axis='x', useOffset=False)
            plt.axvline(x=EF0, color='black', linewidth=1)
            plt.ylim(ymin=0.00)
            if not OPT_DMAX: plt.ylim(ymax=float(dmax0))
            if OPT_DMAX: plt.ylim(ymax=float(OPT_DMAX))
            if OPT_EMAX: plt.xlim(xmax=float(OPT_EMAX))
            if OPT_EMIN: plt.xlim(xmin=float(OPT_EMIN))
            xmin0, xmax0, ymin0, ymax0 = plt.axis()
            print orbit,": ymax =",dmax0,ymax0

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

    if OUTSUFFIX:
        plt.savefig("PDOS"+str(atom)+str(OUTSUFFIX)+".eps")
        plt.savefig("PDOS"+str(atom)+str(OUTSUFFIX)+".pdf")
        plt.savefig("PDOS"+str(atom)+str(OUTSUFFIX)+".png")
    else:
        plt.savefig("PDOS"+str(atom)+".eps")
        plt.savefig("PDOS"+str(atom)+".pdf")
        plt.savefig("PDOS"+str(atom)+".png")

    if not FLAG_NW:
        plt.show()

    plt.close('all')

#   print "NAME",name


