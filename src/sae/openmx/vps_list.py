#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# read_list.py の class 化 (および openmx の vps データに特化)
#  *) 引数で配列を返す仕様
#
# 4列のリストをひたすら split して配列に読み込むだけのアホ仕様
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.02.10 1st
#
################################################################################
################################################################################
# import numpy as np
# from copy import deepcopy
################################################################################
################################################################################
# VPS 及び PAO のパス設定
# VPSLIST のファイル場所確認
# vps and pao 情報リスト読み込み(OpenMX非公式ファイル)
# cutoff 名から英数文字のみ取り出す
#   nlist,list_data = vpsdata.get_list()
#   print nlist
#   for i in range(nlist):
#       print list_data[i]
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re


################################################
# リストを読み込む
# read_list.py とほぼ同等機能
################################################
# 元素記号に対応する情報を抜き出す
# 注意) 同名の元素記号があるときは先頭行のみ吸い出し
class ReadMxVpsList(object):

    def __init__(self, name):
        if not os.path.exists(name):
            sys.exit("STOP: " + name + " not found")
        try:
            tmp = open(name)
            datalist = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: " + name + " does'nt open")
        finally:
            tmp.close()
        self.datalines = datalist.split("\n")
        self.nlist0 = int(len(self.datalines)) - 1

    def get_list(self):
        comment_reg = re.compile("^#.*", re.IGNORECASE)
        self.list_data = []
        j = 0
        for i in range(self.nlist0):
            if not bool(comment_reg.match(self.datalines[i])):
                tmp = self.datalines[i].split()
                if not int(len(tmp)) >= 4:
                    sys.exit(self.name + " Format Error: datalines < 4 ")
                self.list_data.append([tmp[0], tmp[1], tmp[2], tmp[3]])
                j += 1
        self.nlist = j
        return [self.nlist, self.list_data]

    def get_vps_name(self, atom):
        nlist, list_data = self.get_list()
        for i in range(nlist):
            if list_data[i][1] == atom:
                num = list_data[i][0]
                symbol = list_data[i][1]
                cutoff = list_data[i][2]
                vps_orbit = list_data[i][3]
                break
        return [num, symbol, cutoff, vps_orbit]
