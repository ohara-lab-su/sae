#!/usr/bin/env python
# -*- coding: utf-8 -*- 
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#   UPF 形式の PP ファイルから <PP_INPUTFILE> </PP_INPUTFILE> を吸い出す
#
################################################################################
#
# 2015.03.23
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
#import sys
import os
import re
#import numpy as np

#import glob
import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE                                            


################################################################################
if __name__ == '__main__':

    ############################################################################
    base = 'default'
    suffix = 'UPF'
    name = base+'.'+suffix

    parser = optparse.OptionParser(os.getcwd())
    parser = optparse.OptionParser()
    parser.add_option('-i','--input',dest='INPUT')
    options,args = parser.parse_args()

    if options.INPUT:
        name=options.INPUT

    if len(args) >0:
        name=args[0]

    if not os.path.exists(name):
        base = SAE.find_datfiles(suffix)
        name = base[0]+'.'+suffix

#   print "INPUT UPF file: ",name
    ############################################################################

    datlines,num = SAE.read_dataline(name)

    start = '<PP_INPUTFILE>'
    end = '</PP_INPUTFILE>'
    start_reg = re.compile(start)
    end_reg = re.compile(end)

    i=0
    while 1:
        if bool(start_reg.match(datlines[i])):
            i += 1
            while not bool(end_reg.match(datlines[i])):
                print datlines[i]
                i += 1
            break
        i += 1

