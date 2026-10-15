#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# VASP
# OSZICAR 読み込み (汎用,その他)
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応暫定
#
# 2015.02.24
#  get_iter_num() --> get_n_ion_loop() 変更
#
# 2015.01.29
#  get_tmod() の名称を get_md_mode() へ変更
#  (ReadOutcar.get_tmode() ==> ReadOutcar.get_md_mode() への変更に合わせた)
#
# 2015.01.26 startup
#
#   temperature と etotal のゲット
#   IBRION ゲット method 追加
#
################################################################################
################################################################################
# import StructureAnalysisEnvironment as SAE
# import SpaceGroupEnvironment as SGE
################################################################################
################################################################################
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import gzip
import os
import re
import numpy as np


# get_n_ion_loop (旧名) get_iter_num
# 実際に計算した ION iter 数をゲットする
# get_md_mode
# IBRION=0 or それ以外の判定
class ReadVaspOszicar(object):

    def __init__(self, cname):
        if os.path.exists(cname):
            GZIP = False
        elif os.path.exists(cname + ".gz"):
            GZIP = True
        else:
            sys.exit("STOP: " + cname + " or " + cname + ".gz file not found")
        try:
            if GZIP:
                tmp = gzip.open(cname + ".gz")
            else:
                tmp = open(cname)
            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: " + cname + " or " + cname + ".gz does'nt open")
        finally:
            tmp.close()
        self.datlines = datfile.split("\n")
        self.num = len(self.datlines) - 1

    def get_n_ion_loop(self):
        iter_reg = re.compile(".*F=", re.IGNORECASE)
        for i in range(self.num):
            if bool(iter_reg.match(self.datlines[i])):
                tmp = self.datlines[i].split()
                self.n_ion_loop = int(tmp[0])
        return self.n_ion_loop

    def get_md_mode(self):
        iter_reg = re.compile(".*T=")
        self.md_FLAG = False
        for i in range(self.num):
            if bool(iter_reg.match(self.datlines[i])):
                self.md_FLAG = True
                break
        return self.md_FLAG

    def get_temperature(self):
        MD_FLAG = self.get_md_mode()
        if MD_FLAG:
            n_ion_loop = self.get_n_ion_loop()
            self.temperature = np.zeros(n_ion_loop)
            iter_reg = re.compile(".*T=", re.IGNORECASE)
            j = 0
            for i in range(self.num):
                if bool(iter_reg.match(self.datlines[i])):
                    tmp = self.datlines[i].split()
                    self.temperature[j] = float(tmp[2])
                    j += 1
        return self.temperature

    def get_etotal(self):
        MD_FLAG = self.get_md_mode()
        if MD_FLAG:
            n_ion_loop = self.get_n_ion_loop()
            self.ETOTAL = np.zeros(n_ion_loop)
            iter_reg = re.compile(".*E=", re.IGNORECASE)
            j = 0
            for i in range(self.num):
                if bool(iter_reg.match(self.datlines[i])):
                    tmp = self.datlines[i].split()
                    self.ETOTAL[j] = float(tmp[4])
                    j += 1
        return self.ETOTAL
