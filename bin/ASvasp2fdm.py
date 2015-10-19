#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# VASP to FDMNES crystal 情報
#
# using ASE version
#
# (注意)
#  1) ASE のルーチン(cellconst) を使っている
#  2) ASE のmodule を呼び出している
#
################################################################################
#
# 2015.08.18
#  ASE で読み込む構造を止めて、拙作 SAEnv を用いる様にした
#    注意) scale ファクターは 1 を要求
#
# 2015.05.18 startup
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
#
#from ase.io.xyz import *

#from ase import Atoms
#from ase.io import read,write
#from ase.io.vasp import *
#from ase.io.wien2k import *  ## using cellconst

import os
import sys
import optparse
#import numpy as np

from ase.io.vasp import *
import StructureAnalysisEnvironment as SAEnv

################################################################################
def options():
    name = 'POSCAR'
    outname = 'read_pdb.inp'

    parser = optparse.OptionParser()
    parser.add_option( '-i','--ipput',dest='INPUT')
    parser.add_option( '-o','--outname')
    parser.add_option( '-m','--mol',action='store_true',default=False)
    options,args = parser.parse_args()

    if options.INPUT: name = options.INPUT
    if options.outname: outname = options.outname
    if len(args) > 0: name = str(args[0])

    if options.mol:
        MOL=True
    else:
        MOL=False

    if not os.path.exists(name):
        if os.path.exists(name+'.vasp'):
            name = name+'.vasp'
        else:
            sys.exit("STOP: "+name+" file not found")

    return name,outname,MOL

################################################################################
if __name__ == '__main__':

    name,outname,MOL = options()

    cell = SAEnv.Read(filename=name,code='VASP')
    cell.write(code='FDMNES',outname=outname,STD=True,MOL=MOL)
    cell.write(code='FDMNES',outname=outname,MOL=MOL)

## ASE version
#   atoms = read_vasp(name)
#   SAEnv.print_fdmnes0(atoms=atoms,MOL=MOL)
#   SAEnv.print_fdmnes0(outname=outname,atoms=atoms,STD=False,MOL=MOL)
#   SAEnv.print_fdmnes_inp0(atoms=atoms,MOL=MOL)

### SAEnv version
#   cell = SAEnv.Read(filename = name, code = 'VASP')
#   SAEnv.print_fdmnes1(outname=outname,cell=cell,MOL=MOL)
#   SAEnv.print_fdmnes1(outname=outname,cell=cell,STD=False,MOL=MOL)
#   SAEnv.print_fdmnes_inp1(cell=cell,MOL=MOL)


