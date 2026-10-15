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
from __future__ import print_function

# トップディレクトリ関係のエラーは ImportError ではキャッチ出来ない
try:
    from ...copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

###############################################################################

import sys
# import gzip
import os
import re

# import optparse
# import numpy as np

try:
    # sys.path.append('../..')
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    import StructureAnalysisEnvironment as SAEnv
except ImportError:
    import StructureAnalysisEnvironment as SAEnv


# import SpaceGroupEnvironment as SGE

###############################################################################


class ReadFdmFdmfile(object):

    def __init__(self, cname='fdmfile', suffix='.txt'):

        name = cname + suffix

        self.datlines, self.num = SAEnv.read_dataline1(name)

        # 複数入力ファイルの場合は未対応(Noneを返す)
        #
        for i in range(self.num):
            if len(self.datlines[i].split()):
                _line = self.datlines[i].split()[0]

                if bool(re.compile(r'^[0-9]').match(_line)):
                    if _line == '1':
                        self.filout = self.datlines[i + 1].split()[0]
                    else:
                        self.filout = None
                    break

    def get_filout(self):
        return self.filout


###############################################################################
if __name__ == '__main__':
    conv = ReadFdmFdmfile()
    print("%s" % str(conv.filout))
