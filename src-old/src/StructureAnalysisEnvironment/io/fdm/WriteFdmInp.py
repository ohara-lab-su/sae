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

from ase.io import read, write
from ase.io.vasp import *
from ase.io.wien2k import *  ## using cellconst
# from ase.io.xyz import *
from ase import Atoms

import os
import sys
import optparse
import numpy as np


class WriteFdmInp(object):
    def __init__(self, atoms=None):
        """
        :param atoms:  ASE-ATOMS object
        """
        if atoms is not None:
            self.__atoms = atoms

        self.__absorber = 1
        self.__fileout = 'Cu'
        self.__e_range = "-15. 0.2  0. 0.5 10. 1. 45."
        self.__edge = 'K'
        self.__radius = 5
        self.__rmt = None
        self.__energpho = False
        self.__green = False
        self.__MOL = False

    def get_absorber(self):
        return self.__absorber

    def set_absorber(self, val):
        self.__absorber = val

    absorber = property(get_absorber, set_absorber)

    def get_fileout(self):
        return self.__fileout

    def set_fileout(self, val):
        self.__fileout = val

    fileout = property(get_fileout, set_fileout)

    def get_e_range(self):
        return self.__e_range

    def set_e_range(self, val):
        self.__e_range = val

    e_range = property(get_e_range, set_e_range)

    def get_edge(self):
        return self.__edge

    def set_edge(self, val):
        self.__edge = val

    edge = property(get_edge, set_edge)

    def get_radius(self):
        return self.__radius

    def set_radius(self, val):
        self.__radius = val

    radius = property(get_radius, set_radius)

    def get_rmt(self):
        return self.__rmt

    def set_rmt(self, val):
        self.__rmt = val

    def get_energpho(self):
        return self.__energpho

    def set_energpho(self, val_):
        self.__energpho = val_

    energpho = property(get_energpho, set_energpho)

    def get_MOL(self):
        return self.__MOL

    def set_MOL(self, val_):
        self.__MOL = val_

    MOL = property(get_MOL, set_MOL)

    #
    # 書き出し
    #

    def write_structure_inp(self, out, atoms=None, MOL=False):
        """
        構造情報パート

        :param out: ファイルディスクプリター(instance)
        :param atoms:
        :param MOD:
        :return:
        """
        if atoms is None: atoms = self.__atoms

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

    def write_conv_inp(self, out, conv_out=None, ecent=None, elarg=None, gamma_hole=None, gamma_max=None):
        """
        Convolution 情報の書き込み

        :param out: ファイルディスクプリター(instance)
        :param conv_out:
        :param ecent:
        :param elarg:
        :param gamma_hole:
        :param gamma_max:
        :return:
        """
        print(" Convolution", file=out)
        print("", file=out)

        if conv_out is not None:
            print(" Conv_out", file=out)
            print("   %s" % conv_out, file=out)
            print("", file=out)

        if ecent is not None:
            print(" Ecent", file=out)
            print("   %s" % ecent, file=out)
            print("", file=out)

        if elarg is not None:
            print(" Ecent", file=out)
            print("   %s" % elarg, file=out)
            print("", file=out)

        if gamma_hole is not None:
            print(" Gamma_hole", file=out)
            print("   %s" % gamma_hole, file=out)
            print("", file=out)

        if gamma_max is not None:
            print(" Gamma_max", file=out)
            print("   %s" % gamma_max, file=out)
            print("", file=out)

    def write_inp(self, atoms= None, name='read_pdb.inp', absorber=None, fileout=None, e_range=None,
                  edge=None, radius=None, rmt=None, MOL=False):
        return self.write_fdmnes_inp(atoms=atoms, name=name, absorber=absorber, fileout=fileout, e_range=e_range, edge=edge, radius=radius, rmt=rmt, MOL=MOL)

    def write_fdmnes_inp(self,
                         atoms=None,
                         name='read_pdb.inp',
                         absorber=None,
                         fileout=None,
                         e_range=None,
                         edge=None,
                         radius=None,
                         R=None,
                         rmt=None,
                         green=False,
                         energpho=False,
                         conv_out=None,
                         ecent=None,
                         elarg=None,
                         gamma_hole=None,
                         gamma_max=None,
                         MOL=False):
        """
        FDMNES 形式のひな形を作る（構造はここでは作らない)

        :param atoms:  SAE のインスタンス
        :param name: 書き込みINPファイル
        :param absorber: アブソーバー番号
        :param fileout: 出力ファイル名prefix (例 Pd)
        :param e_range: エネルギーレンジ
        :param edge: 吸収端(K,L,,,)
        :param radius: クラスター半径
        :param R: クラスター半径(radiusの別名入力)
        :param rmt: MT半径
        :param green:
        :param energpho:
        :param conv_out: 出力 convolution 名 (fullname)
        :param ecent:
        :param elarg:
        :param gamma_hole:
        :param gamma_max:
        :param MOL:  分子の場合は True
        :return:
        """
        if atoms is None: atoms = self.__atoms
        if absorber is None: absorber = self.__absorber
        if fileout is None: fileout = self.__fileout
        if e_range is None: e_range = self.__e_range
        if edge is None: edge = self.__edge
        if R is not None: radius = R
        if radius is None: radius = self.__radius
        if rmt is None: rmt = self.__rmt
        if energpho is None: energpho = self.__energpho
        if MOL is None: MOL = self.__MOL
        if green is None: green = self.__green

        try:
            out = open(name, 'w')
        except:
            out.close()
            sys.exit("STOP:" + name + ".fdmnes file can't open")

        e_range_comment = "first energy, step, intermediary energy, step ..., last energy"

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

        if energpho:
            print("Energpho", file=out)
        else:
            print("!Energpho", file=out)
        print("", file=out)

        print(" Edge", file=out)
        print("  %s" % edge, file=out)
        print("! L23", file=out)
        print("", file=out)

        print("!Quadrupole", file=out)
        # print("", file=out)
        print(" Relativism", file=out)
        print("", file=out)

        # convolution 情報
        self.write_conv_inp(out, conv_out, ecent, elarg, gamma_hole, gamma_max)

        # print("", file=out)
        print("", file=out)
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

        if green:
            print(" Green", file=out)
            print("", file=out)
        else:
            print("!Green", file=out)
            print("", file=out)

        print(" Radius                       ! Radius of the cluster where final state calculation is performed", file=out)
        radius_comment = 'For a good calculation, this radius must be increased up to 6 or 7 Angstroems'
        print("   %s  ! %s" % (radius, radius_comment), file=out)
        print("", file=out)

        if rmt is not None:
            print("Rmt", file=out)
            print(" %s" % str(rmt), file=out)
            print("", file=out)

        print(" Memory_save", file=out)
        print("", file=out)

        # 構造情報
        self.write_structure_inp(out, atoms, MOL)

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

    def write_fdmnes(self,
                     atoms=None,
                     prefix_name='POSCAR',
                     name=None,
                     STD=True,
                     MOL=False):
        """
        FDMNES 入力形式へ POSCAR を変換する

        :param atoms:
        :param name: 書き込み名のprefix. "name.fdmnes" ファイルとして出力される
        :param STD:
        :param MOL:
        :return:
        """
        if atoms is None:
            atoms = self.__atoms

        if name is not None:
            prefix_name = name

        if STD:
            out = sys.stdout
        else:
            try:
                out = open(prefix_name + '.fdmnes', 'w')
            except:
                out.close()
                sys.exit("STOP:" + prefix_name + ".fdmnes file can't open")

        #  atoms = atoms2.copy()
        self.write_structure_inp(out, atoms, MOL)

        if not STD:
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

    # fdm.write_fdmnes(atoms=atoms, MOL=MOL)
    fdm.write_fdmnes(name=name, atoms=atoms, STD=False, MOL=MOL)
    fdm.write_fdmnes_inp(atoms=atoms, MOL=MOL)
