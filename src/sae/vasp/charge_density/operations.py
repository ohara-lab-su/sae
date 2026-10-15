from sae.errors import legacy_error as _legacy_error

#!/usr/bin/env python
# coding:utf-8

import multiprocessing
import StructureAnalysisEnvironment as SAE
import numpy as np


class SumChargeDensity(object):

    def __init__(self, logger=None):
        if logger is None:
            logger = multiprocessing.get_logger()
        self.__logger = logger

        name = "CHGCAR_Li_100_200"
        instance = SAE.io.ReadVaspChgcar(CHGCAR=name)
        chgdata = instance.chgdata
        tmp = np.copy(chgdata)
        poscar_info = instance.poscar_info
        ngx = instance.ngxc
        ngy = instance.ngyz
        ngz = instance.ngzc

        names = [
            "CHGCAR_Li_200_300",
            "CHGCAR_Li_300_400",
            "CHGCAR_Li_400_500",
            "CHGCAR_Li_500_600",
            "CHGCAR_Li_600_700",
            "CHGCAR_Li_800_900",
            "CHGCAR_Li_900_1000",
            "CHGCAR_Li_1000_1100",
            "CHGCAR_Li_1100_1215",
        ]

        for item in names:
            instance = SAE.io.ReadVaspChgcar(CHGCAR=item)
            chgdata = tmp + instance.chgdata
            poscar_info = instance.poscar_info
            tmp = np.copy(chgdata)
            ngx = instance.ngxc
            ngy = instance.ngyz
            ngz = instance.ngzc

        self.__ngx = ngx
        self.__ngy = ngy
        self.__ngz = ngz
        self.__poscar_info = poscar_info
        self.__chgdata = np.copy(chgdata)
        del instance

    @property
    def chgdata(self):
        return self.__chgdata

    @property
    def ngx(self):
        return self.__ngx

    @property
    def ngy(self):
        return self.__ngy

    @property
    def ngz(self):
        return self.__ngz

    @property
    def poscar_info(self):
        return self.__poscar_info


if __name__ == "__main__":
    loglevel = "debug"
    logger = SAE.util.logger.Logger(loglevel=loglevel)

    chg = SumChgcar(logger=logger)
    chgdata = chg.chgdata
    print(chgdata)
    poscar_info = chg.poscar_info
    ngx = chg.ngx
    ngy = chg.ngy
    ngz = chg.ngz

    print("********** WRITER ************")
    wbv = SAE.io.WriteVaspChgcar(logger=logger)
    wbv.chgdata = chgdata
    wbv.ngx_max = ngx
    wbv.ngy_max = ngy
    wbv.ngz_max = ngz
    wbv.poscar_info = poscar_info

    # print(chgdata)
    # print(type(chgdata))
    # print(chgdata.shape)
    # print(type(chgdata[0,0,139]))

    wbv.write_chgcar()
    print("**************** END ************")

SumChgcar = SumChargeDensity  # historical spelling
