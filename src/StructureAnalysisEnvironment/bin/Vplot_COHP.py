#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vplot_COHP.py
#
##########################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.09.01
#  par ごとの出力モード追加
#
# 2015.06.05
#  startup
#
##########################################################################
from __future__ import print_function
################################################################################
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
#import os
#import gzip
#import optparse
import argparse
#import numpy as np

#import re
#from copy import deepcopy

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

import matplotlib.pyplot as plt
#import matplotlib.cm as cm
#import matplotlib.ticker as tic
#import matplotlib.mlab as mlab

##########################################################################


def options():

#   parser = optparse.OptionParser()
    parser = argparse.ArgumentParser()
#   parser.add_option('-n', '--nw', action='store_true', default=False,)
    parser.add_argument('-n', '--nw', action='store_true', default=False,)
    parser.add_argument('--emax', dest='EMAX',)
    parser.add_argument('--emin', dest='EMIN',)
    parser.add_argument('--dosmax', '--dmax', dest='DMAX',)
    parser.add_argument('--cohpmax', '--ymax', dest='YMAX',)
    parser.add_argument('--cohpmin', '--ymin', dest='YMIN',)
    parser.add_argument('-u', '--up', action='store_true', default=False)
    parser.add_argument('-d', '--dn', action='store_true', default=False)
    parser.add_argument('--spin', action='store_true', default=False)
    parser.add_argument('-p', '--pair', nargs='*')
#   options,  args = parser.parse_args()
    options = parser.parse_args()

    return [options.nw,
            options.DMAX,
            options.EMAX, options.EMIN, options.YMAX, options.YMIN,
            options.up, options.dn, options.spin, options.pair]

##########################################################################
if __name__ == '__main__':

    # set options file
    NO_WINDOW_FLAG,\
        OPT_DMAX, OPT_EMAX, OPT_EMIN, OPT_YMAX, OPT_YMIN, \
        OPT_UP, OPT_DN, OPT_SPIN, OPT_PAIR = options()

    if OPT_DMAX: print("Dmax= %s" % str(OPT_DMAX))
    if OPT_EMAX: print("Emax= %s" % str(OPT_EMAX))
    if OPT_EMIN: print("Emin= %s" % str(OPT_EMIN))
    if OPT_YMAX: print("Ymax= %s" % str(OPT_YMAX))
    if OPT_YMIN: print("Ymax= %s" % str(OPT_YMIN))

    ##########################################################################
    # matplotlib

#   plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 16  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize'] = 18  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth'] = 1.5  # 軸の太さを設定。目盛りは変わらない

#   plt.figure(figsize=(7.00, 9.89))  # for portrait

    ##########################################################################
    spin_list = [0]
    if OPT_UP:
        spin_list = [0]
    if OPT_DN:
        spin_list = [1]
    if OPT_UP and OPT_DN:
        spin_list = [0,1]
    if OPT_SPIN:
        spin_list = [0,1]

    # TOTAL DOS
    dos = SAE.io.ReadLobDos()
    dos_x = dos.get_eng()

    # COHP Average
    cohp = SAE.io.ReadLobCohp()
    cohp_x = cohp.get_eng()

    if OPT_PAIR:
        for i in OPT_PAIR:
            par_label = cohp.bond_index[int(i)]
            print(i,par_label)

    ######################################################## DOS
    plt.subplot(121)
    for s in spin_list:
        if s == 0 : spin_label = 'up'
        if s == 1 : spin_label = 'down'
        label = 'TDOS'+'-'+spin_label
        dos_y = dos.get_tdos(spin=s)
        plt.plot(dos_y, dos_x, linewidth=1, label=label)
#       plt.plot(dos_y, dos_x, color="black", linewidth=1, label='TDOS')
#       plt.fill_between(dos_y,dos_x, 0,facecolor='#cccccc', linewidth=2, label='TDOS')

    plt.axhline(y=0, color="black", linewidth=1)

    if OPT_DMAX: plt.xlim(xmax=float(OPT_DMAX))
    if OPT_EMAX: plt.ylim(ymax=float(OPT_EMAX))
    if OPT_EMIN: plt.ylim(ymin=float(OPT_EMIN))
    plt.xlim(xmin=0)

    plt.xlabel("DOS/eV", fontsize=17)
    plt.ylabel("$E -  E_{\mathrm{F}}$ [eV]", fontsize=17)

    # legend
    leg = plt.legend(fontsize=9, loc='lower right')
    leg.get_frame().set_alpha(0.5)

    ######################################################## COHP Average
    plt.subplot(122)

    print('SPIN_LIST = ',spin_list)
    ################### COHP Average
    if not OPT_PAIR:
        for s in spin_list:
            if s == 0 : spin_label = 'up'
            if s == 1 : spin_label = 'down'
            label = 'Average'+' ('+spin_label+')'
            cohp_y = cohp.get_ave(spin=s)
            plt.plot(-1. * cohp_y, cohp_x, linewidth=1, label=label)

    ################### COHP Pair
    if OPT_PAIR:
        for s in spin_list:
            for i in OPT_PAIR:
                par_label = cohp.bond_index[int(i)]
                if s == 0 : spin_label = 'up'
                if s == 1 : spin_label = 'down'
                label = par_label+'  ('+spin_label+')'
                cohp_pair = cohp.get_cohp(bond=int(i),spin=s)
                plt.plot(-1. * cohp_pair, cohp_x, linewidth=1, label=label)

    plt.axhline(y=0, color="black", linewidth=1)
    plt.axvline(x=0, color="black", linewidth=1)

    if OPT_EMAX: plt.ylim(ymax=float(OPT_EMAX))
    if OPT_EMIN: plt.ylim(ymin=float(OPT_EMIN))
    if OPT_YMAX: plt.xlim(xmax=float(OPT_YMAX))
    if OPT_YMIN: plt.xlim(xmin=float(OPT_YMIN))

    plt.yticks([])
    plt.xlabel("-pCOHP", fontsize=17)

    # legend
    leg = plt.legend(fontsize=9, loc='lower left')
    leg.get_frame().set_alpha(0.5)

    # Y軸の調整
#   plt.ylim( ymin=0 )


#   if spin == 0:

    ##########################################################################

#   plt.xlabel("$E -  E_{\mathrm{F}}$ [eV]", fontsize=20 )

#   leg = plt.legend(fontsize=12)   # 凡例Box
#   leg.get_frame().set_alpha(0.5)  # Alphaチャンネル(半透明化)

    xmin, xmax, ymin, ymax = plt.axis()

#   plt.xlim([-10,10])
#   plt.ylim([0,200])

    plt.savefig("COHP_tate.eps")
    plt.savefig("COHP_tate.pdf")
    plt.savefig("COHP_tate.png")

    if not NO_WINDOW_FLAG:
        plt.show()

    plt.close('all')

##########################################################################
