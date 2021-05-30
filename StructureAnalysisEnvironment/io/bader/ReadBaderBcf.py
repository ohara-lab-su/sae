#!/usr/bin/env python
# coding:utf-8
"""
Bader BCF.dat
"""
import multiprocessing
import math
import numpy as np
import pandas as pd

import StructureAnalysisEnvironment as SAE


class ReadBaderBcf(object):
    def __init__(self, name='BCF.dat', logger=None):
        if logger is None:
            logger = multiprocessing.get_logger()
        self.__logger = logger

        if name is not None:
            self.open(name)

        self.__ngx_max = 150
        self.__ngy_max = 150
        self.__ngz_max = 150

    def open(self, name):
        # df = pd.read_csv(name, sep='\s+')
        self.__df = pd.read_csv(name, skiprows=[1,1], skipfooter=1, delim_whitespace=True, engine='python')

    def search_atomic_volume_num(self, atom):
        """
        :param atom: 検索する原子の番号(POSCARの順番)
        :return volumes_n: atom の所属する bader-bolume 番号（複数有り)
        """
        # print(self.__df.head(3))
        self.__logger.debug("=== search_atomic_volume(%s)" % atom)

        # DF は numpy.float64 で入ってしまうので、atom番号を INT にする
        self.__df['ATOM'] = self.__df['ATOM'].astype(int)
        volumes_n = []

        total_n = len(self.__df['ATOM'])
        for i in range(total_n):
            # 入力した atom 番号の BaderVolume 番号を探す（複数ある場合がある)
            if np.isclose(self.__df['ATOM'][i], int(atom)):
                self.__logger.debug("--> #%s, atom: %s=%s" % (self.__df['#'][i], self.__df['ATOM'][i], atom))
                volumes_n.append(self.__df["#"][i])

        return volumes_n

    def test(self):
        print(self.__df['ATOM'])
        print(self.__df.shape)
        print(self.__df.dtypes)
        print("index  = %s" % self.__df.index)
        print("column = %s" % self.__df.columns)
        print(self.__df.head(3))
        #for a in self.__df['ATOM'][1]:
        #    print(a)


if __name__ == '__main__':

    logger = SAE.util.logger.Logger(loglevel='info')
    atom = 1

    # Bader Volume の調査
    logger.debug('=== get_bader_volume(%s)' % atom)
    bcf = ReadBaderBcf()
    volume_list = bcf.search_atomic_volume_num(atom)
    print(volume_list)

    # # Bader Volume の足し合わせ
    # util = SAE.io.UtilBader()
    # util.sum_bader_volume(volume_list)

    # # Bader Volume の書き出し
    # wbv = SAE.io.WriteBaderVolume()
    # wbv.chgdata = util.bader_volume
    # wbv.poscar_info = util.poscar_info
    # wbv.write_bader_volume('CHGCAR_BvA_%s' % atom)
