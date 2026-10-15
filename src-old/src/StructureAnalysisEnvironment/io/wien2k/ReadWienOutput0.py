#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# WIEK2k case.output0 を読み込む class  ( for lapw0 )
#
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.03.24
#   startup
#
################################################################################
from __future__ import print_function

try:
    from ...copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import sys
import os
import re
# import gzip
import numpy as np

# import optparse

try:
    # sys.path.append('../..')
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    import StructureAnalysisEnvironment as SAEnv
except ImportError:
    import StructureAnalysisEnvironment as SAEnv


# import SpaceGroupEnvironment as SGE

################################################################################
class ReadWienOutput0(object):

    ###############################################
    ## init and Read POSCAR
    def __init__(self, name):
        self.datlines, self.num = SAEnv.read_dataline(name)

        ion_txt = '^:NATO'
        ion_reg = re.compile(ion_txt)

        not_equiv_txt = '.*NOT EQUIV ATOM'
        not_equiv_reg = re.compile(not_equiv_txt)

        equiv_txt = ' +EQUIV ATOM'
        equiv_reg = re.compile(equiv_txt)

        spin_txt = '.*IZED CALCULATION'
        spin_reg = re.compile(spin_txt)

        self.atoms_index = []
        i = 0
        j = 0
        while i < self.num:

            # chk NATOM &  NION
            if bool(ion_reg.match(self.datlines[i])):
                self.nion = int(self.datlines[i].split()[2])
                self.natom = int(self.datlines[i].split()[5])
                self.atoms = np.zeros(self.nion, dtype=int)

            # chk NOT EQUIV ATOM
            if bool(not_equiv_reg.match(self.datlines[i])):
                atom = self.datlines[i].split()[3]
                self.atoms_index.append(atom)
                while not bool(not_equiv_reg.match(self.datlines[i + 1])):
                    if bool(equiv_reg.match(self.datlines[i])):
                        self.atoms[j] = int(self.datlines[i].split()[2])
                    if bool(spin_reg.match(self.datlines[i])):
                        break
                    i += 1
                j += 1

            # chk SPIN
            if bool(spin_reg.match(self.datlines[i])):
                spin_word = self.datlines[i].split()[0]
                if spin_word == 'SPINPOLARIZED':
                    self.nspin = 2
                elif spin_word == 'NON-SPINPOLARIZED':
                    self.nspin = 1
                else:
                    sys.exit("STOP: UNKNOWN SPIN MODE")

            i += 1  # END_while

    ############################################################################
    # atoms_index と ions_index は同じ意味
    # 結局サイトごとの元素記号になるので atoms_index と同じ
    def get_ions_index(self):
        return self.atoms_index

    ############################################################################
    # atoms_index と ions_index は同じ意味(結局サイトごと)
    # 結局サイトごとの元素記号になるので ions_index と同じ
    def get_atoms_index(self):
        return self.atoms_index

    ############################################################################
    # atoms
    def get_atoms(self):
        return self.atoms

    ############################################################################
    def get_ispin(self):
        return self.nspin

    ############################################################################
    def get_nion(self):
        return self.nion

    ############################################################################
    def get_natom(self):
        return self.natom


################################################################################
if __name__ == '__main__':
    name = 'Cu.output0'
    dos = ReadWienOutput0(name)

    nspin = dos.get_ispin()
    natom = dos.get_natom()
    nion = dos.get_nion()
    ions_index = dos.get_ions_index()
    atoms_index = dos.get_atoms_index()
    atoms = dos.get_atoms()

    print("nspin       %s" % str(nspin))
    print("natom       %s" % str(natom))
    print("nion        %s" % str(nion))
    print("atoms_index %s" % str(atoms_index))
    print("atoms       %s" % str(atoms))
