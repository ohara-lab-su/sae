#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# *_coll.cfg (RMC_POT) 読み込み, ION-LOOP 毎の原子位置(&力)読み込み専用の事前準備
#
#  LOOP 回数を算出
#
# [in]     canme  : OUTCARの名前
#
# [return] nloop  : LOOP数
# [return] natom  : 総原子数
# [return] nion   : 原子の種類
#
################################################################################
from copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import sys
import os
import re
from numpy import *


################################################################################
def read_cfg_coll_param(cname):
    try:
        tmp = open(cname + '.cfg')
    except:
        tmp.close()
        sys.exit("Error(read_cfg_coll_param.py): " + cname + " not open")

    datfile = tmp.read()
    tmp.close()
    datlines = datfile.split('\n')

    num = len(datlines) - 1

    # 読み込みスタート行
    lines = 0

    # 全原子数
    t = datlines[lines + 7].split()
    natom = int(t[0])

    # 原子の種類の数
    t = datlines[lines + 8].split()
    nion = int(t[0])

    # ヘッダー部分(固定行)のまとめてスキップ
    lines = lines + 18

    # 原子種ごとの読み込み行
    lines = lines + (nion * 4)

    # 内部座標(ループごとの原子数)
    lines = lines + (natom)

    # ファイルの最後の空白行
    lines = lines + 1

    max_lines = lines  # 一つのループ毎の*.cfg行数
    nloop = num / max_lines  # ループ数

    #   print "MAX_LINES      : ", num
    #   print "MAX_LINES/LOOP : ", max_lines
    #   print "NUM. OF LOOP   : ", nloop

    #   次のループの先頭
    #   print datlines[lines]

    return nloop, natom, nion,

################################################################################
