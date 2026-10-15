#!/usr/bin/env python
# coding:utf-8
# print(chgdata)
# print(type(chgdata))
# print(chgdata.shape)
# print(type(chgdata[0,0,139]))
# Copyright Kengo NAKADA; SAE class library.
import multiprocessing
import numpy as np


class SumChgcar(object):

    def __init__(self, logger=None):
        from sae.vasp.chgcar import ReadVaspChgcar

        if logger is None:
            logger = multiprocessing.get_logger()
        self.__logger = logger
        name = "CHGCAR_Li_100_200"
        instance = ReadVaspChgcar(CHGCAR=name)
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
            instance = ReadVaspChgcar(CHGCAR=item)
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
