#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vplot_LDOSm.py
#
#  Wplot_LDOSm.py (2015.04.22とほぼ同等になるように作成)
#
#   atom は 1 番から(内部的には0番からなので内部的に変換する)
#
##########################################################################
#
# 2015.09.15
#  両スピンモード(上下分割で反転表示)を追加
#
# 2015.04.22
#    startup
#
##########################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
#
__status__ = "alpha"
__version__ = "0.0.5"
##########################################################################

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

##########################################################################


def options():

    dname = 'DOSCAR'
    oname = 'OUTCAR'
    atom = 1  # 0版から始まる

    parser = optparse.OptionParser()
    parser.add_option('-d', '--doscar', dest='DOSCAR', default=dname,)
    parser.add_option('-o', '--outcar', dest='OUTCAR', default=oname,)
    # atom は 1 番から(内部的には0番からなので内部的に変換する)
    parser.add_option('-a', '--atom', )
    parser.add_option('--sp', action='store_true', default=False)
    parser.add_option('--up', action='store_true', default=False)
    parser.add_option('--down', action='store_true', default=False)
    parser.add_option('--spin', action='store_true', default=False)
    parser.add_option('--all', dest='ALL', action='store_true', default=False,)
    parser.add_option('-n', '--nw', action='store_true', default=False,)
    parser.add_option('--emax', dest='EMAX',)
    parser.add_option('--emin', dest='EMIN',)
    parser.add_option('--ymax', dest='YMAX',)
    options,  args = parser.parse_args()

    ## 注意)
    ## all モードは描画せずに、ファイルだけ全部出力するモード

    if options.DOSCAR: dname = options.DOSCAR
    if options.OUTCAR: oname = options.OUTCAR
    if options.atom: atom = int(options.atom)
    if options.ALL: options.nw = True
    if len(args) > 0:
        atom = int(args[0])

    return [dname, oname, atom,
            options.nw, options.ALL,
            options.sp,
            options.up, options.down, options.spin,
            options.EMAX, options.EMIN, options.YMAX]

##########################################################################
if __name__ == '__main__':

    #####################################################
    # set input file
    dname, oname, atom,\
        FLAG_NW, ALL_FLAG,\
        FLAG_SP,\
        FLAG_UP, FLAG_DN, FLAG_SPIN,\
        OPT_EMAX, OPT_EMIN, OPT_YMAX = options()

    #####################################################
    # オプションの確認
    if OPT_EMAX: print "Emax=", OPT_EMAX
    if OPT_EMIN: print "Emin=", OPT_EMIN
    if OPT_YMAX: print "Ymax=", OPT_YMAX

    atom -= 1

    orgx = 0.150
    orgy = 0.080
    off = 0.015
    xsize = 0.75
    ysize0 = 0.71

    #####################################################
    # plot する l軌道のリスト
    if FLAG_SP:
        orbit_list = ['s','p']
    else:
        orbit_list = ['s','p','d']

#   orbit_list = ['s','p','d','f']

    norbit0 = len(orbit_list)

    #####################################################
    # makes instance ( Read DOSCAR )
    dos = SAE.ReadVaspDoscar(dname)

    natom = dos.natom
    title = dos.title
    efermi = dos.efermi
    eng = dos.eng

    #####################################################
    nspin = dos.ispin

    print "NSPIN = ",nspin

    FLAG_SPIN = False
    norbit = norbit0
    if FLAG_UP:
        print "SPIN-UP"
        spin = 0
        spin_list = [0]
        spin_name = ['_up','']
        spin_out = '_up'
    elif FLAG_DN:
        print "SPIN-DOWN"
        spin = 1
        spin_list = [1]
        spin_name = ['','_dn']
        spin_out = '_dn'
    elif FLAG_SPIN or nspin >=2:
        print "BOTH SPIN ( UP, DOWN-SPIN )"
        spin = 1
        spin_list = [1,0]
        spin_name = ['_up','_dn']
        spin_out = '_spin'
        norbit = norbit0 * 2
        FLAG_SPIN = True
    else:
        print "NONMAGNETIC or SPIN-UP "
        spin = 0
        spin_list = [0]
        spin_name = ['']
        spin_out = ''

    ysize = ysize0 / (norbit+1)

    #####################################################
    # 原子種の名前をゲットかのうならばゲットする
    if os.path.exists(oname) or os.path.exists(oname + '.gz'):
        FLAG_OUTCAR = True
        outcar = SAE.ReadVaspOutcar(oname)
        atoms_index_j = outcar.atoms_index_j

#       atoms = outcar.get_atoms_index()
#       atoms_j = outcar.get_atoms_j()
#       for atom in range(natom):
#           print atom,atoms_j[atom], atoms[atoms_j[atom]]
#       print ""

    #####################################################
    # makes label
    if FLAG_OUTCAR:
