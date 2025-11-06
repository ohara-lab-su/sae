#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# PWScf (Quantum ESPRESSO 5..x )
# scf.out ファイル( pw.x 出力ファイル 読み込み)
#
# 1) pw.x 出力ファイル名の第一候補を scf.out とする
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.05.13
#  position_loop の配列構造を修正(ReadMd.py, ReadVapsrun.py 互換)
#  force_loop の配列構造を修正
#
# 2015.05.13
#  force 対応
#
# 2015.05.08 startup
#
################################################################################
from __future__ import print_function

try:
    from ...copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.1.1"

################################################################################

import sys
# import gzip
import os
import re
import optparse
import numpy as np

try:
    # sys.path.append('../..')
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    import StructureAnalysisEnvironment as SAEnv
except ImportError:
    import StructureAnalysisEnvironment as SAEnv


# import SpaceGroupEnvironment as SGE

################################################################################
class ReadPwOut(object):

    def __init__(self, cname):

        self.datlines, self.num = SAEnv.read_dataline(cname)

        natom_reg = re.compile('.*number of atoms/cell.*')
        nion_reg = re.compile('.*number of atomic types.*')
        nbands_reg = re.compile('.*number of Kohn-Sham states=.*')
        nsw_reg = re.compile('.*nstep.*')
        efermi_reg = re.compile('.*the Fermi energy is.*')
        nrho_reg = re.compile('.*negative rho.*')
        ion_loop_reg = re.compile('.*ATOMIC_POSITIONS.*')
        toten_ion_reg = re.compile('.*!.*total energy.*')
        scale_reg = re.compile('.*lattice parameter.*')
        bravais_reg = re.compile('.*bravais-lattice.*')
        save_reg = re.compile('.*save')

        self.nsw = 0
        self.n_ion_loop = 0
        self.atoms_index = []
        self.toten_ion = []
        self.efermi = 'None'

        # 1bhor = 0.529177249 angstrom
        # 1Rydberg = 13.6056981 eV

        for line in self.datlines:

            if bool(bravais_reg.match(line)):
                ibrva = int(line.split()[3])
                if ibrva != 0:
                    sys.exit("STOP: ibrva != 0 ")

            # scale ファクターは angstrom にする
            if bool(scale_reg.match(line)):
                scale0 = float(line.split()[4])
                if line.split()[5] == 'a.u.':
                    self.scale = scale0 * 0.529177249
                else:
                    self.scale = scale0

            if bool(natom_reg.match(line)):
                self.natom = int(line.split()[4])
            if bool(nion_reg.match(line)):
                self.nion = int(line.split()[5])
            if bool(nbands_reg.match(line)):
                self.nbands = int(line.split()[4])
            if bool(nsw_reg.match(line)):
                self.nsw = int(line.split()[2])

            if bool(nrho_reg.match(line)):
                if float(line.split()[5]) == 0.00:
                    self.ispin = 1
                else:
                    self.ispin = 2

            # 実際にループした数をカウント
            if bool(ion_loop_reg.match(line)):
                self.n_ion_loop += 1

            if bool(efermi_reg.match(line)):
                self.efermi = float(line.split()[4])

            if bool(toten_ion_reg.match(line)):
                self.toten_ion.append(float(line.split()[4]))

            if bool(save_reg.match(line)):
                tmp = re.sub('.*Writing output data file ', '', line)
                self.title = str(re.sub('\.save', '', tmp))

        np.array(self.toten_ion)

    #############################################################################
    # atoms[i]       : 原子の種類番号(max=nion)を与えると、原子種の数を返す
    # atoms_index[i] : 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
    def get_atoms_index(self):

        species_v_reg = re.compile('.*atomic species.*valence')
        for i in range(self.num):
            if bool(species_v_reg.match(self.datlines[i])):
                for j in range(self.nion):
                    atom_name = self.datlines[i + j + 1].split()[0]
                    self.atoms_index.append(atom_name)

        return self.atoms_index

    #############################################################################
    # 注意)
    # atoms_index の順番でcoordinateが全て並んでいると仮定するときの atoms
    #
    # atoms[i]       : 原子の種類番号(max=nion)を与えると、原子種の数を返す
    # atoms_index[i] : 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
    def get_atoms(self):

        self.get_atoms_index()
        self.atoms = np.zeros(self.nion, dtype=int)
        atoms_reg = re.compile('.*site n.*')
        for i in range(self.num):
            line = self.datlines[i]
            if bool(atoms_reg.match(line)):
                for j in range(self.natom):
                    tmp = re.sub(' tau.*', '', self.datlines[i + j + 1])
                    tmp = re.sub('^ *\d+ *', '', tmp)
                    tmp = re.sub(' *', '', tmp)
                    for k in range(self.nion):
                        if self.atoms_index[k] == tmp:
                            self.atoms[k] += 1
        return self.atoms

    # ReadVasprun.py 互換
    def get_types(self):
        self.get_atoms()
        self.get_atoms_index()
        TYPES = [self.atoms, self.atoms_index]
        return [TYPES]

    ############################################################################
    # natom までの通し番号で原子種を返す(元素記号ではなくて原子の種類番号を返す)
    def get_atoms_j(self):  # ReadOutcar.py 互換, ReadMxDatMethod.py 互換

        self.get_atoms()
        self.atoms_j = np.zeros(self.natom, dtype=int)
        j = 0
        for ion in range(self.nion):
            for atom in range(self.atoms[ion]):
                self.atoms_j[j] = int(ion)
                j += 1

        return self.atoms_j

    #############################################################################
    # natom までの通し番号で原子種の記号を返す
    # 全ループ構造で完全に同じなので一回見つけたらbreakする
    def get_atoms_index_j(self):  # ReadMd, ReadPoscar, ReadPwIn 互換

        position_reg = re.compile('.*ATOMIC_POSITIONS.*', re.IGNORECASE)
        self.atoms_index_j = []
        for i in range(self.num):
            if bool(position_reg.match(self.datlines[i])):
                for j in range(self.natom):
                    atom_name = self.datlines[i + j + 1].split()[0]
                    self.atoms_index_j.append(atom_name)
                break

        return self.atoms_index_j

    #############################################################################
    # ReadPoscar.py での処理に準ずる構造
    def get_t(self):

        self.t = np.zeros((3, 3))
        crystal_axes_reg = re.compile('.*crystal axes.*')
        for i in range(self.num):
            line = self.datlines[i]
            if bool(crystal_axes_reg.match(line)):
                t1_x = self.datlines[i + 1].split()[3]
                t1_y = self.datlines[i + 1].split()[4]
                t1_z = self.datlines[i + 1].split()[5]

                t2_x = self.datlines[i + 2].split()[3]
                t2_y = self.datlines[i + 2].split()[4]
                t2_z = self.datlines[i + 2].split()[5]

                t3_x = self.datlines[i + 3].split()[3]
                t3_y = self.datlines[i + 3].split()[4]
                t3_z = self.datlines[i + 3].split()[5]

                self.t[0, 0] = t1_x
                self.t[1, 0] = t1_y
                self.t[2, 0] = t1_z

                self.t[0, 1] = t2_x
                self.t[1, 1] = t2_y
                self.t[2, 1] = t2_z

                self.t[0, 2] = t3_x
                self.t[1, 2] = t3_y
                self.t[2, 2] = t3_z

        return self.t

    def get_t_initial(self):
        self.get_t()
        return self.t

    #############################################################################
    # get_final position
    def get_position(self):

        ion_loop_reg = re.compile('.*ATOMIC_POSITIONS.*')
        self.position = np.zeros((self.natom, 3))
        for i in range(self.num):
            line = self.datlines[i]
            if bool(ion_loop_reg.match(line)):
                for j in range(self.natom):
                    self.position[j, 0] = self.datlines[i + j + 1].split()[1]  # x
                    self.position[j, 1] = self.datlines[i + j + 1].split()[2]  # y
                    self.position[j, 2] = self.datlines[i + j + 1].split()[3]  # z

        return self.position

    def get_position_initial(self):
        self.get_position()
        return self.position

    #############################################################################
    def get_position_loop(self):  # ReadMd.py, ReadVasprun.py 互換

        ion_loop_reg = re.compile('.*ATOMIC_POSITIONS.*')
        # self.position_loop = np.zeros((self.natom,3,self.n_ion_loop))
        self.position_loop = np.zeros((self.n_ion_loop, self.natom, 3))
        ion_loop = 0
        for i in range(self.num):
            line = self.datlines[i]
            if bool(ion_loop_reg.match(line)):
                for j in range(self.natom):
                    # self.position_loop[j,0,ion_loop] = self.datlines[i+j+1].split()[1] # x
                    # self.position_loop[j,1,ion_loop] = self.datlines[i+j+1].split()[2] # y
                    # self.position_loop[j,2,ion_loop] = self.datlines[i+j+1].split()[3] # z
                    self.position_loop[ion_loop, j, 0] = self.datlines[i + j + 1].split()[1]  # x
                    self.position_loop[ion_loop, j, 1] = self.datlines[i + j + 1].split()[2]  # y
                    self.position_loop[ion_loop, j, 2] = self.datlines[i + j + 1].split()[3]  # z
                ion_loop += 1

        return self.position_loop

    #############################################################################
    def get_force_loop(self):  # ReadMd.py, ReadVasprun.py 互換

        # self.force_loop = np.zeros((self.natom,3,self.n_ion_loop))
        self.force_loop = np.zeros((self.n_ion_loop, self.natom, 3))
        force_reg = re.compile('.*Forces acting on atoms.*')
        ion_loop = 0
        for i in range(self.num):
            if bool(force_reg.match(self.datlines[i])):
                for j in range(self.natom):
                    # self.force_loop[j,0,ion_loop] = self.datlines[i+j+2].split()[6] # x
                    # self.force_loop[j,1,ion_loop] = self.datlines[i+j+2].split()[7] # y
                    # self.force_loop[j,2,ion_loop] = self.datlines[i+j+2].split()[8] # z
                    self.force_loop[ion_loop, j, 0] = self.datlines[i + j + 2].split()[6]  # x
                    self.force_loop[ion_loop, j, 1] = self.datlines[i + j + 2].split()[7]  # y
                    self.force_loop[ion_loop, j, 2] = self.datlines[i + j + 2].split()[8]  # z
                ion_loop += 1

        return self.force_loop

    #############################################################################
    def get_title(self):
        return self.title

    def get_natom(self):
        return self.natom

    def get_nion(self):
        return self.nion

    def get_nbands(self):
        return self.nbands

    def get_scale(self):
        return self.scale

    def get_nsw(self):
        return self.nsw

    def get_efermi(self):
        return self.efermi

    def get_ispin(self):
        return self.ispin

    def get_n_ion_loop(self):
        return self.n_ion_loop

    ############################################################################
    # ion loop 毎の Total Energy
    def get_toten_ion(self):  # ReadOutcar.py 互換
        return self.toten_ion

    def get_energy_loop(self):  # ReadVasprun.py / ReadMd.py 互換
        return self.toten_ion


