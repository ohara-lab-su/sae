#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 複数の *.xyz ファイルを結合する
#
################################################################################
#
# 2015.03.10
#  startup (python版)
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
import os
import re
#import gzip
#import numpy as np

import optparse 

import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE 

################################################################################
def options(suffix,sumfile):

    # 自動探索(デフォルト), 複数ファイル版
    xyznames = SAE.find_datfiles(suffix)
    if os.path.exists(sumfile):
        xyznames.remove(re.sub('.xyz','',sumfile))

    parser = optparse.OptionParser()
    parser.add_option('-s','--std',action='store_true',default=False,)
    options,args = parser.parse_args()

    # 手動指定: 末尾のxyz を削除した引数名を名前リストに追加する
    if len(args) >0:
        xyznames = []
        for i in range(0,len(args)):
            xyznames.append(re.sub('.xyz$','',args[i]))

    FLAG_STD=options.std

    return [xyznames,FLAG_STD]

################################################################################
if __name__ == '__main__':

    suffix = 'xyz'
    sumfile = 'sum'+'.'+suffix

    xyznames,FLAG_STD = options(suffix,sumfile)

    if not FLAG_STD:
        print "OUTPUT   =",sumfile
        print "SUMFILES ="
        for xyz in xyznames:
            print "          ",
            print xyz+"."+suffix

    sumnum = 0
    sumdat = []
    for name in xyznames:
        datlines,num = SAE.read_dataline(name+'.'+suffix)
        sumnum = sumnum + int(datlines[0])
        for j in range(num-2):
            sumdat.append(datlines[j+2])

    if not FLAG_STD:
        try:
            dat = open(sumfile,'w')
        except:
            sys.exit("STOP: "+sumfile+" can't open")
    else:
        dat = sys.stdout

    print >> dat ,sumnum
    print >> dat ,""
    for i in range(sumnum):
        print >> dat, sumdat[i]

    dat.close()

