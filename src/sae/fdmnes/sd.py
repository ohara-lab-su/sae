# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import optparse
import numpy as np


class ReadFdmSd(object):

    def __init__(
        self,
        sdname,
        suffix="_sd0.txt",
        inpname=None,
        bavname=None,
        absorber=None,
        weight=None,
        bav=None,
    ):
        """

        :param sdname: Pd_sd0.txt のとき Pd が sdname となる
        :param suffix:
        :param inpname: FDMNES の入力ファイルからいくつかの情報を取り出す
        :param bavname:
        :param absorber:
        :param weight:
        :param bav:
        """
        from sae.fdmnes.bav import ReadFdmBav
        from sae.fdmnes.sd_2016 import ReadFdmSd2016
        from sae.fdmnes.sd_2020 import ReadFdmSd2020

        print("")
        print("get fdmnes version")
        try:
            bav = ReadFdmBav(sdname, "_bav.txt")
            fdm_version = bav.get_fdmnes_ver().strip("")
            print("")
            print("version = %s" % fdm_version)
            year = int(fdm_version.split(" ")[-1])
            print(year)
        except:
            print("*** fail *** get fdmnes version")
            new = True
        else:
            if year > 2016:
                new = True
            else:
                new = False
        if new:
            print("load NEW format: sd2020")
            print("")
            self.__sd = ReadFdmSd2020(
                sdname, suffix, inpname, bavname, absorber, weight
            )
        else:
            print("load OLD format: ~sd2016.01.08")
            print("")
            self.__sd = ReadFdmSd2016(
                sdname, suffix, inpname, bavname, absorber, weight
            )

    def get_pdos(self, l=0, m=0, lm=None, spin=0):
        return self.__sd.get_pdos(l, m, lm, spin)

    def get_ldos(self, l=0, spin=0):
        """LDOS(NEDOS, L, SPIN"""
        return self.__sd.get_ldos(l, spin)

    def get_intldos(self, l=0, spin=0):
        """INTLDOS(NEDOS,L,SPIN)"""
        return self.__sd.get_intldos(l, spin)

    def get_tdos(self, spin=0):
        """TDOS(NEDOS, SPIN)"""
        self.__sd.get_tdos(spin)

    def get_inttdos(self, spin=0):
        """INTTDOS(NEDOS, SPIN)"""
        return self.__sd.get_inttdos(spin)

    def get_eng(self):
        return self.__sd.eng

    @property
    def eng(self):
        return self.__sd.eng

    def get_emin(self):
        return self.__sd.emin

    @property
    def emin(self):
        return self.__sd.emin

    def get_emax(self):
        return self.__sd.emax

    @property
    def emax(self):
        return self.__sd.emax

    def get_ymax(self):
        return self.__sd.ymax

    @property
    def ymax(self):
        return self.__sd.ymax

    def get_header(self):
        return self.__sd.header

    @property
    def header(self):
        return self.__sd.header

    def get_num(self):
        """読み込んだ sd ファイルの行数"""
        return self.__sd.num

    @property
    def num(self):
        return self.__sd.num

    def get_sd(self):
        """読み込んだ sd ファイル丸ごと(平均化したら、平均化した値)"""
        return self.__sd.sd

    def get_lmax(self):
        """読み込んだ sd ファイルに基づいて lmax を抽出"""
        return self.__sd.lmax

    @property
    def lmax(self):
        return self.__sd.lmax

    def get_mmax(self):
        return self.__sd.mmax

    @property
    def mmax(self):
        return self.__sd.mmax

    def get_ispin(self):
        return self.__sd.ispin

    @property
    def ispin(self):
        return self.__sd.ispin
