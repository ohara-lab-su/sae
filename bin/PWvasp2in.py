#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#   convert PWScf (Quantum ESPRESSO ) to *.in
#
################################################################################
#
# 2015.03.20
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
import sys
import os
import re
#import numpy as np

#import glob
import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE


################################################################################
def options():

    poscarname = 'POSCAR'
    outbase    = 'POSCAR'
    inpsuffix  = '.in'

    parser = optparse.OptionParser(os.getcwd())
    parser = optparse.OptionParser()

    parser.add_option(  '-s','--stdout',
                       action='store_true',
    )
    parser.add_option( '-i','--input',
                       dest='INPUT',
    )
    parser.add_option( '-o','--output',
                       dest='OUTPUT',
    )
    options, args = parser.parse_args()

    outbase=re.sub('\.in$','',outbase)
    outinp=outbase+inpsuffix

    if options.INPUT:
        poscarname=options.INPUT

    outbase=poscarname
    if options.OUTPUT:
        outbase=re.sub('\.inp$','',options.OUTPUT)
        outinp=outbase+inpsuffix

    # オプション無し引数の時は拡張子自動削除を付けずにそのままファイル名とする
    if len(args) >0:
        poscarname=args[0]

    if poscarname == outinp:
        sys.exit("STOP: INPUT_NAME = OUTPUT_NAME :"+poscarname)

    print "INPUT :",poscarname
    print "OUTPUT:",outbase+inpsuffix

    return [poscarname,outbase,inpsuffix,options.stdout]

################################################################################
if __name__ == '__main__':

    ############################################################################
    # mode
    title       = 'input'
    calculation = 'scf'
    title       = 'input'
    pseudo_dir  = './'
    outdir      = './work/'
    ecutwfc     = 25.0
    ecutrho     = 100.0  # ecutwfc*4.0
    occupations = 'tetrahedra'
    mixing_beta = 0.7
    conv_thr    = 0.01
    mag         = 0.6  # starting_magnetization(1)

    ############################################################################
    # get filename
    poscarname,outbase,inpsuffix,OPT_STD = options()

    ############################################################################
    # POSCAR 読み込み
    poscar = SAE.ReadVaspPoscar(poscarname)

    vasp = poscar.get_vasp_version()
    if vasp < 5:
        sys.exit("STOP: This script requires VASP5 style POSCAR")

   #title = poscar.get_title()
    t = poscar.get_t()
    scale = poscar.get_scale()
    atoms = poscar.get_atoms()
    atoms_index = poscar.get_atoms_index()
    atoms_index_j = poscar.get_atoms_index_j()
    natom = poscar.get_natom()
    nion = poscar.get_nion()
    selective = poscar.get_selective()
    direct = poscar.get_direct()
    position = poscar.get_position()
    fix = poscar.get_fix()

    ion = poscar.get_ion()
    ion_local = poscar.get_ion_local()

    ############################################################################
    # output system.inp
    if OPT_STD:
        out = sys.stdout
    else:
        try:
            out = open(outbase+inpsuffix,'w')
        except:
            out.close()
            sys.exit("STOP: "+outbase+inpsuffix+" can't open")

    print >> out, "&control"
    print >> out, "                calculation = "+"'"+calculation+"'"+","
    print >> out, "                     prefix = "+"'"+title+"'"+","
    print >> out, "                 pseudo_dir = "+"'"+pseudo_dir+"'"+","
    print >> out, "                     outdir = "+"'"+outdir+"'"+","
    print >> out, "/"

    print >> out, "&system"
    print >> out, "                      ibrav = 0,"
    print >> out, "                          a = "+str(scale)+","
    print >> out, "                        nat = "+str(natom)+","
    print >> out, "                       ntyp = "+str(nion)+","
    print >> out, "                    ecutwfc = "+str(ecutwfc)+","
    print >> out, "!                   ecutrho = "+str(ecutrho)+","
    print >> out, "                occupations = "+str(occupations)+","
    print >> out, "!               occupations = 'smearing'"+","
    print >> out, "!                  smearing = 'mp'"+","
    print >> out, "!                  smearing = 'gaussian'"+","
    print >> out, "!                   degauss = 0.01"+","
    print >> out, "!                     nspin = "+"2"+","
    print >> out, "! starting_magnetization(1) = "+str(mag)+","
    print >> out, "/"

    print >> out, "&electrons"
    print >> out, "                mixing_beta = "+str(mixing_beta)+","
    print >> out, "                   conv_thr = "+str(conv_thr)+","
    print >> out, "/"

    print >> out, "CELL_PARAMETERS {alat}"
    print >> out, " %18.15f %18.15f %18.15f" %(t[0,0], t[1,0], t[2,0])
    print >> out, " %18.15f %18.15f %18.15f" %(t[0,1], t[1,1], t[2,1])
    print >> out, " %18.15f %18.15f %18.15f" %(t[0,2], t[1,2], t[2,2])

    print >> out, "ATOMIC_SPECIES"
    for ion in range(nion):
        atomic_weight = SAE.get_atomic_weight1(atoms_index[ion])
       #print >> out, " %s %9.5f" %(atoms_index[ion], atomic_weight)
        print >> out, " %s %9.5f %s%s" \
                %(atoms_index[ion], atomic_weight,atoms_index[ion],"_PSEUDO")

    print >> out, "ATOMIC_POSITIONS {crystal}"
    for j in range(natom):
        print >> out, " %s  %18.15f %18.15f %18.15f" \
                %( atoms_index_j[j], position[j,0], position[j,1], position[j,2] )

    print >> out, "K_POINTS {automatic}"
    print >> out, "6 6 6 0 0 0"

    if not OPT_STD:
        out.close()

