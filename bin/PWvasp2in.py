#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#   convert PWScf (Quantum ESPRESSO ) to *.in
#
################################################################################
#
# 2015.08.24
#  統合化
#
# 2015.08.24
#  統合化の前に print 部分の分離・関数化
#
# 2015.03.20
#  startup
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

import optparse
import sys
import os
import re
#import numpy as np

#import glob
import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE


################################################################################
def options():

    poscarname = 'POSCAR'
    outbase    = 'POSCAR'
    inpsuffix  = '.in'

    parser = optparse.OptionParser(os.getcwd())
    parser = optparse.OptionParser()

    parser.add_option(  '-s','--stdout', action='store_true',)
    parser.add_option( '-i','--input', dest='INPUT',)
    parser.add_option( '-o','--output', dest='OUTPUT',)
    options, args = parser.parse_args()

    outbase=re.sub('\.in$','',outbase)
    outinp=outbase+inpsuffix

    if options.INPUT: poscarname=options.INPUT

    outbase=poscarname
    if options.OUTPUT:
        outbase=re.sub('\.inp$','',options.OUTPUT)
        outinp=outbase+inpsuffix

    # オプション無し引数の時は拡張子自動削除を付けずにそのままファイル名とする
    if len(args) >0: poscarname=args[0]
    if poscarname == outinp: sys.exit("STOP: INPUT_NAME = OUTPUT_NAME :"+poscarname)

    print "INPUT :",poscarname
    print "OUTPUT:",outbase+inpsuffix

    return [poscarname,outbase,inpsuffix,options.stdout]

################################################################################
if __name__ == '__main__':

    poscarname,outbase,inpsuffix,OPT_STD = options()
    cname = outbase+inpsuffix

    cell = SAEnv.Read(filename=poscarname,code='VASP')
    cell.write(outname=cname,code='PWScf',STD=OPT_STD)

