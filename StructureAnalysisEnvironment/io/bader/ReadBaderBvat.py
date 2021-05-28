#!/usr/bin/env python
# coding:utf-8
"""
Bader Volumeファイル BvAt*.dat の読み込み
"""
import os
import sys

try:
    import StructureAnalysisEnvironment as SAE
except:
    sys.path.append(os.path.join(os.path.dirname(__file__), '../vasp'))


class ReadBaderBvat(object):
    def __init__(self, num, BvAt='BvAt', suffix=".dat", sort=False, atoms_index=None):
        """
        :param CHGCAR:
        :param suffix:
        :param sort:
        :param atoms_index:
        """
        self.open(num, BvAt=BvAt, suffix=suffix, sort=sort, atoms_index=atoms_index)

    def open(self, num, BvAt='BvAt', suffix=None, sort=False, atoms_index=None):
        """
        :param num:
        :param BvAt:
        :param suffix:
        :param sort:
        :param atoms_index:
        :return:
        """
        bvat_num = "{:04}".format(num)
        if suffix is None:
            chg_name = BvAt + bvat_num
        else:
            chg_name = BvAt + bvat_num + suffix

        print("CHGCAR = %s" % chg_name)
        self.__chgcar = SAE.io.ReadVaspChgcar(CHGCAR=chg_name, suffix=suffix, sort=sort, atoms_index=atoms_index)
        self.__ngy_max = self.__chgcar.ngyz
        self.__ngz_max = self.__chgcar.ngzc

    @property
    def chgdata(self):
        return self.__chgcar.chgdata

    @property
    def poscar_info(self):
        return self.__chgcar.poscar_info

    @property
    def ngx_max(self):
        return self.__chgcar.ngxc

    @property
    def ngy_max(self):
        return self.__chgcar.ngyz

    @property
    def ngz_max(self):
        return self.__chgcar.ngzc
