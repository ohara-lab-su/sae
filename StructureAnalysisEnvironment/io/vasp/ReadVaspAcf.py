#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# ACF.dat for VASP
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応暫定
#
# 2015.07.07 startup
#
################################################################################
from __future__ import print_function

try:
    from ...copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.5"

################################################################################
import sys
import os
import re
# import gzip
import numpy as np

import optparse

# import SpaceGroupEnvironment as SGE
try:
    sys.path.append('../../')
    import StructureAnalysisEnvironment as SAEnv
except ImportError:
    import StructureAnalysisEnvironment as SAEnv

################################################################################
class ReadVaspAcf(object):

    def __init__(self, poscar=None, potcar=None, acf='ACF.dat'):

        self.datlines, self.num = SAE.read_dataline(acf)

        if isinstance(poscar, SAE.ReadVaspPoscar):
            self.poscar = poscar
            self.natom = self.poscar.natom
            self.nion = self.poscar.nion
            self.atoms = self.poscar.atoms
            self.atoms_index_j = self.poscar.atoms_index_j
        else:
            sys.exit("STOP: poscar is not ReadPoscar instance")

        if isinstance(potcar, SAE.ReadVaspPotcar):
            self.potcar = potcar
            self.atoms_index = self.potcar.atoms_index
            self.atoms_zval = self.potcar.atoms_zval

            self.atoms_zval_j = []
            for k in range(self.nion):
                for l in range(int(self.atoms[k])):
                    self.atoms_zval_j.append(float(self.atoms_zval[k]))
        else:
            sys.exit("STOP: potcar is not ReadVaspPotcar instance")

        line_reg = re.compile('.*-------.*')

        ###################################
        ## get Barder (生) Charge
        self.charge = np.zeros(self.natom)
        self.bader = np.zeros(self.natom)
        i = 2
        while 1:
            self.charge[i - 2] = float(self.datlines[i].split()[4])
            # self.bader[i-2] = self.atoms_zval_j[i-2] - self.charge[i-2]
            self.bader[i - 2] = self.charge[i - 2] - self.atoms_zval_j[i - 2]
            i += 1
            if bool(line_reg.match(self.datlines[i])):
                break
        acfline = i - 2
        if self.poscar is not None:
            if acfline != self.poscar.natom:
                sys.exit("STOP: natom =! ACF.dat line#")

    #       for i in range(self.natom):
    #           print i+1,self.atoms_index_j[i],self.atoms_zval_j[i],self.charge[i]

    def get_nion(self):
        return self.nion

    def get_natom(self):
        return self.natom

    def get_charge(self):
        return self.charge

    def get_bader(self):
        return self.bader

    def get_max_bader(self):
        self.max_bader = max(self.bader)
        return self.max_bader

    def get_min_bader(self):
        self.min_bader = min(self.bader)
        return self.min_bader

    def get_atoms_zval_j(self):
        return self.atoms_zval_j

    def get_atoms_zval(self):
        return self.atoms_zval

    def get_atoms(self):
        return self.atoms

    def get_atoms_index(self):
        return self.atoms_index

    def get_atoms_index_j(self):
        return self.atoms_index


################################################################################
def options():
    name = 'POSCAR'
    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest='INPUT', )
    options, args = parser.parse_args()

    if options.INPUT: name = options.INPUT

    if not os.path.exists(name):
        name0 = 'CONTCAR'
        if not os.path.exists(name0):
            sys.exit("STOP: " + name + " and " + name0 + " file not found")
        else:
            name = name0

    return name


################################################################################
if __name__ == '__main__':

    name = options()

    poscar = SAE.ReadPoscar(name)
    potcar = SAE.ReadVaspPotcar()
    acfdat = ReadVaspAcf(poscar=poscar, potcar=potcar, acf='ACF.dat')
    acfdat.get_max_bader()
    acfdat.get_min_bader()

    print("#  atom  zval  charge  diff")
    for i in range(acfdat.natom):
        print("%3d %s %5.2f %7.3f %7.3f"
              % (i + 1, acfdat.atoms_index_j[i], acfdat.atoms_zval_j[i],
                 acfdat.charge[i], acfdat.bader[i]))

    print("MAX charge %s" % str(acfdat.max_bader))
    print("MIN charge %s" % str(acfdat.min_bader))
#   print poscar.natom
