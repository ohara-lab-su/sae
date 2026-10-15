# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import numpy as np

try:
    import sae as SAEnv
except ImportError:
    import sae as SAEnv


class ReadVaspOutcar(object):

    def __init__(self, cname):
        from sae.common.text import TextFiles

        self.datlines, self.num = TextFiles().read_dataline(cname)
        rec_reg = re.compile(".*reciprocal lattice vectors", re.IGNORECASE)
        title_reg = re.compile(".*POSCAR:")
        nkpts_reg = re.compile(".*NKPTS.*")
        nbands_reg = re.compile(".*NBANDS.*")
        nbands0_reg = re.compile(".*number of bands.*NBANDS=")
        spin_reg = re.compile(".*ISPIN.*", re.IGNORECASE)
        orbit_reg = re.compile(".*LORBIT.*", re.IGNORECASE)
        nsw_reg = re.compile(".*NSW.*", re.IGNORECASE)
        isym_reg = re.compile(".*ISYM   =", re.IGNORECASE)
        ibrion_reg = re.compile(".*IBRION", re.IGNORECASE)
        nwrite_reg = re.compile(".*NWRITE", re.IGNORECASE)
        encut_reg = re.compile(".*ENCUT", re.IGNORECASE)
        nions_reg = re.compile(".*number of ions.*NIONS.*", re.IGNORECASE)
        ion_type_reg = re.compile(".*ions per type", re.IGNORECASE)
        iter_reg = re.compile(".*-- Iteration", re.IGNORECASE)
        toten_ion_reg = re.compile(".*free  energy   TOTEN", re.IGNORECASE)
        volume_ion_reg = re.compile(".*volume of cell", re.IGNORECASE)
        efermi_reg = re.compile("^.*E-fermi")
        self.t = np.zeros((3, 3))
        self.rec_t = np.zeros((3, 3))
        self.lorbit = 0
        self.ispin = 1
        self.nsw = 0
        self.atoms = []
        self.atoms_index = []
        self.volume_ion = []
        i = 0
        while not bool(iter_reg.match(self.datlines[i])):
            if bool(title_reg.match(self.datlines[i])):
                self.title = re.sub(" *$", "", self.datlines[i][9:])
            if bool(nkpts_reg.match(self.datlines[i])):
                try:
                    self.nkpts
                except:
                    self.nkpts = int(self.datlines[i].split()[3])
            if bool(nions_reg.match(self.datlines[i])):
                try:
                    self.natom = self.natom
                except:
                    self.natom = int(self.datlines[i].split()[11])
            if bool(nbands_reg.match(self.datlines[i])):
                try:
                    self.nbands = self.nbands
                except:
                    try:
                        self.nbands = int(self.datlines[i].split()[14])
                    except:
                        try:
                            self.nbands = int(self.datlines[i].split()[8])
                        except:
                            pass
            if bool(spin_reg.match(self.datlines[i])):
                self.ispin = int(self.datlines[i].split()[2])
            if bool(orbit_reg.match(self.datlines[i])):
                self.lorbit = int(self.datlines[i].split()[2])
            if bool(nsw_reg.match(self.datlines[i])):
                self.nsw = int(self.datlines[i].split()[2])
            if bool(isym_reg.match(self.datlines[i])):
                self.isym = int(self.datlines[i].split()[2])
            if bool(ibrion_reg.match(self.datlines[i])):
                self.ibrion = int(self.datlines[i].split()[2])
            if bool(nwrite_reg.match(self.datlines[i])):
                self.nwrite = int(self.datlines[i].split()[2])
            if bool(encut_reg.match(self.datlines[i])):
                self.encut = float(self.datlines[i].split()[2])
            if bool(ion_type_reg.match(self.datlines[i])):
                tmp = self.datlines[i].split()
                self.nion = len(tmp) - 4
                if self.nion >= 10:
                    if os.path.exists("vasprun.xml"):
                        from sae.vasp.vasprun import ReadVaspVasprun

                        vrun = ReadVaspVasprun()
                        self.nion = vrun.get_nion()
                    else:
                        sys.exit("STOP(get_nion): NION >= 10")
            if bool(ion_type_reg.match(self.datlines[i])):
                for ion in range(self.nion):
                    self.atoms.append(int(self.datlines[i].split()[4 + ion]))
            if bool(rec_reg.match(self.datlines[i])):
                t1_x = float(self.datlines[i + 1][3:16])
                t1_y = float(self.datlines[i + 1][16:29])
                t1_z = float(self.datlines[i + 1][29:42])
                rec1_x = float(self.datlines[i + 1][45:58])
                rec1_y = float(self.datlines[i + 1][58:71])
                rec1_z = float(self.datlines[i + 1][71:84])
                t2_x = float(self.datlines[i + 2][3:16])
                t2_y = float(self.datlines[i + 2][16:29])
                t2_z = float(self.datlines[i + 2][29:42])
                rec2_x = float(self.datlines[i + 2][45:58])
                rec2_y = float(self.datlines[i + 2][58:71])
                rec2_z = float(self.datlines[i + 2][71:84])
                t3_x = float(self.datlines[i + 3][3:16])
                t3_y = float(self.datlines[i + 3][16:29])
                t3_z = float(self.datlines[i + 3][29:42])
                rec3_x = float(self.datlines[i + 3][45:58])
                rec3_y = float(self.datlines[i + 3][58:71])
                rec3_z = float(self.datlines[i + 3][71:84])
                self.t[0, 0] = t1_x
                self.t[1, 0] = t1_y
                self.t[2, 0] = t1_z
                self.t[0, 1] = t2_x
                self.t[1, 1] = t2_y
                self.t[2, 1] = t2_z
                self.t[0, 2] = t3_x
                self.t[1, 2] = t3_y
                self.t[2, 2] = t3_z
                self.rec_t[0, 0] = rec1_x
                self.rec_t[1, 0] = rec1_y
                self.rec_t[2, 0] = rec1_z
                self.rec_t[0, 1] = rec2_x
                self.rec_t[1, 1] = rec2_y
                self.rec_t[2, 1] = rec2_z
                self.rec_t[0, 2] = rec3_x
                self.rec_t[1, 2] = rec3_y
                self.rec_t[2, 2] = rec3_z
            if bool(volume_ion_reg.match(self.datlines[i])):
                self.volume_ion.append(float(self.datlines[i].split()[4]))
            i += 1
        self.toten_ion = []
        for j in range(self.num - i):
            if bool(iter_reg.match(self.datlines[i])):
                self.n_ion_loop = int(self.datlines[i].split()[2].replace("(", ""))
            if bool(toten_ion_reg.match(self.datlines[i])):
                self.toten_ion.append(float(self.datlines[i].split()[4]))
            if bool(volume_ion_reg.match(self.datlines[i])):
                self.volume_ion.append(float(self.datlines[i].split()[4]))
            if bool(efermi_reg.match(self.datlines[i])):
                self.efermi = self.datlines[i].split()[2]
            i += 1
        self.toten = self.toten_ion[self.n_ion_loop - 1]
        self.volume = self.volume_ion[self.n_ion_loop]
        j = 0
        potcar_reg = re.compile(".*POTCAR: ")
        for i in range(self.num):
            if bool(potcar_reg.match(self.datlines[i])):
                j += 1
                tmp = str(self.datlines[i].split()[2])
                self.atoms_index.append(tmp)
        j = int(j / 2)
        for i in range(j):
            self.atoms_index.pop()
        if j != self.nion:
            sys.exit("STOP(get_atoms_index): NION !=", NION)
        j = 0
        self.atoms_j = np.zeros(self.natom, dtype=int)
        for ion in range(self.nion):
            for atom in range(self.atoms[ion]):
                self.atoms_j[j] = ion
                j += 1
        j = 0
        self.atoms_index_j = np.zeros(self.natom, dtype="S2")
        for ion in range(self.nion):
            for atom in range(self.atoms[ion]):
                self.atoms_index_j[j] = self.atoms_index[ion]
                j += 1
        if self.isym != 0 and self.isym != -1:
            point_sym_text = ".*The.*tic.*fig.*ion.*ha.* point symmetry "
            point_sym_reg = re.compile(point_sym_text, re.IGNORECASE)
            for i in range(self.num):
                if bool(point_sym_reg.match(self.datlines[i])):
                    src = self.datlines[i]
                    dst = re.sub(point_sym_text, "", src)
                    dst = re.sub("\\.", "", dst)
                    self.point_sym = str(dst)
        else:
            self.point_sym = None
        self.point_symmetry = self.point_sym

    def get_reciprocal_t_init(self):
        return self.rec_t

    def get_t(self):
        return self.t

    def get_title(self):
        return self.title

    def get_nkpts(self):
        return self.nkpts

    def get_nbands(self):
        return self.nbands

    def get_ispin(self):
        return self.ispin

    def get_lorbit(self):
        return self.lorbit

    def get_nsw(self):
        return self.nsw

    def get_natom(self):
        return self.natom

    def get_nion(self):
        return self.nion

    def get_atoms(self):
        return self.atoms

    def get_isym(self):
        return self.isym

    def get_point_symmetry(self):
        return self.point_sym

    def get_ibrion(self):
        return self.ibrion

    def get_nwrite(self):
        return self.nwrite

    def get_n_ion_loop(self):
        return self.n_ion_loop

    def get_toten_ion(self):
        return self.toten_ion

    def get_volume_ion(self):
        return self.volume_ion

    def get_efermi(self):
        return self.efermi

    def get_atoms_j(self):
        return self.atoms_j

    def get_atoms_index_j(self):
        return self.atoms_index_j

    def get_kpoints_mode(self):
        """
        OUTCAR の KPOINTS セッションから KPOINTS ファイルの内容(動作モード)の類推
        かなり未完成。SCF でのオートmesh と band での line-mode の区別くらい
        :return:
        """
        auto_FLAG = False
        line_FLAG = False
        hand_FLAG = False
        car_FLAG = False
        rec_FLAG = False
        kpoints_reg = re.compile(".*KPOINTS:.*")
        for i in range(self.num):
            if bool(kpoints_reg.match(self.datlines[i])):
                if "Automatic" == self.datlines[i + 2].split()[0]:
                    auto_FLAG = True
                if "k-points" == self.datlines[i + 2].split()[0]:
                    line_FLAG = True
                break
        self.FLAGS = [auto_FLAG, line_FLAG, hand_FLAG, car_FLAG, rec_FLAG]
        return self.FLAGS

    def get_kpoints_type(self):
        """
        入力された KPOINTS の座標形式をゲット(cartesian or reciprocal)
        もし band-mode(line-mode) でないのならば、Automatic モードならば
        Automatic と返す
        :return:
        """
        kpoints_reg = re.compile(".*KPOINTS:.*")
        for i in range(self.num):
            if bool(kpoints_reg.match(self.datlines[i])):
                if "Automatic" == self.datlines[i + 2].split()[0]:
                    self.kpoints_type = "Automatic"
                else:
                    self.kpoints_type = self.datlines[i + 2].split()[2]
                break
        return self.kpoints_type

    def get_atoms_index(self):
        """
        atoms_index (My配列) の情報を引っ張るMethod
        VRHFIN ではなく POTCAR: から PP の原子種情報を引っ張る
        get_atoms_index0 との兼ね合いがあるのでもう一度中身のある実行をする
        :return:
        """
        NION = self.get_nion()
        self.atoms_index = []
        j = 0
        potcar_reg = re.compile(".*POTCAR: ")
        for i in range(self.num):
            if bool(potcar_reg.match(self.datlines[i])):
                j += 1
                tmp = str(self.datlines[i].split()[2])
                self.atoms_index.append(tmp)
        j = int(j / 2)
        for i in range(j):
            self.atoms_index.pop()
        if j != NION:
            sys.exit("STOP(get_atoms_index): NION !=%s" % NION)
        return self.atoms_index

    def get_atoms_index0(self):
        """
        atoms_index (My配列) の情報を引っ張るMethod
        名称を get_atoms_index0 と変更 (NWRITE =2 以上でないと動作しない)
        :return:
        """
        NION = self.get_nion()
        self.atoms_index = []
        j = 0
        vrhfin_reg = re.compile(".*VRHFIN =", re.IGNORECASE)
        for i in range(self.num):
            if bool(vrhfin_reg.match(self.datlines[i])):
                j += 1
                src = self.datlines[i]
                dst = re.sub(":.*", "", src)
                dst = re.sub(".*VRHFIN =", "", dst)
                self.atoms_index.append(dst)
        if j != NION:
            sys.exit("STOP(get_atoms_index): NION !=", NION)
        return self.atoms_index

    def get_md_mode(self):
        IBRION = self.get_ibrion()
        if IBRION == 0:
            self.MD_FLAG = True
        else:
            self.MD_FLAG = False
        return self.MD_FLAG

    def get_temperature(self):
        IBRION = self.get_ibrion()
        if IBRION == 0:
            n_ion_loop = self.get_n_ion_loop()
            self.temperature = np.zeros(n_ion_loop)
            ekin_reg = re.compile(".*EKIN_LAT=", re.IGNORECASE)
            j = 0
            for i in range(self.num):
                if bool(ekin_reg.match(self.datlines[i])):
                    tmp = self.datlines[i].split()
                    self.temperature[j] = float(tmp[5])
                    j += 1
        else:
            self.temperature = ["0"]
        return self.temperature

    def get_etotal(self):
        IBRION = self.get_ibrion()
        if IBRION == 0:
            n_ion_loop = self.get_n_ion_loop()
            self.ETOTAL = np.zeros(n_ion_loop)
            etotal_reg = re.compile(".*ETOTAL =", re.IGNORECASE)
            j = 0
            for i in range(self.num):
                if bool(etotal_reg.match(self.datlines[i])):
                    tmp = self.datlines[i].split()
                    self.ETOTAL[j] = float(tmp[4])
                    j += 1
        else:
            toten_ion = self.get_toten_ion()
            self.ETOTAL = toten_ion
        return self.ETOTAL

    def get_toten(self):
        return self.toten

    def get_volume(self):
        return self.volume
