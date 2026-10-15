from sae.errors import legacy_error as _legacy_error

#!/usr/bin/env python
# coding:utf-8
"""
Bader Volumeファイル BvAt*.dat の読み込み
"""
import multiprocessing
import os
import sys

try:
    import StructureAnalysisEnvironment as SAE
except:
    pass  # package imports do not alter sys.path


class VolumeGrid(object):
    def __init__(
        self,
        num,
        BvAt="BvAt",
        suffix=".dat",
        sort=False,
        atoms_index=None,
        logger=None,
        split_chgcar=False,
        POSCAR="POSCAR",
    ):
        """
        BvAt 読み込み。実質的に CHGCAR ファイルを読み込む。

        :param CHGCAR:
        :param suffix:
        :param sort:
        :param atoms_index:
        :param spit_chgcar: True/False, 電荷のファイルと構造情報を別々のファイルから読む
        :param POSCAR: POSCAR 構造情報ファイル名（デフォルト POSCAR)
        """
        if logger is None:
            logger = multiprocessing.get_logger()
        self.__logger = logger

        if split_chgcar:
            # POSCAR 情報を違うファイルから読む(例: header 情報をPOSCARから読んで BvAt の Bader Charge を BvAt から)
            self.split_open(
                num,
                POSCAR=POSCAR,
                BvAt=BvAt,
                suffix=suffix,
                sort=sort,
                atoms_index=atoms_index,
            )
        else:
            # 通常
            self.normal_open(
                num, BvAt=BvAt, suffix=suffix, sort=sort, atoms_index=atoms_index
            )

        # self.open(num, BvAt=BvAt, suffix=suffix, sort=sort, atoms_index=atoms_index)

    def split_open(
        self,
        num,
        POSCAR="POSCAR",
        BvAt="BvAt",
        suffix=None,
        sort=False,
        atoms_index=None,
    ):
        """
        Bader Bug 対応。Bug は BvAt ファイルの構造上が DATA死んでいるので BvAt ファイルをヘッダとフッタにわけてよむ。
        headerは別ファル（POSCAR)などから読む。

        CHGCAR ファイルを読む(ヘッダ情報は別ファイル)

        :param num: 読み込む BvAt ファル番号
        :param BvAt: BvAt ファイルの名前
        :param suffix: BvAt が通常と違う拡張子の時
        :param sort: つかってない
        :param atoms_index:
        :return:
        """
        self.__logger.info("=== split open")
        bvat_num = "{:04}".format(num)
        if suffix is None:
            chg_name = BvAt + bvat_num
        else:
            chg_name = BvAt + bvat_num + suffix

        self.__logger.info("POSCAR: POSCAR = %s" % POSCAR)
        self.__logger.info("BvAt  : BvAt   = %s" % chg_name)
        # self.__chgcar = SAE.io.ReadVaspChgcar(CHGCAR=chg_name, suffix=suffix, sort=sort, atoms_index=atoms_index)

        # Header 部分の取り出し
        header = SAE.io.ReadVaspChgcarHeader(POSCAR)
        header_data = header.get_poscar_info()

        # Footer
        self.__chgcar = SAE.io.ReadVaspChgcarFooter(chg_name, header_data)
        print("END")
        self.__ngy_max = self.__chgcar.ngyz
        self.__ngz_max = self.__chgcar.ngzc

    def normal_open(self, num, BvAt="BvAt", suffix=None, sort=False, atoms_index=None):
        """
        通常のオープン。Bader にバグがないならこれがいい
        CHGCAR ファイルを読む

        :param num: 読み込む BvAt ファル番号
        :param BvAt: BvAt ファイルの名前
        :param suffix:
        :param sort:
        :param atoms_index:
        :return:
        """
        self.__logger.info("=== normal open")
        bvat_num = "{:04}".format(num)
        if suffix is None:
            chg_name = BvAt + bvat_num
        else:
            chg_name = BvAt + bvat_num + suffix

        self.__logger.debug("CHGCAR = %s" % chg_name)
        self.__chgcar = SAE.io.ReadVaspChgcar(
            CHGCAR=chg_name, suffix=suffix, sort=sort, atoms_index=atoms_index
        )
        self.__ngy_max = self.__chgcar.ngyz
        self.__ngz_max = self.__chgcar.ngzc

    def open(
        self,
        num,
        BvAt="BvAt",
        suffix=None,
        sort=False,
        atoms_index=None,
        split_chgcar=False,
    ):
        """
        :param num: 読み込む BvAt ファル番号
        :param BvAt: BvAt ファイルの名前
        :param suffix:
        :param sort:
        :param atoms_index:
        :param split_chgcar: bader program の bug 対応で BvAt から 原子種情報を読まずに別ファイルから読む
        :return:
        """
        if split_chgcar:
            self.split_open(num, BvAt=BvAt, suffix=suffix, sort=False)
        else:
            self.normal_open(num, BvAt=BvAt, suffix=suffix, sort=False)

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


if __name__ == "__main__":
    bader = ReadBaderBvat()


ReadBaderBvat = VolumeGrid  # historical spelling
