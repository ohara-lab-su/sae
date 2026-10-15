#!/usr/bin/env python
# coding:utf-8
"""
Bader Volume の足し算などを行うサポート Method がまとめられた class

*****
体積足し合わせの基本ルーチンはこれ
  sum_bader_volume(self, volume_list)
*****
"""
import multiprocessing
import StructureAnalysisEnvironment as SAE


class UtilBader(object):
    def __init__(self, logger=None):
        if logger is None:
            logger = multiprocessing.get_logger()
        self.__logger = logger

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

    # @property
    # def chgdata(self):
    #     return self.__chgdata

    # @chgdata.setter
    # def chgdata(self, val):
    #     self.__chgdata = val

    @property
    def bader_volume(self):
        return self.__bader_volume

    @bader_volume.setter
    def bader_volume(self, val):
        self.__bader_volume = val

    @property
    def poscar_info(self):
        return self.__poscar_info

    @poscar_info.setter
    def poscar_info(self, val):
        self.__poscar_info = val

    #
    # Method
    #
    def sum_bader_volume(self, volume_list, split_chgcar=False):
        """
        指定原子の番号のBader Volume を積算する
        1) Volume に対応する *.dat から CHG 情報を取り出す
        2) 原子が複数の Volume 領域を持つときは足し合わせる

        :param volume_list:
        :param split_chgcar: POSCAR 情報法を別々のファイルから読み込む(Bader バグ対応)
        :return:
        """
        self.__logger.debug('')
        self.__logger.debug('=== sum_bader_volumes')
        # print(volume_list)

        # volume が複数あるとき
        if len(volume_list) > 1:
            poscar_info_data = []
            bader_volume_data = []

            # BvAtxxx.dat の読み込み
            for i in volume_list:
                self.__logger.debug("")
                self.__logger.debug("=== Read Bader volume = %s" % i)
                self.__logger.debug("")

                # Bader にバグがあるときは BvAt ファイルの構造情報などにバグが出てくるので
                # POSCAR 上を別ファイルから読んで構造情報とFFTmesh上などを別々に読む必要がある。
                if split_chgcar:
                    bvat = SAE.io.ReadBaderBvat(i, split_chgcar=True)
                else:
                    bvat = SAE.io.ReadBaderBvat(i)

                poscar_info_data.append(bvat.poscar_info)
                bader_volume_data.append(bvat.chgdata)

            # BvAtxxx.dat の足し合わせ
            self.__logger.debug("=== sum Bader volume...")
            self.__poscar_info = poscar_info_data[0]
            j = 0
            for i in volume_list:
                try:
                    bader_volume = bader_volume + bader_volume_data[j]
                except:
                    bader_volume = bader_volume_data[j]
                j += 1
            self.__bader_volume = bader_volume
        else:
            self.__logger.debug("Read Bader Volume = %s" % volume_list[0])

            if split_chgcar:
                bvat = SAE.io.ReadBaderBvat(volume_list[0], split_chgcar=True)
            else:
                bvat = SAE.io.ReadBaderBvat(volume_list[0])

            self.__poscar_info = bvat.poscar_info
            self.__bader_volume = bvat.chgdata

        self.__ngx_max = bvat.ngx_max
        self.__ngy_max = bvat.ngy_max
        self.__ngz_max = bvat.ngz_max
        return self.__bader_volume