################################################################################
def options():
    name = 'scf.out'

    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest='INPUT', default=name, )
    options, args = parser.parse_args()

    if options.INPUT: name = options.INPUT
    if len(args) > 0: name = args[0]

    return name


################################################################################
if __name__ == '__main__':

    name = options()
    out = ReadPwOut(name)

    print("NAME %s" % str(name))

    print("TITLE %s" % str(out.get_title()))

    print("LATTICE PARAMETER %6.4f" % (out.get_scale()))

    print("NATOM    %s" % str(out.get_natom()))
    print("NION     %s" % str(out.get_nion()))
    print("NBANDS   %s" % str(out.get_nbands()))
    print("EFERMI   %s" % str(out.get_efermi()))
    print("NSW      %s" % str(out.get_nsw()))
    print("ION-LOOP %s" % str(out.get_n_ion_loop()))

    print("")
    print(out.get_atoms_index())
    print(out.get_atoms())
    print("")

    print("")
    print(out.get_atoms_j())
    print(out.get_atoms_index_j())

    print("")
    print("TRANSLATION VECTOR")
    print(out.get_t())

    print("")
    print(out.get_position())

    print("")
    position_loop = out.get_position_loop()
    for j in range(out.get_n_ion_loop()):
        print("")
        print(position_loop[j, :, :])

#   print "FORCE"
#   force_loop = out.get_force_loop()
#   for j in range(out.get_n_ion_loop()):
#       print ""
#       print force_loop[j,:,:]

#   print "ENERGY"
#   toten_ion = out.get_toten_ion()
#   for i in range(out.get_n_ion_loop()):
#       print toten_ion[i]
