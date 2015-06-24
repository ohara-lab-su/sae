#!/usr/bin/env python
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
#   *_conv.txt plot program
#    ファイル名自動判別を付け加えただけの基本的な XAS plot
#
#   fdXAS.py のゴージャス版
#   fdXAS は書き換えるのを前提としたスクリプト(小文字系)
#
################################################################################
#
# 2015.06.24
#  実験データもプロット可能に
#
# 2015.06.23
#  DOSもプロット可能に
#
# 2015.06.19 FDplot_XAS startup
#
# 2015.05.21 fdXAS startup
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

import sys
#import gzip
import os
#import re
import optparse
#import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

#from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import matplotlib.ticker as ptick


################################################################################
def options():

    name = 'read_pdb.inp'
#   name = 'POSCAR.inp'

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT',)
    parser.add_option(  '--emax',)
    parser.add_option(  '--emin',)
    parser.add_option(  '--ymax',)
    parser.add_option(  '--dmax',)
    parser.add_option(  '-f','--fermi', action='store_true',default=False,)
    parser.add_option(  '-b','--broad', action='store_true',default=False,)
    parser.add_option(  '-d','--dos', action='store_true',default=False,)
    parser.add_option(  '-o','--obs', action='store_true',default=False,)
    options,args = parser.parse_args()

    if options.INPUT: name=options.INPUT
    if len(args) > 0: name=args[0]

    return name,options.emax,options.emin,options.ymax,options.dmax,\
            options.fermi,options.broad,options.dos,options.obs

###############################################################################
if __name__ == '__main__':

    inpname,OPT_EMAX,OPT_EMIN,OPT_YMAX,OPT_DMAX,\
            FLAG_fermi,FLAG_B,FLAG_DOS,FLAG_OBS = options()

    if OPT_EMAX:
        OPT_EMAX=float(OPT_EMAX)
        print "Emax     =",OPT_EMAX
    if OPT_EMIN:
        OPT_EMIN=float(OPT_EMIN)
        print "Emin     =",OPT_EMIN
    if OPT_YMAX:
        OPT_YMAX=float(OPT_YMAX)
        print "Ymax     =",OPT_YMAX
    if OPT_DMAX:
        OPT_DMAX=float(OPT_DMAX)
        print "Ymax(DOS)=",OPT_DMAX

#   eng = conv.get_eng()
#   xas = conv.get_xas()

    plt.rcParams['font.family']     = 'Times New Roman'
    plt.rcParams['font.size']       = 16  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize'] = 14  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']  = 1.5 # 軸の太さを設定。目盛りは変わらない

#   plt.figure(figsize=(7.00, 9.89))  # for portrait
    plt.figure(figsize=(8.10, 9.89))  # for portrait

#   orgx = 0.170
#   orgy = 0.080
#   off = 0.010
#   xsize = 0.75
#   ysize = 0.83/2.
#   plt.axes([orgx,orgy,xsize,ysize])


    ############################################################################
    inp = SAE.ReadFdmInp(inpname)
    filout = inp.get_filout()

    txt = SAE.ReadFdm(filout,'.txt')
    conv = SAE.ReadFdmConv(filout,'_conv.txt')
    sd = SAE.ReadFdmSd(filout,'_sd0.txt')
    bav = SAE.ReadFdmBav(filout,'_bav.txt')

    print "E_edge   =",txt.E_edge
    print "E_fermi  =",txt.E_Fermi

    # XASエネルギー原点の変換
    if not inp.get_energygpho() and not FLAG_fermi:
        txt.eng = txt.eng + txt.E_edge
        conv.eng = conv.eng  + txt.E_edge

    if inp.get_energygpho() and FLAG_fermi:
        txt.eng = txt.eng - txt.E_Fermi - txt.E_edge
        conv.eng = conv.eng - txt.E_Fermi - txt.E_edge

    if not inp.get_energygpho() and FLAG_fermi:
        txt.eng = txt.eng - txt.E_Fermi
        conv.eng = conv.eng - txt.E_Fermi

    ############################################################################
    ## XAS plot
    if FLAG_DOS:
        plt.subplot(3,1,2)
    else:
