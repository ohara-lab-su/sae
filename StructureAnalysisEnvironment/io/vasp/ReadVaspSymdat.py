#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# VASP(+他)
# ReadSymdat.py
#
#  sym.dat ファイルの読み込み
#   vplot_band.py での描画の際に使う symmmetry line の情報ファイル sym.dat
#   の読み込みを行うだけのアホクラス
#
#   Python 化にしたがって、
#   空間群の自動判定+K点リストからの自動判定プログラム作成予定となったので、
#   それまでの暫定処置。永遠に暫定処置かもしれない。
#   ただし、自動処理の有無に関係なく、手動での軸記号描画のためにこの機能は
#   おそくら延々と使う。
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応暫定
#
# 2015.01.29 1st
#
################################################################################
from __future__ import print_function

try:
    from ...copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import sys
import os
import gzip

# import re
# import numpy as np

# from copy import deepcopy

# import StructureAnalysisEnvironment as SAE
# import SpaceGroupEnvironment as SGE

################################################################################
class ReadVaspSymdat(object):

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
        self.num = len(self.datlines) - 1

    # sym.dat 読み込み
    def get_symlines(self):
        self.symlines = []
        for i in range(self.num):
            self.symlines.append(self.datlines[i])
        return self.symlines

    # symlines の数を返す
    def get_num_symlines(self):
        return self.num


################################################################################
if __name__ == '__main__':

    import optparse

    name = 'sym.dat'

    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest='INPUT', )
    options, args = parser.parse_args()

    if options.INPUT: name = options.INPUT
    if len(args) > 0: name = args[0]

    sym = ReadVaspSymdat(name)

    num_symlines = sym.get_num_symlines()
    symlines = sym.get_symlines()

    for i in range(num_symlines):
        print("%s" % str(symlines[i]))

################################################################################
