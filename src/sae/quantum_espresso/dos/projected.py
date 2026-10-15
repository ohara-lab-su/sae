#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# PWScf (Quantum ESPRESSO 5..x )
# dos 関連出力 ファイル( dos.x projwfc.x 出力ファイル 読み込み)
#
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.07.23
#  停止していた開発を再スタート
#
#
# 2015.05.08 startup
#
################################################################################
from __future__ import print_function

from sae._logging import debug_values as _log_debug

from sae.errors import legacy_error as _legacy_error
from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.1.1"

################################################################################

import sys

# import gzip
import os
import glob
import re
import numpy as np

import StructureAnalysisEnvironment as SAEnv

# import SpaceGroupEnvironment as SGE


################################################################################
class ProjectedDOS(object):

    def __init__(self, prefix):

        # cname+'pdos.pdos_tot'
        self.datlines, self.num = SAEnv.read_dataline(prefix + ".pdos.pdos_tot")
        nedos = self.num - 1

        if len(self.datlines[1].split()) > 3:
            ispin = 2
        else:
            ispin = 1

        # 実際に計算している pdos ファイルの取得
        pdos_list = glob.glob(prefix + ".pdos.pdos_atm#*")
        if len(pdos_list) < 1:
            _legacy_error("STOP: " + prefix + ".pdos.pdos_atm#* file not found")
        pdos_list.sort()

        # 計算している pdos ファイルの原子の種類番号のみを取得
        atom_ls = []
        for f in pdos_list:
            tmp = re.sub(prefix + ".pdos.pdos_atm#", "", f)
            atom = int(re.sub("\(.*", "", tmp))
            atom_ls.append(atom)

        # 重複している pdos ファイルの原子種番号を削除(順番は変更しない)
        atom_list = []
        for x in atom_ls:
            if x not in atom_list:
                atom_list.append(x)

        # ユニークは原子種番号の数から全原子数を確保
        natom = len(atom_list)

        # 原子数の通し番号毎の元素記号を記憶する配列を用意
        atoms_index_j = []
        for atom in atom_list:
            pname = glob.glob(prefix + ".pdos.pdos_atm#" + str(atom) + "*")[0]
            tmp = re.sub(prefix + ".pdos.pdos_atm#" + str(atom) + "\(", "", pname)
            tmp = re.sub("\)_wfc#.*", "", tmp).strip()
            atoms_index_j.append(tmp)

        ## 実際に計算している各原子毎に計算しているlの最大値を取得する
        ## 最後の# の番号は軌道番号ではなくて通し番号であることが判明(15.07.22)
        ## このルーチンは削除
        # lmax_list = []
        # for atom in atom_list:
        #    tmp = glob.glob(prefix+'.pdos.pdos_atm#'+str(atom)+'(*')
        #    for g in tmp:
        #        tmp = re.sub(prefix+'.pdos.pdos_atm#','',g)
        #        lmax = int(re.sub('\(.*' ,'',re.sub('\d*\(.*#','',tmp) ))
        #    lmax_list.append(lmax)
        # print "lmax_list: max",len(lmax_list), lmax_list

        l_index_j = []
        for atom in atom_list:
            tmp = glob.glob(prefix + ".pdos.pdos_atm#" + str(atom) + "(*")
            list_tmp = []
            for g in tmp:
                tmp0 = re.sub(prefix + ".pdos.pdos_atm#", "", g)
                tmp0 = re.sub("\d*\(.*#\d\(", "", tmp0)
                tmp0 = re.sub("\)", "", tmp0)
                list_tmp.append(tmp0)
            l_index_j.append(list_tmp)

        l_list = []
        for i in range(natom):
            list_tmp = []
            for j in range(len(l_index_j[i])):
                l = l_index_j[i][j]
                if l == "s":
                    lmax = 0
                if l == "p":
                    lmax = 1
                if l == "d":
                    lmax = 2
                if l == "f":
                    lmax = 3
                list_tmp.append(lmax)
            l_list.append(list_tmp)

        #       for i in range(len(atom_list)):
        #           print l_index_j[i],l_max_list[i]

        #       print "natom:", natom
        #       print "atom_list    : ", atom_list
        #       print "atoms_index_j: ", atoms_index_j
        #       print "l_index_j    : ", l_index_j
        #       print "l_list       : ", l_list

        ################
        # LDOS 収納に使う配列の確保(原子種毎),配列の l_max は固定にする
        l_max = 4  # s,p,d,f
        self.ldos_all = np.zeros((nedos, l_max, natom, ispin))

        ################
        # PDOS 収納に使う配列の確保
        # lm_max = 1+3+5+7 # s+p+d+f
        lm_max = 7  # 軌道成分ごとの lm として保存するので f 軌道の最大値で良い
        lm_list = [1, 3, 5, 7]
        self.pdos_all = np.zeros((nedos, l_max, lm_max, natom, ispin))
        self.eng = np.zeros(nedos)

        ########################################################################
        # 原子種のループ
        for atom in range(natom):

            for ll in range(len(l_index_j[atom])):

                l = int(l_list[atom][ll])
                l_index = l_index_j[atom][ll]

                ## 原子のリスト、原子の持つ軌道番号のリストからファイル名を作成
                ##
                # print atoms_index_j[atom],\
                #        l_list[atom][ll], \
                #        l_index_list[atom][ll]

                pname = (
                    prefix
                    + ".pdos.pdos_atm#"
                    + str(atom + 1)
                    + "("
                    + atoms_index_j[atom]
                    + ")_wfc#"
                    + str(ll + 1)
                    + "("
                    + l_index
                    + ")"
                )
                _log_debug(pname)

                if not os.path.exists(pname):
                    _legacy_error("STOP: " + pname + " not found")

                # 原子種＋軌道におけるデータ読み込み
                data, nline = SAEnv.read_dataline1(pname)
                if nline != nedos:
                    _legacy_error("STOP: Contradiction Number of Data Line :" + pname)

                # print atom, l,l_index, len(data[0].split())
                for spin in range(ispin):
                    for line in range(nline):

                        self.eng[line] = float(data[line].split()[0])
                        self.ldos_all[line, l, atom, spin] = float(
                            data[line].split()[1 + spin]
                        )

                        for lm in range(lm_list[l]):
                            row = (
                                1
                                + ispin
                                - 1
                                + ispin
                                + (lm * ispin - 1 * (ispin - 1))
                                + spin
                            )
                            self.pdos_all[line, l, lm, atom, spin] = float(
                                data[line].split()[row]
                            )

        self.nedos = nedos
        self.ispin = ispin
        self.natom = natom
        self.atoms_index_j = atoms_index_j
        self.l_index_j = l_index_j
        self.lm_list = lm_list

    ############################################################################
    def get_ldos(self, l=0, atom=0, spin=0):

        if isinstance(l, str):
            if l == "s":
                l = 0
                l_index = "s"
            if l == "p":
                l = 1
                l_index = "p"
            if l == "d":
                l = 2
                l_index = "d"
            if l == "d":
                l = 3
                l_index = "4"

        if isinstance(l, int):
            if l == 0:
                l_index = "s"
            if l == 1:
                l_index = "p"
            if l == 2:
                l_index = "d"
            if l == 3:
                l_index = "f"

        if isinstance(spin, str):
            if spin == "up":
                spin = 0
            if spin == "dn":
                spin = 1
            if spin == "down":
                spin = 1

        FLAG_CHK = False
        for chk in self.l_index_j[atom]:
            if chk == l_index:
                FLAG_CHK = True
        if not FLAG_CHK:
            _legacy_error("STOP: " + l_index + "-orbit not calculated")

        if spin > self.ispin - 1:
            _legacy_error("STOP: spin = " + str(spin) + " not calculated")

        self.ldos = self.ldos_all[:, l, atom, spin]
        return self.ldos

    ############################################################################
    # lm は 0 からカウント l=2 のとき、px, py, pz ならば px は lm=0
    def get_pdos(self, l=0, lm=0, atom=0, spin=0):

        if isinstance(l, str):
            if l == "s":
                l = 0
                l_index = "s"
            if l == "p":
                l = 1
                l_index = "p"
            if l == "d":
                l = 2
                l_index = "d"
            if l == "d":
                l = 3
                l_index = "4"

        if isinstance(l, int):
            if l == 0:
                l_index = "s"
            if l == 1:
                l_index = "p"
            if l == 2:
                l_index = "d"
            if l == 3:
                l_index = "f"

        if isinstance(spin, str):
            if spin == "up":
                spin = 0
            if spin == "dn":
                spin = 1
            if spin == "down":
                spin = 1

        FLAG_CHK = False
        for chk in self.l_index_j[atom]:
            if chk == l_index:
                FLAG_CHK = True
        if not FLAG_CHK:
            _legacy_error("STOP: " + l_index + "-orbit not calculated")

        if lm > self.lm_list[l] - 1:
            _legacy_error(
                "STOP: " + l_index + "-orbit , lm=" + str(lm) + " not calculated"
            )

        if spin > self.ispin - 1:
            _legacy_error("STOP: spin = " + str(spin) + " not calculated")

        self.pdos = self.pdos_all[:, l, lm, atom, spin]
        return self.pdos

    ############################################################################
    def get_pdos_all(self):
        return self.pdos_all

    def get_ldos_all(self):
        return self.ldos_all

    def get_natom(self):
        return self.natom

    def get_atoms_index_j(self):
        return self.atoms_index_j

    def get_nedos(self):
        return self.nedos

    def get_ispin(self):
        return self.ispin


