#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# PWscf *.in --> POSCAR 変換出力
#
################################################################################
#
# 2015.05.13 startup
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
#import os
#import re
import optparse
#import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
def write_poscar(\
        cname,\
        title,\
        scale,t,natom,nion,atoms,atoms_index,\
        position):

    try:
        out = open(cname+'.vasp','w')
    except:
        out.close()
        sys.exit("STOP:"+cname+".vasp can't open")

    print >> out, title
    print >> out, " ",scale
    print >> out, "  %13.9f %13.9f %13.9f" %(t[0,0],t[1,0],t[2,0])
    print >> out, "  %13.9f %13.9f %13.9f" %(t[0,1],t[1,1],t[2,1])
    print >> out, "  %13.9f %13.9f %13.9f" %(t[0,2],t[1,2],t[2,2])

    print >> out, " ",
    for i in range(nion):
        print >> out, atoms_index[i],
    print >> out, " "
    print >> out, " ",

    for i in range(nion):
        print >> out, atoms[i],
    print >> out, " "

    print >> out, "Direct"

    for i in range(int(natom)):
        print >> out, " %13.9f %13.9f %13.9f" %(position[i,0],position[i,1],position[i,2]),
        print >> out, ""

    out.close()

################################################################################
def options():
    name = 'scf.in'

    parser = optparse.OptionParser()

    parser.add_option(  '-i','--input', dest='INPUT', default=name,)
    options,args = parser.parse_args()

    if options.INPUT:
        name=options.INPUT

    if len(args) > 0:
        name=args[0]

    return name

################################################################################
if __name__ == '__main__':

    input_name = options()
    pwin = SAE.ReadPwIn(input_name)

    cname = input_name
    title = pwin.get_title()
    scale = pwin.get_scale()
    t = pwin.get_t()
    natom = pwin.get_natom()
    nion = pwin.get_nion()
    atoms = pwin.get_atoms()
    atoms_index = pwin.get_atoms_index()
    position = pwin.get_position()

    write_poscar(\
        cname,\
        title,\
        scale,t,natom,nion,atoms,atoms_index,\
        position)

    print "INPUT  :",input_name
    print "OUTPUT :",input_name+'.vasp'

