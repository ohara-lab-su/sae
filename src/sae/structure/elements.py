# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#
# 入力した原子種の通し番号の下限と上限を返す
# 入力する原子種の種別番号は 1 からスタート
#
# 一応VASP(POSCAR) 用だが、ion[j] のフォーマットが共通ならば全てのプログラムで使える
#
# [in]     atom1   : 原子種の種別番号（POSCAR の種別番号: 1から始まる--> サイト番号)
# [in]     nion    : 原子の種類数
#
# [in/out] atoms[i]: 原子の種類番号(max=nion)を与えると、その原子種の数を返す
#
# [return] start
# [return] end
#
################################################################################
################################################################################
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
# import SpaceGroupEnvironment as SGE
#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 原子番号もしくは元素記号を渡すと原子量を返すルーチン
#
# atomic_weight.list ファイルが必要
#
################################################################################
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#  なにげにpython2依存が酷かった(重複呼び出しを削除)
#
# 2015.02.21 (sun)
#   startup
#   get_atomic_radius.py をベース(ほとんどそのまま)
#
################################################################################
# import SpaceGroupEnvironment as SGE
### 原子番号から原子量を返す
### 元素記号から原子量を返す
#############################
#
# get_atomic_radious 中のルーチンとオーバーラップするので削除する方が良い
#
#### 元素記号から原子番号を返す
## def get_atomic_number1(atom):
##
##     name='atomic_radius.list'
##    #libpath = re.sub('__init__.pyc','',SAE.__file__)
##     libpath = re.sub('__init__.py','',SAE.__file__)
##     if os.path.exists(libpath):
##         name=libpath+name
##         if not os.path.exists(name):
##             name0='atomic_radius.list.py'
##             name=libpath+name0
##     else:
##         for libpath in os.getenv('PYTHONPATH').split(':'):
##             name=libpath+'/'+name
##             if os.path.exists(name):
##                 break
##
##     nlist = SAE.read_list_param(name)
##
##     radius_list = np.zeros((nlist,3),dtype='S4')
##     nlist = SAE.read_list3(name,radius_list)
##
##    for i in range(nlist):
##        if atom == radius_list[i,1]:
##            num=float(radius_list[i,0])
##
##    return num
################################################################################
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
from numpy import *
import numpy as np
import sae as SAE


