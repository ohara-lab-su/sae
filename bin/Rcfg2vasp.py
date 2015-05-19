#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# convert from RMC_POT cfg file to VASP POSCAR file
#
# 2014.10.31
#    関数化 & ライブラリ分離
#
# 2014.10.08
#    Rvasp2cfg.py に仕様を合わせる
#    --> オプション関係を追加
#
# 2014.10.01
#    1st version
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.3"
################################################################################

import sys
import os
import optparse
import numpy as np

import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE 

################################################################################
def options():

    ###############################################
    ## default name
    ##
    cname="igzo" # INPUT BASE filename

    ###############################################
    ## optparse
    parser = optparse.OptionParser()
    
    parser.add_option(  '-i','--input',
                        dest='INPUT',
                        default=cname,
    )
    options,  args = parser.parse_args()
    
    if options.INPUT:
        cname=options.INPUT
    
    #print args,options
    if len(args) > 0:
        #print "script name:",argvs[0]
        cname=args[0]
    
    if cname:
        print "INPUT file name :",cname+".cfg"
        print "OUTPUT file name:",cname+".vasp"
    
    if not os.path.exists(cname+".cfg"):
        sys.exit(cname+".cfg file not found")

    return cname


################################################################################
if __name__ == '__main__':

    # Default & OptionParser
    cname = options()

    # RMC_POT (*.cfg) 読み込み準備関数
    natom,nion = SAE.read_cfg_param(cname)

    # RMC_POT (*.cfg) 読み込み準備
    t           = np.zeros((3,3),dtype=float)
    atoms       = np.zeros(int(nion),dtype=int)
    atoms_j     = np.zeros(int(natom),dtype=int)
    position    = np.zeros((int(natom),3),dtype=float)

    # RMC_POT (*.cfg) ファイル読み込み
    title,header = SAE.read_cfg(cname,t,atoms,atoms_j,position)

   ## TEST print
   #STD=True
   #print_cfg(cname,STD,title,t,natom,nion,atoms,position)

    # RMC_POT (*.cfg) 形式から VASP 形式へ変換
    direct = True   # conv_cfg2vasp は direce を想定(in/out)
    scale   = 1.0   # conv_cfg2vasp は scale 1.0 を想定
    scale,direct = SAE.conv_cfg2vasp(scale,t,natom,direct,position)

    # 擬似VASP5 設定
    dummy   = "In Ga Zn O"
    PV5FLAG = True  # 擬似VASP5 出力

    # VASP4+擬似VASP5 出力
   #print ""
    STD=False
   #STD=True
    SAE.print_poscar4(cname,STD,title,scale,natom,nion,\
                      direct,PV5FLAG,t,atoms,dummy,position)

################################################################################
