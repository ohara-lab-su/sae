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
from __future__ import print_function

try:
    from ...copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.4"

################################################################################

import sys
import gzip
import os
import re
import numpy as np


# import StructureAnalysisEnvironment as SAE
# import SpaceGroupEnvironment as SGE

################################################################################
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

        self.datlines = datfile.split('\n')
        self.num = len(self.datlines) - 1

    # get_n_ion_loop (旧名) get_iter_num
    # 実際に計算した ION iter 数をゲットする
    def get_n_ion_loop(self):
        iter_reg = re.compile('.*F=', re.IGNORECASE)
        for i in range(self.num):
            if bool(iter_reg.match(self.datlines[i])):
                tmp = self.datlines[i].split()
                self.n_ion_loop = int(tmp[0])

        return self.n_ion_loop

    # get_md_mode
    # IBRION=0 or それ以外の判定
    def get_md_mode(self):
        iter_reg = re.compile('.*T=')
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
            iter_reg = re.compile('.*T=', re.IGNORECASE)
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
            iter_reg = re.compile('.*E=', re.IGNORECASE)
            j = 0
            for i in range(self.num):
                if bool(iter_reg.match(self.datlines[i])):
                    tmp = self.datlines[i].split()
                    self.ETOTAL[j] = float(tmp[4])
                    j += 1

        return self.ETOTAL


################################################################################
if __name__ == '__main__':

    import optparse

    name = 'OSZICAR'

    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest='INPUT', )
    options, args = parser.parse_args()

    if options.INPUT: name = options.INPUT
    if len(args) > 0: name = args[0]

    oszicar = ReadVaspOszicar(name)

    n_ion_loop = oszicar.get_n_ion_loop()
    md_mode = oszicar.get_md_mode()
    print("MD_mode %s" % str(md_mode))

    if md_mode:
        temperature = oszicar.get_temperature()
        oszicar.get_temperature()
        etotal = oszicar.get_etotal()

        for i in range(n_ion_loop):
            print("%d %s %s" % (i + 1, str(temperature[i]), str(etotal[i])))
