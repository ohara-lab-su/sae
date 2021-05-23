#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# VASP to FDMNES crystal 情報
#
# 構造ファイル & INPUT file
#
# (注意)
#  1) ASE のルーチン(cellconst) を使っている
#  2) ASE のmodule を呼び出している
#  3) atoms は ASE オブジェクトが前提
#
# FDvasp2fdm.py がベース --> class 化
#
################################################################################
from __future__ import print_function

################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
#
__status__ = "alpha"
__version__ = "0.1.1"

################################################################################
#
from ase.io import read, write
from ase.io.vasp import *
from ase.io.wien2k import *  ## using cellconst
# from ase.io.xyz import *
from ase import Atoms

import os
import sys
import optparse
import numpy as np


class WriteFdmInp():
    def __init__(self, atoms=None):
        """
        :param atoms:  ASE-ATOMS object
        """
        if atoms is not None:
            self.__atoms = atoms

    def write_fdmnes(self, name='POSCAR', atoms=None, STD=True, MOL=False):
        """
        FDMNES 入力形式へ POSCAR を変換する

        :param name:
        :param atoms:
        :param STD:
        :param MOL:
        :return:
        """
        if atoms is None:
            atoms = self.__atoms

        if STD:
            out = sys.stdout
        else:
            try:
                out = open(name + '.fdmnes', 'w')
            except:
                out.close()
                sys.exit("STOP:" + name + ".fdmnes file can't open")

        #   atoms = atoms2.copy()

        cell = atoms.get_cell()
        metT = np.dot(cell, np.transpose(cell))
        cell2 = cellconst(metT)  # from ASE module

        a = cell2[0]
        b = cell2[1]
        c = cell2[2]
        alpha = cell2[3]
        beta = cell2[4]
        gamma = cell2[5]

        nat = len(atoms.get_positions())

        if MOL:
            print(" molecule", file=out)
        else:
            print(" Crystal", file=out)

        print("      %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f" % (a, b, c, alpha, beta, gamma), file=out)
        for ii in range(nat):
            zza = atoms.get_atomic_numbers()[ii]
            # pos = atoms.get_positions()[ii]
            pos = atoms.get_scaled_positions()[ii]
            sym = atoms.get_chemical_symbols()[ii]
            print("   %2d %8.4f %8.4f %8.4f    ! %s" % (zza, pos[0], pos[1], pos[2], sym), file=out)

        if not STD:
            out.close()

    def write_fdmnes_inp(self,
                         name='read_pdb.inp',
                         absorber=1,
                         fileout='Cu',
                         e_range=None,
                         edge='K',
                         radius=5,
                         atoms=None,
                         MOL=False):
        """
        FDMNES 形式のひな形を作る（構造はここでは作らない)

        :param name: 読み込むファイル
        :param absorber: アブソーバー番号
        :param fileout: 出力ファイル名prefix
        :param e_range: エネルギーレンジ
        :param edge: 吸収端(K,L,,,)
        :param radius: クラスター半径
        :param atoms:  SAE のインスタンス
        :param MOL:  分子の場合は True
        :return:
        """
        try:
            out = open(name, 'w')
        except:
            out.close()
            sys.exit("STOP:" + name + ".fdmnes file can't open")

        e_range_comment = "first energy, step, intermediary energy, step ..., last energy"
        if e_range is None:
            e_range = "-15. 0.2  0. 0.5 10. 1. 45."
        #   atoms = atoms2.copy()

        cell = atoms.get_cell()  # from ASE
        metT = np.dot(cell, np.transpose(cell))
        cell2 = cellconst(metT)  # from ASE module

        a = cell2[0]
        b = cell2[1]
        c = cell2[2]
        alpha = cell2[3]
        beta = cell2[4]
        gamma = cell2[5]

        nat = len(atoms.get_positions())

        print("! FDMNES indata file", file=out)
        print("", file=out)
        print("!Nonexc", file=out)
        print("", file=out)
        print(" Absorber", file=out)
        print("  %s" % absorber, file=out)
        print("! allsite", file=out)
        print("", file=out)
        print(" Filout", file=out)
        print("  %s" % fileout, file=out)
        print("", file=out)
        print(" Range                        ! Energy range of calculation (eV)", file=out)
        print("  %s  ! %s " % (e_range, e_range_comment), file=out)
        print("! -15. 0.1 50. 1. 200.        !", file=out)
        print("", file=out)
        print("!Energpho", file=out)
        print("", file=out)
        print(" Edge", file=out)
        print("  %s" % edge, file=out)
        print("! L23", file=out)
        print("", file=out)
        print("!Quadrupole", file=out)
        # print("", file=out)
        print(" Relativism", file=out)
        # print("", file=out)
        print(" Convolution", file=out)
        # print("", file=out)
        print("!No_Fermi", file=out)
        print("!Efermi", file=out)
        print("!  -6.0", file=out)
        print("!Estart", file=out)
        print("! -10.0", file=out)
        print("", file=out)
        print("!SCF", file=out)
        print("!R_self", file=out)
        print("! 5.0", file=out)
        print("!N_self", file=out)
        print("! 100", file=out)
        print("!P_self", file=out)
        print("! 0.05", file=out)
        print("!Delta_E_conv", file=out)
        print("! 0.01", file=out)
        print("", file=out)
        print("!Magnetism", file=out)
        print("!SCF_mag_free", file=out)
        print("", file=out)
        print("!Hubbard", file=out)
        print("! 0.0 6.3 0.0", file=out)
        print("", file=out)
        print("!TDDFT", file=out)
        print("", file=out)
        print("!Green", file=out)
        print("", file=out)

        print(" Radius                       ! Radius of the cluster where final state calculation is performed", file=out)
        radius_comment = 'For a good calculation, this radius must be increased up to 6 or 7 Angstroems'
        print("   %s  ! %s" % (radius, radius_comment), file=out)
        print("", file=out)

        print(" Memory_save", file=out)
        print("", file=out)

        if MOL:
            print(" molecule", file=out)
        else:
            print(" Crystal", file=out)

        print("      %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f" % (a, b, c, alpha, beta, gamma), file=out)
        for ii in range(nat):
            zza = atoms.get_atomic_numbers()[ii]
            # pos = atoms.get_positions()[ii]
            pos = atoms.get_scaled_positions()[ii]
            sym = atoms.get_chemical_symbols()[ii]
            print("   %2d %8.4f %8.4f %8.4f    ! %s" % (zza, pos[0], pos[1], pos[2], sym), file=out)

        print("", file=out)
        print("!Cif_file", file=out)
        print("!  POSCAR.cif", file=out)
        print("", file=out)
        print(" Density", file=out)
        print("  state_all", file=out)
        print("", file=out)
        print("!Adimp", file=out)
        print("! 0.20", file=out)
        print("", file=out)
        print(" End", file=out)
        print("", file=out)

        out.close()


def options():
    name = 'POSCAR'

    parser = optparse.OptionParser()
    parser.add_option('-i', '--ipput', dest='INPUT')
    parser.add_option('-m', '--mol', action='store_true', default=False)
    options, args = parser.parse_args()

    if options.INPUT: name = options.INPUT
    if len(args) > 0: name = str(args[0])

    if options.mol:
        MOL = True
    else:
        MOL = False

    if not os.path.exists(name):
        if os.path.exists(name + '.vasp'):
            name = name + '.vasp'
        else:
            sys.exit("STOP: " + name + " file not found")

    return [name, MOL]


################################################################################
if __name__ == '__main__':
    name, MOL = options()
    atoms = read_vasp(name)
    # atoms.write('POSCAR.pdb',format='pdb')

    fdm = WriteFdmInp(atoms)
    # print atoms.positions
    # print ""
    # print atoms.cell
    # print ""
    # print atoms.get_scaled_positions()

    fdm.write_fdmnes(atoms=atoms, MOL=MOL)
    fdm.write_fdmnes(name=name, atoms=atoms, STD=False, MOL=MOL)
    fdm.write_fdmnes_inp(atoms=atoms, MOL=MOL)
