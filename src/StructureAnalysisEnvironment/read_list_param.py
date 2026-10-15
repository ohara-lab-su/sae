
from sae.errors import legacy_error as _legacy_error
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# list 読み込みの事前準備
#   (注意) コメント行だろうがなんだろうが、一行としてカウントする
#
# [in] cname      : 読み込みファイル名
#
# [return] nlist : リスト数
#
################################################################################
#
# 2014.11.05 1st
#
################################################################################
try:
    from .copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import sys
import os
import re
from numpy import *
from copy import deepcopy


def read_list_param(name):
    if not os.path.exists(name):
        _legacy_error(name + " not found")

    try:
        tmp = open(name)
    except:
        tmp.close()
        _legacy_error("STOP: " + name + " does'nt open")

    datalist = tmp.read()
    tmp.close()
    datlines = datalist.split('\n')
    nlist = int(len(datlines)) - 1

    return nlist
