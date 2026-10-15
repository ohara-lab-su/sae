#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.fdmnes.conv import ReadFdmConv
from sae.fdmnes.inp import ReadFdmInp
from sae.fdmnes.txt import ReadFdmTxt

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FEconv_e2photow.py
#   *_conv.txt ---> *_conv_photoe.txt
#
#   EF からの相対単位を Photon Energy 単位に変換して出力するプログラム
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
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
import optparse


#
################################################################################
#import gzip
#import re
#import argparse
#import numpy as np
#import SpaceGroupEnvironment as SGE
#from matplotlib.ticker import FuncFormatter
#import matplotlib.pyplot as plt
#import matplotlib.ticker as ptick
################################################################################
def options():
    inpname = "read_pdb.inp"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--inp")
    parser.add_option("-t", "--text")
    parser.add_option("-c", "--conv")
    parser.add_option("-f", "--fermi", action="store_true", default=False)
    options, args = parser.parse_args()
    if options.inp:
        inpname = options.inp
    if len(args) > 0:
        inpname = args[0]
    if not os.path.exists(inpname):
        sys.exit("STOP: " + inpname + " not found")
    return (inpname, options.text, options.conv, options.fermi)


###############################################################################
# inpname 他、名前取得
# inp ファイルの分解
# convolution 前の元データ(パラメーター読み込み)
# エネルギー単位変換前の convolution データ(実際に変換するデータ)
# エネルギー単位変換後の出力ファイル
# データーの分解
########################### converter ######################################
if __name__ == "__main__":
    inpname, txtname, convname, FLAG_FERMI = options()
    if not os.path.exists(inpname):
        sys.exit("STOP(inpname): " + inpname + " not found")
    print("--inp  , inpname .inp       : read current mode     =", inpname)
    inp = ReadFdmInp(inpname)
    if inp.get_energygpho():
        sys.exit("STOP: current mode is PhotoEnergy")
    if txtname:
        filout = txtname.replace(".txt", "")
    else:
        filout = inp.get_filout()
    if not os.path.exists(filout + ".txt"):
        sys.exit("STOP(filout,txtname): " + filout + ".txt not found")
    print("--text , filout  .txt       : read E_edge parameter =", filout + ".txt")
    if convname:
        convout = convname.replace("_conv.txt", "")
    else:
        convout = filout
    if not os.path.exists(convout + "_conv.txt"):
        sys.exit("STOP(convout): " + convout + "_conv.txt not found")
    print(
        "--conv , convdata _conv.txt : read XAS data         =", convout + "_conv.txt"
    )
    outfile = convout + "_conv_photoe.txt"
    print("outfile                                             =", outfile)
    txt = ReadFdmTxt(filout, ".txt")
    conv = ReadFdmConv(convout, "_conv.txt")
    print("E_edge                                              =", txt.E_edge)
    print("E_fermi                                             =", txt.E_Fermi)
    if not inp.get_energygpho():
        print("current mode                                        = Fermi")
        #-txt.E_fermi
        txt.eng = txt.eng + txt.E_edge
        #-txt.E_fermi
        conv.eng = conv.eng + txt.E_edge
    if FLAG_FERMI:
        print("Energy - E_fermi                                    = ", txt.E_fermi)
        txt.eng = txt.eng - txt.E_fermi
        conv.eng = conv.eng - txt.E_fermi
    print("---> convert to PhotoEnergy (EF0 + E_edge)")
    try:
        convout = open(outfile, "w")
    except:
        convout.close()
    print("", file=convout)
    for i in range(len(txt.eng)):
        print(" %13.5f  %14.10f" % (txt.eng[i], conv.xas[i]), file=convout)
    convout.close()
