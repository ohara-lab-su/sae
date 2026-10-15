from sae.errors import legacy_error as _legacy_error

#!/usr/bin/env python
# coding:utf-8
import multiprocessing
import sys
import os
import traceback


class Writer(object):
    def __init__(
        self,
        outname=None,
        poscar_info=None,
        ngx_max=None,
        ngy_max=None,
        ngz_max=None,
        logger=None,
    ):
        """
        :param outname:
        """
        if logger is None:
            logger = multiprocessing.get_logger()
        self.__logger = logger

        if outname is None:
            self.__outname = "CHGCAR_NEW"
        else:
            self.__outname = outname

        self.__ngx_max = 150
        self.__ngy_max = 150
        self.__ngz_max = 150
        self.__chgdata = None
        if ngx_max is not None:
            self.__ngx_max = ngx_max
        if ngy_max is not None:
            self.__ngy_max = ngy_max
        if ngz_max is not None:
            self.__ngz_max = ngz_max
        if poscar_info is not None:
            self.__poscar_info = poscar_info

    def get_outname(self):
        return self.__outname

    def set_outname(self, val):
        self.__outname = val

    outname = property(get_outname, set_outname)

    def get_ngx_max(self):
        return self.__ngx_max

    def set_ngx_max(self, val):
        self.__ngx_max = val

    ngx_max = property(get_ngx_max, set_ngx_max)

    def get_ngy_max(self):
        return self.__ngy_max

    def set_ngy_max(self, val):
        self.__ngy_max = val

    ngy_max = property(get_ngy_max, set_ngy_max)

    def get_ngz_max(self):
        return self.__ngz_max

    def set_ngz_max(self, val):
        self.__ngz_max = val

    ngz_max = property(get_ngz_max, set_ngz_max)

    def get_chgdata(self):
        return self.__chgdata

    def set_chgdata(self, val):
        self.__chgdata = val

    chgdata = property(get_chgdata, set_chgdata)

    def get_poscar_info(self):
        return self.__poscar_info

    def set_poscar_info(self, val):
        self.__poscar_info = val

    poscar_info = property(get_poscar_info, set_poscar_info)

    def write_chgcar(
        self,
        chgdata=None,
        poscar_info=None,
        ngx_max=None,
        ngy_max=None,
        ngz_max=None,
        outname=None,
    ):
        return self.print_chgcar(
            chgdata=chgdata,
            poscar_info=poscar_info,
            ngx_max=ngx_max,
            ngy_max=ngy_max,
            ngz_max=ngz_max,
            outname=outname,
        )

    def print_chgcar(
        self,
        chgdata=None,
        poscar_info=None,
        ngx_max=None,
        ngy_max=None,
        ngz_max=None,
        outname=None,
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
        if chgdata is None:
            chgdata = self.__chgdata

        if ngx_max is None:
            self.ngx_max = self.__ngx_max

        if ngy_max is None:
            self.ngy_max = self.__ngy_max

        if ngz_max is None:
            self.ngz_max = self.__ngz_max

        if poscar_info is None:
            poscar_info = self.__poscar_info

        if outname is None:
            outname = self.__outname

        self.__logger.info("outname = %s" % outname)
        self.__logger.info("ngx_max = %s" % self.ngx_max)
        self.__logger.info("ngy_max = %s" % self.ngy_max)
        self.__logger.info("ngz_max = %s" % self.ngz_max)

        try:
            out = open(outname, "w")
        except:
            _legacy_error("STOP: %s can't open." % outname)
        # else:
        #     out = sys.stdout

        # 元のPOSCAR情報を取得
        title = poscar_info[0]
        scale = poscar_info[1]
        t = poscar_info[2]
        vasp = poscar_info[3]
        nion = poscar_info[4]
        atoms = poscar_info[5]
        atoms_index = poscar_info[6]
        natom = poscar_info[7]
        selective = poscar_info[8]
        direct = poscar_info[9]
        position = poscar_info[10]
        fix = self.poscar_info[11]

        # ion = self.get_ion()
        # ion_local = self.get_ion_local()
        # atoms_index_j = self.get_atoms_index_j()

        # POSCAR 相当情報の書き込み
        #
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

        # print("write VASP style (new) CHGCAR files: plase wait...", file=sys.stdout)
        self.__logger.debug("write VASP style (new) CHGCAR files: plase wait...")
        ngx_max = self.ngx_max * 1
        ngy_max = self.ngy_max * 1
        ngz_max = self.ngz_max * 1

        # WRITE CHGCAR/ELFCAR DATA
        print("", file=out)
        print("%d %d %d" % (ngx_max, ngy_max, ngz_max), file=out)

        inner_counter = 0
        for nx in range(0, ngx_max):
            for ny in range(0, ngy_max):
                for nz in range(0, ngz_max):
                    inner_counter += 1
                    try:
                        if chgdata[nx, ny, nz] < 0.001:
                            print(
                                "{:<12.5e}".format(chgdata[nx, ny, nz]),
                                file=out,
                                end="",
                            )
                        elif 0.001 <= chgdata[nx, ny, nz] < 10:
                            print(
                                "{:<12.5f}".format(chgdata[nx, ny, nz]),
                                file=out,
                                end="",
                            )
                        # print("%11.5f " % self.__chgdata[nx, ny, nz], end="")
                        elif chgdata[nx, ny, nz] >= 10.00:
                            print(
                                "{:<12.5e}".format(chgdata[nx, ny, nz]),
                                file=out,
                                end="",
                            )
                            # print("%12.5e " % self.__chgdata[nx, ny, nz], end="")
                        else:
                            print(
                                "{:<12.5e}".format(chgdata[nx, ny, nz]),
                                file=out,
                                end="",
                            )
                    except Exception as e:
                        print("***Error***, %s" % e)
                        print("nx = %s" % nx)
                        print("ny = %s" % ny)
                        print("nz = %s" % nz)
                        print("chgdata = %s" % chgdata[nx, ny, nz])

                    # if inner_counter >= 10:
                    if inner_counter >= 5:
                        inner_counter = 0
                        print("", file=out)

        out.close()


WriteVaspChgcar = Writer  # historical spelling
