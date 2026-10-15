#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# WIEK2k case.dos 用
# Wldos ( Wldos の出力形式はほぼ Vldos と同様 )
#
#
# 基本クラスのテストも兼ねる
#
# dos = SAE.ReadWienDos(lists)
#   d = dos.get_raw_dos(atom=ion,orbit='d')
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.03.26
#  output0 が見つからない時の対応
#  軌道成分のチェック(s,p,d,fプロット項目の追加等)
#
# 2015.03.25
#   spin 対応version
#
# 2015.03.25
#   startup
#
################################################################################
from __future__ import print_function
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014,2015 Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"
################################################################################

import sys
import os
import re
#import gzip
#import numpy as np

import optparse

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
def options():

    case = re.sub('.*/','',os.getcwd())
    unit = 'ev'
    output = 'ldos.dat'

    parser = optparse.OptionParser(os.getcwd())

    parser.add_option( '-i','--input', dest='INPUT', )
    parser.add_option( '-o','--output', dest='OUTPUT', )
    parser.add_option( '-e','--ev', action='store_true', )
    parser.add_option( '-s','--std', action='store_true', )
    parser.add_option( '-f','--fermi', action='store_true', )

    options, args = parser.parse_args()

    if options.ev:
        unit='ev'
    else:
        unit='None'

    if options.INPUT:
        case = options.INPUT

    if options.OUTPUT:
        output = options.OUTPUT

    if options.std:
        FLAG_STD=True
    else:
        FLAG_STD=False

    if options.fermi:
        FLAG_FERMI=True
    else:
        FLAG_FERMI=False

    return case,output,unit,FLAG_STD,FLAG_FERMI

################################################################################
if __name__ == '__main__':

    case,output,unit,STD,FERMI = options()

    lists = SAE.find_suffix3(case+'.dos',unit)
    if not lists:
        sys.exit("STOP: "+case+".dos* file not found")

    print("READ FILE    :", end="")
    for i in lists:
        print(i, end="")
    print("")
    print("OUT FILE     :",output)

    #####################################################
    ## check SPIN
    if os.path.exists(case+'.output0'):
        output0_file = case+'.output0'
    elif os.path.exists(case+'.output0.gz'):
        output0_file = case+'.output0.gz'
    elif os.path.exists(case+'.output0000'):
        output0_file = case+'.output0000'
    elif os.path.exists(case+'.output0000.gz'):
        output0_file = case+'.output0000.gz'
    else:
        sys.exit("STOP: output0 file not found")

    output0 = SAE.io.ReadWienOutput0(output0_file)
    nspin = output0.get_ispin()
    FLAG_SPIN = False
    if nspin >= 2:
        FLAG_SPIN = True

    #####################################################
    ## SPIN 有りの時に list のスピン毎の作り直し
    if FLAG_SPIN:
        up = []
        dn = []
        for i in lists:
            up.append(re.sub('up','',re.sub('dn','',i))+'up')
            dn.append(re.sub('up','',re.sub('dn','',i))+'dn')
        up_lists = list(set(up))
        dn_lists = list(set(dn))

    #####################################################
    # Open File
    try:
        if not STD:
            out = open(output,'w')
        else:
            out = sys.stdout
    except:
        out.close()
        sys.exit("STOP: can'nt open :"+output)

    #####################################################
    # spin1 のデーターの後そのまま spin2 が並ぶだけの形式
    for spin in range(nspin):

        if FLAG_SPIN and spin == 0:
            lists = up_lists
        if FLAG_SPIN and spin == 1:
            lists = dn_lists

        dos = SAE.ReadWienDos(lists)

        nion = dos.get_nion()
        nedos = dos.get_nedos()
        efermi = dos.get_efermi()
        eng = dos.get_eng()
        plot_ions = dos.get_plot_ions()

        if spin == 1:
            print("FERMI ENERGY :",efermi)
            if FERMI:
                print("FERMI --> 0  :")

        # s,p,d oribt がそれぞれの ion で計算されていることが必須
        for ion in plot_ions:

            FT=False
            FS=False
            FP=False
            FD=False
            FF=False
            if dos.chk_raw_dos(atom=0,orbit='total-DOS'):
                tot = dos.get_raw_dos(atom=ion,orbit='total-DOS')
                FT=True
            if dos.chk_raw_dos(atom=ion,orbit='s'):
                s = dos.get_raw_dos(atom=ion,orbit='s')
                FS=True
            if dos.chk_raw_dos(atom=ion,orbit='p'):
                p = dos.get_raw_dos(atom=ion,orbit='p')
                FP=True
            if dos.chk_raw_dos(atom=ion,orbit='d'):
                d = dos.get_raw_dos(atom=ion,orbit='d')
                FD=True
            if dos.chk_raw_dos(atom=ion,orbit='f'):
                f = dos.get_raw_dos(atom=ion,orbit='f')
                FF=True

            print("", file=out)
            print("", file=out)
            print("", file=out)
            print("#", file=out)
            print("#", file=out)
            print("#     nspin = "+str(nspin), file=out)
            print("#      spin = "+str(spin+1), file=out)
            print("#       ion = "+str(ion), file=out)
            print("#    efermi =",efermi, file=out)
            if FERMI:
                print("#    efermi -> 0", file=out)
            print("#", file=out)
            print("#    eng, ", file=out, end="")
            if FT:
                print("tot, ", file=out, end="")
            if FS:
                print("s, ", file=out, end="")
            if FP:
                print("p, ", file=out, end="")
            if FD:
                print("d, ", file=out, end="")
            if FF:
                print("f, ", file=out, end="")
            print("", file=out)
            print("#", file=out)

           #for orbit in ['s','p','d']:
           #    if not dos.chk_raw_dos(atom=ion,orbit=orbit):
           #        sys.exit("STOP: does'nt font data in orbit "+str(orbit))

            for i in range(nedos):
                if FERMI:
                    energy = eng[i] - efermi
                else:
                    energy = eng[i]
               #print >>out, "%11.5f %14.8f %14.8f %14.8f %14.8f" \
               #              % ( energy,tot[i],s[i],p[i],d[i] )
                print("%11.5f " % ( energy ), file=out, end="")
                if FT:
                    print("%14.8f " % ( tot[i] ), file=out, end="")
                if FS:
                    print("%14.8f " % ( s[i] ), file=out, end="")
                if FP:
                    print("%14.8f " % ( p[i] ), file=out, end="")
                if FD:
                    print("%14.8f " % ( d[i] ), file=out, end="")
                if FF:
                    print("%14.8f " % ( f[i] ), file=out, end="")
                print("")

    if not STD:
        out.close()

