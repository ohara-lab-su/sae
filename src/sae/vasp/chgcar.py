# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.structure.base import Method
import sys
import os
import re
import multiprocessing
import math
import numpy as np

try:
    Method = Method
except ImportError:
    Method = Method
reduced_memory = False


class ReadVaspChgcar(Method):

    def __init__(
        self, CHGCAR="CHGCAR", suffix=".vasp", sort=False, atoms_index=None, logger=None
    ):
        """init and Read CHGCAR

        :param CHGCAR: 読み込みファイルの名前
        :param suffix: 実はこれは使ってない(2022/05/14)
        :param sort:
        :param atoms_index:
        """
        if logger is None:
            logger = multiprocessing.get_logger()
        self.__logger = logger
        self.open(CHGCAR=CHGCAR, suffix=suffix, sort=sort, atoms_index=sort)

    @property
    def ngxc(self):
        return self.__ngxc

    @property
    def ngyz(self):
        return self.__ngyz

    @property
    def ngzc(self):
        return self.__ngzc

    @property
    def chgdata(self):
        """チャージ情報を取り出す(numpy)"""
        return self.__chgdata

    @property
    def poscar_info(self):
        """POSCAR 情報の取り出し"""
        return self.get_poscar_info()

    def open(self, CHGCAR="CHGCAR", suffix=".vasp", sort=False, atoms_index=None):
        from sae.common.text import TextFiles
        from sae.structure.elements import ElementTable

        self.datlines, self.num = TextFiles().read_dataline(CHGCAR)
        self.system = self.datlines[0]
        self.title = self.system
        self.scale = float(self.datlines[1])
        self.__logger.debug("--- Read STRUCTURE DATA")
        t1_x = float(self.datlines[2].split()[0])
        t1_y = float(self.datlines[2].split()[1])
        t1_z = float(self.datlines[2].split()[2])
        t2_x = float(self.datlines[3].split()[0])
        t2_y = float(self.datlines[3].split()[1])
        t2_z = float(self.datlines[3].split()[2])
        t3_x = float(self.datlines[4].split()[0])
        t3_y = float(self.datlines[4].split()[1])
        t3_z = float(self.datlines[4].split()[2])
        self.t = np.zeros((3, 3))
        self.t[0, 0] = t1_x
        self.t[1, 0] = t1_y
        self.t[2, 0] = t1_z
        self.t[0, 1] = t2_x
        self.t[1, 1] = t2_y
        self.t[2, 1] = t2_z
        self.t[0, 2] = t3_x
        self.t[1, 2] = t3_y
        self.t[2, 2] = t3_z
        self.t1_len = math.sqrt(t1_x * t1_x + t1_y * t1_y + t1_z * t1_z)
        self.t2_len = math.sqrt(t2_x * t2_x + t2_y * t2_y + t2_z * t2_z)
        self.t3_len = math.sqrt(t3_x * t3_x + t3_y * t3_y + t3_z * t3_z)
        i = 5
        self.vasp_version = 5
        atoms = self.datlines[i].split()
        if atoms[0].isdigit():
            self.vasp_version = 4
        del atoms
        self.__logger.debug("    vasp version = %s" % self.vasp_version)
        i = 5
        self.atoms_index = []
        self.atoms = []
        if self.vasp_version == 4:
            self.atoms.extend(self.datlines[i].split())
        elif self.vasp_version == 5:
            self.atoms_index.extend(self.datlines[i].split())
            self.atoms.extend(self.datlines[i + 1].split())
        else:
            sys.exit("Error: unknown VASP format")
        self.atoms = np.array(self.atoms, dtype=int)
        self.nion = len(self.atoms)
        self.atoms_number = np.zeros(self.nion, dtype=int)
        for i in range(self.nion):
            self.__logger.debug("atoms_index[%d] = %s" % (i, self.atoms_index[i]))
            self.atoms_number[i] = ElementTable().get_atomic_number1(
                str(self.atoms_index[i])
            )
        print("Confirmation of the total number of atoms")
        self.natom = 0
        for j in range(self.nion):
            sum = int(self.atoms[j])
            self.natom = self.natom + sum
        if not reduced_memory:
            print("Create ion[j]")
            self.ion = np.zeros(self.natom, dtype=int)
            tmp = -1
            for j in range(self.nion):
                local = -1
                for k in range(int(self.atoms[j])):
                    tmp += 1
                    local += 1
                    self.ion[tmp] = int(j)
        if not reduced_memory:
            print("Create ion_local[j]")
            self.ion = np.zeros(self.natom, dtype=int)
            self.ion_local = np.zeros(self.natom, dtype=int)
            tmp = -1
            for j in range(self.nion):
                local = -1
                for k in range(int(self.atoms[j])):
                    tmp += 1
                    local += 1
                    self.ion_local[tmp] = int(local)
        if self.vasp_version == 4:
            i = 5 + 1
        else:
            i = 6 + 1
        num_reg = re.compile("^[+-]?(\\d*\\.\\d+|\\d+\\.?\\d*)([eE][+-]?\\d+|)\\Z")
        selective_reg = re.compile("^S.*", re.IGNORECASE)
        if bool(num_reg.match(self.datlines[i].split()[0])):
            print("%s" % str(self.datlines[i].split()[0]))
            sys.exit("Format Error")
        elif bool(selective_reg.match(self.datlines[i].split()[0])):
            self.selective = True
        else:
            self.selective = False
        if self.vasp_version == 4:
            i = 5 + 1
        else:
            i = 6 + 1
        if self.selective:
            i += 1
        direct_reg = re.compile("^D.*", re.IGNORECASE)
        car_reg = re.compile("^C.*", re.IGNORECASE)
        if bool(num_reg.match(self.datlines[i].split()[0])):
            print("%s" % str(self.datlines[i].split()[0]))
            sys.exit("Format Error")
        if bool(direct_reg.match(self.datlines[i].split()[0])):
            self.direct = True
        elif bool(car_reg.match(self.datlines[i].split()[0])):
            self.direct = False
        print("get atomic coordinate position")
        if self.vasp_version == 4:
            i = 5
        else:
            i = 6
        if self.selective:
            i += 1
        print("natom = %d" % self.natom)
        print("init: position")
        self.position = np.zeros((int(self.natom), 3))
        print("init: fix")
        self.fix = np.zeros((int(self.natom), 3), dtype="S")
        i += 2
        current_datlines = i
        for j in range(self.natom):
            print("%s" % j)
            self.position[j, 0] = float(self.datlines[i + j].split()[0])
            self.position[j, 1] = float(self.datlines[i + j].split()[1])
            self.position[j, 2] = float(self.datlines[i + j].split()[2])
            if self.selective:
                if len(self.datlines[i + j].split()) < 6:
                    sys.exit("STOP: corrdinate line Format Error")
                self.fix[j, 0] = str(self.datlines[i + j].split()[3])
                self.fix[j, 1] = str(self.datlines[i + j].split()[4])
                self.fix[j, 2] = str(self.datlines[i + j].split()[5])
            current_datlines = i + j
        self.__logger.debug("--- END (readline = %s)" % current_datlines)
        self.read_mesh_data(startline=current_datlines + 2)

    def read_mesh_data(self, startline=None, mode="CHGCAR"):
        """
        電荷密度構造 の読み込み (2018.08.18)
        VASP マニュアルより下記
        WRITE(IU, FORM)(((C(NX, NY, NZ), NX=1, NGXC), NY=1, NGYZ), NZ=1, NGZC)

        self.__chgdata = np.zeros((self.__ngxc, self.__ngyz, self.__ngzc))

        :param startline:
        :param mode:
        :return:
        """
        self.__logger.debug("--- Read MESH DATA and Makes CELL INDEX")
        if startline is None:
            return
        self.__ngxc = int(self.datlines[startline].split()[0])
        self.__ngyz = int(self.datlines[startline].split()[1])
        self.__ngzc = int(self.datlines[startline].split()[2])
        self.__logger.debug(
            "READ MeshDATA: NGXC=%d, NGYZ=%d, HGZC=%d"
            % (self.__ngxc, self.__ngyz, self.__ngzc)
        )
        self.rate_x = self.t1_len / self.__ngxc
        self.rate_y = self.t2_len / self.__ngyz
        self.rate_z = self.t3_len / self.__ngzc
        mesh_max = self.__ngxc * self.__ngyz * self.__ngzc
        self.__logger.debug("mesh_max = %s" % mesh_max)
        self.__logger.debug("mode     = %s" % mode)
        if mode == "CHGCAR":
            mesh_max_line = int(mesh_max / 5)
        elif mode == "ELFCAR":
            mesh_max_line = int(mesh_max / 10)
        else:
            self.__logger.error("Error")
            return
        start_mesh_index = startline + 1
        self.__chgdata = np.zeros((self.__ngxc, self.__ngyz, self.__ngzc))
        chglist = ""
        for i in range(mesh_max_line):
            tmp_ = self.datlines[start_mesh_index + i]
            chglist += "".join(tmp_)
        chgarray = chglist.split()
        if len(chgarray) != mesh_max:
            self.__logger.debug("added to read line")
            chglist += "".join(self.datlines[start_mesh_index + i + 1])
            chgarray = chglist.split()
        self.__logger.debug("num. CHG array = %s" % len(chgarray))
        if len(chgarray) != mesh_max:
            print(tmp_)
            print("read error")
        i = 0
        for nx in range(0, self.__ngxc):
            for ny in range(0, self.__ngyz):
                for nz in range(0, self.__ngzc):
                    self.__chgdata[nx, ny, nz] = float(chgarray[i])
                    i += 1
        self.__logger.debug("--- END: read_mesh_data()")
        self.__logger.debug("")

    def get_poscar_info(self):
        """POSCAR 情報の取り出し
        リストなので順番維持
        return [title, scale, t, vasp, nion, atoms, atoms_index, natom, selective, direct, position, fix]:
        """
        title = self.title
        scale = self.scale
        t = self.get_t()
        vasp = self.get_vasp_version()
        nion = self.get_nion()
        atoms = self.get_atoms()
        atoms_index = self.get_atoms_index()
        natom = self.get_natom()
        selective = self.get_selective()
        direct = self.get_direct()
        position = self.get_position()
        fix = self.get_fix()
        return [
            title,
            scale,
            t,
            vasp,
            nion,
            atoms,
            atoms_index,
            natom,
            selective,
            direct,
            position,
            fix,
        ]

    def init_ave_elf(self):
        """
        ELF 積算解析（ある原点を中心としたELFの球積分値の解析)用のために
        chgcar/elfcar のデータを 3x3x3 の super-cell とする

        self.__chgdata[nx, ny, nz] にて chg/elf が読み込まれている必要がある

        :return: chgdata_s[nx, ny, nz]: 3x3x3 スーパーセル化した chgdata のマトリックス
        """
        self.chgdata_s = np.zeros((self.__ngxc * 3, self.__ngyz * 3, self.__ngzc * 3))
        sx = [0, self.__ngxc, self.__ngxc * 2]
        sy = [0, self.__ngyz, self.__ngyz * 2]
        sz = [0, self.__ngzc, self.__ngzc * 2]
        self.__logger.debug("makes chgcar super-cell: plase waite...")
        for nx in range(0, self.__ngxc):
            for ny in range(0, self.__ngyz):
                for nz in range(0, self.__ngzc):
                    s = self.__chgdata[nx, ny, nz]
                    for i in range(3):
                        for j in range(3):
                            for k in range(3):
                                self.chgdata_s[nx + sx[i], ny + sy[j], nz + sz[k]] = s
        return self.chgdata_s

    def sphere_integral_elf(self, r_diff=1.0):
        """
        ある原点からのある半径内での ELF の平均値

        事前に chg/elf の 3x3x3 スーパーセルを作っておく必要がある
        self.chgdata_s[nx, ny, nz]
        self.__ngxc
        self.__ngyz
        self.__ngzc
        self.rate_x
        self.rate_y
        self.rate_z

        :param r_diff: 半径
        :return: self.ave_elf[nx, ny, nz]: CHGCAR 形式(FFT-MESHパートのみ)のマトリックス
        """
        from sae.vasp.elf import ElfIntegration

        self.ave_elf = ElfIntegration().sphere_integral_of_elf(
            self.chgdata_s,
            self.__ngxc,
            self.__ngyz,
            self.__ngzc,
            self.rate_x,
            self.rate_y,
            self.rate_z,
            r_diff=r_diff,
        )
        return self.ave_elf

    def inverse_chgcar_OLD(self, chgcar=None):
        """
        入力の CHGCAR を各要素毎に 1/CHGCAR して結果を 新しい CHGCAR を返す
        :param chgcar:
        :return:
        """
        if chgcar is None:
            chgcar = self.__chgdata
        return 1 / chgcar

    def inverse_chgcar(self, chgcar=None, offset=None):
        """
        入力の CHGCAR を各要素毎に -1 を掛けて, 最小の CHAEGE(元データで言うところの最大値) を足して
        ゼロとするオフセット処理をして CHGCAR を返す
        :param chgcar:
        :return:
        """
        if chgcar is None:
            if offset is None:
                chgcar = self.__chgdata * -1
            else:
                chgcar = self.__chgdata * -1 + offset
        return chgcar

    def get_chgcar(self, chgcar=None):
        if chgcar is None:
            chgcar = self.__chgdata
        return chgcar

    def print_chgcar(
        self, chgcar=None, ngx_max=None, ngy_max=None, ngz_max=None, outname=None
    ):
        """
        CHGCAR 形式での出力

        in: 元のPOSCAR情報すべて
        in: self.__ngxc
        in: self.__ngyz
        in: self.__ngzc

        :param: ngx: FFT-mesh, None のときは読み込んだ CHGCAR の mesh そのまま
        :param: ngy: FFT-mesh, None のときは読み込んだ CHGCAR の mesh そのまま
        :param: ngz: FFT-mesh, None のときは読み込んだ CHGCAR の mesh そのまま
        :param: chgcar: chgdata[x,y,z]: FFT-MESH のchgdata
        :param: filename: ファイル名を入れたらファイル書き出し
        """
        if chgcar is None:
            chgcar = self.__chgdata
        if ngx_max is None:
            ngx = self.__ngxc
        if ngy_max is None:
            ngy_max = self.__ngyz
        if ngz_max is None:
            ngz_max = self.__ngzc
        if outname is not None:
            try:
                out = open(outname, "w")
            except:
                sys.exit("STOP: %s can't open." % outname)
        else:
            out = sys.stdout
        title = self.get_title()
        scale = self.get_scale()
        t = self.get_t()
        vasp = self.get_vasp_version()
        nion = self.get_nion()
        atoms = self.get_atoms()
        atoms_index = self.get_atoms_index()
        natom = self.get_natom()
        selective = self.get_selective()
        direct = self.get_direct()
        position = self.get_position()
        fix = self.get_fix()
        ion = self.get_ion()
        ion_local = self.get_ion_local()
        atoms_index_j = self.get_atoms_index_j()
        print("%s" % str(title), file=out)
        print("  %13.9f" % scale, file=out)
        print("  %13.9f %13.9f %13.9f" % (t[0, 0], t[1, 0], t[2, 0]), file=out)
        print("  %13.9f %13.9f %13.9f" % (t[0, 1], t[1, 1], t[2, 1]), file=out)
        print("  %13.9f %13.9f %13.9f" % (t[0, 2], t[1, 2], t[2, 2]), file=out)
        if vasp >= 5:
            print(" ", file=out, end="")
            for i in range(nion):
                print("%s " % str(atoms_index[i]), file=out, end="")
            print(" ", file=out)
        print(" ", file=out, end="")
        for i in range(nion):
            print("%s " % str(atoms[i]), file=out, end="")
        print(" ", file=out)
        if selective:
            print("Selective Dynamics", file=out)
        if direct:
            print("Direct", file=out)
        else:
            print("Cartesian", file=out)
        for j in range(natom):
            print(
                " %13.9f %13.9f %13.9f"
                % (position[j, 0], position[j, 1], position[j, 2]),
                file=out,
                end="",
            )
            if selective:
                print("", file=out, end="")
                print(
                    "%s %s %s" % (str(fix[j, 0]), str(fix[i, 1]), str(fix[i, 2])),
                    file=out,
                    end="",
                )
            print("", file=out)
        print(
            "write VASP style (new) %s files: plase wait..." % outname, file=sys.stdout
        )
        ngx_max = self.__ngxc * 1
        ngy_max = self.__ngyz * 1
        ngz_max = self.__ngzc * 1
        inner_counter = 0
        print("", file=out)
        print("%d %d %d" % (ngx_max, ngy_max, ngz_max), file=out)
        for nx in range(0, ngx_max):
            for ny in range(0, ngy_max):
                for nz in range(0, ngz_max):
                    inner_counter += 1
                    if chgcar[nx, ny, nz] < 0.001:
                        print("{:<12.5e}".format(chgcar[nx, ny, nz]), file=out, end="")
                    elif 0.001 <= chgcar[nx, ny, nz] < 10:
                        print("{:<12.5f}".format(chgcar[nx, ny, nz]), file=out, end="")
                    elif chgcar[nx, ny, nz] >= 10.0:
                        print("{:<12.5e}".format(chgcar[nx, ny, nz]), file=out, end="")
                    else:
                        print("{:<12.5e}".format(chgcar[nx, ny, nz]), file=out, end="")
                    if inner_counter >= 10:
                        inner_counter = 0
                        print("", file=out)
        out.close()

    def print_ave_elfcar(self, outname=None):
        """
        ラッパー関数
        self.ave_elf[nx,ny,nz]: ELF を あるFFT-MESH上で積算した値をその FFT-MESH のマップとして保存したもの
                                CHGCAR と同じ形式

        :param outname:
        :return:
        """
        self.print_chgcar(
            self.ave_elf,
            ngx_max=self.__ngxc,
            ngy_max=self.__ngyz,
            ngz_max=self.__ngzc,
            outname=outname,
        )

    def print_super_chgcar(self, x_times=3, y_times=3, z_times=3, outname=None):
        """
        (test) 3x3x3 スーパーセルとして作成した CHGCAR mesh を CHGCAR 形式で出力する

        in: self.__ngxc
        in: self.__ngyz
        in: self.__ngzc

        in: self.chgdata_s[x,y,z]: スーパーセル FFT-MESH data
        :param: filename: ファイル名を入れたらファイル書き出し(CHGパートのみ)
        """
        if outname is not None:
            try:
                out = open(outname, "w")
            except:
                sys.exit("STOP: %s can't open." % outname)
        else:
            out = sys.stdout
        self.__logger.debug(
            "write VASP style (new) %s files: plase wait..." % outname, file=sys.stdout
        )
        ngx_max = self.__ngxc * x_times
        ngy_max = self.__ngyz * y_times
        ngz_max = self.__ngzc * z_times
        inner_counter = 0
        print("", file=out)
        print("", file=out)
        print("%d %d %d" % (ngx_max, ngy_max, ngz_max), file=out)
        for nx in range(0, ngx_max):
            for ny in range(0, ngy_max):
                for nz in range(0, ngz_max):
                    inner_counter += 1
                    if self.chgdata_s[nx, ny, nz] >= 0.001:
                        print(
                            "{:<12.5f}".format(self.chgdata_s[nx, ny, nz]),
                            file=out,
                            end="",
                        )
                    else:
                        print(
                            "{:<12.5e}".format(self.chgdata_s[nx, ny, nz]),
                            file=out,
                            end="",
                        )
                    if inner_counter >= 10:
                        inner_counter = 0
                        print("", file=out)
        out.close()

    def conv_rot_euler(self, alpha, beta, gamma):
        """
        基本並進ベクトルを、alpha, beta, gamma で回す
        VASP 表記とは転置した形で t ベクトルに入っているの注意
        注意) むしろ VASP 表記が転置している
        ここでは転置したまま,正しい基本並進ベクトルのまま処理をする
        :param alpha:
        :param beta:
        :param gamma:
        :return:
        """
        from sae.geometry.rotation import Rotations

        R = Rotations().rotate_euler(alpha, beta, gamma)
        t = self.get_t()
        t1 = np.matrix([t[0, 0], t[0, 1], t[0, 2]])
        t1r = t1 * R
        t2 = np.matrix([t[1, 0], t[1, 1], t[1, 2]])
        t2r = t2 * R
        t3 = np.matrix([t[2, 0], t[2, 1], t[2, 2]])
        t3r = t3 * R
        R_t = np.matrix(
            [
                [t1r[0, 0], t1r[0, 1], t1r[0, 2]],
                [t2r[0, 0], t2r[0, 1], t2r[0, 2]],
                [t3r[0, 0], t3r[0, 1], t3r[0, 2]],
            ]
        )
        position = self.get_position()
        natom = self.get_natom()
        R_position = np.zeros((natom, 3))
        for j in range(natom):
            p = np.matrix([position[j, 0], position[j, 1], position[j, 2]])
            pr = p * R
            R_position[j, 0] = pr[0, 0]
            R_position[j, 1] = pr[0, 1]
            R_position[j, 2] = pr[0, 2]
        return (R_t, R_position)

    def conv_direct2car(self, ABS=None):
        from sae.geometry.coordinates import CoordinateTransforms

        if ABS is not None:
            ABS = False
        elif isinstance(ABS, str):
            if ABS == "vasp" or ABS == "VASP":
                ABS = True
        self.scale, self.direct = CoordinateTransforms().conv_direct2cara(
            ABS, self.scale, self.t, self.natom, self.direct, self.position
        )

    def print_poscar(self, outname="POSCAR", STD=True):
        """
        POSCAR パートを表示する、outname 入力がある場合はファイル出力
        :param outname:
        :param STD:
        :return:
        """
        from sae.vasp.poscar_writer import PoscarWriter

        PoscarWriter().print_poscar(
            outname,
            STD,
            self.title,
            self.scale,
            self.natom,
            self.nion,
            self.selective,
            self.direct,
            self.vasp_version,
            self.t,
            self.atoms,
            self.atoms_index,
            self.position,
            self.fix,
        )

    def conv_supercell(self, times=(1, 1, 1)):
        """
        スーパーセル作成 Method
        関数版を持ってきただけのやっつけ対応

        :param times:
        :return:
        """
        from sae.geometry.coordinates import CoordinateTransforms
        from sae.geometry.supercell import SupercellOperations

        super_x = int(times[0])
        super_y = int(times[1])
        super_z = int(times[2])
        if self.direct:
            ABS = True
            self.scale, self.direct = CoordinateTransforms().conv_direct2cara(
                ABS, self.scale, self.t, self.natom, self.direct, self.position
            )
        supers = super_x * super_y * super_x
        sv = np.zeros((supers, 3))
        sp = np.zeros((self.natom * supers, 3))
        ion_sp = np.zeros(self.natom * supers)
        ion_local_sp = np.zeros(self.natom * supers)
        fix_sp = np.zeros((self.natom * supers, 3), dtype="S")
        sp_j = np.zeros(self.natom * supers)
        SupercellOperations().make_supercell1(
            super_x,
            super_y,
            super_z,
            self.t,
            self.natom,
            self.nion,
            self.atoms,
            self.ion,
            self.ion_local,
            self.position,
            sv,
            ion_sp,
            ion_local_sp,
            sp_j,
            sp,
            self.fix,
            fix_sp,
        )
        SupercellOperations().make_supercell_param(
            super_x, super_y, super_z, self.nion, self.atoms, self.t
        )
        self.natom = self.natom * supers
        if not self.direct:
            self.scale, self.direct = CoordinateTransforms().conv_car2direct(
                self.scale, self.t, self.natom, self.direct, sp
            )
        self.ion = ion_sp
        self.ion_local = ion_local_sp
        self.position = sp
        self.fix = fix_sp
        self.sp_j = sp_j
