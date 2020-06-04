#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 汎用データーリード
#   read_list との違いは cut 引数があるか否か
#
# cut 引数
#    データーファイルの読み込みスタート行を指定できる
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2014.11.19 1st
#
################################################################################
from __future__ import print_function
from copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import sys
import os
import re
from numpy import *
from copy import deepcopy

comment_reg = re.compile('^#.*', re.IGNORECASE)


########################################
## find_list は (dimension)次元配列
## 好きな次元で利用可能
##
def read_dat(name, dimension, dat, cut):
    if not os.path.exists(name):
        sys.exit("STOP(read_dat.py): " + name + " not found")

    try:
        tmp = open(name)
    except:
        tmp.close()
        sys.exit("STOP(read_dat.py): " + name + " does'nt open")

    datalist = tmp.read()
    tmp.close()
    datalines = datalist.split('\n')
    nlist = int(len(datalines)) - 1

    j = 0
    for i in range(cut, nlist):
        tmp = datalines[i].split()
        for k in range(dimension):
            dat[i, k] = tmp[k]
        j += 1

    nlist = j
    return nlist


########################################
## find_list は2次元配列
##
def read_dat2(name, dat, cut):
    if not os.path.exists(name):
        sys.exit("STOP(read_dat.py): " + name + " not found")

    try:
        tmp = open(name)
    except:
        sys.exit("STOP(read_dat.py): " + name + " does'nt open")
    datalist = tmp.read()
    tmp.close
    datalines = datalist.split('\n')
    nlist = int(len(datalines)) - 1

    j = 0
    for i in range(cut, nlist):
        tmp = datalines[i].split()
        dat[i, 0] = tmp[0]
        dat[i, 1] = tmp[1]
        j += 1

    nlist = j
    return nlist


########################################
## find_list は5次元配列
##
def read_dat5(name, dat, cut):
    if not os.path.exists(name):
        sys.exit("STOP(read_dat.py): " + name + " not found")

    try:
        tmp = open(name)
    except:
        sys.exit("STOP(read_dat.py): " + name + " does'nt open")
    datalist = tmp.read()
    tmp.close
    datalines = datalist.split('\n')
    nlist = int(len(datalines)) - 1

    j = 0
    for i in range(cut, nlist):
        tmp = datalines[i].split()
        dat[i, 0] = tmp[0]
        dat[i, 1] = tmp[1]
        dat[i, 2] = tmp[2]
        dat[i, 3] = tmp[3]
        dat[i, 4] = tmp[4]
        j += 1

    nlist = j
    return nlist


########################################
# exsample)
if __name__ == '__main__':

    cname = 'igzo.fit'
    cut = 12

    nlist = sum(1 for line in open(cname))
    fitdat = zeros((nlist, 5))
    ndat = read_dat5(cname, fitdat, cut)

    for i in range(cut, nlist):
        print(" %12.6e  %+18.12e  %+18.12e  %+18.12e  %+18.12e"
              % (fitdat[i, 0],  # Q
                 fitdat[i, 1],  # S(Q) RMC++
                 fitdat[i, 2],  # renormalized experimental S(Q)
                 fitdat[i, 3],  # original exp. S(Q)
                 fitdat[i, 4]))  # additive backgroupd
