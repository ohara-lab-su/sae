#!/usr/bin/env python
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# sets.in (HiLPAW) 書き出しルーチンの基本
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
#
# 2015.02.16
#  無駄な import をコメントアウト
#
################################################################################

import sys
import os

#import re
#import optparse
#from numpy import *


def print_sets(cname,STD,\
               title,nspin,spg_name,lattices,nion,sg_atoms,sg_atoms_index,sg_position,kinfo,kpoints):

    if STD:
        out = sys.stdout
    else:
        if os.path.exists(cname):
            sys.exit("STOP(print_sets.py): "+cname+" exists")
        else:
            try:
                out = open(cname,'w')
            except:
                out.close()
                sys.exit("STOP(print_sets.py): "+cname+" does'nt open")

    print >> out, title
    print >> out, "-----nspin"
    print >> out, nspin
    print >> out, "-----space group"
    print >> out, spg_name
    print >> out, "  %8.4f %8.4f %8.4f" %(lattices[0],lattices[1],lattices[2])
    print >> out, "  %8.4f %8.4f %8.4f" %(lattices[3],lattices[4],lattices[5])
    print >> out, "-----atoms"
    print >> out, " ",nion

    index = 0
    for i in range(nion):
        print >> out, sg_atoms_index[i], sg_atoms[i]
        for j in range(sg_atoms[i]):
            print >> out, " %13.9f %13.9f %13.9f" \
                           %(sg_position[index,0], sg_position[index,1], sg_position[index,2])
            index += 1

    print "-----k points"
    print kinfo
    print kpoints[0],kpoints[1],kpoints[2]

    out.close()

