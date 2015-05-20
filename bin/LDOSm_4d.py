#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# LDOS.py 
#
# Vplot_LDOSm.py (2015.04.22 ベース)
# Simple 化 nonmag版
#
################################################################################
#
# 2015.04.22
#    startup
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
__version__    = "0.0.5"
################################################################################

#import sys
#import os
#import gzip
import optparse
import numpy as np

#import re
#from copy import deepcopy

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

import matplotlib.pyplot as plt
import matplotlib.cm as cm
#import matplotlib.mlab as mlab

################################################################################
def options():

    atom = 1 # 0版から始まる

    parser = optparse.OptionParser()
    parser.add_option( '-a', '--atom', )
    parser.add_option( '--emax', dest='EMAX',)
    parser.add_option( '--emin', dest='EMIN',)
    options,  args = parser.parse_args()

    if options.atom:
        atom = options.atom

    if len(args) > 0:
        atom = int(args[0])

    return [atom,options.EMAX,options.EMIN]

################################################################################
if __name__ == '__main__':

    #####################################################
    #
    nspin = 1 # non-spin( nspin=1 ), spin( nspin=2 )
    spin = 0  # non-spin/up-spin( spin=0 ), dn-spin( spin=1 )

    #####################################################
    # set input file
    atom,OPT_EMAX,OPT_EMIN = options()

    #####################################################
    # オプションの確認

    title = 'VASP 4d-periodic(FCC)'
    output = 'LDOS_periodic_4d_FCC_atom'

    EMAX0 = 10
    EMIN0 = -10

    # if 0 ,automatic mode
    ymax_tdos = 0
    ymax_ldos = 7

#   orbit = 0 # s
#   orbit = 1 # p
    orbit = 2 # d

    #####################################################

    dname_list = [ 'Mo/FCC_NM_3.81',
                   'Tc/FCC_NM_3.81',
                   'Ru/FCC_NM_3.81',
                   'Rh/FCC_NM_3.81',
                   'Pd/FCC_NM_3.81',
                   'Ag/FCC_NM_3.81' ]


    #####################################################

    if OPT_EMAX:
        pass
       #print "Emax=",OPT_EMAX
    else:
        OPT_EMAX = EMAX0

    if OPT_EMIN:
        pass
       #print "Emin=",OPT_EMIN
    else:
        OPT_EMIN = EMIN0

    print "Emin=",OPT_EMIN
    print "Emax=",OPT_EMAX
    atom -= 1

    #####################################################
    #
    plt.rcParams['font.size']         = 18
    plt.rcParams['legend.fontsize']   = 10
    plt.rcParams['axes.linewidth']    = 1.5
    plt.figure(figsize=(7.00, 9.89))  # for portrait

    orgx = 0.150
    orgy = 0.082
    off = 0.020
    xsize = 0.75
    ysize = 0.78/len(dname_list)

    #####################################################
    #
    j=0
    for dname in dname_list:

        plt.axes([ orgx,orgy, xsize, ysize ])

        dname = dname+'/DOSCAR'
        print "DOSCAR: ",dname

        dos = SAE.ReadDoscar(dname)
        eng = dos.get_eng() - dos.get_efermi()

        c = cm.prism(j*20/4)
        ldos = dos.get_tdos(spin)
       #ldos = dos.get_ldos(orbit,atom,spin)
        plt.plot(eng,ldos, color=c, linewidth=1, label=dname)
        plt.axvline(x=0,color="black",linewidth=1)

#       leg = plt.legend(fontsize=12,bbox_to_anchor=(orgx,orgy+ysize*4),loc='lower left')
        leg = plt.legend(fontsize=8,loc='upper right')
        leg.get_frame().set_alpha(0.5)

        xl = plt.xlabel("$E -  E_{\mathrm{F}}$ [eV]", fontsize=20 )
        yl = plt.ylabel("DOS/eV", fontsize=20 )
        plt.ylim( ymin=0 )

        if ymax_ldos > 0 :
            plt.ylim( 0, float(ymax_ldos) )
        if OPT_EMAX:
            plt.xlim( xmax=float(OPT_EMAX) )
        if OPT_EMIN:
            plt.xlim( xmin=float(OPT_EMIN) )

        if j != 0:
            plt.xticks([])
            plt.xlabel("")
            plt.ylabel("")

        orgy = orgy + ysize + off
        j+=1

    plt.title(title,fontsize=16)
    plt.savefig(output+str(atom+1)+".eps")
    plt.savefig(output+str(atom+1)+".pdf")
    plt.savefig(output+str(atom+1)+".png")

    plt.show()
    plt.close('all')

################################################################################
