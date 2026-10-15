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
################################################################################
# import gzip
# import optparse
# sys.path.append('../..')
# import SpaceGroupEnvironment as SGE
################################################################################
################################################################################
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import numpy as np


###############################################
## init and Read POSCAR
############################################################################
# atoms_index と ions_index は同じ意味
# 結局サイトごとの元素記号になるので atoms_index と同じ
############################################################################
# atoms_index と ions_index は同じ意味(結局サイトごと)
# 結局サイトごとの元素記号になるので ions_index と同じ
############################################################################
# atoms
############################################################################
############################################################################
############################################################################
class ReadWienOutput0(object):

    def __init__(self, name):
        from sae.common.text import TextFiles

        self.datlines, self.num = TextFiles().read_dataline(name)
        ion_txt = "^:NATO"
        ion_reg = re.compile(ion_txt)
        not_equiv_txt = ".*NOT EQUIV ATOM"
        not_equiv_reg = re.compile(not_equiv_txt)
        equiv_txt = " +EQUIV ATOM"
        equiv_reg = re.compile(equiv_txt)
        spin_txt = ".*IZED CALCULATION"
        spin_reg = re.compile(spin_txt)
        self.atoms_index = []
        i = 0
        j = 0
        # chk NATOM &  NION
        # chk NOT EQUIV ATOM
        # chk SPIN
        while i < self.num:
            if bool(ion_reg.match(self.datlines[i])):
                self.nion = int(self.datlines[i].split()[2])
                self.natom = int(self.datlines[i].split()[5])
                self.atoms = np.zeros(self.nion, dtype=int)
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
            if bool(spin_reg.match(self.datlines[i])):
                spin_word = self.datlines[i].split()[0]
                if spin_word == "SPINPOLARIZED":
                    self.nspin = 2
                elif spin_word == "NON-SPINPOLARIZED":
                    self.nspin = 1
                else:
                    sys.exit("STOP: UNKNOWN SPIN MODE")
            # END_while
            i += 1

    def get_ions_index(self):
        return self.atoms_index

    def get_atoms_index(self):
        return self.atoms_index

    def get_atoms(self):
        return self.atoms

    def get_ispin(self):
        return self.nspin

    def get_nion(self):
        return self.nion

    def get_natom(self):
        return self.natom
