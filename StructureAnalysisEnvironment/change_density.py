################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# *.dat (RMC_POT) ファイル読み込み、density を書きなおして *.dat 出力する
#
# ほぼ再利用できない （しにくい）特化型アホルーチン (2014.11.07)
#
# [in]     STD     : 標準出力するかどうかのフラグ
# [in]     datname : 読み込む、基本となる *.dat ファイル   
# [in]     outname : 出力する *.dat ファイル名
#
# [in]     density : 新しい density の値
#
################################################################################
#
# 2014.10.11.07 1st
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
__version__    = "0.0.1"                                                                  
################################################################################

import sys
import os
import optparse
import numpy as np


def change_density(STD,datname,outname,density):

    ###############################################
    ## Open RMC_POT cfg file
    ##
    tmp = open(datname+'.dat')
    datfile = tmp.read()
    tmp.close

    datlines = datfile.split('\n')
    nline = len(datlines)
    
    header = datlines[0]
    lines = datlines[1].split()
    n = len(lines)

    ###
    if STD:
        out = sys.stdout
    else:
        out = open(outname+'.dat','w')

    print >> out, datlines[0].rstrip()

    lines[0] = density
    for i in range(n):
        print >> out, lines[i],
    print >> out, ""

    for i in range(2,nline):
        print >> out, datlines[i].rstrip()

    out.close
    
    return

