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
        radius_list = np.zeros((nlist, 3), dtype="S4")
        nlist = TextFiles().read_list3(name, radius_list)
        for i in range(nlist):
            try:
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
        radius_list = np.zeros((nlist, 3), dtype="S4")
        nlist = TextFiles().read_list3(name, radius_list)
        for i in range(nlist):
            try:
                atom_name = radius_list[i, 1].decode()
            except:
                atom_name = radius_list[i, 1]
            if atom == atom_name:
                num = float(radius_list[i, 0])
        return num

    def get_atomic_symbol0(self, num):
        """
        原子番号から元素記号を返す
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
        radius_list = np.zeros((nlist, 3), dtype="S4")
        nlist = TextFiles().read_list3(name, radius_list)
        symbol = ""
        for i in range(nlist):
            if num == int(radius_list[i, 0]):
                try:
                    symbol = radius_list[i, 1].decode("ascii")
                except:
                    symbol = radius_list[i, 1]
        return symbol

    def get_atomic_weight0(self, num):
        from sae.common.text import TextFiles

        name = "atomic_weight.list"
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
