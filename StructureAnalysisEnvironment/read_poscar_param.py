#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# POSCAR
#
# [in/out] POSCAR   : POSCAR file name
#
# [retun]  nion     : number of ion
# [retun]  natom    : number of atom
# [retun]  VASP     : VASP version
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
#
# 2015.01.21
#  for GZIP
#
# 2014.10.30 1st
#
################################################################################
from __future__ import print_function
from copyright import *

__status__ = "alpha"
__version__ = "0.0.2"

################################################################################

import sys
import os
import gzip


# import re
# from numpy import *

def read_poscar_param(POSCAR):
    ###############################################
    ## Open POSCAR file
    ##
    if os.path.exists(POSCAR):
        GZIP = False
    elif os.path.exists(POSCAR + ".gz"):
        GZIP = True
    else:
        sys.exit("STOP: " + POSCAR + " or " + POSCAR + ".gz file not found")

    try:
        if GZIP:
            tmp = gzip.open(POSCAR + ".gz")
        else:
            tmp = open(POSCAR)

        datfile = tmp.read()
    except:
        tmp.close()
        sys.exit("STOP: " + POSCAR + " does'nt open")
    finally:
        tmp.close()

    datlines = datfile.split('\n')

    #   print "number of line",len(datlines)
    #   for i in range(len(datlines)):
    #       print i, datlines[i]

    ###############################################
    ## get VASP version, atoms and index
    ##
    i = 5
    atoms = datlines[i].split()
    if atoms[0].isdigit():
        VASP = 4
    else:
        VASP = 5
        atoms_index = list(atoms)
        i += 1
        atoms = datlines[i].split()
        # print atoms_index[0]," ", atoms_index[1]

    ###############################################
    ## TEST print
    ##
    # if VASP > 4:
    #    for j in range(len(atoms)):
    #        print atoms_index[j],
    #    print ""
    #
    # for j in range(len(atoms)):
    #    print atoms[j],
    # print ""

    ###############################################
    ## get number of atoms
    ##
    nion = int(len(atoms))
    natom = 0
    for j in range(nion):
        sum = int(atoms[j])
        natom = natom + sum
    # print "natom= ",natom

    return [nion, natom, VASP]


################################################################################
if __name__ == '__main__':
    POSCAR = 'POSCAR'
    nion, natom, VASP = read_poscar_param(POSCAR)

    print("nion  = %s" % str(nion))
    print("natom = %s" % str(natom))
    print("VASP  = %s" % str(VASP))
