#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#   convert VASP POSCAR to OpenMX *.dat
#   for OpenMX 3.7.*
#
#  実行にはPAO と VPS の情報一覧を必須とする
#
#    情報一覧ファイル
#    openmx_defaults_vpsdata
#
#       1) カレントをサーチ
#       2) ホーム直下の DFT_DATA13 ディレクトリをサーチ
#       3) ../DFT_DATA13 ディレクトリをサーチ
#       4) ~/openmx1/ ディレクトリをサーチ
#
#    vpsdata ファイルを発見したら読み込む
#    vapdata ファイルの中身は PAO の軌道情報および VPS 情報で
#    元素記号から最低限動くデフォルトの PAO/VPS 情報を引っ張るために用いる
#
################################################################################
#
# 2015.08.20
#   関数化&分離化&統合化バージョン
#
################################################################################
from __future__ import print_function
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014,2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.1.0"
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
    datname    = 'POSCAR'

    parser = optparse.OptionParser(os.getcwd())
    parser = optparse.OptionParser()

    parser.add_option( '-s','--stdout', action='store_true',)
    parser.add_option( '-i','--input', dest='INPUT',)
    parser.add_option( '-o','--output', dest='OUTPUT',)
    parser.add_option( '-d','--direct', action='store_true', dest='FRAC',)
    options, args = parser.parse_args()

    # VASP 入力ファイル名の自動取得
    if not os.path.exists(poscarname):
        poscarname0 = SAEnv.find_datfile('vasp')
        if poscarname0 is None:
            sys.exxit("STOP: POSCAR or .vasp files not found")
        poscarname = poscarname0+'.vasp'

    if options.INPUT:
        poscarname=options.INPUT

    if options.OUTPUT:
        datname=options.OUTPUT

    # もし拡張子 .dat がついていたらそれを消す
    datname=re.sub('\.dat','',datname)

    # オプション無し引数の時は拡張子自動削除を付けずにそのままファイル名とする
    if len(args) >0:
       #print "POSCAR:",args[0]
        poscarname=args[0]

    return [poscarname,datname,options.stdout,options.FRAC]


################################################################################
if __name__ == '__main__':

    ## options
    poscarname,datname,OPT_STD,OPT_FRAC = options()

    print "INPUT :",poscarname
    print "OUTPUT:",datname+".dat"

    cell = SAEnv.Read(filename=poscarname,code='VASP')
    cell.write(outname=datname,code='OpenMX',calinfo='VASP',STD=OPT_STD,FRAC=OPT_FRAC)


