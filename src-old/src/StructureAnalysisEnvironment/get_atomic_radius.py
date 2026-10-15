# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 原子番号もしくは元素記号を渡すと原子半径を返すルーチン等
# (いささかルーチン全体の基本センスが古いので扱いにくい)
#
# カレントに atomic_radius.list ファイルが必要
#
################################################################################
from __future__ import print_function

try:
    from .copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################
#
# 2018.08.16
#  Python2/3 両対応(主にファイル読み子関係なので注意)
#
# 2015.05.19
#  原子番号から元素記号を返すルーチンを追加
#
# 2015.02.16
#  import の名前空間を変更
#
################################################################################

import sys
import os

import numpy as np
import StructureAnalysisEnvironment as SAE


# import SpaceGroupEnvironment as SGE


def get_atomic_radius0(num):
    """
    原子番号から原子半径を返す
    :param num:
    :return:
    """
    base = 'atomic_radius.list'
    base_py = 'atomic_radius.list.py'

    ldir = os.path.dirname(SAE.__file__)
    name = ldir + '/' + base

    if not os.path.exists(name):
        name = ldir + '/' + base_py
        if not os.path.exists(name):
            sys.exit("STOP: %s or %s file not found." % (base, base_py))

    # commented out 2020.06.23
    # ldir = os.path.dirname(SAE.__file__)
    # if not os.path.exists(name):
    #     if os.path.exists(ldir + '/' + name):
    #         name = ldir + '/' + name
    #     else:
    #         name = 'atomic_radius.list.py'
    #         if not os.path.exists(name):
    #             sys.exit("STOP: " + name + " file not found")

    nlist = SAE.read_list_param(name)  # pre read

    radius_list = np.zeros((nlist, 3), dtype='S4')
    nlist = SAE.read_list3(name, radius_list)

    for i in range(nlist):
        if num == radius_list[i, 0]:
            radius = float(radius_list[i, 2])

    return radius


def get_atomic_radius1(atom):
    """
    元素記号(str)から原子半径(float)を返す
    :param atom:
    :return:
    """
    base = 'atomic_radius.list'
    base_py = 'atomic_radius.list.py'

    ldir = os.path.dirname(SAE.__file__)
    name = ldir + '/' + base

    if not os.path.exists(name):
        name = ldir + '/' + base_py
        if not os.path.exists(name):
            sys.exit("STOP: %s or %s file not found." % (base, base_py))

    # commented out 2020.06.23
    # ldir = os.path.dirname(SAE.__file__)
    # if not os.path.exists(name):
    #     if os.path.exists(ldir + '/' + name):
    #         name = ldir + '/' + name
    #     else:
    #         name = 'atomic_radius.list.py'
    #         if not os.path.exists(name):
    #             if os.path.exists(ldir + '/' + name):
    #                 name = ldir + '/' + name
    #             else:
    #                 sys.exit("STOP: " + name + " file not found")

    nlist = SAE.read_list_param(name)  # pre read

    radius_list = np.zeros((nlist, 3), dtype='S4')
    nlist = SAE.read_list3(name, radius_list)

    for i in range(nlist):
        try:
            atom_name = radius_list[i, 1].decode()  # for Python3
        except:
            atom_name = radius_list[i, 1]

        if atom == atom_name:
            radius = float(radius_list[i, 2])

    return radius


def get_atomic_number1(atom):
    """
    元素記号(str)から原子番号(float)を返す
    :param atom:
    :return:
    """
    base = 'atomic_radius.list'
    base_py = 'atomic_radius.list.py'

    ldir = os.path.dirname(SAE.__file__)
    name = ldir + '/' + base

    if not os.path.exists(name):
        name = ldir + '/' + base_py
        if not os.path.exists(name):
            sys.exit("STOP: %s or %s file not found." % (base, base_py))

    # commented out 2020.06.23
    # ldir = os.path.dirname(SAE.__file__)
    # if not os.path.exists(name):
    #     if os.path.exists(ldir + '/' + name):
    #         name = ldir + '/' + name
    #     else:
    #         name = 'atomic_radius.list.py'
    #         if not os.path.exists(name):
    #             if os.path.exists(ldir + '/' + name):
    #                 name = ldir + '/' + name
    #             else:
    #                 sys.exit("STOP: " + name + " file not found")

    # ファイルの全行数を確保
    nlist = SAE.read_list_param(name)  # pre read

    radius_list = np.zeros((nlist, 3), dtype='S4')
    nlist = SAE.read_list3(name, radius_list)

    for i in range(nlist):
        try:
            atom_name = radius_list[i, 1].decode()  # for Python3
        except:
            atom_name = radius_list[i, 1]

        if atom == atom_name:
            num = float(radius_list[i, 0])

        # modified 2020.06.23
        # try:
        #     if atom.decode() == atom_name:
        #         num = float(radius_list[i, 0])
        # except:
        #     if atom == atom_name:
        #         num = float(radius_list[i, 0])

    return num


def get_atomic_symbol0(num):
    """
    原子番号から元素記号を返す
    :param num:
    :return:
    """
    # new out 2020.06.23
    base = 'atomic_radius.list'
    base_py = 'atomic_radius.list.py'

    ldir = os.path.dirname(SAE.__file__)
    name = ldir + '/' + base

    if not os.path.exists(name):
        name = ldir + '/' + base_py
        if not os.path.exists(name):
            sys.exit("STOP: %s or %s file not found." % (base, base_py))

    nlist = SAE.read_list_param(name)  # pre read

    radius_list = np.zeros((nlist, 3), dtype='S4')
    nlist = SAE.read_list3(name, radius_list)

    symbol = ''
    for i in range(nlist):
        if num == int(radius_list[i, 0]):
            # new routine (with decode) 2020.06.23
            # symbol = str(radius_list[i, 1])
            try:
                symbol = radius_list[i, 1].decode('ascii')
            except:
                symbol = radius_list[i, 1]

    return symbol
