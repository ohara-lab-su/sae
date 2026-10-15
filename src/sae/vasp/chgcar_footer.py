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


class ReadVaspChgcarFooter(Method):

    def __init__(
        self,
        CHGCAR,
        header_data,
        suffix=".vasp",
        sort=False,
        atoms_index=None,
        logger=None,
    ):
        """
        init and Read CHGCAR

        :param CHGCAR: 読み込みファイルの名前(必須)
        :param header: CHGCAR のヘッダ情報(必須)
        :param suffix: 使ってない
        :param sort:
        :param atoms_index:
        """
        if logger is None:
            logger = multiprocessing.get_logger()
        self.__logger = logger
        self.open(CHGCAR, header_data, suffix=suffix, sort=sort, atoms_index=sort)

    def read_header(self):
        pass

    def open(self, CHGCAR, header_data, suffix=".vasp", sort=False, atoms_index=None):
        from sae.common.text import TextFiles

        self.datlines, self.num = TextFiles().read_dataline(CHGCAR)
        print("--- Read Dummy Header = ", CHGCAR)
        self.title = header_data[0]
        self.scale = header_data[1]
        self.t = header_data[2]
        self.vasp_version = header_data[3]
        self.nion = header_data[4]
        self.atoms = header_data[5]
        self.atoms_index = header_data[6]
        self.natom = header_data[7]
        self.selective = header_data[8]
        self.direct = header_data[9]
        print("-------------------")
        print(self.title)
        print(self.scale)
        print(self.t)
        print(self.vasp_version)
        print(self.nion)
        print(self.atoms)
        print(self.atoms_index)
        print(self.natom)
        print(self.selective)
        print(self.direct)
        print("-------------------")
        self.__logger.info("vasp version = %s" % self.vasp_version)
        if self.vasp_version == 4:
            i = 5 + 1
        else:
            i = 6 + 1
        if self.selective:
            i += 1
        i += 1
        print("natom = %d" % self.natom)
        print("init: position")
        self.position = np.zeros((int(self.natom), 3))
        print("init: fix")
        self.fix = np.zeros((int(self.natom), 3), dtype="S")
        j = 0
        current_datlines = 0
        for j in range(self.natom):
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
        print(
            "last atomc position =",
            j,
            " %16.12f %16.12f %16.12f"
            % (self.position[j, 0], self.position[j, 1], self.position[j, 2]),
        )
        self.__logger.info("--- END (readline = %s)" % current_datlines)
        self.read_mesh_data(startline=current_datlines + 2)

    def read_mesh_data(self, startline=None, mode="CHGCAR"):
        self.__logger.info("--- Read MESH DATA (FFT-mesh) and Makes CELL INDEX")
        if startline is None:
            return
        t1_x = self.t[0, 0]
        t1_y = self.t[1, 0]
        t1_z = self.t[2, 0]
        t2_x = self.t[0, 1]
        t2_y = self.t[1, 1]
        t2_z = self.t[2, 1]
        t3_x = self.t[0, 2]
        t3_y = self.t[1, 2]
        t3_z = self.t[2, 2]
        self.t1_len = math.sqrt(t1_x * t1_x + t1_y * t1_y + t1_z * t1_z)
        self.t2_len = math.sqrt(t2_x * t2_x + t2_y * t2_y + t2_z * t2_z)
        self.t3_len = math.sqrt(t3_x * t3_x + t3_y * t3_y + t3_z * t3_z)
        print("t1 len = ", self.t1_len)
        print("t2 len = ", self.t2_len)
        print("t3 len = ", self.t3_len)
        self.ngxc = int(self.datlines[startline].split()[0])
        self.ngyz = int(self.datlines[startline].split()[1])
        self.ngzc = int(self.datlines[startline].split()[2])
        self.__logger.info(
            "NGXC=%d, NGYZ=%d, HGZC=%d" % (self.ngxc, self.ngyz, self.ngzc)
        )
        self.rate_x = self.t1_len / self.ngxc
        self.rate_y = self.t2_len / self.ngyz
        self.rate_z = self.t3_len / self.ngzc
        mesh_max = self.ngxc * self.ngyz * self.ngzc
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
        self.__chgdata = np.zeros((self.ngxc, self.ngyz, self.ngzc))
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
        for nx in range(0, self.ngxc):
            for ny in range(0, self.ngyz):
                for nz in range(0, self.ngzc):
                    self.__chgdata[nx, ny, nz] = float(chgarray[i])
                    i += 1
        self.__logger.debug("--- END: read_mesh_data()")
        self.__logger.debug("")

    @property
    def chgdata(self):
        """チャージ情報を取り出す(numpy)"""
        return self.__chgdata

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

    @property
    def poscar_info(self):
        """POSCAR 情報の取り出し"""
        return self.get_poscar_info()

    def init_ave_elf(self):
        """
        ELF 積算解析（ある原点を中心としたELFの球積分値の解析)用のために
        chgcar/elfcar のデータを 3x3x3 の super-cell とする

        self.__chgdata[nx, ny, nz] にて chg/elf が読み込まれている必要がある

        :return: chgdata_s[nx, ny, nz]: 3x3x3 スーパーセル化した chgdata のマトリックス
        """
        self.chgdata_s = np.zeros((self.ngxc * 3, self.ngyz * 3, self.ngzc * 3))
        sx = [0, self.ngxc, self.ngxc * 2]
        sy = [0, self.ngyz, self.ngyz * 2]
        sz = [0, self.ngzc, self.ngzc * 2]
        self.__logger.debug("makes chgcar super-cell: plase waite...")
        for nx in range(0, self.ngxc):
            for ny in range(0, self.ngyz):
                for nz in range(0, self.ngzc):
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
        self.ngxc
        self.ngyz
        self.ngzc
        self.rate_x
        self.rate_y
        self.rate_z

        :param r_diff: 半径
        :return: self.ave_elf[nx, ny, nz]: CHGCAR 形式(FFT-MESHパートのみ)のマトリックス
        """
        from sae.vasp.elf import ElfIntegration

        self.ave_elf = ElfIntegration().sphere_integral_of_elf(
            self.chgdata_s,
            self.ngxc,
            self.ngyz,
            self.ngzc,
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
        in: self.ngxc
        in: self.ngyz
        in: self.ngzc

        :param: ngx: FFT-mesh, None のときは読み込んだ CHGCAR の mesh そのまま
        :param: ngy: FFT-mesh, None のときは読み込んだ CHGCAR の mesh そのまま
        :param: ngz: FFT-mesh, None のときは読み込んだ CHGCAR の mesh そのまま
        :param: chgcar: chgdata[x,y,z]: FFT-MESH のchgdata
        :param: filename: ファイル名を入れたらファイル書き出し
        """
        if chgcar is None:
            chgcar = self.__chgdata
        if ngx_max is None:
            ngx = self.ngxc
        if ngy_max is None:
            ngy_max = self.ngyz
        if ngz_max is None:
            ngz_max = self.ngzc
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
        ngx_max = self.ngxc * 1
        ngy_max = self.ngyz * 1
        ngz_max = self.ngzc * 1
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
            ngx_max=self.ngxc,
            ngy_max=self.ngyz,
            ngz_max=self.ngzc,
            outname=outname,
        )

    def print_super_chgcar(self, x_times=3, y_times=3, z_times=3, outname=None):
        """
        (test) 3x3x3 スーパーセルとして作成した CHGCAR mesh を CHGCAR 形式で出力する

        in: self.ngxc
        in: self.ngyz
        in: self.ngzc

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
        ngx_max = self.ngxc * x_times
        ngy_max = self.ngyz * y_times
        ngz_max = self.ngzc * z_times
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
