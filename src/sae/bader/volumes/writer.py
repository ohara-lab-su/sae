from sae.errors import legacy_error as _legacy_error

#!/usr/bin/env python
# coding:utf-8
"""
Bader Volume の書き出し
実質的には CHGCAR 書き出しと同じ(CHGCAR書き出しルーチンのadapter的なクラスとなっている)
UtilBader()　で作成した、足し合わせた Bader Volume などの書き出し用。
"""
import multiprocessing
import StructureAnalysisEnvironment as SAE


class VolumeWriter(object):
    def __init__(
        self,
        outname="CHGCAR_BvAt",
        chgdata=None,
        poscar_info=None,
        ngx_max=None,
        ngy_max=None,
        ngz_max=None,
        logger=None,
    ):
        """
        :param outname:
        :param chgdata:
        :param poscar_info:
        :param ngx_max:
        :param ngy_max:
        :param ngz_max:
        :param logger:
        """
        if logger is None:
            logger = multiprocessing.get_logger()
        self.__logger = logger

        self.__outname = outname
        self.__chgdata = chgdata
        self.__poscar_info = poscar_info
        self.__ngx_max = 150
        self.__ngy_max = 150
        self.__ngz_max = 150

        if ngx_max is not None:
            self.__ngx_max = ngx_max

        if ngy_max is not None:
            self.__ngy_max = ngy_max

        if ngz_max is not None:
            self.__ngz_max = ngz_max

    @property
    def ngx_max(self):
        return self.__ngx_max

    @ngx_max.setter
    def ngx_max(self, val):
        self.__ngx_max = val

    @property
    def ngy_max(self):
        return self.__ngy_max

    @ngy_max.setter
    def ngy_max(self, val):
        self.__ngy_max = val

    @property
    def ngz_max(self):
        return self.__ngz_max

    @ngz_max.setter
    def ngz_max(self, val):
        self.__ngz_max = val

    @property
    def chgdata(self):
        return self.__chgdata

    @chgdata.setter
    def chgdata(self, val):
        self.__chgdata = val

    @property
    def poscar_info(self):
        return self.__poscar_info

    @poscar_info.setter
    def poscar_info(self, val):
        self.__poscar_info = val

    @property
    def outname(self):
        return self.__outname

    @outname.setter
    def outname(self, val):
        self.__outname = val

    def write_bader_volume(self, outname=None):
        if outname is None:
            outname = self.__outname
        self.__logger.debug("=== write_bader_volume(): outname = %s" % outname)

        chgcar = SAE.io.WriteVaspChgcar(logger=self.__logger)
        chgcar.poscar_info = self.__poscar_info
        chgcar.chgdata = self.__chgdata
        chgcar.ngx_max = self.__ngx_max
        chgcar.ngy_max = self.__ngy_max
        chgcar.ngz_max = self.__ngz_max
        chgcar.write_chgcar(outname=outname)


WriteBaderVolume = VolumeWriter  # historical spelling