#       atom_label = str(atoms[atoms_j[atom]]) + str(atom + 1)
        atom_label = atoms_index_j[atom] + str(atom + 1)
        print "atom =", atom + 1, atom_label+spin_out
    else:
        atom_label = str(atom)
        print "atom =", atom + 1, atom_label+spin_out

    #####################################################
    if ALL_FLAG:
        a1 = 0
        a2 = natom
    else:
        a1 = int(atom)
        a2 = int(atom) + 1

    print "plot atom number: #"+str(a1)+" - #"+str(a2)

    for atom in range(a1, a2):

        #####################################################
        #
        plt.rcParams['font.size'] = 15
        plt.rcParams['legend.fontsize'] = 10
        plt.rcParams['axes.linewidth'] = 1.5
        plt.figure(figsize=(7.00, 9.89))  # for portrait


        XTICKS_FLAG = False
        #####################################################
        # plot TDOS
        for spin in spin_list:

            plt.axes([orgx, orgy, xsize, ysize])

            tdos = dos.get_tdos(spin)

            # makes label
            label='total'+spin_name[spin]

            # !!!!! plot TDOS !!!!!
            plt.plot(eng - efermi, tdos, color="black", linewidth=2, label=label)
            plt.axvline(x=0, color="black", linewidth=1)

            # ytics の調整
            if FLAG_SPIN:
                plt.locator_params(axis='y', nbins=4)

            # makes xticks
            if not XTICKS_FLAG:
                xl = plt.xlabel("$E -  E_{\mathrm{F}}$ [eV]", fontsize=15)
                yl = plt.ylabel("DOS/eV", fontsize=15)
                XTICKS_FLAG = True
            else:
                plt.xticks([])

            # down spin 反転
            if FLAG_SPIN and spin == 1:
                xmin_dn, xmax_dn, ymin_dn, ymax_dn = plt.axis()
                plt.ylim([ymax_dn,0])
            else:
                plt.ylim(ymin=0)

            if OPT_EMAX: plt.xlim(xmax=float(OPT_EMAX))
            if OPT_EMIN: plt.xlim(xmin=float(OPT_EMIN))
            if OPT_YMAX: plt.ylim(ymax=float(OPT_YMAX))

            leg = plt.legend(fontsize=12)
            leg.get_frame().set_alpha(0.5)

            orgy = orgy + ysize
        orgy = orgy + off

        #####################################################
        # plot LDOS
        j = 1
        for orbit in range(len(orbit_list)):

            for spin in spin_list:

                plt.axes([orgx, orgy, xsize, ysize])

                d = dos.get_ldos(orbit, atom, spin)
                e = eng - efermi

                # makes color & label
                c = cm.prism(j * 20 / norbit0)
                lab = atom_label +"_"+orbit_list[orbit]+spin_name[spin]

                # !!!!! plot LDOS !!!!!
                plt.plot(e, d, linestyle="-", color=c, linewidth=2, label=lab)
                plt.axvline(x=0, color="black", linewidth=1)

                # ytics の調整
                if FLAG_SPIN:
                    plt.locator_params(axis='y', nbins=4)

                # makex xticks
                if spin == 0:
                    plt.ylim(ymin=0)
                    xmin_up, xmax_up, ymin_up, ymax_up = plt.axis()
                    plt.ylim([0,ymax_up])

                # DOS: down spin 反転
                if FLAG_SPIN and spin == 1:
                    xmin_dn, xmax_dn, ymin_dn, ymax_dn = plt.axis()
                    plt.ylim([ymax_dn,0])

                leg = plt.legend(fontsize=12)
                leg.get_frame().set_alpha(0.5)

                plt.xticks([])
                plt.ylabel("")

                if OPT_EMAX: plt.xlim(xmax=float(OPT_EMAX))
                if OPT_EMIN: plt.xlim(xmin=float(OPT_EMIN))
                if OPT_YMAX: plt.ylim(ymax=float(OPT_YMAX))

                orgy = orgy + ysize
            orgy = orgy +off
            j += 1

        #####################################################

        # makes title
#       if FLAG_SPIN:
#           if FLAG_UP:
#               plt.title(title + "  spin-up (" +
#                         str(atom_label) + ") ", fontsize=18)
#           if FLAG_DN:
#               plt.title(title + "  spin-down (" +
#                         str(atom_label) + ") ", fontsize=18)
#       else:
#           plt.title(title + "  (" + str(atom_label) + ") ", fontsize=18)

#       plt.xlim([-10,10])
#       plt.ylim([0,200])

        plt.savefig("LDOS" + str(atom + 1) + spin_out + ".eps")
        plt.savefig("LDOS" + str(atom + 1) + spin_out + ".pdf")
        plt.savefig("LDOS" + str(atom + 1) + spin_out + ".png")

        if not FLAG_NW:
            plt.show()

        plt.close('all')
        # atom END
        #####################################################

##########################################################################
