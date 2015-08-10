#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 原子番号もしくは元素記号を渡すと原子量を返すルーチン
#
# atomic_weight.list ファイルが必要
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"
################################################################################
#
# 2015.02.21 (sun)
#   startup
#   get_atomic_radius.py をベース(ほとんどそのまま)
#
################################################################################

import os
import re

import numpy as np
import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE


### 原子番号から原子量を返す
def get_atomic_weight0(num):

    name='atomic_weight.list'
    libpath = re.sub('__init__.pyc','',SAE.__file__)
    if os.path.exists(libpath):
        name=libpath+name
        if not os.path.exists(name):
            name0='atomic_weight.list.py'
            name=libpath+name0
    else:
        for libpath in os.getenv('PYTHONPATH').split(':'):
            name=libpath+'/'+name
            if os.path.exists(name):
                break

    nlist = SAE.read_list_param(name)

    radius_list = np.zeros((nlist,3),dtype='S4')
    nlist = SAE.read_list3(name,radius_list)

    for i in range(nlist):
        if num == radius_list[i,0]:
            weight=float(radius_list[i,2])

    return weight


### 元素記号から原子量を返す
def get_atomic_weight1(atom):

    name='atomic_weight.list'
    libpath = re.sub('__init__.pyc','',SAE.__file__)
    if os.path.exists(libpath):
        name=libpath+name
        if not os.path.exists(name):
            name0='atomic_weight.list.py'
            name=libpath+name0
    else:
        for libpath in os.getenv('PYTHONPATH').split(':'):
            name=libpath+'/'+name
            if os.path.exists(name):
                break

    nlist = SAE.read_list_param(name)

    radius_list = np.zeros((nlist,3),dtype='S4')
    nlist = SAE.read_list3(name,radius_list)

    for i in range(nlist):
        if atom == radius_list[i,1]:
            weight=float(radius_list[i,2])

    return weight


#### 元素記号から原子番号を返す
def get_atomic_number1(atom):

    name='atomic_radius.list'
    libpath = re.sub('__init__.pyc','',SAE.__file__)
    if os.path.exists(libpath):
        name=libpath+name
        if not os.path.exists(name):
            name0='atomic_radius.list.py'
            name=libpath+name0
    else:
        for libpath in os.getenv('PYTHONPATH').split(':'):
            name=libpath+'/'+name
            if os.path.exists(name):
                break

    nlist = SAE.read_list_param(name)

    radius_list = np.zeros((nlist,3),dtype='S4')
    nlist = SAE.read_list3(name,radius_list)

    for i in range(nlist):
        if atom == radius_list[i,1]:
            num=float(radius_list[i,0])

    return num


################################################################################

if __name__ == '__main__':

    print get_atomic_weight1('Cu')

