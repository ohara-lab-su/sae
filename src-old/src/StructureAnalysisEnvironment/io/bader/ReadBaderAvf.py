#!/usr/bin/env python
# coding:utf-8
"""
Bader AVF.dat
"""
import multiprocessing
import math
import numpy as np
import pandas as pd

import StructureAnalysisEnvironment as SAE


class ReadBaderAvf(object):
    def __init__(self, name='AVF.dat', logger=None):
        if logger is None:
            logger = multiprocessing.get_logger()
        self.__logger = logger

        if name is not None:
            self.open(name)

    def open(self, name='AVF.dat'):
        """
         Atom                     Volume(s)
        ------------------------------------------------------------------------
           1   ...     214
           2   ...     217

        :param name:
        :return:
        """
        # 最初の二行を消して、index を自分で作る
        self.__df = pd.read_csv(name,
                                header=None,
                                skiprows=2,  # 読み込みskip行
                                usecols=[0, 2],  # 読み込む列の指定
                                names=['Atom', 'Volume(s)'],  # 行の読み込みを消したので手動で加える
                                skipfooter=1,   # 最後に読まない行
                                delim_whitespace=True, engine='python')

        # Atom を index にする
        self.__df = self.__df.set_index('Atom')
        # Atom 列（ ... の文字）となるを消す
        # self.__df = self.__df.drop('arrow', axis=1)

        # print('****')
        # print(self.__df.at[2, 'Volume(s)'])
        # print('****')
        print(self.__df)

    def search_atomic_volume_num(self, atom):
        """
        :param atom: 検索する原子の番号(POSCARの順番)
        :return volumes_n: atom の所属する bader-bolume 番号（複数有り)
        """
        self.__logger.debug("=== search_atomic_volume(atom=%s)" % atom)
        return self.__df.at[atom, 'Volume(s)']


if __name__ == '__main__':

    logger = SAE.util.logger.Logger(loglevel='info')
    atom = 1

    # Bader Volume の調査
    bcf = ReadBaderAvf(logger=logger)
    volume = bcf.search_atomic_volume_num(1)
    print(volume)
