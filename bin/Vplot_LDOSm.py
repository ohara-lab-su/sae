#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vplot_LDOSm.py
#
#  Wplot_LDOSm.py (2015.04.22とほぼ同等になるように作成)
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
import os
#import gzip
import optparse
#import numpy as np

#import re
#from copy import deepcopy

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

import matplotlib.pyplot as plt
import matplotlib.cm as cm
#import matplotlib.mlab as mlab

################################################################################
def options():

    dname = 'DOSCAR'
    oname = 'OUTCAR'
    atom = 1 # 0版から始まる

    parser = optparse.OptionParser()
    parser.add_option( '-d','--doscar', dest='DOSCAR', default=dname,)
    parser.add_option( '-o', '--outcar', dest='OUTCAR', default=oname,)
    parser.add_option( '-a', '--atom', )
    parser.add_option( '--up', action='store_true', default=False,)
    parser.add_option( '--down', action='store_true', default=False,)
    parser.add_option( '--all', dest='ALL',action='store_true', default=False,)
    parser.add_option( '-n', '--nw', action='store_true', default=False,)
    parser.add_option( '--emax', dest='EMAX',)
    parser.add_option( '--emin', dest='EMIN',)
    parser.add_option( '--ymax', dest='YMAX',)
    options,  args = parser.parse_args()

    if options.DOSCAR: dname=options.DOSCAR
    if options.OUTCAR: oname=options.OUTCAR
    if options.atom: atom = int(options.atom)
    if options.ALL: options.nw = True
    if len(args) > 0: atom = int(args[0])

    return [dname,oname,atom,\
            options.nw,options.ALL,\
            options.up,options.down,\
            options.EMAX,options.EMIN,options.YMAX]

################################################################################
if __name__ == '__main__':

    #####################################################
    # set input file
    dname,oname,atom,\
            NO_WINDOW_FLAG,ALL_FLAG,\
            OPT_UP,OPT_DN,\
            OPT_EMAX,OPT_EMIN,OPT_YMAX = options()

    #####################################################
    # オプションの確認
    if OPT_EMAX: print "Emax=",OPT_EMAX
    if OPT_EMIN: print "Emin=",OPT_EMIN
    if OPT_YMAX: print "Ymax=",OPT_YMAX

    if OPT_UP:
        print "SPIN-UP"
        spin=0
    elif OPT_DN:
        print "SPIN-DOWN"
        spin=1
    else:
        print "NONMAGNETIC"
        spin=0

    atom -= 1

    #####################################################
    # makes instance ( Read DOSCAR )
    dos = SAE.ReadVaspDoscar(dname)

    nspin = dos.get_ispin()
    natom = dos.get_natom()
    title =  dos.get_title()
    efermi = dos.get_efermi()
    eng = dos.get_eng()

    FLAG_SPIN = False
    if nspin >=2:
        FLAG_SPIN = True

    #####################################################
    # makes instance ( Read OUTCAR )
    if os.path.exists(oname) or os.path.exists(oname+'.gz'):
        FLAG_OUTCAR=True
        outcar = SAE.ReadVaspOutcar(oname)
        atoms = outcar.get_atoms_index()
        atoms_j = outcar.get_atoms_j()
#       for atom in range(natom):
#           print atom,atoms_j[atom], atoms[atoms_j[atom]]
#       print ""

    #####################################################
    # makes label
    if FLAG_OUTCAR:
        atom_label =str(atoms[atoms_j[atom]])+str(atom+1)
        if nspin == 1:
            print "atom =",atom+1,atom_label
        else:
            print "atom(spin) =",atom+1,"("+str(spin+1)+")",atom_label
    else:
        atom_label =str(atom)
        if nspin == 1:
            print "atom =",atom+1
        else:
            print "atom(spin) =",atom+1,"("+str(spin+1)+")"

    #####################################################
    print "IONS: ",atoms
    if ALL_FLAG:
        a1 = 0
        a2 = natom
    else:
        a1 = int(atom)
        a2 = int(atom)+1

    for atom in range(a1,a2):

        #####################################################
        #
        plt.rcParams['font.size']         = 18
        plt.rcParams['legend.fontsize']   = 10
        plt.rcParams['axes.linewidth']    = 1.5
        plt.figure(figsize=(7.00, 9.89))  # for portrait

        orgx = 0.150
        orgy = 0.080
        off = 0.034
        xsize = 0.75
        ysize = 0.74/4

        #####################################################
        # plot TDOS
        plt.axes([ orgx,orgy, xsize, ysize ])
        tdos = dos.get_tdos(spin)
        plt.plot(eng-efermi,tdos, color="black", linewidth=2, label='total')
        plt.axvline(x=0,color="black",linewidth=1)

        leg = plt.legend(fontsize=12)
        leg.get_frame().set_alpha(0.5)

        xl = plt.xlabel("$E -  E_{\mathrm{F}}$ [eV]", fontsize=20 )
        yl = plt.ylabel("DOS/eV", fontsize=20 )
        plt.ylim( ymin=0 )
        if OPT_EMAX:
            plt.xlim( xmax=int(OPT_EMAX) )
        if OPT_EMIN:
            plt.xlim( xmin=int(OPT_EMIN) )
        if OPT_YMAX:
            plt.ylim( ymax=int(OPT_YMAX) )

        orgy = orgy + ysize + off

        #####################################################
        # plot LDOS
        orbit_list = ['s','p','d']
        j=1
        for orbit in range(0,3): # s(0),p(1),d(2)

            plt.axes([ orgx,orgy, xsize, ysize ])
            c = cm.prism(j*20/4)
            ldos = dos.get_ldos(orbit,atom,spin)
            plt.plot(eng-efermi,ldos, linestyle="-", \
                    color=c, linewidth=2, label=atom_label+"-"+orbit_list[orbit])
            plt.axvline(x=0,color="black",linewidth=1)

            leg = plt.legend(fontsize=12)
            leg.get_frame().set_alpha(0.5)

            plt.xticks([])
            plt.ylabel("")
            plt.ylim( ymin=0 )
            if OPT_EMAX:
                plt.xlim( xmax=int(OPT_EMAX) )
            if OPT_EMIN:
                plt.xlim( xmin=int(OPT_EMIN) )
            if OPT_YMAX:
                plt.ylim( ymax=int(OPT_YMAX) )

            orgy = orgy + ysize + off
            j += 1
        #####################################################

        if FLAG_SPIN:
            if OPT_UP:
                plt.title(title+"  spin-up ("+str(atom_label)+") ",fontsize=18)
            if OPT_DN:
                plt.title(title+"  spin-down ("+str(atom_label)+") ",fontsize=18)
        else:
            plt.title(title+"  ("+str(atom_label)+") ",fontsize=18)

#       plt.xlim([-10,10])
#       plt.ylim([0,200])

        plt.savefig("LDOS"+str(atom+1)+".eps")
        plt.savefig("LDOS"+str(atom+1)+".pdf")
        plt.savefig("LDOS"+str(atom+1)+".png")

        if not NO_WINDOW_FLAG:
            plt.show()

        plt.close('all')
        # atom END
        #####################################################

################################################################################
