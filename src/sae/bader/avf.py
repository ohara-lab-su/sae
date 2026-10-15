#!/usr/bin/env python
# coding:utf-8
# Bader Volume の調査
# Copyright Kengo NAKADA; SAE class library.
"""
Bader AVF.dat
"""

import multiprocessing
import math
import numpy as np
import pandas as pd


class ReadBaderAvf(object):

    def __init__(self, name="AVF.dat", logger=None):
        if logger is None:
            logger = multiprocessing.get_logger()
        self.__logger = logger
        if name is not None:
            self.open(name)

    # 最初の二行を消して、index を自分で作る
    # Atom を index にする
    # Atom 列（ ... の文字）となるを消す
    # self.__df = self.__df.drop('arrow', axis=1)
    # print('****')
    # print(self.__df.at[2, 'Volume(s)'])
    # print('****')
    def open(self, name="AVF.dat"):
        """
         Atom                     Volume(s)
        ------------------------------------------------------------------------
           1   ...     214
           2   ...     217

        :param name:
        :return:
        """
        # 読み込みskip行
        # 読み込む列の指定
        # 行の読み込みを消したので手動で加える
        # 最後に読まない行
        self.__df = pd.read_csv(
            name,
            header=None,
            skiprows=2,
            usecols=[0, 2],
            names=["Atom", "Volume(s)"],
            skipfooter=1,
            delim_whitespace=True,
            engine="python",
        )
        self.__df = self.__df.set_index("Atom")
        print(self.__df)

    def search_atomic_volume_num(self, atom):
        """
        :param atom: 検索する原子の番号(POSCARの順番)
        :return volumes_n: atom の所属する bader-bolume 番号（複数有り)
        """
        self.__logger.debug("=== search_atomic_volume(atom=%s)" % atom)
        return self.__df.at[atom, "Volume(s)"]