class ElementTable:

    def get_atom_start(self, atom1, nion, atoms):
        atom1_0 = atom1 - 1
        k = 0
        for i in range(nion):
            if atom1 < 1:
                sys.exit("STOP: unknown number, atom1 = " + str(atom1))
            if i == atom1_0:
                start = k
                end = k + int(atoms[i]) - 1
            k = k + int(atoms[i])
        #   print "==="
        #   print "k_start", start
        #   print "k_end",   end
        #   print "k_last", k
        return [start, end]

    def get_atomic_radius0(self, num):
        """
        原子番号から原子半径を返す
        :param num:
        :return:
        """
        from sae.common.text import TextFiles

        base = "atomic_radius.list"
        base_py = "atomic_radius.list.py"
        ldir = os.path.dirname(SAE.__file__)
        name = ldir + "/" + base
        if not os.path.exists(name):
            name = ldir + "/" + base_py
            if not os.path.exists(name):
                sys.exit("STOP: %s or %s file not found." % (base, base_py))
        nlist = TextFiles().read_list_param(name)
        # commented out 2020.06.23
        # ldir = os.path.dirname(SAE.__file__)
        # if not os.path.exists(name):
        #     if os.path.exists(ldir + '/' + name):
        #         name = ldir + '/' + name
        #     else:
        #         name = 'atomic_radius.list.py'
        #         if not os.path.exists(name):
        #             sys.exit("STOP: " + name + " file not found")
        # pre read
        radius_list = np.zeros((nlist, 3), dtype="S4")
        nlist = TextFiles().read_list3(name, radius_list)
        for i in range(nlist):
            if num == radius_list[i, 0]:
                radius = float(radius_list[i, 2])
        return radius

    def get_atomic_radius1(self, atom):
        """
        元素記号(str)から原子半径(float)を返す
        :param atom:
        :return:
        """
        from sae.common.text import TextFiles

        base = "atomic_radius.list"
        base_py = "atomic_radius.list.py"
        ldir = os.path.dirname(SAE.__file__)
        name = ldir + "/" + base
        if not os.path.exists(name):
            name = ldir + "/" + base_py
            if not os.path.exists(name):
                sys.exit("STOP: %s or %s file not found." % (base, base_py))
        nlist = TextFiles().read_list_param(name)
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
        # pre read
        radius_list = np.zeros((nlist, 3), dtype="S4")
        nlist = TextFiles().read_list3(name, radius_list)
        for i in range(nlist):
            try:
                # for Python3
                atom_name = radius_list[i, 1].decode()
            except:
                atom_name = radius_list[i, 1]
            if atom == atom_name:
                radius = float(radius_list[i, 2])
        return radius

    def get_atomic_number1(self, atom):
        """
        元素記号(str)から原子番号(float)を返す
        :param atom:
        :return:
        """
        from sae.common.text import TextFiles

        base = "atomic_radius.list"
        base_py = "atomic_radius.list.py"
        ldir = os.path.dirname(SAE.__file__)
        name = ldir + "/" + base
        if not os.path.exists(name):
            name = ldir + "/" + base_py
            if not os.path.exists(name):
                sys.exit("STOP: %s or %s file not found." % (base, base_py))
        nlist = TextFiles().read_list_param(name)
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
        # pre read
        radius_list = np.zeros((nlist, 3), dtype="S4")
        nlist = TextFiles().read_list3(name, radius_list)
        for i in range(nlist):
            try:
                # for Python3
                atom_name = radius_list[i, 1].decode()
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

    def get_atomic_symbol0(self, num):
        """
        原子番号から元素記号を返す
        :param num:
        :return:
        """
        from sae.common.text import TextFiles

        # new out 2020.06.23
        base = "atomic_radius.list"
        base_py = "atomic_radius.list.py"
        ldir = os.path.dirname(SAE.__file__)
        name = ldir + "/" + base
        if not os.path.exists(name):
            name = ldir + "/" + base_py
            if not os.path.exists(name):
                sys.exit("STOP: %s or %s file not found." % (base, base_py))
        nlist = TextFiles().read_list_param(name)
        # pre read
        radius_list = np.zeros((nlist, 3), dtype="S4")
        nlist = TextFiles().read_list3(name, radius_list)
        symbol = ""
        for i in range(nlist):
            # new routine (with decode) 2020.06.23
            # symbol = str(radius_list[i, 1])
            if num == int(radius_list[i, 0]):
                try:
                    symbol = radius_list[i, 1].decode("ascii")
                except:
                    symbol = radius_list[i, 1]
        return symbol

    def get_atomic_weight0(self, num):
        from sae.common.text import TextFiles

        name = "atomic_weight.list"
        # libpath = re.sub('__init__.pyc','',SAE.__file__) # for Python2
        libpath = re.sub("__init__.py", "", SAE.__file__)
        if os.path.exists(libpath):
            name = libpath + name
            if not os.path.exists(name):
                name0 = "atomic_weight.list.py"
                name = libpath + name0
        else:
            for libpath in os.getenv("PYTHONPATH").split(":"):
                name = libpath + "/" + name
                if os.path.exists(name):
                    break
        nlist = TextFiles().read_list_param(name)
        radius_list = np.zeros((nlist, 3), dtype="S4")
        nlist = TextFiles().read_list3(name, radius_list)
        for i in range(nlist):
            if num == radius_list[i, 0]:
                weight = float(radius_list[i, 2])
        return weight

    def get_atomic_weight1(self, atom):
        from sae.common.text import TextFiles

        name = "atomic_weight.list"
        # libpath = re.sub('__init__.pyc','',SAE.__file__)
        libpath = re.sub("__init__.py", "", SAE.__file__)
        if os.path.exists(libpath):
            name = libpath + name
            if not os.path.exists(name):
                name0 = "atomic_weight.list.py"
                name = libpath + name0
        else:
            for libpath in os.getenv("PYTHONPATH").split(":"):
                name = libpath + "/" + name
                if os.path.exists(name):
                    break
        nlist = TextFiles().read_list_param(name)
        radius_list = np.zeros((nlist, 3), dtype="S4")
        nlist = TextFiles().read_list3(name, radius_list)
        for i in range(nlist):
            if atom == radius_list[i, 1] or atom == radius_list[i, 1].decode("ascii"):
                weight = float(radius_list[i, 2])
        return weight
