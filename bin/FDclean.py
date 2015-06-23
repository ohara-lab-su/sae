#!/usr/bin/env python
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDclean
# *.in ファイルを読み込んで Filout タグから名前を取得し
# Filout* ファイルを消す
#
################################################################################
#
# 2015.06.19 startup
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
__version__    = "0.1.1"
################################################################################

#import sys
#import gzip
import os
#import re
import optparse
#import numpy as np
import glob

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
def options():

    name = 'read_pdb.inp'
#   name = 'POSCAR.inp'

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT',)
    options,args = parser.parse_args()

    if options.INPUT:
        name=options.INPUT

    if len(args) > 0:
        name=args[0]

    return name

################################################################################
if __name__ == '__main__':

    name = options()
    out = SAE.ReadFdmInp(name)

    filout = out.get_filout()
    print 'fileout :',filout

    filelist = glob.glob(filout+'*.txt')

    print ""
    for i in filelist:
        print "DELETE : "+i
        os.remove(i)

    if os.path.exists('fdm.out'):
        print "DELETE : fdm.out"
        os.remove('fdm.out')

    if os.path.exists('PBS_log'):
        print "DELETE : PBS_log"
        os.remove('PBS_log')

