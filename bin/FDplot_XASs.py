#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
#   *_{1,2,3,,,}_conv.txt plot program
#
#  allsite で出力した XAS の結果(_conv.txt) をまとめてプロット
#
#
################################################################################
#
# 2015.07.01 fdXAS startup
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
#import optparse
import argparse
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

#   parser = optparse.OptionParser()
    parser = argparse.ArgumentParser()
    parser.add_argument(  '-i','--input', dest='INPUT',)
    parser.add_argument(  '--emax',)
    parser.add_argument(  '--emin',)
    parser.add_argument(  '--ymax',)
    parser.add_argument(  '-f','--fermi', action='store_true',default=False,)
    parser.add_argument(  '-o','--obs', action='store_true',default=False,)
    parser.add_argument(  '-a','--average', nargs='*')
#   options,args = parser.parse_args()
    options = parser.parse_args()

    if options.INPUT: name=options.INPUT
#   if len(args) > 0: name=args[0]

    if not os.path.exists(name):
        name = 'conv.inp'

    return name,options.emax,options.emin,options.ymax,\
            options.fermi,options.obs,\
            options.average

###############################################################################
if __name__ == '__main__':

    inpname,OPT_EMAX,OPT_EMIN,OPT_YMAX,\
            FLAG_fermi,FLAG_OBS,AV = options()

    if not AV:
        sys.exit("STOP: plase input absorber number (potion: -a)")

    if OPT_EMAX:
        OPT_EMAX=float(OPT_EMAX)
        print "Emax     =",OPT_EMAX
    if OPT_EMIN:
        OPT_EMIN=float(OPT_EMIN)
        print "Emin     =",OPT_EMIN
    if OPT_YMAX:
        OPT_YMAX=float(OPT_YMAX)
        print "Ymax     =",OPT_YMAX


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

    calculation = inp.get_calculation()
    if calculation:
        filout = calculation.replace('.txt','')
    else:
        filout = inp.get_filout()

    print "INP FILE  = ",inpname
    print "DATA FILE = ",filout

    ## 計算結果の読み込み
    if AV:
        txt = SAE.ReadFdmTxt(filout+'_'+str(AV[0]),'.txt')
    else:
        txt = SAE.ReadFdmTxt(filout,'.txt')

    print "E_edge   =",txt.E_edge
    print "E_fermi  =",txt.E_Fermi


    filbav = inp.get_filout()
    if filbav is None:
        sys.exit("STOP: fileout TAG not found in "+inpname)


    print "-----"
    for ab in range(len(AV)):
        filout = filbav+'_'+str(ab+1)
        convname = filout+'_conv.txt'
        print convname
        if not os.path.exists(convname):
            sys.exit("STOP: "+convname+" not found")

        conv = SAE.ReadFdmConv(filout,'_conv.txt')

        # XASエネルギー原点の変換 (*.txt ファイルおよび *_conv.txt 読み込み)
        if not inp.get_energygpho() and not FLAG_fermi:
            txt.eng = txt.eng + txt.E_edge
            conv.eng = conv.eng  + txt.E_edge

        if inp.get_energygpho() and FLAG_fermi:
            txt.eng = txt.eng - txt.E_Fermi - txt.E_edge
            conv.eng = conv.eng - txt.E_Fermi - txt.E_edge

        if not inp.get_energygpho() and FLAG_fermi:
            txt.eng = txt.eng - txt.E_Fermi
            conv.eng = conv.eng - txt.E_Fermi

        ########################################################################
    #   plt.subplot()
        plt.subplot(2,1,2)

        plt.plot(conv.eng,conv.xas,linewidth=1,label='absorber='+str(ab+1))
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

        if OPT_EMAX: plt.xlim( xmax=float(OPT_EMAX))
        if OPT_EMIN: plt.xlim( xmin=float(OPT_EMIN))
        if OPT_YMAX: plt.ylim( ymax=float(OPT_YMAX))

        xas_xmin,xas_xmax,xas_ymin,xas_ymax = plt.axis()

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

