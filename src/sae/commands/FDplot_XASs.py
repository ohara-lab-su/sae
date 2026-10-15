#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.athena.nor import ReadAthenaNor
from sae.fdmnes.conv import ReadFdmConv
from sae.fdmnes.inp import ReadFdmInp
from sae.fdmnes.txt import ReadFdmTxt

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
# 2018.08.17
#  Python2/3 両対応
#
# 2015.07.01 fdXAS startup
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import argparse
import matplotlib.pyplot as plt
import matplotlib.ticker as ptick


#
################################################################################
# import gzip
# import re
# import optparse
# import numpy as np
# import SpaceGroupEnvironment as SGE
# from matplotlib.ticker import FuncFormatter
################################################################################
#   name = 'read_pdb.inp'
#   name = 'POSCAR.inp'
#   parser = optparse.OptionParser()
#   options,args = parser.parse_args()
#   if options.INPUT: name=options.INPUT
#   if len(args) > 0: name=args[0]
########## inpname 取得
def options():
    from sae.fdmnes.fdmfile import ReadFdmFdmfile

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="INPUT")
    parser.add_argument("--emax")
    parser.add_argument("--emin")
    parser.add_argument("--ymax")
    parser.add_argument("-f", "--fermi", action="store_true", default=False)
    parser.add_argument("-o", "--obs", action="store_true", default=False)
    parser.add_argument("-a", "--average", nargs="*")
    options = parser.parse_args()
    if options.INPUT:
        inpname = options.INPUT
    elif os.path.exists("fdmfile.txt"):
        fdmfiletxt = ReadFdmFdmfile()
        inpname = fdmfiletxt.filout
    else:
        inpname = "read_pdb.inp"
    if not os.path.exists(inpname) or inpname is None:
        sys.exit(inpname + " file not fount")
    return (
        inpname,
        options.emax,
        options.emin,
        options.ymax,
        options.fermi,
        options.obs,
        options.average,
    )


###############################################################################
#   plt.figure(figsize=(7.00, 9.89))  # for portrait
#   orgx = 0.170
#   orgy = 0.080
#   off = 0.010
#   xsize = 0.75
#   ysize = 0.83/2.
#   plt.axes([orgx,orgy,xsize,ysize])
############################################################################
## 計算結果の読み込み
############################################################################
if __name__ == "__main__":
    inpname, OPT_EMAX, OPT_EMIN, OPT_YMAX, FLAG_fermi, FLAG_OBS, AV = options()
    if not AV:
        sys.exit("STOP: plase input absorber number (potion: -a)")
    if OPT_EMAX:
        OPT_EMAX = float(OPT_EMAX)
        print("Emax     =", OPT_EMAX)
    if OPT_EMIN:
        OPT_EMIN = float(OPT_EMIN)
        print("Emin     =", OPT_EMIN)
    if OPT_YMAX:
        OPT_YMAX = float(OPT_YMAX)
        print("Ymax     =", OPT_YMAX)
    plt.rcParams["font.family"] = "Times New Roman"
    # ラベル等のフォントサイズ
    plt.rcParams["font.size"] = 16
    # レジェンドのフォントサイズ
    plt.rcParams["legend.fontsize"] = 14
    # 軸の太さを設定。目盛りは変わらない
    plt.rcParams["axes.linewidth"] = 1.5
    # for portrait
    plt.figure(figsize=(8.1, 9.89))
    inp = ReadFdmInp(inpname)
    calculation = inp.get_calculation()
    if calculation:
        filout = calculation.replace(".txt", "")
    else:
        filout = inp.get_filout()
    print("INP FILE  = ", inpname)
    print("DATA FILE = ", filout)
    if AV:
        txt = ReadFdmTxt(filout + "_" + str(AV[0]), ".txt")
    else:
        txt = ReadFdmTxt(filout, ".txt")
    print("E_edge   =", txt.E_edge)
    print("E_fermi  =", txt.E_Fermi)
    filbav = inp.get_filout()
    if filbav is None:
        sys.exit("STOP: fileout TAG not found in " + inpname)
    print("-----")
    # XASエネルギー原点の変換 (*.txt ファイルおよび *_conv.txt 読み込み)
    ########################################################################
    #   plt.subplot()
    #   plt.ticklabel_format(axis='x',style='plain')
    #   if FLAG_fermi:
    #       plt.xlabel("Energy above Fermi [eV]")
    #   else:
    #       plt.xlabel("Photon Energy [eV]")
    #   leg = plt.legend(fontsize=12,loc='lower right')
    ############################################################################
    # Athena data plot
    for ab in range(len(AV)):
        filout = filbav + "_" + str(ab + 1)
        convname = filout + "_conv.txt"
        print(convname)
        if not os.path.exists(convname):
            sys.exit("STOP: " + convname + " not found")
        conv = ReadFdmConv(filout, "_conv.txt")
        if not inp.get_energygpho() and (not FLAG_fermi):
            txt.eng = txt.eng + txt.E_edge
            conv.eng = conv.eng + txt.E_edge
        if inp.get_energygpho() and FLAG_fermi:
            txt.eng = txt.eng - txt.E_Fermi - txt.E_edge
            conv.eng = conv.eng - txt.E_Fermi - txt.E_edge
        if not inp.get_energygpho() and FLAG_fermi:
            txt.eng = txt.eng - txt.E_Fermi
            conv.eng = conv.eng - txt.E_Fermi
        plt.subplot(2, 1, 2)
        plt.plot(conv.eng, conv.xas, linewidth=1, label="absorber=" + str(ab + 1))
        plt.ticklabel_format(axis="x", useOffset=False)
        plt.ylabel("Absorption [arb. unit]")
        EF0 = txt.E_edge + txt.E_fermi
        if FLAG_fermi:
            plt.axvline(x=0, color="black", linewidth=1)
        else:
            plt.axvline(x=EF0, color="black", linewidth=1)
        leg = plt.legend(loc="lower right")
        leg.get_frame().set_alpha(0.5)
        if OPT_EMAX:
            plt.xlim(xmax=float(OPT_EMAX))
        if OPT_EMIN:
            plt.xlim(xmin=float(OPT_EMIN))
        if OPT_YMAX:
            plt.ylim(ymax=float(OPT_YMAX))
        xas_xmin, xas_xmax, xas_ymin, xas_ymax = plt.axis()
        if FLAG_fermi:
            plt.xlabel("Energy above Fermi [eV]")
        else:
            plt.xlabel("Photon Energy [eV]")
        #   leg = plt.legend(fontsize=12,loc='lower right')
        #   leg = plt.legend(loc='upper right')
        if FLAG_OBS:
            obs_file = filout + "_obs.txt.nor"
            if not os.path.exists(obs_file):
                sys.exit("STOP: " + obs_file + " not found")
            nor = ReadAthenaNor(obs_file)
            plt.subplot(2, 1, 1)
            plt.plot(nor.eng, nor.nor, label="obs.")
            plt.xlim([xas_xmin, xas_xmax])
            plt.ticklabel_format(axis="x", useOffset=False)
            leg = plt.legend(loc="lower right")
            leg.get_frame().set_alpha(0.5)
    plt.savefig("XAS.eps")
    plt.savefig("XAS.pdf")
    plt.savefig("XAS.png")
    plt.show()
    plt.close("all")
