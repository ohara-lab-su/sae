#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
# *.txt ファイル
#
###############################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.11.12 startup
#
###############################################################################
# トップディレクトリ関係のエラーは ImportError ではキャッチ出来ない
###############################################################################
# import gzip
# import optparse
# import numpy as np
# sys.path.append('../..')
# import SpaceGroupEnvironment as SGE
###############################################################################
###############################################################################
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re


class ReadFdmFdmfile(object):

    # 複数入力ファイルの場合は未対応(Noneを返す)
    #
    def __init__(self, cname="fdmfile", suffix=".txt"):
        from sae.common.text import TextFiles

        name = cname + suffix
        self.datlines, self.num = TextFiles().read_dataline1(name)
        for i in range(self.num):
            if len(self.datlines[i].split()):
                _line = self.datlines[i].split()[0]
                if bool(re.compile("^[0-9]").match(_line)):
                    if _line == "1":
                        self.filout = self.datlines[i + 1].split()[0]
                    else:
                        self.filout = None
                    break

    def get_filout(self):
        return self.filout
