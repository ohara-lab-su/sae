# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.structure.base import Method
import sys
import re
import optparse
import numpy as np
import collections

try:
    Method = Method
except ImportError:
    Method = Method
from ase.io.wien2k import *


class ReadFdmInp(Method):
    """
    FDMNES の input ファイル名を読み込む
    """

    def __init__(self, inpname, suffix=".inp", sort=True, atoms_index=None):
        from sae.common.text import TextFiles
        from sae.structure.elements import ElementTable
        from sae.structure.ordering import AtomOrdering

        self.datlines, self.num = TextFiles().read_dataline(inpname)
        self.datlines, self.num = TextFiles().del_comment(self.datlines)
        nonexec_reg = re.compile(".*Nonexc.*", re.IGNORECASE)
        magnetism_reg = re.compile(".*Magnetism.*", re.IGNORECASE)
        energygpho_reg = re.compile(".*Energpho.*", re.IGNORECASE)
        absorber_reg = re.compile(".*Absorber.*", re.IGNORECASE)
        filout_reg = re.compile(".*Fil.*out.*", re.IGNORECASE)
        atom_reg = re.compile("^\\S*Atom", re.IGNORECASE)
        crystal_reg = re.compile(".*crystal.*", re.IGNORECASE)
        crystal_p_reg = re.compile(".*crystal_p.*", re.IGNORECASE)
        mole_reg = re.compile(".*molecule.*", re.IGNORECASE)
        char_reg = re.compile("\\D", re.IGNORECASE)
        comment_reg = re.compile("^!.*", re.IGNORECASE)
        allsite_reg = re.compile("^.*allsite.*", re.IGNORECASE)
        calculation_reg = re.compile("^.*Calculation.*", re.IGNORECASE)
        conv_out_reg = re.compile("^.*Conv_out.*", re.IGNORECASE)
        convolution_reg = re.compile("^.*Convolution.*", re.IGNORECASE)
        center_abs_reg = re.compile("^.*Center_abs.*", re.IGNORECASE)
        self.ispin = 1
        self.allsite = False
        self.energygpho = False
        self.position = []
        self.convolution = False
        self.center_abs = False
        self.nonexc = False
        for i in range(self.num):
            print("%s" % self.datlines[i])
            if bool(nonexec_reg.match(self.datlines[i])):
                self.nonexc = True
            if bool(energygpho_reg.match(self.datlines[i])):
                self.energygpho = True
            if bool(atom_reg.match(self.datlines[i])) and (
                not bool(comment_reg.match(self.datlines[i]))
            ):
                sys.exit("STOP(ReadFdmInp): non support Atom tag")
            if bool(magnetism_reg.match(self.datlines[i])):
                self.ispin = 2
            if bool(allsite_reg.match(self.datlines[i])):
                self.allsite = True
            if bool(filout_reg.match(self.datlines[i])):
                if len(self.datlines[i].split()) > 1:
                    self.filout = self.datlines[i].split()[1].strip()
                else:
                    self.filout = self.datlines[i + 1].strip()
            if bool(calculation_reg.match(self.datlines[i])):
                self.calculation = str(self.datlines[i + 1].split()[0])
            if bool(conv_out_reg.match(self.datlines[i])):
                self.conv_out = self.datlines[i + 1].split()[0]
            if bool(convolution_reg.match(self.datlines[i])):
                self.convolution = True
            if bool(center_abs_reg.match(self.datlines[i])):
                self.center_abs = True
            if bool(absorber_reg.match(self.datlines[i])):
                if len(self.datlines[i].split()) > 1:
                    self.absorber = int(self.datlines[i].split()[1].strip())
                else:
                    self.absorber = int(self.datlines[i + 1].strip())
            if bool(crystal_reg.match(self.datlines[i])) and (
                not bool(comment_reg.match(self.datlines[i]))
            ):
                self.MOL = False
                if not len(self.datlines[i + 1].split()) >= 6:
                    print(self.datlines[i + 1].split())
                    sys.exit(
                        "STOP(ReadFdmInp): a,b,c,alpha,beta,gamma INPUT LINE error"
                    )
                i += 1
                lattice_a = float(self.datlines[i].split()[0])
                lattice_b = float(self.datlines[i].split()[1])
                lattice_c = float(self.datlines[i].split()[2])
                alpha = float(self.datlines[i].split()[3])
                beta = float(self.datlines[i].split()[4])
                gamma = float(self.datlines[i].split()[5])
                self.cellparam = [lattice_a, lattice_b, lattice_c, alpha, beta, gamma]
                self.t = coorsys(self.cellparam)
                self.atoms_index_j = []
                while 1:
                    i += 1
                    if len(self.datlines[i].split()) > 0:
                        if bool(char_reg.match(self.datlines[i].split()[0])):
                            break
                        zz = int(self.datlines[i].split()[0])
                        x = float(self.datlines[i].split()[1])
                        y = float(self.datlines[i].split()[2])
                        z = float(self.datlines[i].split()[3])
                        symbol_ = ElementTable().get_atomic_symbol0(zz)
                        self.atoms_index_j.append(symbol_)
                        self.position.append([x, y, z])
                    if i == self.num:
                        break
            elif bool(mole_reg.match(self.datlines[i])) and (
                not bool(comment_reg.match(self.datlines[i]))
            ):
                self.MOL = True
                if not len(self.datlines[i + 1].split()) >= 6:
                    print(self.datlines[i + 1].split())
                    sys.exit("STOP: a,b,c,alpha,beta,gamma INPUT LINE error")
                i += 1
                lattice_a = float(self.datlines[i].split()[0])
                lattice_b = float(self.datlines[i].split()[1])
                lattice_c = float(self.datlines[i].split()[2])
                alpha = float(self.datlines[i].split()[3])
                beta = float(self.datlines[i].split()[4])
                gamma = float(self.datlines[i].split()[5])
                self.cellparam = [lattice_a, lattice_b, lattice_c, alpha, beta, gamma]
                self.t = coorsys(self.cellparam)
                self.atoms_index_j = []
                print("====")
                while 1:
                    i += 1
                    if len(self.datlines[i].split()) > 0:
                        if bool(char_reg.match(self.datlines[i].split()[0])):
                            break
                        zz = int(self.datlines[i].split()[0])
                        x = float(self.datlines[i].split()[1])
                        y = float(self.datlines[i].split()[2])
                        z = float(self.datlines[i].split()[3])
                        symbol_ = ElementTable().get_atomic_symbol0(zz)
                        self.atoms_index_j.append(symbol_)
                        self.position.append([x, y, z])
                    if i == self.num:
                        break
                    print(self.atoms_index_j)
            else:
                pass
            if bool(crystal_p_reg.match(self.datlines[i])):
                self.position = []
                self.atoms_index_j = []
        print("=== END of READ INP")
        print("")
        print("input file name = %s" % inpname)
        print("Fileout         = %s" % self.filout)
        print("ISPIN           = %s" % self.ispin)
        print("Allist          = %s" % self.allsite)
        print("Energypho       = %s" % self.energygpho)
        print("Convolutaion    = %s" % self.convolution)
        print("Center_abs      = %s" % self.center_abs)
        print("Noexc           = %s" % self.nonexc)
        print(self.atoms_index_j)
        try:
            self.filout = self.filout
        except:
            self.filout = self.calculation
        self.position = np.array(self.position)
        self.natom = len(self.position)
        counter = collections.Counter(self.atoms_index_j)
        self.nion = len(counter)
        self.atoms = np.zeros(self.nion, dtype=int)
        self.atoms_index = []
        self.atoms_number = np.zeros(self.nion, dtype=int)
        i = 0
        for atom, cnt in counter.most_common():
            self.atoms_index.append(atom)
            self.atoms_number[i] = ElementTable().get_atomic_number1(atom)
            self.atoms[i] = cnt
            i += 1
        self.atoms_number_j = np.zeros(self.natom, dtype=int)
        for i in range(self.natom):
            self.atoms_number_j[i] = ElementTable().get_atomic_number1(
                str(self.atoms_index_j[i])
            )
        self.atoms_j = np.zeros(self.natom, dtype=int)
        j = 0
        for ion in range(self.nion):
            for atom in range(self.atoms[ion]):
                self.atoms_j[j] = int(ion)
                j += 1
        self.fix = np.zeros((self.natom, 3), dtype="S")
        self.fix[:, :] = "F"
        if sort:
            (
                self.sort_index,
                self.sort_index_r,
                self.atoms,
                self.atoms_index,
                self.atoms_index_j,
            ) = AtomOrdering().sort_atom_index_j(self.atoms_index_j)
            (
                self.sort_index,
                self.sort_index_r,
                self.atoms,
                self.atoms_index,
                self.atoms_number_j,
            ) = AtomOrdering().sort_atom_number_j(self.atoms_number_j)
            self.position = AtomOrdering().sort_position(
                self.sort_index_r, self.position
            )
            self.fix = AtomOrdering().sort_fix(self.sort_index_r, self.fix)
        self.ion = np.zeros(self.natom, dtype=int)
        tmp = -1
        for j in range(self.nion):
            local = -1
            for k in range(int(self.atoms[j])):
                tmp += 1
                local += 1
                self.ion[tmp] = int(j)
        self.ion_local = np.zeros(self.natom, dtype=int)
        tmp = -1
        for j in range(self.nion):
            local = -1
            for k in range(int(self.atoms[j])):
                tmp += 1
                local += 1
                self.ion_local[tmp] = int(local)
        self.title = self.filout
        self.nspin = self.ispin
        self.system = self.title
        self.vasp_version = None
        self.selective = False
        self.direct = True
        self.scale = 1.0
        self.sort_index = None
        self.sort_index_r = None

    def get_ispin(self):
        return self.ispin

    def get_nonexc(self):
        return self.nonexc

    def get_allsite(self):
        return self.allsite

    def get_energygpho(self):
        return self.energygpho

    def get_absorber(self):
        self.absorber = self.absorber if hasattr(self, "absorber") else 1
        return self.absorber

    def get_convolution(self):
        return self.convolution

    def get_conv_out(self):
        self.conv_out = self.conv_out if hasattr(self, "conv_out") else None
        return self.conv_out

    def get_calculation(self):
        self.calculation = self.calculation if hasattr(self, "calculation") else None
        return self.calculation

    def get_filout(self):
        self.filout = self.filout if hasattr(self, "filout") else None
        return self.filout

    def get_cellparam(self):
        return self.cellparam

    def sort_atoms_index_j(self):
        from sae.structure.ordering import AtomOrdering

        (
            self.sort_index,
            self.sort_index_r,
            self.atoms,
            self.atoms_index,
            self.atoms_index_j,
        ) = AtomOrdering().sort_atom_index_j(self.atoms_index_j)
        return (
            self.sort_index,
            self.sort_index_r,
            self.atoms,
            self.atoms_index,
            self.atoms_index_j,
        )

    def sort_position(self):
        from sae.structure.ordering import AtomOrdering

        if self.sort_index_r is None:
            self.sort_atoms_index_j()
        self.position = AtomOrdering().sort_position(self.sort_index_r, self.position)
        return self.position

    def get_atoms_index_j(self):
        return self.atoms_index_j

    def get_natom(self):
        return self.natom
