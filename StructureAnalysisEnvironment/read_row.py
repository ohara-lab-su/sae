# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# read_rowe(filename,Column)
#
#  filename ファイル の Column 番目の row数を返す
#  結局ファイルまるごと読んでしまうアホ仕様
#
################################################################################
#
# 2015.07.01
#   startup
#
################################################################################
from __future__ import print_function
from copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import sys
import os
import gzip


################################################################################
def read_row(name, column=0):
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

    datlines = datfile.split('\n')
    num = len(datlines) - 1
    row = len(datlines[column].split())

    return row, num
