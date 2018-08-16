# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 原子番号もしくは元素記号を渡すと原子半径を返すルーチン等
# (いささかルーチン全体の基本センスが古いので扱いにくい)
#
# カレントに atomic_radius.list ファイルが必要
#
################################################################################
from __future__ import print_function
###############################################################################
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
# 2018.08.16
#  Python2/3 両対応(主にファイル読み子関係なので注意)
#
# 2015.05.19
#  原子番号から元素記号を返すルーチンを追加
#
# 2015.02.16
#  import の名前空間を変更
#
################################################################################

import sys
import os

import numpy as np
import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE


### 原子番号から原子半径を返す
def get_atomic_radius0(num):

    name='atomic_radius.list'

    ldir = os.path.dirname(SAE.__file__)
    if not os.path.exists(name):
        if os.path.exists( ldir+'/'+name ):
            name=ldir+'/'+name
        else:
            name='atomic_radius.list.py'
            if not os.path.exists(name):
                sys.exit("STOP: "+name+" file not found")

    nlist = SAE.read_list_param(name) # pre read

    radius_list = np.zeros((nlist,3),dtype='S4')
    nlist = SAE.read_list3(name,radius_list)

    for i in range(nlist):
        if num == radius_list[i,0]:
            radius=float(radius_list[i,2])

    return radius

### 元素記号(str)から原子半径(float)を返す
def get_atomic_radius1(atom):

    name='atomic_radius.list'

    ldir = os.path.dirname(SAE.__file__)
    if not os.path.exists(name):
        if os.path.exists( ldir+'/'+name ):
            name=ldir+'/'+name
        else:
            name='atomic_radius.list.py'
            if not os.path.exists(name):
                if os.path.exists( ldir+'/'+name ):
                    name=ldir+'/'+name
                else:
                    sys.exit("STOP: "+name+" file not found")

    nlist = SAE.read_list_param(name) # pre read

    radius_list = np.zeros((nlist,3),dtype='S4')
    nlist = SAE.read_list3(name,radius_list)

    for i in range(nlist):
        try:
            atom_name = radius_list[i,1].decode() # for Python3
        except:
            atom_name = radius_list[i,1]

        if atom == atom_name:
            radius = float(radius_list[i,2])

    return radius

### 元素記号(str)から原子番号(float)を返す
def get_atomic_number1(atom):

    name='atomic_radius.list'

    ldir = os.path.dirname(SAE.__file__)
    if not os.path.exists(name):
        if os.path.exists( ldir+'/'+name ):
            name=ldir+'/'+name
        else:
            name='atomic_radius.list.py'
            if not os.path.exists(name):
                if os.path.exists( ldir+'/'+name ):
                    name=ldir+'/'+name
                else:
                    sys.exit("STOP: "+name+" file not found")

    # ファイルの全行数を確保
    nlist = SAE.read_list_param(name) # pre read

    radius_list = np.zeros((nlist,3),dtype='S4')
    nlist = SAE.read_list3(name, radius_list)

    for i in range(nlist):
        try:
            atom_name = radius_list[i,1].decode() # for Python3
        except:
            atom_name = radius_list[i,1]

        if atom == atom_name:
            num = float(radius_list[i,0])

    return num

### 原子番号から元素記号を返す
def get_atomic_symbol0(num):

    name='atomic_radius.list'

    ldir = os.path.dirname(SAE.__file__)
    if not os.path.exists(name):
        if os.path.exists( ldir+'/'+name ):
            name=ldir+'/'+name
        else:
            name='atomic_radius.list.py'
            if not os.path.exists(name):
                if os.path.exists( ldir+'/'+name ):
                    name=ldir+'/'+name
                else:
                    sys.exit("STOP: "+name+" file not found")

    nlist = SAE.read_list_param(name) # pre read

    radius_list = np.zeros((nlist,3),dtype='S4')
    nlist = SAE.read_list3(name,radius_list)

    for i in range(nlist):
        if num == int(radius_list[i,0]):
            symbol = str(radius_list[i,1])

    return symbol
