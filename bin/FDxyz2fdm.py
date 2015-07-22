#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
# xyz to FDMNES crystal 情報
#
################################################################################
#
# 2015.06.30
#  == None --> is None
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
import os
import sys
import optparse
#import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
def write_fdmnes(xyz,name='POSCAR',STD=True):

    if STD:
        out = sys.stdout
    else:
        try:
            out = open(name+'.fdmnes','w')
        except:
            out.close()
            sys.exit("STOP:"+name+".fdmnes file can't open")

    natom = xyz.get_natom()
    atoms_index_j = xyz.get_atoms_index_j()
    position = xyz.get_position()

    print >> out, " molecule"

    print >> out, "      1.0 1.0 1.0 90.0 90.0 90.0"
    for ii in range(natom):
        pos = position[ii]
        sym = atoms_index_j[ii]
        zza = SAE.get_atomic_number1(atoms_index_j[ii])

        print >> out, "   %2d %12.6f %12.6f %12.6f    ! %s"  % ( zza,pos[0],pos[1],pos[2],sym )

    if not STD:
        out.close()


################################################################################
def write_fdmnes_inp(xyz,name='read_pdb.inp'):


    natom = xyz.get_natom()
    atoms_index_j = xyz.get_atoms_index_j()
    position = xyz.get_position()

#   max_x = max(position[:,0])
#   max_y = max(position[:,1])
#   max_z = max(position[:,2])
#   min_x = min(position[:,0])
#   min_y = min(position[:,1])
#   min_z = min(position[:,2])

#   print max_x,max_y,max_z
#   print min_x,min_y,min_z
#   print abs(max_x-min_x),abs(max_y-min_y),abs(max_z-min_z)
#   print (max_x-min_x)/2.,(max_y-min_y)/2.,(max_z-min_z)/2.

#   lattice = max(abs(max_x-min_x),abs(max_y-min_y),abs(max_z-min_z)) + 1
#   print lattice


    try:
        out = open(name,'w')
    except:
        out.close()
        sys.exit("STOP:"+name+".fdmnes file can't open")

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

    print >> out, " molecule"

    print >> out, "      1.0 1.0 1.0 90.0 90.0 90.0"
#   print >> out, "      "+str(lattice)+" "+str(lattice)+" "+str(lattice)+" 90.0 90.0 90.0"
    for ii in range(natom):
        pos = position[ii]
        sym = atoms_index_j[ii]
        zza = SAE.get_atomic_number1(atoms_index_j[ii])
#       px = pos[0]/lattice
#       py = pos[1]/lattice
#       pz = pos[1]/lattice
        px = pos[0]
        py = pos[1]
        pz = pos[2]
        print >> out, "   %2d %12.6f %12.6f %12.6f    ! %s"  % ( zza,px,py,pz,sym )

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

    MD0 = "xyzfile"
    suffix = "md"

    MD = MD0+'.'+suffix

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT',)
    options,  args = parser.parse_args()

    if options.INPUT: MD=options.INPUT
    if len(args) > 0: MD=args[0]

    if not os.path.exists(MD):
        MD0 = SAE.find_datfile('md')
        suffix ='md'
        if MD0 is None:
            MD0 = SAE.find_datfile('xyz')
            suffix ='xyz'
            if MD0 is None:
                sys.exit("STOP: INPUT file not found.")

        if not os.path.exists(MD0+'.md'):
            MD0 = SAE.find_datfile('xyz')
            suffix ='xyz'
            if not os.path.exists(MD0+'.xyz'):
                sys.exit("STOP")

    MD = MD0+'.'+suffix

    MOL = True

    return MD0,suffix,MOL

################################################################################
if __name__ == '__main__':

    MD0,suffix,MOL = options()
    MD = MD0+'.'+suffix
    xyz = SAE.ReadMd(MD)

    write_fdmnes(xyz)
    write_fdmnes(xyz,name=MD0,STD=False)
    write_fdmnes_inp(xyz)

#   natom = xyz.get_natom()
#   atoms_index_j = xyz.get_atoms_index_j()
#   position = xyz.get_position()

#   print natom
#   print ""
#   for j in range(natom):
#       print " %s %13.9f %13.9f %13.9f" \
#               %(atoms_index_j[j],position[j,0],position[j,1],position[j,2])

