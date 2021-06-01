#!/usr/bin/env python
# coding:utf-8
"""
Bader Volume の足し算などを行うサポート Method がまとめられた class
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

    def sum_bader_volume(self, volume_list):
        """
        指定原子の番号のBader Volume を積算する
        1) Volume に対応する *.dat から CHG 情報を取り出す
        2) 原子が複数の Volume 領域を持つときは足し合わせる

        :param volume_list:
        :return:
        """
        self.__logger.debug('')
        self.__logger.debug('=== sum_bader_volumes')
        #print(volume_list)

        if len(volume_list) > 1:
            poscar_info_list = []
            bader_volume_list = []
            for i in volume_list:
                self.__logger.debug("Read Bader volume = %s" % i)
                # BvAtxxx.dat の読み込み
                bvat = SAE.io.ReadBaderBvat(i)
                poscar_info_list.append(bvat.poscar_info)
                bader_volume_list.append(bvat.chgdata)

            self.__logger.debug("sum Bader volume...")
            self.__poscar_info = poscar_info_list[0]
            for i in volume_list:
                try:
                    bader_volume = bader_volume + bader_volume[i]
                except:
                    bader_volume = bader_volume[i]
            self.__bader_volume = bader_volume
        else:
            self.__logger.debug("Read Bader Volume = %s" % volume_list[0])
            bvat = SAE.io.ReadBaderBvat(volume_list[0])
            self.__poscar_info = bvat.poscar_info
            self.__bader_volume = bvat.chgdata

        self.__ngx_max = bvat.ngx_max
        self.__ngy_max = bvat.ngy_max
        self.__ngz_max = bvat.ngz_max
        return self.__bader_volume