################################################################################
def options():
    import optparse

    prefix = "Fe"
    parser = optparse.OptionParser()

    parser.add_option(
        "-i",
        "--input",
        dest="INPUT",
    )
    options, args = parser.parse_args()

    if not os.path.exists(prefix + ".pdos.pdos_tot"):
        pdosname = glob.glob("*.pdos.pdos_tot")
        if len(pdosname) == 1:
            prefix = re.sub(".pdos.pdos_tot", "", pdosname[0])

    if options.INPUT:
        prefix = options.INPUT
    if len(args) > 0:
        prefix = args[0]

    return prefix


################################################################################
if __name__ == "__main__":

    prefix = options()
    dos = ReadPwPdos(prefix)

    #   lm_list = [1,3,5,7]

    print("PREFIX       : %s" % str(prefix))
    print("NEDOS        : %s" % str(dos.nedos))
    print("ispin        : %s" % str(dos.ispin))
    print("natom        : %s" % str(dos.natom))
    print("atoms_index_j: %s" % str(dos.atoms_index_j))
    print("l_index_j    : %s" % str(dos.l_index_j))

    ENG = dos.eng
    #   LDOSup = dos.get_ldos(l=0,atom=0,spin=0)
    #   LDOSdn = dos.get_ldos(l=0,atom=0,spin=1)

    PDOSup = dos.get_pdos(l=2, lm=2, atom=0, spin=0)
    #   PDOSdn = dos.get_pdos(l=2,lm=2,atom=0,spin=1)

    #   for i in range(dos.nedos):
    #       print ENG[i], LDOSup[i], LDOSdn[i]

    for i in range(dos.nedos):
        #       print ENG[i], PDOSup[i], PDOSdn[i]
        print("%s %s" % (str(ENG[i]), str(PDOSup[i])))


ReadPwPdos = ProjectedDOS  # historical spelling
