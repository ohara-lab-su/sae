# Copyright Kengo NAKADA; SAE class library.
"""
Bader BCF.dat

原子の番号から Bader Volume 番号を取り出すなど (AVF.dat の情報とconsistentなはず)
"""

import multiprocessing
import math
import numpy as np
import pandas as pd


class ReadBaderBcf(object):

    def __init__(self, name="BCF.dat", logger=None):
        if logger is None:
            logger = multiprocessing.get_logger()
        self.__logger = logger
        if name is not None:
            self.open(name)
        self.__ngx_max = 150
        self.__ngy_max = 150
        self.__ngz_max = 150

    def open(self, name="BCF.dat"):
        self.__df = pd.read_csv(
            name, skiprows=[1, 1], skipfooter=1, delim_whitespace=True, engine="python"
        )

    def get_distance(self, atom):
        """
        BCF にて、atom 番号を指定して、distance を取り出す。
        :param atom: 引き出したい atom の番号
        :return:
        """
        self.__logger.debug("")
        self.__df["ATOM"] = self.__df["ATOM"].astype(int)
        distance = None
        charge = None
        index_n = len(self.__df["ATOM"])
        for i in range(index_n):
            bader_atom = self.__df["ATOM"][i]
            if np.isclose(bader_atom, int(atom)):
                distance = self.__df["DISTANCE"][i]
                charge = self.__df["CHARGE"][i]
                volume_num = self.__df["#"][i]
                self.__logger.info(
                    "-->volume#=%s, atom=%s, charge=%s, distance=%s"
                    % (volume_num, bader_atom, charge, distance)
                )
        return distance

    def get_charge(self, atom):
        """
        BCF にて、atom 番号を指定して、charge を取り出す。
        :param atom: 引き出したい atom の番号
        :return:
        """
        self.__logger.debug("")
        self.__df["ATOM"] = self.__df["ATOM"].astype(int)
        distance = None
        charge = None
        index_n = len(self.__df["ATOM"])
        for i in range(index_n):
            bader_atom = self.__df["ATOM"][i]
            if np.isclose(bader_atom, int(atom)):
                distance = self.__df["DISTANCE"][i]
                charge = self.__df["CHARGE"][i]
                volume_num = self.__df["#"][i]
                self.__logger.info(
                    "-->volume#=%s, atom=%s, charge=%s, distance=%s"
                    % (volume_num, bader_atom, charge, distance)
                )
        return charge

    def search_atomic_volume_num(self, atom):
        """
        [注意]
        -p all_bader オプションで BvAtxxx.dat ファイルが Bader Volume を示しているときに意味がある

        :param atom: 検索する原子の番号(POSCARの順番)
        :return volumes_n: atom の所属する bader-bolume 番号（複数有り)
        """
        self.__logger.debug("=== search_atomic_volume(%s)" % atom)
        self.__df["ATOM"] = self.__df["ATOM"].astype(int)
        volumes_n = []
        total_n = len(self.__df["ATOM"])
        for i in range(total_n):
            if np.isclose(self.__df["ATOM"][i], int(atom)):
                self.__logger.debug(
                    "--> #%s, atom: %s=%s"
                    % (self.__df["#"][i], self.__df["ATOM"][i], atom)
                )
                volumes_n.append(self.__df["#"][i])
        return volumes_n

    def test(self):
        print(self.__df["ATOM"])
        print(self.__df.shape)
        print(self.__df.dtypes)
        print("index  = %s" % self.__df.index)
        print("column = %s" % self.__df.columns)
        print(self.__df.head(3))
