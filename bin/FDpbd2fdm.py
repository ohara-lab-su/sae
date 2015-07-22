#!/usr/bin/env python
################################################################################
# PDB to FDMNES crystal 情報
#  using ASE version
#
################################################################################
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
from ase.io import read,write
from ase.io.vasp import *
#from ase.io.xyz import *
from ase import Atoms

import os
import sys
import optparse
import numpy as np

################################################################################
# from ase.io.wien2k
def cellconst(metT):
    """ metT=np.dot(cell,cell.T) """
    aa = np.sqrt(metT[0, 0])
    bb = np.sqrt(metT[1, 1])
    cc = np.sqrt(metT[2, 2])
    gamma = np.arccos(metT[0, 1] / (aa * bb)) / np.pi * 180.0
    beta = np.arccos(metT[0, 2] / (aa * cc)) / np.pi * 180.0
    alpha = np.arccos(metT[1, 2] / (bb * cc)) / np.pi * 180.0
    return np.array([aa, bb, cc, alpha, beta, gamma])

################################################################################
def options():
    name = 'POSCAR.pdb'

    parser = optparse.OptionParser()
    parser.add_option( '-i','--ipput',dest='INPUT')
    options,args = parser.parse_args()

    if options.INPUT: name = options.INPUT
    if len(args) > 0: name = str(args[0])

    if not os.path.exists(name):
        sys.exit("STOP: "+name+" file not found")

    return name

################################################################################
def chk_cryst(fileobj):

    cryst = False
    if isinstance(fileobj, str):
        fileobj = open(fileobj)

    for line in fileobj.readlines():
        if line.startswith('CRYST1'):
            cryst = True

    fileobj.close()

    return cryst

################################################################################
def write_fdmnes(name='POSCAR.pdb',atoms=None,STD=True,MOL=False):

    if STD:
        out = sys.stdout
    else:
        try:
            out = open(name+'.fdmnes','w')
        except:
            out.close()
            sys.exit("STOP:"+name+".fdmnes file can't open")

#   atoms = atoms2.copy()

    cell = atoms.get_cell()
    metT = np.dot(cell, np.transpose(cell))
    cell2 = cellconst(metT)

    a = cell2[0]
    b = cell2[1]
    c = cell2[2]
    alpha = cell2[3]
    beta = cell2[4]
    gamma = cell2[5]

    nat = len(atoms.get_positions())

    # PDB ファイル中のCRYST1タグのチェック
    if MOL:
        print >> out, " molecule"
    else:
        print >> out, " Crystal"

    print >> out, "      %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f" % ( a,b,c,alpha,beta,gamma )
    for ii in range(nat):
        zza = atoms.get_atomic_numbers()[ii]
       #pos = atoms.get_positions()[ii]
        pos = atoms.get_scaled_positions()[ii]
        sym = atoms.get_chemical_symbols()[ii]
        print >> out, "   %2d %8.4f %8.4f %8.4f    ! %s"  % ( zza,pos[0],pos[1],pos[2],sym )

    if not STD:
        out.close()

################################################################################
if __name__ == '__main__':

    name = options()

    atoms = read(name,format='pdb')

#   print "atoms.cell"
#   print atoms.cell
#   print atoms.cellpar
#   print ""
#   print "atoms.positions"
#   print atoms.positions
#   print ""
#   print "atoms.gt_scaled_positions"
#   print atoms.get_scaled_positions()

    if chk_cryst(name):
        MOL=False
    else:
        MOL=True

    write_fdmnes(atoms=atoms,MOL=MOL)
    write_fdmnes(name=name,atoms=atoms,STD=False,MOL=MOL)

