#!/usr/bin/env python
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# PWscf *.out --> CONTCAR(POSCAR) 変換出力
#
# 構造緩和の final だけを抜き出す
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
    name = 'scf.out'

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

    output_name = options()
    pwout = SAE.ReadPwOut(output_name)

    cname = output_name+'.CONTCAR'
    title = pwout.get_title()
    scale = pwout.get_scale()
    t = pwout.get_t()
    natom = pwout.get_natom()
    nion = pwout.get_nion()
    atoms = pwout.get_atoms()
    atoms_index = pwout.get_atoms_index()
    position = pwout.get_position()

    write_poscar(\
        cname,\
        title,\
        scale,t,natom,nion,atoms,atoms_index,\
        position)

    print "INPUT  :",output_name
    print "OUTPUT :",output_name+'.CONTCAR'+'.vasp'

