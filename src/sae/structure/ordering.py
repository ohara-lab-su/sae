#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# atoms_index_j を与えられたらその内容をグルーピングして
#
#  1) atoms および atoms_index を作成
#  2) グルーピング前の atoms_index_j と グルーピング後の atoms_index
#     の対応 index 情報を作る
#
#     sort_index   : sort_index --> original_index
#     sort_index_r : original_index --> sort_index
#
#  データー構造の特性上、計算コードを問わない
#
################################################################################
#
# 2015.08.20
#  startup
#
################################################################################
################################################################################
# import copy
################################################################################
# 無秩序に並んだ atoms_index_j とそれに対応する position があるとき
# atoms_index, atoms を作成し、その秩序に合わせて position をソート
# するための汎用ルーチンの作成
#
#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# atoms_number_j を与えられたらその内容をグルーピングして
#
#  1) atoms および atoms_number, atoms_index を作成
#  2) グルーピング前の atoms_number_j と グルーピング後の atoms_number
#     の対応 index 情報を作る
#
#     sort_index   : sort_index --> original_index
#     sort_index_r : original_index --> sort_index
#
#  データー構造の特性上、計算コードを問わない
#
################################################################################
#
# 2015.08.20
#  startup
#
################################################################################
################################################################################
# import copy
################################################################################
#
#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# fix,sort_index_r を与えられたらその内容にしたがって fix をソートする
#
#  データー構造の特性上、計算コードを問わない
#
# sort_position との違いはデータータイプの違いだけ
#
################################################################################
#
# 2015.08.20
#  startup
#
################################################################################
################################################################################
# import copy
# import collections
#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# position,sort_index_r を与えられたらその内容にしたがって position をソートする
#
#  データー構造の特性上、計算コードを問わない
#
################################################################################
#
# 2015.08.20
#  startup
#
################################################################################
################################################################################
# import copy
# import collections
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import numpy as np
import collections


class AtomOrdering:

    def sort_atom_index_j(self, atoms_index_j):
        #   # atoms_index_j のソート (この方式は使わない、お蔵行き)
        #   atoms_index_j = copy.copy(atoms_index_j)
        #   atoms_index_js = copy.copy(atoms_index_j)
        #   atoms_index_js.sort(key=lambda x:x[0])
        natom = len(atoms_index_j)
        # ION 数および atoms, atoms_index の作成
        counter = collections.Counter(atoms_index_j)
        nion = len(counter)
        atoms = np.zeros(nion, dtype=int)
        atoms_index = []
        i = 0
        for atom, cnt in counter.most_common():
            atoms_index.append(atom)
            atoms[i] = cnt
            i += 1
        # ソート用のindexの作成
        # sort_index --> original_index
        sort_index = np.zeros(natom, dtype=int)
        # original_index --> sort_index
        sort_index_r = np.zeros(natom, dtype=int)
        for i in range(natom):
            # sort+index
            index = 0
            for k in range(nion):
                # original_index
                for j in range(natom):
                    if atoms_index[k] == atoms_index_j[j]:
                        sort_index[index] = j
                        sort_index_r[j] = index
                        index += 1
        #   print sort_index
        #   print sort_index_r
        #   position_s = np.zeros((natom,3))
        #   for original in range(natom):
        #       sort = sort_index_r[original]
        #       position_s[sort,:] = position[original,:]
        atoms_index_js = [""] * natom
        for original in range(natom):
            sort = sort_index_r[original]
            atoms_index_js[sort] = atoms_index_j[original]
        #   print atoms_index_js
        return (sort_index, sort_index_r, atoms, atoms_index, atoms_index_js)

    def sort_atom_number_j(self, atoms_number_j):
        from sae.structure.elements import ElementTable

        natom = len(atoms_number_j)
        # ION 数および atoms, atoms_index の作成
        counter = collections.Counter(atoms_number_j)
        nion = len(counter)
        atoms = np.zeros(nion, dtype=int)
        atoms_index = []
        atoms_number = np.zeros(nion, dtype=int)
        i = 0
        for number, cnt in counter.most_common():
            atoms_index.append(ElementTable().get_atomic_symbol0(int(number)))
            atoms_number[i] = int(number)
            atoms[i] = cnt
            i += 1
        # ソート用のindexの作成
        # sort_index --> original_index
        sort_index = np.zeros(natom, dtype=int)
        # original_index --> sort_index
        sort_index_r = np.zeros(natom, dtype=int)
        for i in range(natom):
            # sort+index
            index = 0
            for k in range(nion):
                # original_index
                for j in range(natom):
                    if atoms_number[k] == atoms_number_j[j]:
                        sort_index[index] = j
                        sort_index_r[j] = index
                        index += 1
        #   print sort_index
        #   print sort_index_r
        #   position_s = np.zeros((natom,3))
        #   for original in range(natom):
        #       sort = sort_index_r[original]
        #       position_s[sort,:] = position[original,:]
        atoms_number_js = np.zeros(natom, dtype=float)
        for original in range(natom):
            sort = sort_index_r[original]
            atoms_number_js[sort] = atoms_number_j[original]
        #   print atoms_index_js
        return (sort_index, sort_index_r, atoms, atoms_index, atoms_number_j)

    def sort_fix(self, sort_index_r, fix):
        natom = len(fix)
        fix_s = np.zeros((natom, 3), dtype="S")
        for original in range(natom):
            sort = sort_index_r[original]
            fix_s[sort, :] = fix[original, :]
        return fix_s

    def sort_position(self, sort_index_r, position):
        natom = len(position)
        position_s = np.zeros((natom, 3))
        for original in range(natom):
            sort = sort_index_r[original]
            position_s[sort, :] = position[original, :]
        return position_s
