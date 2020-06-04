#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# WIEK2k case.xspec
#
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.07.22
#  入力ファイル名にsuffixを付けても、つけなくても(別オプションでsuffix指定)
#  どちらでも動作するように変更。
#
# 2015.07.22
#  インスタンス変数重視の体制へ変更
#
# 2015.06.30
#   == None --> is None
#
# 2015.04.06
#  .xspec のヘッダを返すようにした
#
# 2015.04.06
#  suffix を引数で与えるように(オプショナル)した。
#
# 2015.03.30
#  get_ymax_xas() 追加
#
# 2015.03.28(sat)
#  startup
#
################################################################################
from __future__ import print_function
###############################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014,2015 Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"
################################################################################

import sys
import os
import re
#import gzip
import numpy as np

#import optparse

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
class ReadWienXspec(object):

    def __init__(self,case='case',spin=None,suffix='.xspec'):

        if spin is None:
            spin = ''

        if not os.path.exists(case+suffix):
            case = case.replace(suffix,'')

        self.datlines,self.num = SAE.read_dataline(case+suffix+spin)

        self.head = []
        self.head.append(self.datlines[0])
        self.head.append(self.datlines[1])

        s_reg = re.compile(' #S=.*')
        g_reg = re.compile(' #GAMMA=.*')

        self.eng = []
        self.xas  = []
        self.s = 0.0
        self.g = 0.0

        for i in range(self.num):
            line = self.datlines[i]

            if bool(s_reg.match(line)):
                self.s = float(line.split()[1])
            if bool(g_reg.match(line)):
                self.g = float(line.split()[1])

            if not bool(s_reg.match(line)) and not bool(g_reg.match(line)):
                self.eng.append(float(line.split()[0]))
                self.xas.append(float(line.split()[1]))

        self.eng = np.array(list(self.eng))
        self.xas = np.array(list(self.xas))

        self.gamma = self.g
        self.ymax_xas = max(self.xas)
        self.xasmax = self.ymax_xas
        self.emax = max(self.eng)
        self.emin = min(self.eng)

    def get_head(self):
        return self.head

    def get_eng(self):
       #self.eng = np.array(self.eng)
        return self.eng

    def get_xas(self):
       #self.xas = np.array(self.xas)
        return self.xas

    def get_ymax_xas(self):
       #self.ymax_xas = max(self.xas)
        return self.ymax_xas

    def get_emin(self):
       #self.emin = min(self.eng)
        return self.emin

    def get_emax(self):
       #self.emax = max(self.eng)
        return self.emax

    def get_s(self):
        return self.s

    def get_gamma(self):
        return self.g

    def write(self,outputname=None):
        if outputname is None:
            out = sys.stdout
        else:
            try:
                out = open(outputname,'w')
            except:
                out.close()
                sys.exit(outputname+" can't not open")

        nxas = len(self.xas)
        for i in range(nxas):
            print("%9.5f %14.8f" % (self.eng[i], self.xas[i]), file=out)

        if not outputname is None:
            out.close()

################################################################################
if __name__ == '__main__':

    import optparse

    case = re.sub('.*/','',os.getcwd())
   #case = 'Cu'

    suffix = '.xspec'

    unit = 'ev'

    parser = optparse.OptionParser(os.getcwd())
    parser.add_option( '-i','--input', dest='INPUT', )
    options, args = parser.parse_args()

    if options.INPUT: case=options.INPUT

    xspec = ReadWienXspec(case=case,suffix=suffix)
    head = xspec.get_head()
    for i in head:
        print("%d" % i)
    xspec.write()

