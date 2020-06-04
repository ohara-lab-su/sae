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
from __future__ import print_function
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
#import argparse
#import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

#from matplotlib.ticker import FuncFormatter
#import matplotlib.pyplot as plt
#import matplotlib.ticker as ptick


################################################################################
def options():

    inpname = 'read_pdb.inp'

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--inp',)
    parser.add_option(  '-t','--text',)
    parser.add_option(  '-c','--conv',)
    parser.add_option(  '-f','--fermi', action='store_true',default=False,)
    options,args = parser.parse_args()

    if options.inp: inpname=options.inp
    if len(args) > 0: inpname=args[0]

    if not os.path.exists(inpname):
        sys.exit("STOP: "+inpname+" not found")

    return inpname,\
           options.text,\
           options.conv,\
           options.fermi

###############################################################################
if __name__ == '__main__':

    # inpname 他、名前取得
    inpname,txtname,convname,FLAG_FERMI = options()
    if not os.path.exists(inpname):
        sys.exit("STOP(inpname): "+inpname+' not found')
    print("--inp  , inpname .inp       : read current mode     =",inpname)

    # inp ファイルの分解
    inp = SAE.ReadFdmInp(inpname)
    if inp.get_energygpho():
        sys.exit("STOP: current mode is PhotoEnergy")

    # convolution 前の元データ(パラメーター読み込み)
    if txtname:
        filout = txtname.replace('.txt','')
    else:
        filout = inp.get_filout()
    if not os.path.exists(filout+'.txt'):
        sys.exit("STOP(filout,txtname): "+filout+'.txt not found')
    print("--text , filout  .txt       : read E_edge parameter =",filout+".txt")


    # エネルギー単位変換前の convolution データ(実際に変換するデータ)
    if convname:
        convout = convname.replace('_conv.txt','')
    else:
        convout = filout
    if not os.path.exists(convout+'_conv.txt'):
        sys.exit("STOP(convout): "+convout+'_conv.txt not found')
    print("--conv , convdata _conv.txt : read XAS data         =",convout+"_conv.txt")


    # エネルギー単位変換後の出力ファイル
    outfile = convout+'_conv_photoe.txt'
    print("outfile                                             =",outfile)


    # データーの分解
    txt = SAE.ReadFdmTxt(filout,'.txt')
    conv = SAE.ReadFdmConv(convout,'_conv.txt')
    print("E_edge                                              =",txt.E_edge)
    print("E_fermi                                             =",txt.E_Fermi)


    ########################### converter ######################################
    if not inp.get_energygpho():
        print("current mode                                        = Fermi")
        txt.eng = txt.eng + txt.E_edge     #-txt.E_fermi
        conv.eng = conv.eng  + txt.E_edge  #-txt.E_fermi

    if FLAG_FERMI:
        print("Energy - E_fermi                                    = ",txt.E_fermi)
        txt.eng = txt.eng   - txt.E_fermi
        conv.eng = conv.eng - txt.E_fermi

    print("---> convert to PhotoEnergy (EF0 + E_edge)")
    try:
        convout = open(outfile,'w')
    except:
        convout.close()

    print("", file=convout)
    for i in range(len(txt.eng)):
        print(" %13.5f  %14.10f" %(txt.eng[i], conv.xas[i]), file=convout)

    convout.close()

