#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDmakeConvAllsite.py
#
#  allsite 計算用
#
#   -i conv.inp
#    を参照して すべてのサイトの conv を行う conv.inp と fdmfile.txt を作成する
#
################################################################################
#
# 2015.06.30 startup
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

import sys
#import gzip
import os
import glob
import re
#import fnmatch
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

    name = 'read_pdb.inp'
#   name = 'POSCAR.inp'

    parser = optparse.OptionParser()
#   parser = argparse.ArgumentParser()
#   parser.add_argument(  '-i','--input', dest='INPUT',)
    parser.add_option(  '-i','--input', dest='INPUT',)
#   options = parser.parse_args()
    options,args = parser.parse_args()

    if options.INPUT: name=options.INPUT

    if not os.path.exists(name):
        name = 'conv.inp'

    return name

###############################################################################
if __name__ == '__main__':

    inpname = options()
    inp = SAE.ReadFdmInp(inpname)

    filout = inp.get_filout()
    if filout is None:
        sys.exit("STOP: fileout TAG not found in "+inpname)

    print "redfile =",inpname
    print "filout  = ",filout

    calname = []
    for i in sorted(glob.glob(filout+'_*.txt')):
        if bool(re.compile(filout+'_\d+.txt').match(i)):
            calname.append(i)

    ncal = len(calname)
    try:
        fdmlist = open('fdmfile.txt','w')
    except:
        fdmlist.close()
    print >> fdmlist, ""
    print >> fdmlist, " "+str(ncal)

    for i in range(ncal):
        print calname[i]
        convname = 'conv_'+str(i+1)+'.inp'
        try:
            convinp = open(convname,'w')
        except:
            convinp.close()
        print >> fdmlist, convname

        print >> convinp, ""
        print >> convinp, " Filout"
        print >> convinp, "   "+filout
        print >> convinp, ""
        print >> convinp, " Calculation"
        print >> convinp, "   "+calname[i]
        print >> convinp, ""
        print >> convinp, " Conv_out"
        print >> convinp, "   "+calname[i].replace('.txt','')+'_conv.txt'
        print >> convinp, ""
        print >> convinp, " Convolution"
        print >> convinp, ""
        print >> convinp, "END"

        convinp.close()

    fdmlist.close()