#       plt.subplot()
        plt.subplot(2,1,2)

    if not FLAG_B:
        plt.plot(txt.eng,txt.xas,color='green',linewidth=1,label='XAS')
    plt.plot(conv.eng,conv.xas,color='red',linewidth=3,label='XAS broad')

    plt.ticklabel_format(axis='x',useOffset=False)
#   plt.ticklabel_format(axis='x',style='plain')

#   if FLAG_fermi:
#       plt.xlabel("Energy above Fermi [eV]")
#   else:
#       plt.xlabel("Photon Energy [eV]")
    plt.ylabel("Absorption [arb. unit]")

    EF0 =txt.E_edge + txt.E_fermi
    if FLAG_fermi:
        plt.axvline(x=0,color='black',linewidth=1)
    else:
        plt.axvline(x=EF0,color='black',linewidth=1)


#   leg = plt.legend(fontsize=12,loc='lower right')
    leg = plt.legend(loc='lower right')
    leg.get_frame().set_alpha(0.5)

    if OPT_EMAX:
        plt.xlim( xmax=float(OPT_EMAX))
    if OPT_EMIN:
        plt.xlim( xmin=float(OPT_EMIN))
    if OPT_YMAX:
        plt.ylim( ymax=float(OPT_YMAX))

    xas_xmin,xas_xmax,xas_ymin,xas_ymax = plt.axis()

    ############################################################################
    ## DOS plot
    if FLAG_DOS:
        plt.subplot(3,1,3)

        dos_p = sd.get_ldos(l='p')
        plt.plot(conv.eng,dos_p,linewidth=1,label='absorber-LDOS(p)')
        plt.ticklabel_format(axis='x',useOffset=False)

        dos_s = sd.get_ldos(l='s')
        plt.plot(conv.eng,dos_s,linewidth=1,label='absorber-LDOS(s)')
        plt.ticklabel_format(axis='x',useOffset=False)

        plt.ylabel("DOS [stat/eV]")
        if FLAG_fermi:
            plt.axvline(x=0,color='black',linewidth=1)
        else:
            plt.axvline(x=EF0,color='black',linewidth=1)

    #   leg = plt.legend(fontsize=12,loc='lower right')
        leg = plt.legend(loc='upper right')
        leg.get_frame().set_alpha(0.5)

        if OPT_EMAX:
            plt.xlim( xmax=float(OPT_EMAX))
        if OPT_EMIN:
            plt.xlim( xmin=float(OPT_EMIN))
        if OPT_DMAX:
            plt.ylim( ymax=float(OPT_DMAX))

    if FLAG_fermi:
        plt.xlabel("Energy above Fermi [eV]")
    else:
        plt.xlabel("Photon Energy [eV]")

    ############################################################################
    # Athena data plot
    if FLAG_OBS:
        obs_file = filout+'_obs.txt.nor'
        if not os.path.exists(obs_file):
            sys.exit("STOP: "+obs_file+" not found")

        nor = SAE.ReadAthenaNor(obs_file)
        if FLAG_DOS:
            plt.subplot(3,1,1)
        else:
            plt.subplot(2,1,1)

        plt.plot(nor.eng,nor.nor,label='obs.')
        plt.xlim([xas_xmin,xas_xmax])
        plt.ticklabel_format(axis='x',useOffset=False)

    #   leg = plt.legend(fontsize=12,loc='lower right')
    #   leg = plt.legend(loc='upper right')
        leg = plt.legend(loc='lower right')
        leg.get_frame().set_alpha(0.5)

    ############################################################################

    plt.savefig("XAS.eps")
    plt.savefig("XAS.pdf")
    plt.savefig("XAS.png")

    plt.show()

    plt.close('all')

#   print "NAME",name


