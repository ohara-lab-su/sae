#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OUTCAR 読み込み, ION-LOOP 毎の原子位置(&力)読み込み専用の事前準備
#
#  LOOP 回数を算出
#
# [in]     canme  : OUTCARの名前
# [in]     natom  : 総原子数
# [return] nloop  : LOOP数
#
################################################################################
try:
    from copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import sys
import gzip
import os
import re
import optparse
from numpy import *


################################################################################
def read_outcar_param(cname, natom):
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

    datlines = datfile.split('\n')

    num = len(datlines) - 1

    nion_reg = re.compile('.*NIONS = ', re.IGNORECASE)
    tforce_reg = re.compile('.*TOTAL-FORCE', re.IGNORECASE)
    tvector_reg = re.compile('.*Lattice vectors:', re.IGNORECASE)
    a_reg = re.compile('.*ALAT       =', re.IGNORECASE)
    potcar_reg = re.compile('.*POTCAR:', re.IGNORECASE)

    # 総原子数のチェック
    for i in range(num):

        # 原子の総数 (NATOM)
        if bool(nion_reg.match(datlines[i])):
            lines = datlines[i].split()
            natom_outcar = int(lines[11])

    if natom != natom_outcar:
        sys.exit("OUTCAR is inconsistent with POSCAR")

    # 原子に働く力(およびステップごとの座標の読み込み
    loop = 0
    for i in range(num):
        if bool(tforce_reg.match(datlines[i])):
            loop += 1
        # for j in range(natom):
        #    pass
        #   #print datlines[i+j+2]
        # print ""

    return loop

################################################################################
