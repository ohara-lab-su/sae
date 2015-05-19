#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#  Vxml2MD は vasprun.xml --> *.xyz (MD) 形式
#  Vxdat2MD は XDATCAR --> *.xyz (MD) 形式
#
#  ただし、OUTCAR が存在しない時は Vxdat2MD は エネルギーの項目は追加しない
#
################################################################################
#
# 2015.01.22 startup
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

#import sys
import optparse
#import xml.etree.ElementTree as ET

#import numpy as np
import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE  

#import os
#import re
#from copy import deepcopy


################################################################################
def options():                                                                  
                                                                                
    XDATCAR = "XDATCAR"
                                                                                
    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input',
                        dest='INPUT',
                        default=XDATCAR,
    )
    options,  args = parser.parse_args()
                                                                                
    if options.INPUT:
        XDATCAR=options.INPUT
                                                                                
    if len(args) > 0:
        XDATCAR=args[0]
                                                                                
    return XDATCAR


################################################################################
if __name__ == '__main__':

#   name = 'XDATCAR'
    name = options()
    xdat = SAE.ReadXdat(name)

    nion = xdat.get_nion()
    natom = xdat.get_natom()
    vasp = xdat.get_vasp_version()
    title = xdat.get_title()
    scale = xdat.get_scale()
    t = xdat.get_t()
    atoms = xdat.get_atoms()
    atoms_index = xdat.get_atoms_index()

    direct = xdat.get_direct()
    nloop = xdat.get_nloop()

    for i in range(nloop):
        print natom
        print "%s %10d" %( "   step=", i+1 )
        xyz = xdat.get_xyz(loop=i)
        j=0
        for k in range(nion):
            for l in range(int(atoms[k])):
                print "  %2s %12.8f %12.8f %12.8f" \
                        % ( atoms_index[k],xyz[j,0],xyz[j,1],xyz[j,2])
                j += 1


