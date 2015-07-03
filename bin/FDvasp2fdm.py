#!/usr/bin/env python
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
def write_fdmnes(name='POSCAR',atoms=None,STD=True,MOL=False):

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
def write_fdmnes_inp(name='read_pdb.inp',atoms=None,MOL=False):

    try:
        out = open(name,'w')
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

    print >> out, "! FDMNES indata file"
    print >> out, ""
    print >> out, " Absorber"
    print >> out, "  1"
    print >> out, "! allsite"
    print >> out, ""
    print >> out, " Filout"
    print >> out, "  Cu"
    print >> out, ""
    print >> out, " Range                        ! Energy range of calculation (eV)"
    print >> out, "  -15. 0.2  0. 0.5 10. 1. 45. ! first energy, step, intermediary energy, step ..., last energy"
    print >> out, "! -15. 0.1 50. 1. 200.        !"
    print >> out, ""
    print >> out, "!Energpho"
    print >> out, ""
    print >> out, " Edge"
    print >> out, "  K"
    print >> out, "! L23"
    print >> out, ""
    print >> out, " Relativism"
    print >> out, ""
    print >> out, "!Magnetism"
    print >> out, ""
    print >> out, "!Quadrupole"
    print >> out, ""
    print >> out, "!TDDFT"
    print >> out, ""
    print >> out, " Green"
    print >> out, ""
    print >> out, "!No_Fermi"
    print >> out, "! SCF"
    print >> out, ""
    print >> out, " Radius                       ! Radius of the cluster where final state calculation is performed"
    print >> out, "   3.0                         ! For a good calculation, this radius must be increased up to 6 or 7 Angstroems"
    print >> out, ""
    print >> out, " Memory_save"
    print >> out, ""

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

    print >> out, ""
    print >> out, " Density"
    print >> out, "  state_all"
    print >> out, ""
    print >> out, "!Adimp"
    print >> out, "! 0.20"
    print >> out, ""
    print >> out, " Convolution"
    print >> out, ""
    print >> out, " End"
    print >> out, ""

    out.close()

################################################################################
def options():
    name = 'POSCAR'

    parser = optparse.OptionParser()
    parser.add_option( '-i','--ipput',dest='INPUT')
    parser.add_option( '-m','--mol',action='store_true',default=False)
    options,args = parser.parse_args()

    if options.INPUT: name = options.INPUT
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

    return [name,MOL]

################################################################################
if __name__ == '__main__':

    name,MOL = options()
    atoms = read_vasp(name)
    #atoms.write('POSCAR.pdb',format='pdb')

    #print atoms.positions
    #print ""
    #print atoms.cell
    #print ""
    #print atoms.get_scaled_positions()

    write_fdmnes(atoms=atoms,MOL=MOL)
    write_fdmnes(name=name,atoms=atoms,STD=False,MOL=MOL)
    write_fdmnes_inp(atoms=atoms,MOL=MOL)

