#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.vasp.doscar import ReadVaspDoscar

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
# 2018.08.15
#  Python2/3 両対応
#
# 2015.04.22
#    startup
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import optparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


#
################################################################################
#import sys
#import os
#import gzip
#import re
#from copy import deepcopy
#import SpaceGroupEnvironment as SGE
#import matplotlib.mlab as mlab
################################################################################
def options():
    # 0版から始まる
    atom = 1
    parser = optparse.OptionParser()
    parser.add_option("-a", "--atom")
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--emin", dest="EMIN")
    options, args = parser.parse_args()
    if options.atom:
        atom = options.atom
    if len(args) > 0:
        atom = int(args[0])
    return [atom, options.EMAX, options.EMIN]


################################################################################
#####################################################
#
#####################################################
# set input file
#####################################################
# オプションの確認
# if 0 ,automatic mode
#   orbit = 0 # s
#   orbit = 1 # p
#####################################################
#   dname_list = [ 'Sc/FCC_NM_3.61',
#                  'Ti/FCC_NM_3.61',
#                  'V/FCC_NM_3.61',
#                  'Cr/FCC_NM_3.61',
#                  'Mn/FCC_NM_3.61',
#                  'Fe/FCC_NM_3.61',
#                  'Co/FCC_NM_3.61',
#                  'Ni/FCC_NM_3.61',
#                  'Cu/FCC_NM_3.61' ]
#####################################################
#####################################################
#
#####################################################
if __name__ == "__main__":
    # non-spin( nspin=1 ), spin( nspin=2 )
    nspin = 1
    # non-spin/up-spin( spin=0 ), dn-spin( spin=1 )
    spin = 0
    atom, OPT_EMAX, OPT_EMIN = options()
    title = "VASP 3d-periodic (FCC)"
    output = "LDOS_periodic_3d_FCC_atom"
    EMAX0 = 10
    EMIN0 = -10
    ymax_tdos = 0
    ymax_ldos = 7
    # d
    orbit = 2
    dname_list = [
        "Cr/FCC_NM_3.61",
        "Mn/FCC_NM_3.61",
        "Fe/FCC_NM_3.61",
        "Co/FCC_NM_3.61",
        "Ni/FCC_NM_3.61",
        "Cu/FCC_NM_3.61",
    ]
    #print "Emax=",OPT_EMAX
    if OPT_EMAX:
        pass
    else:
        OPT_EMAX = EMAX0
    #print "Emin=",OPT_EMIN
    if OPT_EMIN:
        pass
    else:
        OPT_EMIN = EMIN0
    print("Emin=", OPT_EMIN)
    print("Emax=", OPT_EMAX)
    atom -= 1
    plt.rcParams["font.size"] = 18
    plt.rcParams["legend.fontsize"] = 10
    plt.rcParams["axes.linewidth"] = 1.5
    # for portrait
    plt.figure(figsize=(7.0, 9.89))
    orgx = 0.15
    orgy = 0.082
    xsize = 0.75
    ysize = 0.78 / len(dname_list)
    off = 0.02
    j = 0
    #####################################################
    #ldos = dos.get_ldos(orbit,atom,spin)
    #####################################################
    #       leg = plt.legend(fontsize=12,bbox_to_anchor=(orgx,orgy+ysize*4),loc='lower left')
    for dname in dname_list:
        plt.axes([orgx, orgy, xsize, ysize])
        dname = dname + "/DOSCAR"
        print("DOSCAR: ", dname)
        dos = ReadVaspDoscar(dname)
        eng = dos.get_eng() - dos.get_efermi()
        ldos = dos.get_tdos(spin)
        c = cm.prism(j * 20 / 4)
        plt.plot(eng, ldos, color=c, linewidth=1, label=dname)
        plt.axvline(x=0, color="black", linewidth=1)
        leg = plt.legend(fontsize=8, loc="upper right")
        leg.get_frame().set_alpha(0.5)
        xl = plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=20)
        yl = plt.ylabel("DOS/eV", fontsize=20)
        plt.ylim(ymin=0)
        if ymax_ldos > 0:
            plt.ylim(ymax=float(ymax_ldos))
        if OPT_EMAX:
            plt.xlim(xmax=float(OPT_EMAX))
        if OPT_EMIN:
            plt.xlim(xmin=float(OPT_EMIN))
        if j != 0:
            plt.xticks([])
            plt.xlabel("")
            plt.ylabel("")
        orgy = orgy + ysize + off
        j += 1
    plt.title(title, fontsize=16)
    plt.savefig(output + str(atom + 1) + ".eps")
    plt.savefig(output + str(atom + 1) + ".pdf")
    plt.savefig(output + str(atom + 1) + ".png")
    plt.show()
    plt.close("all")
