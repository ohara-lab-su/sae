#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# VASP
# ReadEigenval.py
#
#  EIGENVAL 読み込みクラス (Vband.pl を参考)
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応暫定
#
# 2015.01.28
#  title の取得における末尾までの空白削除を追加
#
# 2015.01.27 startup
#
################################################################################
from __future__ import print_function

try:
    from ...copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.2"

################################################################################

import sys
import os
import re
import gzip
import numpy as np


# from copy import deepcopy


################################################################################
class ReadVaspEigenval(object):

    def __init__(self, name):

        if os.path.exists(name):
            GZIP = False
        elif os.path.exists(name + ".gz"):
            GZIP = True
        else:
            sys.exit("STOP: " + name + " or " + name + ".gz file not found")

        try:
            if GZIP:
                tmp = gzip.open(name + ".gz")
            else:
                tmp = open(name)
            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: " + name + " or " + name + ".gz does'nt open")
        finally:
            tmp.close()

        self.datlines = datfile.split('\n')

    # DOSCAR & EIGENVAL 共通フォーマット(0-4)
    def get_natom(self):  # VASP 的には NSIONS に相当
        tmp = self.datlines[0].split()  # NATOM
        self.N_ATOM = int(tmp[0])
        return self.N_ATOM

    # DOSCAR & EIGENVAL 共通フォーマット(0-4)
    def get_title(self):  # VASP 的には SYSTEM に相当かと
        src = str(self.datlines[4])  # SYSTEM
        self.SYSTEM = re.sub(' *$', '', src)
        return self.SYSTEM

    # NKPTS
    def get_nkpts(self):
        tmp = self.datlines[5].split()
        self.NKPTS = int(tmp[1])
        return self.NKPTS

    # NBANDS
    def get_nbands(self):
        tmp = self.datlines[5].split()
        self.NBANDS = int(tmp[2])
        return self.NBANDS

    # ISPIN を類推
    def get_ispin(self):
        ispin_flag = len(self.datlines[8].split())
        if ispin_flag >= 3:
            self.NSPIN = 2
        else:
            self.NSPIN = 1
        return self.NSPIN

    # EIGENVAL,固有値の情報 をゲット
    def get_eigenval(self):
        NSPIN = self.get_ispin()
        NBANDS = self.get_nbands()
        NKPTS = self.get_nkpts()

        i = 6
        self.eigenval = np.zeros((NBANDS, NKPTS, NSPIN))
        for k in range(NKPTS):
            i += 1
            #           tmp = self.datlines[i].split()
            #           kx = float(tmp[0])
            #           ky = float(tmp[1])
            #           kz = float(tmp[2])
            #           w  = float(tmp[3])
            i += 1
            for j in range(NBANDS):
                tmp = self.datlines[i].split()
                ispin = 0
                self.eigenval[j, k, ispin] = float(tmp[1])
                if NSPIN >= 2:
                    ispin += 1
                    self.eigenval[j, k, ispin] = float(tmp[2])
                i += 1
        return self.eigenval

    # EIGENVAL,K点の情報 をゲット
    def get_eigenval_kxyz(self):
        NBANDS = self.get_nbands()
        NKPTS = self.get_nkpts()

        i = 6
        self.eigenval_kxyzw = np.zeros((NKPTS, 4))
        for k in range(NKPTS):
            i += 1
            tmp = self.datlines[i].split()
            kx = float(tmp[0])
            ky = float(tmp[1])
            kz = float(tmp[2])
            w = float(tmp[3])
            self.eigenval_kxyzw[k, 0] = kx
            self.eigenval_kxyzw[k, 1] = ky
            self.eigenval_kxyzw[k, 2] = kz
            self.eigenval_kxyzw[k, 3] = w
            i += 1
            for j in range(NBANDS):
                i += 1
        return self.eigenval_kxyzw

    # 全バンドの中から固有値の最大と最小を探す(アホルーチン)
    def get_max_eigenval(self):
        NSPIN = self.get_ispin()
        NBANDS = self.get_nbands()
        NKPTS = self.get_nkpts()

        eigenval = self.get_eigenval()

        all_eigen_list = np.zeros(NSPIN * NBANDS * NKPTS)
        i = 0
        for ispin in range(NSPIN):
            for j in range(NBANDS):
                for k in range(NKPTS):
                    all_eigen_list[i] = eigenval[j, k, ispin]
                    i += 1

        eigen_max = max(all_eigen_list)
        eigen_min = min(all_eigen_list)

        return [eigen_min, eigen_max]


################################################################################
if __name__ == '__main__':

    import optparse

    name = 'EIGENVAL'

    parser = optparse.OptionParser()
    parser.add_option('-i', '--input',
                      dest='INPUT',
                      default=name,
                      )
    options, args = parser.parse_args()

    if options.INPUT:
        name = options.INPUT

    if len(args) > 0:
        name = args[0]

    band = ReadVaspEigenval(name)

    NATOM = band.get_natom()
    TITLE = band.get_title()
    NKPTS = band.get_nkpts()
    NBANDS = band.get_nbands()
    NSPIN = band.get_ispin()

    #   print "NATOM  = ",NATOM
    #   print "TITLE  = ",TITLE
    #   print "NKPTS  = ",NKPTS
    #   print "NBANDS = ",NBANDS
    #   print "NSPIN  = ",NSPIN

    eigenval = band.get_eigenval()

    for ispin in range(NSPIN):
        for j in range(NBANDS):
            print("")
            print("")
            print("")
            print("## ISPIN = %s" % str(NSPIN))
            print("## SPIN  = %s" % str(ispin))
            print("## NBAND = %s" % str(NBANDS))
            print("## BAND  = %s" % str(j))
            print("## EF    = ")
            print("")
            print("")
            print("")
            for k in range(NKPTS):
                print("%5d %14.8f" % (k + 1, eigenval[j, k, ispin]))

    print("")
    eigen_max, eigen_min = band.get_max_eigenval()
    print("%s %s" % (eigen_max, eigen_min))

################################################################################
