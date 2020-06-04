# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# コメントアウト(#) 対応のリード(アホ仕様)
#
################################################################################
#
# 2014.11.05 1st
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
import os
import re
from numpy import *
from copy import deepcopy

comment_reg = re.compile('^#.*', re.IGNORECASE)


########################################
## find_list は1次元配列
##
def read_list1(name, find_list):
    if not os.path.exists(name):
        sys.exit(name + " not found")

    try:
        tmp = open(name)
    except:
        tmp.close()
        sys.exit("STOP: " + name + " does'nt open")

    datalist = tmp.read()
    tmp.close()
    datalines = datalist.split('\n')
    nlist0 = int(len(datalines)) - 1

    j = 0
    for i in range(nlist0):
        if not bool(comment_reg.match(datalines[i])):
            tmp = datalines[i].split()
            find_list[j] = tmp[0]
            j += 1

    nlist = j
    return nlist


########################################
## find_list は3次元配列(num,atom,radius)
##
def read_list3(name, find_list):
    if not os.path.exists(name):
        sys.exit(name + " not found")

    tmp = open(name)
    datalist = tmp.read()
    tmp.close
    datalines = datalist.split('\n')
    nlist0 = int(len(datalines)) - 1

    j = 0
    for i in range(nlist0):
        if not bool(comment_reg.match(datalines[i])):
            tmp = datalines[i].split()
            if not int(len(tmp)) >= 3:
                sys.exit(name + " Format Error: datalines < 3 ")

            find_list[j, 0] = tmp[0]
            find_list[j, 1] = tmp[1]
            find_list[j, 2] = tmp[2]
            j += 1

    nlist = j
    return nlist


########################################
## find_list は4次元配列(atom,data_x,data_y,data_z)
##
def read_list4(name, find_list):
    if not os.path.exists(name):
        sys.exit(name + " not found")

    tmp = open(name)
    datalist = tmp.read()
    tmp.close
    datalines = datalist.split('\n')
    nlist0 = int(len(datalines)) - 1

    j = 0
    for i in range(nlist0):
        if not bool(comment_reg.match(datalines[i])):
            tmp = datalines[i].split()
            if not int(len(tmp)) >= 4:
                sys.exit(name + " Format Error: datalines < 4 ")

            find_list[j, 0] = tmp[0]
            find_list[j, 1] = tmp[1]
            find_list[j, 2] = tmp[2]
            find_list[j, 3] = tmp[3]
            j += 1

    nlist = j
    return nlist
